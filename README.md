# GRUPO 7 - SERVICIO API PARA GESTION DE PARQUEADEROS

## Preguntas para Trabajo Final

### 1. ¿Si este sistema se desplegara en un parqueadero real con múltiples accesos, ¿qué cambios arquitectónicos serían necesarios para garantizar disponibilidad, sincronización y escalabilidad del servicio?

Si el sistema de parqueaderos presentado se desplegara en un parqueadero real con múltiples accesos, sería necesario realizar varios cambios arquitectónicos para garantizar la disponibilidad, sincronización y escalabilidad del servicio.

En primer lugar, la API desarrollada con Flask debería dejar de ejecutarse como una aplicación monolítica en una sola instancia. En su lugar se debería implementar una arquitectura basada en múltiples instancias detrás de un balanceador de carga, lo que permitiría distribuir las solicitudes entre varios servidores. Otra opción adicional sería colocar un servidor central donde corra la API y thin clients en los accesos que se conecten a la API alojada en el servidor central.

En cuanto a la base de datos, el uso de SQLite no es adecuado para este escenario. Sería necesario migrar a un sistema de gestión de bases de datos más robusto como PostgreSQL o SQL Server, que soporte múltiples conexiones simultáneas, transacciones y mecanismos de bloqueo adecuados para evitar inconsistencias en los registros de entrada y salida de vehículos.

Para garantizar la sincronización de datos entre múltiples accesos, se deberían implementar mecanismos de control de concurrencia y transacciones, asegurando que una misma placa no pueda registrar múltiples ingresos o salidas inconsistentes al mismo tiempo.

Adicionalmente, para mejorar la escalabilidad, se podría contenerizar la aplicación utilizando Docker y gestionarla con un orquestador como Kubernetes, lo que permitiría escalar automáticamente el número de instancias según la demanda.

Para la alta disponibilidad, sería recomendable desplegar la solución en una nube como Google Cloud Platform utilizando servicios gestionados como balanceadores de carga, bases de datos replicadas y almacenamiento redundante.

Finalmente, se podrían incorporar mecanismos de cacheo y colas de mensajes para desacoplar procesos críticos, como el cálculo de pagos o registros, mejorando el rendimiento general del sistema y la experiencia del usuario.

### 2. ¿Cómo podrían hacer el sistema más flexible para soportar distintos esquemas de cobro?

Para hacer el sistema más flexible y permitir soportar distintos esquemas de cobro, sería necesario desacoplar la lógica de cálculo del valor a pagar del resto de la aplicación y hacerla configurable.
En la implementación actual el cálculo del costo está directamente integrado en el código del API desarrollado con Flask, lo que limita la capacidad de adaptarse a nuevos modelos de negocio. Para mejorar esto se podría implementar un diseño basado en patrones como estrategia donde cada tipo de tarifa (por hora, tarifa fija, tarifas por fracciones, tarifas diferenciadas por horario) se maneje como un módulo independiente.

Además, los esquemas de cobro deberían almacenarse en una base de datos en lugar de estar definidos en el código. Al migrar de SQLite a una base de datos más robusta como PostgreSQL, se podrían definir tablas para tarifas, reglas de cobro y configuraciones dinámicas que puedan modificarse sin necesidad de redeplegar el sistema.
También sería recomendable exponer endpoints adicionales en el API que permitan administrar estos esquemas de cobro (crear, actualizar, eliminar tarifas), facilitando la gestión desde una interfaz administrativa.

Para mayor flexibilidad, se podrían definir reglas basadas en condiciones como:
•	Tipo de vehículo 
•	Tiempo de permanencia 
•	Horarios (diurno/nocturno) 
•	Días especiales o feriados

Finalmente se podría integrar pasarelas de pago como PlaceToPay o similares a los cuales se envía los datos de facturación y el cliente podría realizar el pago en línea mediante tarjetas bancarias.

### 3. ¿Qué mejoras implementarían en el diseño de la API para separar correctamente la lógica de negocio (cálculo de tarifas, validaciones) de la capa de presentación (HTML)?

Para separar correctamente la lógica de negocio de la capa de presentación, sería necesario aplicar una arquitectura en capas que permita desacoplar responsabilidades dentro del sistema.

Actualmente, en la API desarrollada con Flask, la generación del HTML y la lógica de negocio están parcialmente mezcladas, lo que dificulta el mantenimiento y la escalabilidad del sistema.

Como mejora, se podría implementar una estructura basada en el patrón MVC (Modelo-Vista-Controlador) que estaria estructurado de la siguente manera:
•	Modelo: Encargado de la interacción con la base de datos. Aquí se gestionaría el acceso a datos en SQLite o una base de datos más robusta. 
•	Controlador: Manejaría los endpoints del API, recibiendo las solicitudes HTTP, validando datos de entrada y delegando la lógica de negocio a servicios especializados. 
•	Servicios: Aquí residiría la lógica de negocio, como el cálculo de tarifas, validaciones de placas y reglas de operación. Esta capa sería independiente del framework y reutilizable. 
•	Vista: Encargada únicamente de la presentación, utilizando templates HTML o incluso separando completamente el frontend en otra aplicación. 

Adicionalmente, se recomienda transformar el sistema en una API REST pura que devuelva respuestas en formato JSON, desacoplando completamente el frontend. De esta manera, el HTML podría ser consumido por un cliente independiente mientras la API se enfoca únicamente en la lógica y los datos.

También sería buena práctica organizar el proyecto en módulos separados como por ejemplo: routes/, services/, models/, templates/, lo que facilitaría la mantenibilidad y desarrollo del sistema.


## Parte 1 – Construcción del API

•	Código fuente del API

Como parte del ejercicio desarrollamos un api básico para gestionar el ingreso y salida de un parqueadero, basados en el número de placa, levantamos un html simple que al ingresar el número de placa permite registrar la hora de ingreso y salida de los vehículos, además permite calcular el valor a pagar y registro del pago para permitir la salida del vehículo del parqueadero.
Se desarrolló el API utilizando Flask, además se hace uso de las librerías datetime, math y sqlite3 para implementar una base de datos sencilla que almacene los datos de vehículos y los registros de entrada y salida.
Además del endpoint principal, se desarrollaron los endpoints para el cálculo del valor a pagar y para consultar y borrar registros de la base de datos sqlite


<img width="886" height="386" alt="image" src="https://github.com/user-attachments/assets/922cadc7-b3c0-4c62-9969-2a5206e4ec93" />

Funcionalidades mínimas
Se cuenta con endpoints GET, POST, validación básica de datos y manejo de errores.

Parte 2 – Uso de Branches
Para el desarrollo se crearon 4 branches, una master y 3 devs, una para cada integrante que aportó con una funcionalidad específica, para posteriormente realizar los merges hacia la Branch master.

<img width="886" height="475" alt="image" src="https://github.com/user-attachments/assets/e8b5c5c9-7e25-45a1-8fa5-df72b238956b" />


Parte 3 – Contenerización
Ya con la API funcional se procedió a generar el archivo DockerFile para la generación del contenedor para la ejecución de la API, así como el archivo requeriments.txt para importar flask al contenedor.

<img width="886" height="756" alt="image" src="https://github.com/user-attachments/assets/c6dde898-f929-436b-a1dc-a929040fb0df" />



<img width="886" height="494" alt="image" src="https://github.com/user-attachments/assets/a356feae-53bc-43de-adc8-384c5163ff48" />


Parte 4 – Pruebas con curl
Se realizaron las pruebas con curl para obtener los datos desde el API, tanto para los endpoints GET, POST y manejo de errores.


<img width="834" height="445" alt="image" src="https://github.com/user-attachments/assets/f833c4d9-4468-42f1-b08e-451a5d350c07" />


<img width="980" height="377" alt="image" src="https://github.com/user-attachments/assets/e0b06dd7-6a78-4bff-b5b1-8ddc02f81242" />


<img width="1809" height="705" alt="image" src="https://github.com/user-attachments/assets/362329c3-2d76-4636-be7e-4f44b54ed417" />


Parte 5 – Despliegue en Cloud
•	El API fue cargado a Google Cloud, clonando el repositorio de GitHub.

<img width="1138" height="373" alt="image" src="https://github.com/user-attachments/assets/405f3e4e-2e5e-46d3-8f3c-a2840a617dcb" />


<img width="2358" height="800" alt="image" src="https://github.com/user-attachments/assets/fe605c81-1170-4821-be57-b18d78f9e9fc" />

No se publicó el API en el servicio de nube ya que no se cuenta con una cuenta de billing para proceder con la publicación.

<img width="2434" height="872" alt="image" src="https://github.com/user-attachments/assets/12633242-c97c-4aee-8805-4fa3280decc4" />

Parte 6 – Evidencia
•	API funcionando localmente


<img width="886" height="498" alt="image" src="https://github.com/user-attachments/assets/61252eaa-5a67-479e-b73c-312f6fc344a7" />

<img width="886" height="445" alt="image" src="https://github.com/user-attachments/assets/bc0e4192-9a61-4465-9e24-a18d5b66cdc7" />

•	Construcción de imagen Docker


<img width="1416" height="692" alt="image" src="https://github.com/user-attachments/assets/ae138eb4-6307-402f-9d6f-f321271a1a9c" />


<img width="1533" height="116" alt="image" src="https://github.com/user-attachments/assets/cdd102bb-bb06-47df-a060-6e50407192b1" />

<img width="2123" height="1198" alt="image" src="https://github.com/user-attachments/assets/bc4803da-e4aa-473b-b861-0af08c022ac4" />

<img width="1650" height="253" alt="image" src="https://github.com/user-attachments/assets/d2e763b0-62ff-447d-9b95-aa8437112287" />


•	Prueba curl exitosa


<img width="834" height="445" alt="image" src="https://github.com/user-attachments/assets/3a5cb4d3-d57c-48d1-af9a-37c2598234df" />


•	API desplegada en Cloud


<img width="2434" height="872" alt="image" src="https://github.com/user-attachments/assets/b98d5a3d-b261-4f25-9050-bd241b0ada0a" />

•	Endpoint accesible públicamente.
El endpoint no pudo ser accesible públicamente debido a la ausencia de cuenta de facturación en Google Cloud.


