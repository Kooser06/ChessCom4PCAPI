import math
import requests
import re, sys, time
from itertools import count
from collections import namedtuple
from urllib.parse import urljoin
from requests.exceptions import ConnectionError, HTTPError, ReadTimeout
from urllib3.exceptions import ProtocolError
try:
    from http.client import RemoteDisconnected
except ImportError:
    from http.client import BadStatusLine as RemoteDisconnected
import backoff

ENDPOINTS = {
    "arrow": "/bot?token={}&arrows={}",
    "chat": "/bot?token={}&chat={}",
    "play": "/bot?token={}&play={}",
    "resign": "/bot?token={}&play=R",
    "stream": "/bot?token={}&stream=1"
}

class Api():
    def __init__(self, url, token, version):
        self.header = {}
        self.url = url
        self.token = token
        self.version = version
        self.session = requests.Session()
        self.set_user_agent("?")

    def is_final(exception):
        return isinstance(exception, HTTPError) and exception.response.status_code < 500

    @backoff.on_exception(backoff.constant,
        (RemoteDisconnected, ConnectionError, ProtocolError, HTTPError, ReadTimeout),
        max_time=60,
        interval=0.1,
        giveup=is_final)
    def api_get(self, path):
        url = urljoin(self.url, path)
        response = self.session.get(url, timeout=2)
        response.raise_for_status()
        return response.json()

    def stream(self):
        url = urljoin(self.url, ENDPOINTS["stream"].format(self.token))
        return requests.get(url, headers=self.header, stream=True)

    def arrow(self, data):
        return self.api_get(ENDPOINTS["arrow"].format(self.token, data))

    def play(self, move):
        return self.api_get(ENDPOINTS["play"].format(self.token, move))

    def chat(self, message):
        return self.api_get(ENDPOINTS["chat"].format(self.token, message))

    def resign(self):
        return self.api_get(ENDPOINTS["resign"].format(self.token))

    def set_user_agent(self, user):
        self.header.update({"User-Agent": "chesscom-bot/{} user:{}".format(self.version, user)})
        self.session.headers.update(self.header)

col = (3, 2, 1, 0)
pvs = (100, 300, 425, 525, 1025, 60000)
pst = [[
    (
         0,   0,  0,  0,   0,   0,   0,   0,
         10,  15, 5,  10,  10,  10,  20,  15,
        -5,  -10, 20, 15,  20, -5,  -5,  -5,
        -10, -5,  10, 10,  10,  10, -5,   0,
         15,  20, 15, 15,  10, -5,   0,   0,
         5,   25, 0,  15, -20,  0,   0,   0,
         0,   0,  0,  0,   0,   0,   0,   0,
         0,   0,  0,  0,   0,   0,   0,   0
    ),
    (
    
    ),
], [
    (
        0, 0, -10, -5,  -10, -15,  10, 0,
        0, 0,  25, -5,  -10, -10, -5,  0,
        0, 0,  20, -5,  -5,  -5,  -5,  0,
        0, 0,  15,  20,  10, -10, -5,  0,
        0, 0,  10,  15,  20,  5,   10, 0,
        0, 0,  0,   20,  15,  15,  15, 0,
        0, 0,  0,   0,   10,  20,  20, 0,
        0, 0,  0,   0,   0,  -5,  -5,  0
    ),
    (
        
    ),
], [
    (
         0,   0,   0,   0,  0,  0,   0,   0,
         0,   0,   0,   0,  0,  0,   0,   0,
         0,   0,   0,  -20  15, 20,  25,  5,
         0,   0,  -5,   10, 15, 15,  20,  15,
         0,  -5,   10,  10, 10, 10, -5,  -10,
        -5,  -5,  -5,   20, 15, 20, -10, -5,
         15,  20,  10,  10, 10, 5,   15,  10,
         0,   0,   0,   0,  0,  0,   0,   0
    ),
], [
    (

    )
]]
