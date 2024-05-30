#!/usr/bin/env python3
"""module for filtering and replacing a string"""
import re


def filter_datum(fields, redaction, message, separator):
    """function for filtering and replacing a string using regex"""
    for field in fields:
        message = re.sub(f'{field}=(.*?){separator}',
                         f'{field}={redaction}{separator}', message)
    return message
