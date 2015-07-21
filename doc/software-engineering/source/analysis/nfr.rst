Requisitos no funcionales
=========================

NFR-1: Tiempo de ejecución
--------------------------

- **Versión**: 1
- **Autores**: Diego Martín
- **Fuentes**: Análisis preliminar
- **Objetivos asociados**: OBJ-1, OBJ-2
- **Requisitos asociados**: RF-1, RF-2
- **Descripción**: El tiempo de ejecución de todas las operaciones a realizar no deberá afectar negativamente a la experiencia del usuario. Se acepta un tiempo de ejecución razonable aquel menor que 5 segundos. 
- **Importancia**: Alta
- **Urgencia**: Alta
- **Estado**: Completo
- **Estabilidad**: Estable

NFR-2: Tomcat
-------------

- **Versión**: 1
- **Autores**: Diego Martín
- **Fuentes**: Análisis preliminar
- **Objetivos asociados**: OBJ-1
- **Requisitos asociados**: RF-2, RF-3
- **Descripción**: El sistema deberá configurar automáticamente una instancia del contenedor de servicios **Tomcat** para cada usuario.
- **Importancia**: Media
- **Urgencia**: Media
- **Estado**: Completo
- **Estabilidad**: Estable

NFR-3: Confidencialidad
-----------------------

- **Versión**: 1
- **Autores**: Diego Martín
- **Fuentes**: Análisis preliminar
- **Objetivos asociados**: OBJ-1
- **Requisitos asociados**: RF-1, RF-2
- **Descripción**: El sistema deberá garantizar que todos los datos de los diferentes usuarios serán transferidos utilizando canales seguros y su manipulación en un nodo no deberá comprometer la privacidad de los mismos.
- **Importancia**: Alta
- **Urgencia**: Alta
- **Estado**: Completo
- **Estabilidad**: Estable

NFR-4: Seguridad
----------------

- **Versión**: 1
- **Autores**: Diego Martín
- **Fuentes**: Análisis preliminar
- **Objetivos asociados**: OBJ-1
- **Requisitos asociados**: RF-1, RF-2
- **Descripción**: Todas las comunicaciones entre los diferentes nodos que impliquen la transferencia de datos privados o la solicitud de ejecución de una acción con privilegios de superusuario utilizará conexiones TLS/SSL con validación de un certificado en ambos lados del canal (cliente y servidor).
- **Importancia**: Muy alta
- **Urgencia**: Alta
- **Estado**: Completo
- **Estabilidad**: Estable
  
NFR-5: Lenguaje de programación para el módulo PAM
--------------------------------------------------

- **Versión**: 1
- **Autores**: Diego Martín
- **Fuentes**: Análisis preliminar
- **Objetivos asociados**: OBJ-1
- **Requisitos asociados**: RF-1
- **Descripción**: Los módulos de PAM son vinculados a este servicio como bibliotecas compartidas, generalmente programadas en C. Se deberá por tanto implementar toda la funcionalidad en este lenguaje.
- **Importancia**: Alta
- **Urgencia**: Alta
- **Estado**: Completo
- **Estabilidad**: Estable
- **Comentarios**: Si bien existen mecanismos de interconexión con otros lenguajes (como `pam-python (http://pam-python.sourceforge.net/) <http://pam-python.sourceforge.net/>`_), se consideran alternativas más complejas que no aportan ningún tipo de ventaja.

NFR-6: Lenguaje de programación para el receptor
------------------------------------------------

- **Versión**: 1
- **Autores**: Diego Martín
- **Fuentes**: Análisis preliminar
- **Objetivos asociados**: OBJ-2
- **Requisitos asociados**: RF-2
- **Descripción**: La implementación del receptor, encargado de la creación de los diferentes directorios y posterior configuración se realizará en el lenguaje Python utilizando el *framework* Twisted como herramienta de soporte.
- **Importancia**: Alta
- **Urgencia**: Alta
- **Estado**: Completo
- **Estabilidad**: Estable

.. 
    - **Versión**:
    - **Autores**:
    - **Fuentes**:
    - **Objetivos asociados**
    - **Requisitos asociados**
    - **Descripción**
    - **Importancia**
    - **Urgencia**
    - **Estado**
    - **Estabilidad**
    - **Comentarios**


