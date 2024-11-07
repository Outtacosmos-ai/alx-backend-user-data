#!/usr/bin/env python3
"""
Module for handling personal data
"""

import logging
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Returns the log message obfuscated
    """
    for field in fields:
        pattern = f'{field}=.*?{separator}'
        repl = f'{field}={redaction}{separator}'
        message = re.sub(pattern, repl, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Filters values in incoming log records using filter_datum
        """
        log_message = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            log_message, self.SEPARATOR)


if __name__ == "__main__":
    message = ("name=Bob;email=bob@dylan.com;"
               "ssn=000-123-0000;password=bobby2019;")
    log_record = logging.LogRecord("my_logger", logging.INFO,
                                   None, None, message, None, None)
    formatter = RedactingFormatter(fields=("email", "ssn", "password"))
    print(formatter.format(log_record))
