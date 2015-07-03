.. polousers documentation master file, created by
   sphinx-quickstart on Sun Jun 14 13:54:08 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to polousers's documentation!
=====================================

La gestión de los usuarios debe ser realizada de forma transparente. Permitiendo a los usuarios acceder al mismo en cualquier nodo y sin ningún tipo de configuración necesaria por su parte, acceder a todos los recursos presentes en el resto de nodos.

El sistema delega parte de la gestión de los usuarios a un directorio **LDAP**, gestionando el acceso al sistema mediante el módulo **PAM**. Sin embargo, debido a las necesidades particulares del sistema, la configuración básica de **PAM** y las herramientas incluidas no son suficientes para conseguir el funcionamiento deseado, y por ello es necesario desarrollar un conjunto de herramientas propias.


Contents:

.. toctree::
   :maxdepth: 2

   description
   reference/intro
   software_engineering/intro



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

