from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
#from fastapi.responses import HTMLResponse # Importing HTMLResponse for converting json response to HTML and displaying in browser
from fastapi.templating import Jinja2Templates # Importing Jinja2Templates for rendering HTML templates
from fastapi import HTTPException, status    # Importing HTTPException for error handling and status for HTTP status codes
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from schemas import PostResponse, PostCreate

app = FastAPI()
templates = Jinja2Templates(directory="templates") # Setting up Jinja2 templates directory
app.mount("/static", StaticFiles(directory="static"), name="static") # Mounting static files directory - take 3 arguments: url path, StaticFiles instance with directory, and name

@app.get("/" ,include_in_schema=False, name="home") # a decorator to define a GET endpoint at the root URL - returning HTML response by setting response_class
@app.get("/posts", include_in_schema=False, name="posts") # a decorator to define a GET endpoint at /posts URL - this is stacking decorators to have multiple routes for the same function
def home(request: Request): #adding argument request of type Request to pass to the template
    return templates.TemplateResponse(
        request, 
        "home.html", 
        {"posts": posts, "title": "Home"}, # Passing request, template name, and context dictionary to the template response

    ) # Simple GET endpoint returning a greeting message - converting json response to HTML using Jinja2 template - passing posts data to the template as dictionary

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

@app.get("/api/posts", response_model=list[PostResponse]) # GET endpoint to retrieve all posts
def get_posts():
    return {"posts": posts} # Return the list of posts

#fastapi dev main.py --port - running in dev mode auto reloads on code changes
## Create Post
@app.post(
    "/api/posts",
    response_model=PostResponse, #Postresponse 
    status_code=status.HTTP_201_CREATED,
)
def create_post(post: PostCreate):
    new_id = max(p["id"] for p in posts) + 1 if posts else 1
    new_post = {
        "id": new_id,
        "author": post.author,
        "title": post.title,
        "content": post.content,
        "date_posted": "April 23, 2025",
    }
    posts.append(new_post)
    return new_post


@app.get("/api/posts/{post_id}", response_model=PostResponse) # GET endpoint to retrieve a specific post by ID
def get_post(post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found") # Return the specific post or an error message if not found

@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException): #this will handle all HTTP exceptions globally
    message = (
        exception.detail   # Use the exception detail if available
        if exception.detail  # and isinstance(exception.detail, str)
        else "An error occurred. Please check your request and try again."
    )

    if request.url.path.startswith("/api"):   #checking if the request is for API endpoint and returning JSON response
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )

    return templates.TemplateResponse( #checking if the request is for normal endpoint and returning HTML response
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError): #this will handle validation errors globally
    if request.url.path.startswith("/api"):  #checking if the request is for API endpoint and returning JSON response
        return JSONResponse( 
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,  #422 status code for validation errors
            content={"detail": exception.errors()}, #returning the validation errors in the response
        )

    return templates.TemplateResponse(  #checking if the request is for normal endpoint and returning HTML response
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )



posts: list[dict]  = [
    {
        "id": 12,
        "author": "Sunath Khadikar",
        "title": "AI is next big thing",
        "content": "Agentic AI and MCP will take over soon, coding is an outdated skill",
        "date_posted": "May 22, 2025" 

    },
    {
        "id": 13,
        "author": "Jane Doe",
        "title": "The Future of Web Development",
        "content": "With the rise of frameworks like React and Vue, web development is evolving rapidly.",
        "date_posted": "June 15, 2025"
    },
    {
        "id": 14,
        "author": "John Smith",
        "title": "Machine Learning Basics",
        "content": "Understanding algorithms and data preprocessing is key to ML success.",
        "date_posted": "July 10, 2025"
    },
    {
        "id": 15,
        "author": "Alice Johnson",
        "title": "Cybersecurity Trends",
        "content": "As threats increase, implementing robust security measures is crucial.",
        "date_posted": "August 5, 2025"
    },
    {
        "id": 16,
        "author": "Bob Wilson",
        "title": "Cloud Computing Explained",
        "content": "AWS, Azure, and GCP offer scalable solutions for modern applications.",
        "date_posted": "September 20, 2025"
    }
]
