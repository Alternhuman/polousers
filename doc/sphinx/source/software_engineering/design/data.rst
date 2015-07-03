Diseño de datos
===============

Objetos de datos
----------------

El sistema utilizará las siguientes estructuras de datos:

- Objetos ``pam_handle_t`` para la representación del estado del módulo PAM
- Objetos ``pwd``, con la información del usuario de relevancia.

Estructuras de archivo
----------------------

Se consultan varias fuentes de datos en la aplicación:

- Fichero de configuración ``/etc/polohomedir/polousers.cfg``, que permite modificar el comportamiento de la aplicación.
- Los certificados almacenados en el directorio ``/etc/polohomedir/certs``.
- Ficheros de *log*, que permiten analizar *a posteriori* el comportamiento del programa, en particular ante algún tipo de situación irregular.
- El directorio ``/etc/skel`` (o aquel que se especifique) para los diferentes ficheros a copiar.
- Los dicheros del directorio Tomcat a modificar, entre los que destaca el fichero ``apache-tomcat-<versión>/conf/server.xml``.