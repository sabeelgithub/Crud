from fastapi import FastAPI,Depends,HTTPException
from typing import List,Annotated
from sqlalchemy.orm import Session
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.database import engine,get_db
from .schemas import UserCreate,UserResponse,UserUpdate
from . import models
from .models import User

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session,Depends(get_db)]

@app.post("/add_users", response_model=UserResponse)
def create_user(user: UserCreate, db:db_dependency):
    db_user = User(**user.dict(exclude_unset=True))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/get_users", response_model=List[UserResponse])
def get_users(db: db_dependency):
    return db.query(User).all()

@app.patch("/update_users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db:db_dependency):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/delete_users/{user_id}")
def delete_user(user_id: int, db:db_dependency):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted"}



@app.post("/send_invite")
def send_invite():
    sender_email = "mohammedsabeeltc786@gmail.com"
    # recipients = ["sabeelmohammedtc786@gmail.com","harikrishnansr007@gmail.com"]
    recipients = ["shraddha@aviato.consulting","pooja@aviato.consulting","sabeelmohammedtc786@gmail.com","harikrishnansr007@gmail.com"]
    subject = "API Documentation Invitation"
    body = """
            <html>
            <body>
                <div style="width: 600px; margin: auto; padding: 20px; font-family: Arial, sans-serif; background-color: #f4f4f4; border: 1px solid #ddd;">
                    <h1 style="background-color: #3971e0; color: white; padding: 10px 0; text-align: center;">API Documentation Invitation</h1>
                    <p>Hello,</p>
                    <p>I am excited to invite you to view my User Management API documentation on <strong>ReDoc</strong>.</p>
                    <p>You can access the documentation by clicking the button below:</p>
                    <div style="text-align: center; margin: 20px 0;">
                        <a href="https://crud-428709.el.r.appspot.com/redoc" style="display: inline-block; padding: 15px 25px; color: white; background-color: #3971e0; text-decoration: none; border-radius: 5px; font-size: 16px;">View API Documentation</a>
                    </div>
                    <p>As per the requirements, I have set up the API to handle user management for three different projects. The API supports the following operations:</p>
                    <ul>
                        <li>Create User</li>
                        <li>List User Details</li>
                        <li>Update User Details</li>
                        <li>Delete User</li>
                    </ul>
                    <p>I have also set up a GCP free tier account for deployment and GCP Postgres for the database.</p>
                    <p>I appreciate your time and look forward to your feedback.</p>
                    <div style="background-color: #3971e0; color: white; text-align: center; padding: 20px; border-radius: 5px; margin-top: 20px;">
                        <p style="font-size: 14px;">Thank you,</p>
                        <p style="font-size: 16px;">Mohammed Sabeel Tc</p>
                        <p style="font-size: 14px;">If you have any questions, feel free to reply to this email or contact me at <a href="mailto:mohammedsabeeltc786@gmail.com" style="color: white; text-decoration: underline;">mohammedsabeeltc786@gmail.com</a>.</p>
                    </div>
                </div>
            </body>
        </html>
            """

    msg = MIMEMultipart("alternative")
    msg["From"] = sender_email
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, "pijwwvkyyxmhdccr")
            server.sendmail(sender_email, recipients, msg.as_string())
        return {"message": "Invitation email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")

