Requisitos funcionales
======================

RF-1: Inicio de sesión
----------------------

- **Versión**: 1
- **Autores**: Diego Martín
- **Fuentes**: Análisis preliminar
- **Objetivos asociados**: OBJ-1, OBJ-2, OBJ-3
- **Requisitos asociados**: IRQ-1, NRF-3, NRF-4
- **Descripción**: Al acceder al sistema, el nodo deberá notificar este evento a todos los demás componentes del sistema distribuido.
- **Precondición**
- **Secuencia normal**:

    1. El usuario accede al nodo con sus credenciales.
    2. El módulo PAM validará las credenciales consultando las diferentes fuentes de datos dispuestas. En caso de que estas no sean correctas, el caso de uso finaliza y el usuario es notificado. Si las credenciales son correctas, se continúa.
    3. Se carga el módulo creado y comienza la configuración local.
    4. Una vez que la configuración local ha finalizado, se realiza la detección de los diferentes nodos utilizando **Marco**.
    5. Se solicita de forma iterativa la creación y configuración de los ficheros y parámetros del usuario a todos los nodos. Comienza el caso de uso RF-2 en cada uno de los nodos
    6. El nodo al que el usuario se ha conectado da acceso a este.
- **Poscondición**: El sistema ha sido configurado para que el usuario se conecte al mismo.
- **Excepciones**:

    + En caso de que se dé un error en la conexión con algún nodo, se registra el incidente.
- **Rendimiento**: Alto
- **Frecuencia**: Alta
- **Importancia**: Muy alta
- **Urgencia**: Alta
- **Estado**: Completo
- **Estabilidad**: Estable

RF-2: Creación y configuración
------------------------------

- **Versión**: 1
- **Autores**: Diego Martín
- **Fuentes**: Análisis preliminar
- **Objetivos asociados**: OBJ-2, OBJ-3
- **Requisitos asociados**: NFR-2, NFR-4
- **Descripción**: A petición del actor **ACT-2** el actor **ACT-3** configurará el nodo para que el usuario indicado pueda trabajar.
- **Precondición**
- **Secuencia normal**:

    1. El actor recibe una solicitud de creación.
    2. Se verifican la identidad del solicitante según lo especificado en el requisito no funcional **NFR-4**.
    3. Se verifica que la petición contiene datos válidos (comando correcto, argumentos válidos, etcétera)
    4. Con el objetivo de cumplir el requisito no funcional **NFR-1** el solicitante es notificado de que la operación se realizará en lugar de recibir una confirmación del estado de esta cuando sea realizada. El tiempo de operación es significativo cuando el número de nodos a los que se solicita la creación es elevado y se realiza iterativamente. Este tiempo de espera bloquearía el acceso al sistema hasta que todas las operaciones concluyan.
    5. Se crea el directorio de usuario.
    6. En caso de que el directorio ``/etc/skel`` (o aquel donde se encuentre el directorio esqueleto) contenga una copia del contenedor de servicios *Tomcat*, comienza el caso de uso **RF-3**.
- **Poscondición**: El usuario puede acceder a la totalidad del sistema desde un único punto de entrada.
- **Excepciones**:

    + En caso de algún error inesperado durante el proceso, se almacena un registro de esta situación.
- **Rendimiento**: Alto
- **Frecuencia**: Alta
- **Importancia**: Alta
- **Urgencia**: Alta
- **Estado**: Completo
- **Estabilidad**: Estable

RF-3: Configuración de Tomcat
-----------------------------

- **Versión**: 1
- **Autores**: Diego Martín
- **Fuentes**: Análisis preliminar
- **Objetivos asociados**: OBJ-2
- **Requisitos asociados**: IRQ-2, NFR-2
- **Descripción**: En caso de que el usuario deba disponer de una instancia de Tomcat, se configuran los parámetros específicos para su cuenta.
- **Precondición**
- **Secuencia normal**

    1. El caso de uso comienza como extensión del caso de uso **RF-2**, tras la copia del directorio que contiene la instancia de Tomcat.
    2. La aplicación revisa todos los ficheros de configuración y ajusta aquellos parámetros de forma adecuada para el usuario. Un ejemplo son los puertos TCP que se abrirán para la instancia.
- **Poscondición**: El usuario dispone de una instancia de Tomcat configurada.
- **Excepciones**:

    + En caso de algún error inesperado durante el proceso, se almacena un registro de esta situación.
- **Rendimiento**: Alto
- **Frecuencia**: Alta
- **Importancia**: Media
- **Urgencia**: Media
- **Estado**: Completo
- **Estabilidad**: Estable

Vista de casos de uso
---------------------

.. toctree::
    :maxdepth: 2

    uc

.. 
    - **Versión**: 
    - **Autores**: 
    - **Fuentes**: 
    - **Objetivos asociados**: 
    - **Requisitos asociados**: 
    - **Descripción**
    - **Precondición**
    - **Secuencia normal**
    - **Poscondición**
    - **Excepciones**
    - **Rendimiento**
    - **Frecuencia**
    - **Importancia**
    - **Urgencia**
    - **Estado**
    - **Estabilidad**
    - **Comentarios**