/*!
\file pam_mkpolohomedir.c
 PAM Make Home Dir module

     This module will create a users home directory if it does not exist
     when the session begins. This allows users to be present in central
     database (such as nis, kerb or ldap) without using a distributed
     file system or pre-creating a large number of directories.

     The module creates the home directory in all nodes of the system,
     thus ensuring that the system will be fully functional for the user.
     
     Here is a sample /etc/pam.d/login file for Debian GNU/Linux
     2.1:
     
     auth       requisite  pam_securetty.so
     auth       sufficient pam_ldap.so
     auth       required   pam_pwdb.so
     auth       optional   pam_group.so
     auth       optional   pam_mail.so
     account    requisite  pam_time.so
     account    sufficient pam_ldap.so
     account    required   pam_pwdb.so
     session    required   pam_mkhomedir.so skel=/etc/skel/ umask=0022
     session    required   pam_pwdb.so
     session    optional   pam_lastlog.so
     password   required   pam_pwdb.so   
     
     Released under the GNU LGPL version 2 or later
     Based on the pam_mkhomedir module originally written by 
     Jason Gunthorpe <jgg@debian.org> Feb 1999
     Structure taken from pam_lastlogin by Andrew Morgan 
         <morgan@parc.power.net> 1996
 */

#define _GNU_SOURCE 1
#include <stdarg.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <pwd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <dirent.h>
#include <syslog.h>

#include <security/pam_modules.h>
#include <security/_pam_macros.h>
         
#include "createpolodir.h"
/*
 * here, we make a definition for the externally accessible function
 * in this file (this definition is required for static a module
 * but strongly encouraged generally) it is used to instruct the
 * modules include file to define the function prototypes.
 */

#define PAM_SM_SESSION



/* argument parsing */
#define MKPOLOHOMEDIR_DEBUG      020  /* keep quiet about things */
#define MKPOLOHOMEDIR_QUIET      040  /* keep quiet about things */


static unsigned int UMask = 0022;
static char SkelDir[BUFSIZ] = "/etc/skel"; /* THIS MODULE IS NOT THREAD SAFE */

/*!
 Sends a message to the syslog
 \param err Message priority
 \param format The formatting string for the message
 \param ... values for the formatting string
*/
static void _log_err(int err, const char *format, ...)
{
    va_list args;

    va_start(args, format);
    openlog("PAM-mkpolohomedir", LOG_CONS|LOG_PID, LOG_AUTH);
    vsyslog(err, format, args);
    va_end(args);
    closelog();
}

/*!
    Parses the arguments
    \param flags Behaviour modifiers
    \param argc The number of arguments
    \param argv The arguments
    \return A bitwise-modified integer with all the flags
*/
static int _pam_parse(int flags, int argc, const char **argv)
{
    int ctrl = 0;

    /* does the appliction require quiet? */
    if ((flags & PAM_SILENT) == PAM_SILENT)
        ctrl |= MKPOLOHOMEDIR_QUIET;

    /* step through arguments */
    for (; argc-- > 0; ++argv)
    {
        if (!strcmp(*argv, "silent")) {
            ctrl |= MKPOLOHOMEDIR_QUIET;

        } else if (!strncmp(*argv,"umask=",6)) {
            UMask = strtol(*argv+6,0,0);

        } else if (!strncmp(*argv,"skel=",5)) {
            strncpy(SkelDir,*argv+5,sizeof(SkelDir));
            SkelDir[sizeof(SkelDir)-1] = '\0';

        } else {
            _log_err(LOG_ERR, "unknown option; %s", *argv);
        }
    }

    D(("ctrl = %o", ctrl));
    return ctrl;
}

/*!
    This common function is used to send a message to the applications 
    conversion function. Our only use is to ask the application to print 
    an informative message that we are creating a home directory 
    \param pamh Information about the user
    \param ctrl Controlling flags
    \param nargs The number of arguments in message
    \param message An array of messages
    \param response The responses to those messages
*/
static int converse(pam_handle_t * pamh, int ctrl, int nargs,
                    struct pam_message **message, 
                    struct pam_response **response)
{
    int retval;
    struct pam_conv *conv;

    D(("begin to converse"));

    retval = pam_get_item(pamh, PAM_CONV, (const void **) &conv);
    if (retval == PAM_SUCCESS){

        retval = conv->conv(nargs, 
                            (const struct pam_message **) message, 
                            response, 
                            conv->appdata_ptr);

        D(("returned from application's conversation function"));

        if (retval != PAM_SUCCESS && (ctrl & MKPOLOHOMEDIR_DEBUG))
        {
            _log_err(LOG_DEBUG, 
                     "conversation failure [%s]", 
                     pam_strerror(pamh, retval));
        }

    }else {
        _log_err(LOG_ERR, 
                 "couldn't obtain coversation function [%s]", 
                 pam_strerror(pamh, retval));
    }

     D(("ready to return from module conversation"));

     return retval;   /* propagate error status */
}

/*!
 Ask the application to display a short text string for us.
 \param pamh Information about the user
 \param ctrl Controlling flags
 \param remark The message
 \return An status of the operation. 
*/
static int make_remark(pam_handle_t * pamh, int ctrl, const char *remark)
{
    int retval;

    if ((ctrl & MKPOLOHOMEDIR_QUIET) != MKPOLOHOMEDIR_QUIET) {
        struct pam_message msg[1], *mesg[1];
        struct pam_response *resp = NULL;

        mesg[0] = &msg[0];
        msg[0].msg_style = PAM_TEXT_INFO;
        msg[0].msg = remark;

        retval = converse(pamh, ctrl, 1, mesg, &resp);

        msg[0].msg = NULL;
        if (resp)
        {
    _pam_drop_reply(resp, 1);
        }
    } else {
        D(("keeping quiet"));
        retval = PAM_SUCCESS;
    }

    D(("returning %s", pam_strerror(pamh, retval)));
    return retval;
}

/* Do the actual work of creating a home dir */
/*!
    Creates the home directory, using MarcoPolo in the rest of the nodes
    \param pamh The information about the PAM session
    \param ctrl Controlling flags
    \param pwd The information about the user
    \param dest The home directory to create
*/
static int create_homedir(pam_handle_t * pamh, int ctrl,
                          const struct passwd *pwd,
                          const char *source, const char *dest)
{
    char remark[BUFSIZ];
    DIR *D;
    struct dirent *Dir;

    /* Mention what is happening, if the notification fails that is OK */
    if (snprintf(remark,sizeof(remark),"Creating home directory '%s'.", dest) == -1)
        return PAM_PERM_DENIED;

    make_remark(pamh, ctrl, remark);

    /* Create the new directory */
    if (mkdir(dest,0700) != 0)
    {
        _log_err(LOG_DEBUG, "unable to create directory %s",source);
        return PAM_PERM_DENIED;
    }   
    if (chmod(dest,0777 & (~UMask)) != 0 ||
         chown(dest,pwd->pw_uid,pwd->pw_gid) != 0)
    {
        _log_err(LOG_DEBUG, "unable to change perms on directory %s",dest);
        return PAM_PERM_DENIED;
    }

    /* See if we need to copy the skel dir over. */
    if ((source == NULL) || (strlen(source) == 0))
    {
        return PAM_SUCCESS;
    }

    /* Scan the directory */
    D = opendir(source);
    if (D == 0)
    {
        _log_err(LOG_DEBUG, "unable to read directory %s",source);
        return PAM_PERM_DENIED;
    }

    for (Dir = readdir(D); Dir != 0; Dir = readdir(D))
    {  
        int SrcFd;
        int DestFd;
        int Res;
        struct stat St;
        char newsource[PATH_MAX], newdest[PATH_MAX];

        /* Skip some files.. */
        if (strcmp(Dir->d_name,".") == 0 || strcmp(Dir->d_name,"..") == 0){
            continue;
        }

        /* Determine what kind of file it is. */
        snprintf(newsource,sizeof(newsource),"%s/%s",source,Dir->d_name);
        if (lstat(newsource,&St) != 0){
            continue;
        }

        /* We'll need the new file's name. */
        snprintf(newdest,sizeof(newdest),"%s/%s",dest,Dir->d_name);

        /* If it's a directory, recurse. */
        if (S_ISDIR(St.st_mode))
        {
             create_homedir(pamh, ctrl, pwd, newsource, newdest);
             continue;
        }

        /* If it's a symlink, create a new link. */
        if (S_ISLNK(St.st_mode))
        {
            char pointed[PATH_MAX];
            memset(pointed, 0, sizeof(pointed));
            if(readlink(newsource, pointed, sizeof(pointed) - 1) != -1)
            {
                if(symlink(pointed, newdest) == 0){
                    if (lchown(newdest,pwd->pw_uid,pwd->pw_gid) != 0)
                    {
                        _log_err(LOG_DEBUG, "unable to chang perms on link %s",
                                            newdest);
                        return PAM_PERM_DENIED;
                    }
                }
            }
            continue;
        }

        /* If it's not a regular file, it's probably not a good idea to create
         * the new device node, FIFO, or whatever it is. */
        if (!S_ISREG(St.st_mode))
        {
            continue;
        }

        /* Open the source file */
        if ((SrcFd = open(newsource,O_RDONLY)) < 0 || fstat(SrcFd,&St) != 0)
        {
            _log_err(LOG_DEBUG, "unable to open src file %s",newsource);
            return PAM_PERM_DENIED;
        }
        stat(newsource,&St);

        /* Open the dest file */
        if ((DestFd = open(newdest,O_WRONLY | O_TRUNC | O_CREAT,0600)) < 0)
        {
            close(SrcFd);
             _log_err(LOG_DEBUG, "unable to open dest file %s",newdest);
            return PAM_PERM_DENIED;
        }

        /* Set the proper ownership and permissions for the module. We make
             the file a+w and then mask it with the set mask. This preseves
             execute bits */
        if (fchmod(DestFd,(St.st_mode | 0222) & (~UMask)) != 0 ||
            fchown(DestFd,pwd->pw_uid,pwd->pw_gid) != 0)
        {
            close(SrcFd);
            close(DestFd);
            _log_err(LOG_DEBUG, "unable to chang perms on copy %s",newdest);
            return PAM_PERM_DENIED;
        }

        /* Copy the file */
        do
        {
            Res = read(SrcFd,remark,sizeof(remark));
            if (Res < 0 || write(DestFd,remark,Res) != Res)
            {
                close(SrcFd);
                close(DestFd);
                _log_err(LOG_DEBUG, "unable to perform IO");
                return PAM_PERM_DENIED;
            }
        }
        while (Res != 0);
        close(SrcFd);
        close(DestFd);
    }

    

    make_remark(pamh, ctrl, remark);
    //createdirs(dest, pwd->pw_uid,pwd->pw_gid);  //call the function here

    return PAM_SUCCESS;
}

/* --- authentication management functions (only) --- */

/*!
    Opens a PAM session. This is the entry point to the module
    \param pamh The PAM session information given by PAM
    \param flags Several control flags
    \param argc The number of arguments passed to the module in the configuration files
    \param argv The arguments passed to the module
    \return A status code
*/
PAM_EXTERN
int pam_sm_open_session(pam_handle_t * pamh, int flags, int argc, const char **argv)
{
    int retval, ctrl;
    const char *user;
    const struct passwd *pwd;
    struct stat St;
        
    /* Parse the flag values */
    ctrl = _pam_parse(flags, argc, argv);

    /* Determine the user name so we can get the home directory */
    retval = pam_get_item(pamh, PAM_USER, (const void **) &user);
    if (retval != PAM_SUCCESS || user == NULL || *user == '\0')
    {
        _log_err(LOG_NOTICE, "user unknown");
        return PAM_USER_UNKNOWN;
    }

    /* Get the password entry */
    pwd = getpwnam(user);
    if (pwd == NULL)
    {
        D(("couldn't identify user %s", user));
        return PAM_CRED_INSUFFICIENT;
    }

    /* Stat the home directory, if something exists then we assume it is
        correct and return a success before asking the rest of the nodes
        to clone the directory*/

    create_polo_directories(pwd->pw_dir, pwd->pw_uid, pwd->pw_gid);

    if (stat(pwd->pw_dir,&St) == 0)
        return PAM_SUCCESS;
    //Contingency for user directory if it does not exist
    if (snprintf(remark,sizeof(remark),"Creating directory in the rest of the nodes... '%s'.", dest) == -1)
        return PAM_PERM_DENIED;
    return create_homedir(pamh,ctrl,pwd,SkelDir,pwd->pw_dir);
}

/* Ignore */
/*!
    Closes the session. This is the exit point
    \param pamh The PAM session information
    \param flags Some control flags
    \param argc The number of arguments passed
    \param argv The arguments
*/
PAM_EXTERN 
int pam_sm_close_session(pam_handle_t * pamh, int flags, int argc ,const char **argv)
{
     return PAM_SUCCESS;
}

#ifdef PAM_STATIC

/* static module data */
struct pam_module _pam_mkhomedir_modstruct =
{
     "pam_mkpolohomedir",
     NULL,
     NULL,
     NULL,
     pam_sm_open_session,
     pam_sm_close_session,
     NULL,
};

#endif
