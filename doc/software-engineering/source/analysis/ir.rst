Requisitos de información
=========================

IRQ-1 Información de usuario
----------------------------

- **Versión**: 1
- **Autores**: Diego Martín
- **Fuentes**: Análisis preliminar
- **Objetivos asociados**: OBJ-1
- **Requisitos asociados**: RF-1
- **Descripción**: Se consultará la información de los usuarios que accedan al sistema con el objetivo de realizar las acciones asociadas al evento de inicio de sesión de forma acorde a cada uno de ellos.
- **Datos específicos**: UID, GID, $HOME
- **Tiempo de vida**: El tiempo necesario para que la operación se lleve a cabo (generalmente menos de 5 segundos).
- **Ocurrencias simultáneas**: Tantas como usuarios accedan concurrentemente al sistema.
- **Importancia**: Muy alta
- **Urgencia**: Muy alta
- **Estado**: Completo
- **Estabilidad**: Estable
  
IRQ-2 Directorio ``/etc/skel``
------------------------------

- **Versión**: 1
- **Autores**: Diego Martín
- **Fuentes**: Análisis preliminar
- **Objetivos asociados**: OBJ-1
- **Requisitos asociados**: RF-2
- **Descripción**: Siguiendo la secuencia típica de creación de usuarios en un sistema UNIX, se utilizarán los archivos almacenados en el directorio ``/etc/skel`` como referencia para los ficheros a incluir en el directorio HOME creado.
- **Datos específicos**
- **Tiempo de vida**: Permanente.
- **Ocurrencias simultáneas**: Una única ocurrencia.
- **Importancia**: Muy alta
- **Urgencia**: Muy alta
- **Estado**: Completo
- **Estabilidad**: Estable