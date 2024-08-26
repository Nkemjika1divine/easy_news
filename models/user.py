#!/usr/bin/python3
"""The User module"""
from bcrypt import hashpw, checkpw, gensalt
from email.message import EmailMessage
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String
from utils.utility import generate_token
import smtplib


class User(BaseModel, Base):
    """The User model"""
    __tablename__ = "users"
    name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(20), nullable=False)
    reset_token = Column(String(50), nullable=True)
    role = Column(String(10), nullable=False)
    email_verified = Column(String(10), nullable=False, default="no")
    email_token = Column(String(10), nullable=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    

    def hash_password(self, password: str = None) -> str:
        """Hashes a user's password"""
        if not password or type(password) is not str:
            return None
        return hashpw(password.encode("utf8"), gensalt())
    

    def is_valid_password(self, password: str = None) -> bool:
        """Verifies to ensure that password entered is the same in the DB"""
        if not password or type(password) is not str:
            return False
        if self.password is None:
            return False
        return checkpw(password.encode("utf-8"), self.password.encode("utf-8"))
    

    def generate_password_token(self, user_id: str = None) -> str:
        """Generated a password token using uuid"""
        from models import storage
        if not user_id or type(user_id) is not str:
            return None
        user = storage.search_key_value("User", "id", user_id)
        if not user:
            raise ValueError()
        token = generate_token()
        user[0].reset_token = token
        storage.save()
        return token
    

    def update_password(self, token: str = None, password: str = None) -> None:
        """Updates a user's password"""
        from models import storage
        user = storage.search_key_value("User", "reset_token", token)
        if not user:
            raise ValueError()
        user = user[0]
        user.password = self.hash_password(password)
        user.reset_token = None
        storage.save()
    

    def send_email_token(self) -> bool:
        """sends token to the user email"""
        from models import storage
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()

            server.login('placerssocials@gmail.com', 'plvp oyzo qjmy eonv')
            message = "Hi {}...\n\nYour verification token is {}.\n\nUse this to validate your email".format(self.display_name(), self.email_token)

            msg = EmailMessage()
            msg["Subject"] = "OTP Verifiation"
            msg["From"] = "placerssocials@gmail.com"
            msg["To"] = self.email
            msg.set_content(message)

            server.send_message(msg)
            return True
        except smtplib.SMTPAuthenticationError:
            print("Failed to authenticate with the SMTP server. Check your username and password.")
        except smtplib.SMTPRecipientsRefused:
            print("The recipient address was refused by the server.")
        except smtplib.SMTPSenderRefused:
            print("The sender address was refused by the server.")
        except smtplib.SMTPDataError:
            print("The SMTP server refused the email data.")
        except smtplib.SMTPConnectError:
            print("Failed to connect to the SMTP server.")
        except smtplib.SMTPException as e:
            print(f"An SMTP error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return False