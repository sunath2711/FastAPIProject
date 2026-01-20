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