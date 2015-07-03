Dominio del problema
====================

El sistema distribuido a crear debe satisfacer una serie de requisitos que definen diferentes características relacionadas con la "transparencia" del sistema. Una de estas transparencias es la de acceso: un usuario debe acceder al sistema distribuido por cualquier punto de acceso y ser capaz de realizar el mismo tipo de acciones.

Las propiedades distribuidas del sistema dificultam la creación de un sistema de gestión de usuarios que sea coherente para todos los nodos y garantice que los diferentes usuarios disponen del mismo conjunto de herramientas. Un problema particular que se deriva de esta circunstancia son los directorios y configuración de cada usuario.

Por ello, es necesario crear un sistema de gestión de la información de usuario de forma que esta sea completamente distribuida. Se plantea aprovechar el sistema de autenticación presente en la infraestructura (un directorio **LDAP**) para la gestión de las credenciales de acceso e identificación y MarcoPolo como herramienta de descubrimiento. Dicho sistema contará con dos roles claramente diferenciados: un módulo para PAM (*Pluggable Authentication Module*) que gestionará la información de los diferentes usuarios y un servicio que gestione la creación de los diferentes ficheros y la configuración necesaria para que el sistema sea plenamente funcional.

.. TODO: análisis de alternativas