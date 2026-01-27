@app.get("/") # a decorator to define a GET endpoint at the root URL
def home(): #this function handles requests to the root URL - not using async for simplicity
    return {"message": "Hello World"} # Simple GET endpoint returning a greeting message

fastapi dev main.py - running in dev mode auto reloads on code changes

127.0.0.1:8080/docs - makes docs automatically for our routes
/redoc - also automatically for all routes

creatin another decorator /api/posts to get all the posts in json format 

Can stack two decoartors on the same function to display the same html page or response as / and /posts in main.py
All these apis are visible in /doc and /redoc , however we only want the API ones to be thre and html not required to have clear view - so we add include_in_schema=False for html pages
gives separatin btw api routes and html routes
we have kept api routes to return json and html routes for webpages
######################################################

# Templates in FastAPI
Jinja2 templates

While FastAPI is primarily known for building JSON-based APIs, Jinja2 allows it to function like a traditional web framework (like Flask or Django) by generating web pages on the server and sending them to the browser.

Key Concepts
Templating Engine: Jinja2 is a "logic-heavy" templating engine. It lets you write standard HTML and embed Python-like logic (loops, if-statements, variables) using special markers.

First we imported Request from fastapi to make use of jinja2 templates
created a directory templates with home.html 
then removed the class=HTMLResponse since we are no longer directly loading html content , instead having it in tmplates
So we add 
def home(request: Request):  
    return templates.TemplateResponse(request, "home.html") 

pass request as argument and response has the html page we want

we then added dynamic data loading from main.py posts list
we create for loop and if block for conditions and what to print inside home.html templates
then inside the main.py return templates.TemplateResponse(request, "home.html") we added 
     {"posts": posts, "title": "Home"},

it reutns all post, and if title is provided it accordingly runs the if block

# Template inheritance
Craete one parent template that is applicavle to all pages and all the child will inherit it and add their own updates on top 
this saves coderewriting and mentioning same code in each html page

we created a layout.html with the common structure and decalred a 
<body>
    {% block content %} <!-- Block to be overridden by child templates -->
    {% endblock %}
</body>

Now changing the home.html 
we only keep the content unique to that page and extends the rest from layout parent

{% extends "layout.html" %} <!-- Extending the layout template so we don't repeat the same HTML structure -->
{% block content %} <!-- Start of content block to override the parent template's content block -->
{% for post in posts %}  <!-- Loop through each post in the posts list . this adds dynamic content -->
    <div class="post"> 
        <h2>{{ post.title }}</h2>
        <p>{{ post.content }}</p>
        <p>{{ post.author }}</p>
        <small>Posted on {{ post.date_posted }}</small>
    </div>
    <hr>
{% endfor %}
{% endblock %} 

After this we added css and more styling to both home and layout and brought out a strcutre using bootstrap.css
created a static folder with all icons, profile, and under css/main.css for styling

now to imort static directry in templates we first have import using Fastapi 
from fastapi.staticfiles import StaticFiles

post that mount the static path
app.mount("/static", StaticFiles(directory="static"), name="static") # Mounting static files directory -
 take 3 arguments: url path, StaticFiles instance with directory, and name

 Now we can utilise the static folder for styling

 Further in home and layout.html for href or page links , we avoided using # and instead used url_for 
               <a class="nav-link active" aria-current="page" href="{{ url_for('home') }}">Home</a> <!-- Home link - we are passing the function name 'home' to url_for instead of plain # href , this is a better practice for dynamic routing -->
the function name in main is passed here corrspeding to the page and the end point is linked accordingly- the above is for / or /posts

later we added name in each endpoints to create distinction for home and posts 



# Working on single post opening up and endpoints
Path Parameters

We now want indivual posts on each endpoint with the posts id being in the endpoint
like /api/post/12 /api/posts/23 which open indivual post 
first to have end points

we create new endpoint as 

@app.get("/api/posts/{post_id}") 
we create a function to call here def get_post and pass integer inside it
using a for loop we srch inside posts lists for that id , if it matches we return the post 

def get_post(post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            return post
    return {"error": "Post not found"}

INFO   127.0.0.1:59483 - "GET /api/posts/1 HTTP/1.1" 200
INFO   127.0.0.1:49809 - "GET /api/posts/12 HTTP/1.1" 200

currently even if the id doesnt exists , it gives 200 successfull as response
which should not be the case

then we import the HTTPException and status from fastapi
and update the function with raise HTTPException with a message so it displays
also validation is checked automatically if we type /api/posts/abc - so it gives
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": [
        "path",
        "post_id"
      ],
      "msg": "Input should be a valid integer, unable to parse string as an integer",
      "input": "ab"
    }
  ]
}
now we build indivudal pages 
first we create the post.html page 
it extends the layout.html and then nuisances for its own page with edit and delte post options - later for crud operations 

then we create another function for pages with endpoint /post/{post_id}
similar to the get_post function 
@app.get("/posts/{post_id}", include_in_schema=False) # GET endpoint to retrieve a specific post by ID
def post_page(post_id: int, request: Request): #2 arguments: post_id from URL and request of type Request
    for post in posts:
        if post.get("id") == post_id:
            return templates.TemplateResponse( # Rendering the template for the specific post
                request,
                "post.html", # Template for displaying a single post
                {"post": post, "title": post["title"][:50]}, # Passing the specific post and title to the template
            )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

the only difference gere is the return for the function, where we return templates.TemplateResponse 
which is passed with request, template for sigle post, and the post value when matches otherwise an http exception.
/posts/12 - gives specfic post displayed

Now we work on making the post headings as links to our posts currently the main page post do not open the post as indivudal pages
for that in the home.html we update the href in post.title to <a class="article-title" href="{{ url_for('post_page', post_id=post.id) }}">{{ post.title }}</a>
url_for(''post_page) this is the function to be called and post_id is passed as that function also requires the same.

We also work on improving error handling, currently we get 404 if no post exist but on html we get a json which is not most ideal way to tell
error
first import 
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

we added two new decorators for global exception handling
@app.exception_handler(StarletteHTTPException) -to handle HTTP exception
@app.exception_handler(RequestValidationError) - to handle request validation error 


#Working on CREATE NEW POST
Pydantic:
Pydantic is a popular Python library for data validation and settings management, leveraging Python's type hints to define data structures, parse incoming data (like JSON, API requests), and automatically validate that data against your schema, ensuring it's clean, correctly typed, and adheres to rules, preventing errors and making applications more robust. It helps enforce data integrity, offers automatic type conversion (e.g., strings to integers), provides clear error messages for invalid data, and integrates seamlessly with frameworks like FastAPI for building APIs. 


Currently we lack a reposnse model, if u check the api docs there is no schema or model for response in paramters it shows parameters, we should be having what is the response return there
not just success response

we create a new separate file called schemas.py for defining the response
we then import 
from pydantic import BaseModel, Fields, ConfigDict

we create class PostBase that inherits from BaseModel 
Another class to create Post that inherits from PostBase - this will take the content of psotbase whenever created
PostResponse - defines what we return from our API 


class PostResponse(PostBase):  #these fields or this class is what we return from the API
    model_config = ConfigDict(from_attributes=True) # enable to read objects from attributes and not just dictionary

    id: int
    date_posted: str

these variables are generated on their own and not rpovided so part of response.
The response_model=PostResponse parameter in the @app.post decorator serves several key purposes in FastAPI. It's a way to define and enforce the structure of the data your API returns to clients. Here's a breakdown of its use and significance:

1. Response Validation and Serialization
What It Does: FastAPI automatically validates that the return value from your create_post function matches the PostResponse Pydantic model. If the returned data doesn't conform (e.g., missing fields or wrong types), FastAPI raises an error during development/testing.
How It Works: In your code, create_post returns a dictionary (new_post). FastAPI converts this dict into a PostResponse instance, ensuring it includes all required fields (id, title, content, author, date_posted). It then serializes this into JSON for the HTTP response.
Benefit: This prevents bugs where your function accidentally returns malformed data. For example, if you forgot to include id, FastAPI would catch it.


Basicall we accept data and validate then and there with PostCreate and PostBase , if any of it fails we have vlaidation errors that are thrown 
if success then PostResponse is what is returned 

the same concept is carry forwarded when working with databases just that the schema is little different

this data is in memory so goes away if i restart the server. there fore now we switch to databases

SQLAlchemy Database is pretty much standard for production server with python 
-------------
using models is built on top of fastapi model and sql , gives more control in this type of structure
 Flow: 

 Request comes in ---> Pydantic comes into picture for validation ---> SQLalchemy stores/retrieves data based on request ---> Pydantic formats the response ---> Response is received

 engine = create_engine(
Starts creating a database engine using create_engine. The comment explains that the engine represents the connection to the database.

    SQLALCHEMY_DATABASE_URL,
Passes the database URL to the engine creation.

    connect_args={"check_same_thread": False},
Provides connection arguments; check_same_thread: False is specific to SQLite to allow connections from multiple threads, which is useful in web applications.

)
Closes the create_engine call.

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Creates a session factory (SessionLocal) bound to the engine. autocommit=False means transactions must be committed manually, and autoflush=False prevents automatic flushing of changes.

class Base(DeclarativeBase):
Defines a base class Base inheriting from DeclarativeBase, which is used as the base for all database models in SQLAlchemy.

    pass
The class body is empty, as it's just a base class.

def get_db():
Defines a generator function get_db to provide database sessions.

    with SessionLocal() as db:
Creates a new session instance using SessionLocal and uses it in a context manager.

        yield db
Yields the session object, allowing it to be used in FastAPI dependency injection for handling database operations. The session is automatically closed when the context exits.
