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