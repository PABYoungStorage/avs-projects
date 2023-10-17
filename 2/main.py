from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import random
import smtplib
from email.mime.text import MIMEText

app = FastAPI()

# Sample user data as a list (replace with a database in a real application)
users_db = []

# Temporary storage for password reset tokens (replace with a database in a real application)
password_reset_tokens = {}

# Model for user registration
class User(BaseModel):
    email: str
    password: str

# Model for requesting a password reset
class PasswordResetRequest(BaseModel):
    email: str

# Model for password reset
class PasswordReset(BaseModel):
    email: str
    token: str
    new_password: str

# Route for user registration
@app.post("/api/signup", response_model=dict)
def register_user(user: User):
    # Check if the email already exists
    if any(existing_user.email == user.email for existing_user in users_db):
        raise HTTPException(status_code=400, detail="Email already exists")
    
    users_db.append(user)
    return {"message": "User registered successfully"}

# Route for user login
@app.post("/api/signin", response_model=dict)
def login_user(user: User):
    # Check if the email and password match
    if any(existing_user.email == user.email and existing_user.password == user.password for existing_user in users_db):
        return {"message": "User login successful"}
    else:
        raise HTTPException(status_code=400, detail="Invalid credentials")

# Route to serve the HTML form for signup
@app.get("/signup", response_class=HTMLResponse)
async def signup_form():
    with open("./templates/signup.html", "r") as html:
        return HTMLResponse(content=html.read())

# Route to serve the HTML form for signup
@app.get("/signin", response_class=HTMLResponse)
async def signup_form():
    with open("./templates/signin.html", "r") as html:
        return HTMLResponse(content=html.read())


# Password Reset Routes
@app.post("/api/password-reset/request", response_model=dict)
def request_password_reset(request: PasswordResetRequest):
    user_email = request.email

    # Check if the email exists in the user database
    if any(existing_user.email == user_email for existing_user in users_db):
        # Generate a password reset token (for simplicity, we're using random here)
        reset_token = str(random.randint(1000, 9999))

        # Store the token in temporary storage (replace with a database)
        password_reset_tokens[user_email] = reset_token

        # Send a password reset email (you should replace this with your email sending logic)
        send_password_reset_email(user_email, reset_token)

        return {"message": "Password reset email sent successfully"}
    else:
        raise HTTPException(status_code=400, detail="Email not found")

def send_password_reset_email(email, token):
    # Replace this with your actual email sending logic
    # Example using smtplib (you may need to configure your email server settings)
    server = smtplib.SMTP("smtp.outlook.com", 587)
    server.starttls()
    server.login("your_username", "your_password")

    message = f"Click this link to reset your password: http://localhost:8000/reset?email={email}&token={token}"
    msg = MIMEText(message)
    server.sendmail(email, email, msg.as_string())
    server.quit()


@app.post("/api/password-reset/reset", response_model=dict)
def reset_password(reset_data: PasswordReset):
    user_email = reset_data.email
    token = reset_data.token
    new_password = reset_data.new_password

    # Check if the token matches the one in temporary storage
    if user_email in password_reset_tokens and password_reset_tokens[user_email] == token:
        # Reset the user's password (you should update this to store in your database)
        for user in users_db:
            if user.email == user_email:
                user.password = new_password
                break

        # Clear the token from temporary storage
        del password_reset_tokens[user_email]

        return {"message": "Password reset successful"}
    else:
        raise HTTPException(status_code=400, detail="Invalid token")

# Route to serve the HTML form for password reset
@app.get("/password-reset", response_class=HTMLResponse)
async def password_reset_form():
    with open("./templates/passwordreset.html", "r") as html:
        return HTMLResponse(content=html.read())
