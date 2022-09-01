#!/usr/bin/env python3
"""5. Encrypting passwords"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Expects one string argument name password
    and returns a salted, hashed password,
    which is a byte string.
    """
    encoded_psw = bytes(password, 'utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(encoded_psw, salt)
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Implement an is_valid function that expects 2 arguments
    and returns a boolean.
    Arguments:
    hashed_password: bytes type
    password: string type
    Use bcrypt to validate that the provided password
    matches the hashed password.
    """
    encoded_psw = bytes(password, 'utf-8')
    if bcrypt.checkpw(encoded_psw, hashed_password) is True:
        return True
    return False
