import random
import time
import argparse
import webbrowser
import requests
import json


def get_response(response, timeout=5, max_retries=5, backoff_factor=1.3):
    delay = 0
    for i in range(max_retries):
        try:
            query = response
            return query
        except:
            pass
        time.sleep(delay)
        dalay = min(delay * backoff_factor, timeout)
        delay += random.random()
    raise ConnectionResetError("Error")