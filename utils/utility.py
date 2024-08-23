#!/usr/bin/python3
"""Utility module"""
import random
import re


def generate_token() -> str:
    """Generates a randon 6 digit number and returns it"""
    otp = ""
    for i in range(6):
        otp += str(random.randint(0, 9))
    return otp


def validate_email_pattern(email: str = None) -> bool:
    """Checks to ensure that the email entered is an email pattern using regex"""
    if not email:
        return False
    pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    return bool(pattern.match(email))