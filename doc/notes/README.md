# Udacity Full Stack Development Nanodegree

This is the lecture notes for **RESTful API development** of Udacity's Full Stack Development Nanodegree

---

## API

### Overview

**API** stands for Application Programming Interface.

* API doesn't expose the implementation of functionality
* A controlled way to expose application and its data
* Standard way to interact with application and its data

### How Does API Support Frontend

For standard Flux application, the frontend and the backend interact using API.

* Client sends a request to the API server
* The API server parses that request
* Assuming the request is formatted correctly, the server queries the database for the information or performs the action in the request
* The server formats the response and sends it back to the client
* The client renders the response according to its implementation

### REST

**REST** stands for Representational State Transfer.

* **Uniform Interface** Every rest architecture must have a standardized way of accessing and processing data resources. This include unique resource identifiers (i.e., unique URLs) and self-descriptive messages in the server response that describe how to process the representation (for instance JSON vs XML) of the data resource.
* **Stateless** Every client request is self-contained in that the server doesn't need to store any application data in order to make subsequent requests
* **Client-Server** There must be both a client and server in the architecture
* **Cacheable & Layered System** Caching and layering increases networking efficiency. Since the server is stateless, all the responses can be cached for improved efficiency.

---

## HTTP

### Overview

**Hypertext Transfer Protocol** is a protocol that provides a standardized way for computers to communicate with each other. It has been the foundation for data communication over the internet since 1990 and is integral to understanding how client-server communication functions.

* **Connectionless** When a request is sent, the client opens the connection; once a response is received, the client closes the connection. The client and server only maintain a connection during the response and request. Future responses are made on a new connection.
* **Stateless** There is no dependency between successive requests.
* **Not Sessionless** Utilizing headers and cookies, sessions can be created to allow each HTTP request to share the same context.
* **Media Independent** Any type of data can be sent over HTTP as long as both the client and server know how to handle the data format. In our case, we'll use JSON.

### URI

URLs are a specific type of URI that is used to locate a resource on the internet when a client makes a request to a server.

* **Scheme** Specifies the protocol used to access the resource, HTTP or HTTPS. In our example http.
* **Host** Specifies the host that holds the resources. In our example www.example.com.
* **Path** Specifies the specific resource being requested. In our example, /tasks.
* **Query** An optional component, the query string provides information the resource can use for some purpose such as a search parameter. In our example, /term=homework.

### Request

HTTP requests are sent from the client to the server to initiate some operation.

#### Elements

In addition to the URL, HTTP requests have other elements to specify the requested resource.

* **Method** Defines the operation to be performed
* **Path** The URL of the resource to be fetched, excluding the scheme and host
* **HTTP** Version
* **Headers** optional information, success as Accept-Language
* **Body** optional information, usually for methods such as POST and PATCH, which contain the resource being sent to the server

#### Methods

* **GET** **ONLY retrieves** information for the requested resource of the given URI
* **POST** Send data to the server to **create a new resource**.
* **PUT** **Replaces** all of the representation of the target resource with the request data
* **PATCH** **Partially modifies** the representation of the target resource with the request data
* **DELETE** **Removes** all of the representation of the resource specified by the URI
* **OPTIONS** Sends the communication options for the requested resource

### Response

After the request has been received by the server and processed, the server returns an HTTP response message to the client. The response informs the client of the outcome of the requested operation.

#### Elements

* **Status Code & Status Message**
* **HTTP Version**
* **Headers** similar to the request headers, provides information about the response and resource representation. Some common headers include:
    * **Date**
    * **Content-Type** the media type of the body of the request
* **Body** optional data containing the requested resource

#### Status Code

Codes fall into five categories

* **1xx** Informational
* **2xx** Success
* **3xx** Redirection
* **4xx** Client Error
* **5xx** Server Error

Below are the common codes. For further details please refer to [HTTP Dogs](https://httpstatusdogs.com/)

* **200** OK
* **201** Created
* **304** Not Modified
* **400** Bad Request
* **401** Unauthorized
* **404** Not Found
* **405** Method Not Allowed
* **500** Internal Server Error

### Debugging Tools -- cURL

**Curl** is a command line tool that completes IP transfers of data using URLs. One quick way to test your API.

#### Commonly Used Options

* **-X** or --request COMMAND
* **-d** or --data DATA
* **-F** or --form CONTENT
* **-u** or --user USER[:PASSWORD]
* **-H** or --header LINE

### API Organization

When organizing API endpoints, they should be based on the resources instead of on actions. The request methods will determine what action should be taken at a given URL endpoint. Your entire API's scheme should be consistent, clear and concise. 

#### Should be Intuitive

#### Organize by Resource

* Use nouns in the path, not verbs
* The method used will determine the operation taken

#### Keep a Consistent Scheme

* Plural nouns for collections
* Use parameters to specify a specific item

#### Don’t be Too Complex or Lengthy

* No longer than collection/item/collection
* If the above hierarchy cannot solve the problem, think about re-structuring the application

### CORS

#### Overview

**CORS** stands for cross-origin resource sharing. By default, the web uses **the same-origin policy** that a web application using those APIs can only request resources from **the same origin the application was loaded from**, unless the response from other origins includes the right CORS headers.

Following cases all belong to **cross-origin**:

* Different domains
* Different subdomains (example.com and api.example.com)
* Different ports (example.com and example.com:1234)
* Different protocols (http://example.com and https://example.com)

Modern browsers handle the client side of cross-origin sharing, including headers and policy enforcement. **The CORS standard means for backend developers the server should be able to handle CORS request and response headers**

#### Implementation

When the server receives a request with method OPTIONS, it include the following header options in response to implement CORS policies:

* **Access-Control-Allow-Origin**
    What client domains can access its resources. For any domain use *
* **Access-Control-Allow-Credentials**
    Only if using cookies for authentication - in which case its value must be true
* **Access-Control-Allow-Methods**
    List of HTTP request types allowed
* **Access-Control-Allow-Headers**
    List of http request header values the server will allow, particularly useful if you use any custom headers

#### Integration with Flask

```python
# Import Dependencies
from flask import Flask
from flask_cors import CORS

def create_app(test_config=None):
    app = Flask(__name__)
    # Option 1 -- basic initialization
    # CORS(app)
    # Option 2 -- resource specific usage
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    # CORS Headers 
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response
    
    @app.route('/messages')
    # Option 3 -- route specific usage
    @cross_origin()
    def get_messages():
        return 'GETTING MESSAGES'
```

### Flask Routes

#### Basic

```python
@app.route('/hello')
def get_greeting():
    return jsonify({'message':'Hello, World!'})
```

#### Variable Rule

```python
# Using <converter:variable_name> to specify parameters to be passed from URL to function as arguments
@app.route('/entrees/<int:entree_id>')
def retrieve_entree(entree_id):
    return 'Entree %d' % entree_id
```

#### HTTP Methods

By default, the @app.route decorator answers only get requests.

```python
@app.route('/hello', methods=['GET', 'POST'])
def greeting():
    if request.method == 'POST':
        return create_greeting()
    else:
        return send_greeting()
```

OPTIONS requests are automatically implemented and HEAD is also automatically implemented if GET is present.

#### Query Parameters

The below examples show the format of query parameters. When writing query parameters convention dictates that:

* A question mark precedes the query parameters
* Parameters are in key=value pairs with an equal sign in between the key and value
* Sets of parameters are separated by an ampersand

```python
@app.route('/entrees', methods=['GET'])
  def get_entrees():
    page = request.args.get('page', 1, type=int)
```
