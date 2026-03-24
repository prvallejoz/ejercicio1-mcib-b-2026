GRUPO 7 - SERVICIO API PARA GESTION DE PARQUEADEROS

Parte 1 – Construcción del API
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


