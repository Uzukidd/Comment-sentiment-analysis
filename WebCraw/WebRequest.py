#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


def get(url, decode = "utf-8", headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}):
    response = requests.get(url, headers = headers)

    response.content.decode(decode)

    return response

def selectElement(text, selector, typo = 'lxml') :

    soup = BeautifulSoup(text, typo)

    res = soup.select(selector)

    return res
