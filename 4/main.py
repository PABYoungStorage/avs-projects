from fastapi import FastAPI, Form, Depends, HTTPException, Cookie
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

# Demo user credentials (you should use a database in a production environment).
demo_users = [
    {"username": "demo", "password": "password",
        "token": "vxcmsdfuh34508uglkm34kjvfkjofg9845jnfgb45"},
]

# OAuth2PasswordBearer is a helper class to get the token from the request headers.


def oauth2_scheme(token):
    for u in demo_users:
        if u["token"] == token:
            return True
        else:
            return False


@app.get("/")
async def get_index():
    with open("./templates/index.html", "r") as html:
        return HTMLResponse(content=html.read())
# FastAPI routes for login and home pages.


class User(BaseModel):
    username: str
    password: str


@app.post("/login")
async def login(data: User):
    user = next((u for u in demo_users if u["username"]
                == data.username and u["password"] == data.password), None)
    print(user)
    if user:
        return {"success": True, "token": user["token"]}
    else:
        return {"success": False}


@app.get("/home")
async def home(token: str = Depends(oauth2_scheme)):
    if token:
        return HTMLResponse(content=HomeHtml)
    else:
        return HTTPException(status_code=401, detail="Not Authorized")


HomeHtml = '''
<!DOCTYPE html>
<html>
    <head>
        <title>
            home page
        </title>
    </head>
    <body>
        <h1>
            welcome to the home page
        </h1>
    </body>
</html>
'''
