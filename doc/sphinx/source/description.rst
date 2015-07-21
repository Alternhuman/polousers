Descripción
===========

Requirements
------------

The distributed system is made of a series of independent nodes to which the users can access. It is required that they can use the existing resources in any node without explicit access to them (with a shell remote session, for instance). Another requirement is that no prior configuration has to be done.

.. El sistema se compone de una serie de nodos independientes a los cuales pueden acceder los usuarios indistintamente. Se desea que los usuarios puedan utilizar los recursos presentes en cualquier nodo sin tener que acceder directamente a ellos (mediante una sesión remota, por ejemplo), y puedan empezar a trabajar sin tener que realizar ningún tipo de configuración.

This requirement is partially covered with the **PAM** modules ``pam_unix.so`` (local users management) [3]_, ``pam_ldap.so`` (**LDAP** user management) [4]_ and particularly, ``pam_mkhomedir.so`` [5]_, which allows the creation of a user directory if the user has logged in for the first time.

.. Esta necesidad está parcialmente cubierta por los módulo de PAM **pam_unix.so** (gestión de usuarios locales) [3]_, ``pam_ldap.so`` (gestión de usuarios del servidor **LDAP**) [4]_ y en particular **pam_mkhomedir.so** [5]_, que permite la creación de un directorio de usuario si el mismo ha iniciado sesión por primera vez en esta máquina.

However, one of the features of the system is the uniformity of its nodes regarding user management. Therefore, it is required that the users have a basic set of data in all nodes on the first logging. The ``pam_mkhomedir`` module does not cover this task, since it only creates the directory (copying the ``/etc/skel``) in the machine where the access was done.

.. Sin embargo, una de las características del sistema es la uniformidad de sus nodos en cuando a usuarios se refiere. Por ello, es deseable que los usuarios cuenten con un conjunto básico de datos en cualquier nodo del sistema a la hora de acceder por primera vez. El módulo **pam_mkhomedir** no lleva a cabo esta tarea, pues únicamente crea el directorio (realizando una copia de ``/etc/skel`` de inicio del usuario en la máquina donde se ha realizado el acceso).

It is necessary to create a mechanism to perform this task. Taking advantage of **PAM**, a new module complementary to ``pam_mkhomedir`` has been created. The module is named ``pam_mkpolohomedir`` and uses MarcoPolo for the task.

.. Es por tanto necesario crear un mecanismo para llevar a cabo dicha tarea. Aprovechando la funcionalidad de PAM, se ha procedido a crear un módulo complementario a **pam_mkhomedir** denominado **pam_mkpolohomedir**, que aprovecha la herramienta **MarcoPolo** para realizar su cometido.

Module features
---------------

The functionality of a **PAM** module is packaged in a shared object linked in execution time with the rest of the **PAM** components, as indicated in the configuration files of the module (usually under ``/etc/pam.d``). [1]_. The module must be stored in the ``/lib/security`` folder.

.. Características del módulo
    --------------------------

.. La funcionalidad de un módulo de **PAM** se recoge en un objecto compartido que se vincula en tiempo de ejecución con el resto de componentes de **PAM** según se disponga en los ficheros de configuración del módulo (generalmente situados en ``/etc/pam.d/``). [1]_ y que se debe almacenar en ``/lib/security``.  

In this particular task, the module will use MarcoPolo to detect all the available nodes and then will ask for the creation of the directory, as well as some aditional tasks.

.. En el caso particular a resolver, el módulo será invocado tras la ejecución del módulo **pam_mkhomedir**, y se encargará de, aprovechando la funcionalidad de MarcoPolo, detectar todos los nodos disponibles en la red y proceder a la creación en los mismos del directorio de inicio, así como la realización de una serie de tareas adicionales.

All the functionality is implemented in the ``pam_mkpolohomedir.c`` file. The module gets the relevant information (name, UID and GID of the user) through the parameters that **PAM** called the module with [2]_. The structure of the code is partially based on the ``pam_mkhomedir`` module [6]_, taking some functions from this module.

.. Toda la funcionalidad se recoge en el fichero ``pam_mkpolohomedir.c``. Dicho módulo recoge la información de interés (nombre, uid y gid del usuario) a través de llamadas al núcleo de **PAM** [2]_. La estructura del código se basa parcialmente en el del módulo **pam_makehomedir** [6]_, tomando varias funciones del mismo.


.. literalinclude:: src/pam_mkpolohomedir.c
    :language: c
    :lines: 355-372

After the information is gathered, the ``create_polo_homedir`` and ``createdirs`` search for the nodes (using the **Marco** binding) and then request to them the creation of the directory.

.. Una vez obtenida dicha información, las funciones ``create_polo_homedir`` y ``createdirs`` se encargan de la búsqueda de los nodos del sistema (aprovechando el *binding* de **Marco**) y de contactar con ellos.

Directory creation
------------------

.. 
    Creación del directorio
    -----------------------

Each node has an instance of the **polousers** slave, the service in charge of receiving and processing all the requests. The service is implemented using the **Twisted** *framework*, verifiying the identity of each requestor using TLS-based (Transport Layer Security) sockets.

.. Cada nodo cuenta con una instancia del esclavo de **polousers**, el servicio que se encarga de recibir las peticiones de creación de usuarios. Dicho servicio se implementa sobre el *framework* **Twisted**, y verifica la autoría de cada petición mediante sockets sobre TLS (*Transport Layer Security*).

Once the directory is created, the service acknowledges the requestor, which logs the operation. In fact the acknowledgement is done a bit earlier, in order to speed up the process.


.. Una vez creado el directorio, el servicio así lo indica al solicitante, que almacena el registro de dicha operación.

A **PAM** module must implement a series of function which consitute the entry points to it.

.. Un módulo en PAM debe implementar una serie de funciones que constituirán los puntos de entrada al módulo.

- ``PAM_EXTERN int pam_sm_open_session(pam_handle_t * pamh, int flags, int argc ,const char **argv)``

    It is the function that **PAM** invokes when the module is linked. It passes as parameters a ``pam_handle_t`` structure with all the relevant information about the user who just logged in. The parameters indicated in the **PAM** configuration files are also included (in this case, the directory permissions and the location of the skeleton directory).

    .. Es la función que **PAM** invoca al incluir el módulo. Incluye en el mismo una estructura ``pam_handle_t`` con toda la información relevante sobre el usuario que ha iniciado sesión y los parámetros indicados en los ficheros de configuración de ``PAM`` (en el caso de este módulo, los permisos del directorio de inicio y la localización del directorio *skeleton*). 

- ``PAM_EXTERN int pam_sm_close_session(pam_handle_t * pamh, int flags, int argc, const char **argv)``

    It is the function that **PAM** uses to indicate that the session has finished. In this module, it includes no functionality, however it must be included.
    ..  Es la función que **PAM** utiliza para indicar al módulo que la sesión ha terminado. En el caso del módulo a crear no se debe realizar ninguna acción en este evento, sin embargo es necesario implementarla debido a que PAM la requiere.

- ``struct pam_module _pam_mkhomedir_modstruct``

    Defines the module features and entry points. It is only necessary when the linking is statically done.

    .. Define las características del módulo y los puntos de entrada que define.


Bibliografía
------------

.. [1] A. G. Morgan and T. Kukuk, The Linux-PAM Module Writers' Guide. linux-pam.org, 1.1.2 ed., Aug. 2010.
.. [2] A. G. Morgan and T. Kukuk, The Linux-PAM Module Writers' Guide, ch. 2. What can be expected by the module. linux-pam.org, 1.1.2 ed., Aug. 2010.
.. [3] pam_unix(8) - Linux man pages.
.. [4] pam_ldap(5) - Linux man pages.
.. [5] J. Gunthorpe, pam_mkhomedir(8) - Linux man pages.
.. [6] J. Gunthorpe, "PAM Make Home Dir module," tech. rep., Feb. 1993.

.. 
    .. [linux-pam-guide] A. G. Morgan and T. Kukuk, The Linux-PAM Module Writers' Guide. linux-pam.org, 1.1.2 ed., Aug. 2010.
    .. [linux-pam-guide-ch2] A. G. Morgan and T. Kukuk, The Linux-PAM Module Writers' Guide, ch. 2. What can be expected by the module. linux-pam.org, 1.1.2 ed., Aug. 2010.
    .. [man_pam_unix] pam_unix(8) - Linux man pages.
    .. [man_pam_ldap] pam_ldap(5) - Linux man pages.
    .. [man_pam_mkhomedir] J. Gunthorpe, pam_mkhomedir(8) - Linux man pages.
    .. [pam_makehomedir_code] J. Gunthorpe, "PAM Make Home Dir module," tech. rep., Feb. 1993.