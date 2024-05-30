#!/usr/bin/env python3
"""module for filtering and replacing a string"""
import re


def filter_datum(fields, redaction, message, separator):
    """function for filtering and replacing a string using regex"""
    return re.sub('|'.join(f'{field}=.*?{separator}' for field in fields),
                  f'{redaction}{separator}', message)
