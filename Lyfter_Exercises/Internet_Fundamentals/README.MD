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

| API type | Data format | Flexibility level                       | Implementation difficulty | Current use (High / Medium / Slow) |
|----------|-------------|-----------------------------------------|---------------------------|------------------------------------|
| REST     | JSON/XML    | Medium, the server defines the response | Low                       | Hig                                |
| SOAP     | XML only    | Low, the contract (WSDL) defines it     | High                      | Low                                |
| GraphQL  | JSON        | High, the client defines the response   | Medium                    | Medium                             |

For a modern startup building an online booking app, REST is the better choice.
Why?, here my explanation:
A booking system is transactional CRUD over a fer resources such as: users, providers, slots, and reservations. REST fits that model directly, and the hard parts are already solved at the protocol level. Availability queries are the most frequent operation and are cacheable by by URL, sometimes GraphQL gives up by posting everything to a single endpoint. Concurrent bookings for the same slot are handled with 409 conflict, and retried payments with an idempotency key header. The services of a booking startup depends on Stripe, Twilio, calendar providers, all of them speak REST, and a small team ships faster with it. GraphQL wins once the product runs several clients (web, iOS, Android, an admin dashboard), that is a scaling decision, not a staring one.  

Summary:
REST scales better in traffic of data because it can use HTTP caching, but it serves the same data in one fixed shape.
GraphQL scales better in variety of clients, if the app needs to serve different shapes of the same data (When Android, iOS and web clients need different shapes of he same data, and you find yourself creating a separate endpoint for each one, GraphQL is a good fit, the client declares which fields it wants, so onw schema serves all three)
SOAP is better when a formally enforced contract is required between organizations that do not trust each other.

## 4. Exploring APIs with Postman
### 4.1 API selection
- **API Name:**
    RESTful API
- **Description:**
    RESTful API is a free REST API for testing and learning, it's baked by a real database, it allows to save, update, get and delete data through HTTP requests, with a similar behavior of a production backend. 
    See below what it offers:
    - It supports five methods: GET, POST, PUT, PATCH and DELETE.
    - Enabled CORS for all domains, so you can make requests from a browser or Postman.
    - HTTPS in all its endpoints.
    - The fields "data" accepts any valid JSON structure.
    - 13 preloaded sample objects: (Apple products, Samsung, etc), to consult without creating anything.

API Site URL: https://restful-api.dev/

### 4.2 Postman configuration
- **Collection name:**
    RESTful API
- **Added requests:**
  - GET 
  - POST 
  - PUT
  - PATCH
  - DELETE

### 4.3 Analysis and execution

| Request                    | Method | Endpoint                                                         | Status Code | Notes                            |
|----------------------------|--------|------------------------------------------------------------------|-------------|----------------------------------|
| Get all objects            |  GET   | https://restful-api.dev/objects                                  | 200 OK      | All the objects were shown.      |
| Add a new object           | POST   | https://restful-api.dev/objects                                  | 200 OK      | The object was created.          |
| Update an object           | PUT    | https://restful-api.dev/objects/ff808181a067127101a09322e5007dad | 200 OK      | The object was totally updated.  |
| Partially update an object | PATCH  | https://restful-api.dev/objects/ff808181a067127101a09322e5007dad | 200 OK      | The object was partially updated.| 
| Delete an object           | DELETE | https://restful-api.dev/objects/ff808181a067127101a0933274777df5 | 200 OK      | The object was deleted.          |

### 4.4 Technical Explanation
    RESTful API is a free REST API for testing and learning, it's baked by a real database, it allows to save, update, get and delete data through HTTP requests, with a similar behavior of a production backend.
#### [Get all objects]
- **HTTP Method:**
    GET
- **Endpoint:**
    https://restful-api.dev/objects
- **Parameters / body:**
    None
- **Response description:**
    Retrieves a predefined set of sample objects from the public API. This endpoint provides a limited, reserved selection available for demonstration purposes - not all stored objects created by you or others. Object structure: id, name and data{}
**What did I learn from the process?**
    I learned how HTTP GET requests work and how to receive the values
#### [Add new object]
- **HTTP Method:**
    POST
- **Endpoint:**
    https://restful-api.dev/objects
- **Parameters / body:**
    body = {
            "name": "Apple MacBook Pro 16",
            "data": {
                "year": 2019,
                "price": 1849.99,
                "CPU model": "Intel Core i9",
                "Hard disk size": "1 TB"
                    }
                 }
- **Response description:**
    Retrieves the complete created object additional with the creation date.
**What did I learn from the process?**
    I learned how to create new objects through a POST method.

#### [Update an object]
- **HTTP Method:**
    PUT
- **Endpoint:**
    https://restful-api.dev/objects/ff808181a067127101a09322e5007dad
- **Parameters / body:**
    body = {
  "name": "Samsung Galaxy S24 FE UPDATED",
  "data": {
    "year": 2024,
    "price": 500,
    "CPU model": "Exynos 2400e 4nm UPDATED",
    "Hard disk size": "128GB UPDATED"
  }
}
- **Response description:**
    Retrieves the complete updated object additional with the updated date.
**What did I learn from the process?**
    I learned how to update a complete object through a PUT method.

#### [Partially update an object]
- **HTTP Method:**
    PATCH
- **Endpoint:**
    https://restful-api.dev/objects/ff808181a067127101a09322e5007dad
- **Parameters / body:**
    body = {
            "name": "Samsung Galaxy S24 FE UPDATED with patch"
           }
- **Response description:**
    Retrieves the complete updated object additional with the updated date.
**What did I learn from the process?**
    I learned how to partially update an object through a PATCH method.

#### [Delete an object]
- **HTTP Method:**
    DELETE
- **Endpoint:**
    https://restful-api.dev/objects/ff808181a067127101a0933274777df5
- **Parameters / body:**
    None
- **Response description:**
    Retrieves a message letting the user know that the object was deleted:
    {
    "message": "Object with id = ff808181a067127101a0933274777df5 has been deleted."
    }
**What did I learn from the process?**
    I learned how to consume a DELETE method to delete objects.


### 4.5 Final reflection
    What I learned about how APIs work

    An API is a contract, not a piece of code. The client and the server agree on a set of operations and on what each response means, and HTTP already carries most of that agreement: the method states the intent, the URL identifies the resource, and the status code carries the outcome. A 409 is not a bug in my code, it is the server telling me someone booked that slot first. The difference between REST, SOAP and GraphQL comes down to one question: who decides the shape of the response. The server, the contract, or the client. 

    How Postman helped me understand client–server communication

    Postman made the request visible. Seeing the method, headers, body and response side by side turned an abstract step into a structured text message I could read. It also let me test the protocol instead of reading about it. 