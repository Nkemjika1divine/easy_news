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