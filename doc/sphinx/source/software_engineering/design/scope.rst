Ámbito
======

Todos los equipos participantes en el sistema contarán con dos componentes de funcionalidad claramente definida:

- Un módulo para PAM denominado ``pam_mkpolohomedir`` que se compilará como biblioteca compartida y será almacenado en el archivo ``/lib/security/pam_mkpolohomedir.so``.
- Un servicio apoyado sobre el *framework* `Twisted <http://twistedmatrix.com/>`_ que recogerá las peticiones del módulo y las procesará.
  
Se utilizarán el *binding* de Marco para C en el caso del módulo de PAM y el *binding* para Python en el caso del servicio creado sobre Twisted. 