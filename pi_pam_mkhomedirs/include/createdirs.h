/*!
	\file createdirs.h
*/
#ifndef CREATE
#define CREATE

/*!
    Requests the creation of the home directory for a user.
    \param home The name of the directory
    \param uid The uid of the owner of the home directory
    \param gid The main group of which the user is a member of
    \returns A status code. If other than 0, a message will be logged.
*/
int createdirs(const char*, int , int );

#endif