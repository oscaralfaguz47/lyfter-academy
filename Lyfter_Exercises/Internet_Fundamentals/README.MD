# Internet Fundamentals

## 1. From Client to Server
    When I type www.youtube.com in my browser, the following steps take place:
    1. The browser parses the input and, because youtube.com is on the HSTS preload list, forces the HTTPS scheme.
    2. DNS resolves the domain name into a public IP address. The browser first checks its own cache, then the OS cache, and only then queries a recursive resolver, which walks the hierarchy: root server, .com TLD servers and then Youtube's authoritative name servers.
    3. With the IP address the browser opens a TCP connection to por 443, followed by a TLS handshake, the server presents its certificate, the browser validates it against a trusted Certificate Authority (CA), and both sides derive the session keys.
    4. Over the encrypted channel, the browser sends an HTTP Get request for the path "/", including headers such as Host, Cookies and User-agent.
    5. The server returns a 200 response with the HTML document.
    6. The browser parses the HTML, build the DOM, and requests the CSS, Javascript and images it references, then renders the page.
    7. The player requests the video itself from a separate CDN host "googlevideo.com".

    HTTPS is simple HTTP running over TLS, it provides three things that plain HTTP does not such as: encryption, authentication of the server through its certificate and integrity of the data in transit  

## 2. Frontend & Backend in action
    Assuming I'm building a web app to schedule appointments.
    1. Some parts corresponding to the frontend are: The login, the dashboard where the user can see the pending appointments, the calendar and the form to schedule a new appointment. And some parts corresponding to the backend are: The logic to validate if the selected date is available to schedule an appointment, the methods to return the pending appointments that the frontend would show on the dashboard and the logic on how the appointments are going to be saved in the database.
    2. For the frontend I would use: React, Typescript and NextJS, and for the backend I would use C# to build the API in in ASP.NET Framework, SQL server for the database and Swagger to design and documentation of the API. 
    3. The fronted would communicate with that backend via HTTP protocol, by using the backend methods Get, Post, Put, Patch and Delete.

    API: stands for Application Programming Interface, it allows the communication between a web client or between other APIs.
    HTTP: Hyper Text Transfer Protocol, is a set of rules that allow the communication between the web client such as web browsers and servers to internet.
    Request/Response: Request is a message that client sends to the server and a response is what the server sends back to the client    

## 3. REST vs SOAP vs GraphQL

| API Type | Data format | Nivel de flexibilidad | Dificultad de implementación | Uso actual (Alta / Media / Baja) |
|-------------|------------------------|------------------------|-------------------------------|-----------------------------------|
| REST        |                        |                        |                                |                                    |
| SOAP        |                        |                        |                                |                                    |
| GraphQL     |                        |                        |                                |                                    |

**¿Cuál es más apropiada para una startup moderna? ¿Por qué?**

## 4. Explorando APIs con Postman

### 4.1 Selección de la API
- **Nombre de la API:**
- **Descripción:**

### 4.2 Configuración en Postman
- **Nombre de la colección:**
- **Solicitudes agregadas:**
  - GET -
  - POST -
  - PUT/PATCH/DELETE -

### 4.3 Ejecución y análisis

| Solicitud | Método | Endpoint | Código de estado | Notas |
|-----------|--------|----------|-------------------|-------|
|           |        |          |                   |       |

### 4.4 Explicación técnica

#### [Nombre de la solicitud]
- **Método HTTP:**
- **Endpoint:**
- **Parámetros / body:**
- **Descripción de la respuesta:**

**¿Qué aprendiste del proceso?**

### 4.5 Reflexión final