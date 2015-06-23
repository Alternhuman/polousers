Descripción
===========

Necesidades
-----------

El sistema se compone de una serie de nodos independientes a los cuales pueden acceder los usuarios indistintamente. Se desea que los usuarios puedan utilizar los recursos presentes en cualquier nodo sin tener que acceder directamente a ellos (mediante una sesión remota, por ejemplo), y puedan empezar a trabajar sin tener que realizar ningún tipo de configuración.

Esta necesidad está parcialmente cubierta por los módulo de PAM **pam_unix.so** (gestión de usuarios locales) [3]_, ``pam_ldap.so`` (gestión de usuarios del servidor **LDAP**) [4]_ y en particular **pam_mkhomedir.so** [5]_, que permite la creación de un directorio de usuario si el mismo ha iniciado sesión por primera vez en esta máquina.

Sin embargo, una de las características del sistema es la uniformidad de sus nodos en cuando a usuarios se refiere. Por ello, es deseable que los usuarios cuenten con un conjunto básico de datos en cualquier nodo del sistema a la hora de acceder por primera vez. El módulo **pam_mkhomedir** no lleva a cabo esta tarea, pues únicamente crea el directorio (realizando una copia de ``/etc/skel`` de inicio del usuario en la máquina donde se ha realizado el acceso).

Es por tanto necesario crear un mecanismo para llevar a cabo dicha tarea. Aprovechando la funcionalidad de PAM, se ha procedido a crear un módulo complementario a **pam_mkhomedir** denominado **pam_mkpolohomedir**, que aprovecha la herramienta **MarcoPolo** para realizar su cometido.

Características del módulo
--------------------------

La funcionalidad de un módulo de **PAM** se recoge en un objecto compartido que se vincula en tiempo de ejecución con el resto de componentes de **PAM** según se disponga en los ficheros de configuración del módulo (generalmente situados en ``/etc/pam.d/``). [1]_ y que se debe almacenar en ``/lib/security``.  

En el caso particular a resolver, el módulo será invocado tras la ejecución del módulo **pam_mkhomedir**, y se encargará de, aprovechando la funcionalidad de MarcoPolo, detectar todos los nodos disponibles en la red y proceder a la creación en los mismos del directorio de inicio, así como la realización de una serie de tareas adicionales.

Toda la funcionalidad se recoge en el fichero ``pam_mkpolohomedir.c``. Dicho módulo recoge la información de interés (nombre, uid y gid del usuario) a través de llamadas al núcleo de **PAM** [2]_. La estructura del código se basa parcialmente en el del módulo **pam_makehomedir** [6]_, tomando varias funciones del mismo.


.. literalinclude:: src/pam_mkpolohomedir.c
    :language: c
    :lines: 355-372

.. \cfile{pam_mkpolohomedir}{Obtención de la información del usuario}{355}{372}

Una vez obtenida dicha información, las funciones ``create_polo_homedir`` y ``createdirs`` se encargan de la búsqueda de los nodos del sistema (aprovechando el *binding* de **Marco**) y de contactar con ellos.

Creación del directorio
-----------------------

Cada nodo cuenta con una instancia del esclavo de **polousers**, el servicio que se encarga de recibir las peticiones de creación de usuarios. Dicho servicio se implementa sobre el *framework* **Twisted**, y verifica la autoría de cada petición mediante sockets sobre TLS (*Transport Layer Security*).

Una vez creado el directorio, el servicio así lo indica al solicitante, que almacena el registro de dicha operación.

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