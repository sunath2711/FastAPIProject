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