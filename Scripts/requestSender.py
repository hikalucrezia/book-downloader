from array import array
from queue import Empty
from socket import gethostbyaddr
from webbrowser import get
import requests
import re
import os
import PySimpleGUI as sg
import binascii


def sendRequest(values: array, page: int, ranStr: str):
    url, postHeaders = makeHeadersArray(values["-headers"])
    if url is None or postHeaders is None:
        return
    postRes = requests.post(url, headers=postHeaders, data={
        "id"+ranStr+"_hf_0": "", "changeScale": "1", "pageNumEditor": page, "enterPageSubmit": 1})
    return postRes


def checkValidations(values: array):
    if values["-firstpage"] == '':
        sg.popup_error('Error code: 3-01; First page value empty')
        return False
    elif values["-finalpage"] == '':
        sg.popup_error('Error code: 3-02; Final page value empty')
        return False
    elif int(values["-firstpage"]) >= int(values["-finalpage"]):
        sg.popup_error(
            'Error code: 3-03; Final page value the same or above first page value')
        return False
    elif int(values["-firstpage"]) < 1:
        sg.popup_error(
            'Error code: 3-04; First page value cannot be smaller value than 1')
        return False
    elif os.path.exists(os.getcwd() + "/"+values["-foldername"]):
        sg.popup_error('Error code: 3-05; This folder already exists')
        return False
    return True


def makeHeadersArray(rawHeaders):
    urlPattern = '.*?(\/elib/html\/Viewer\/Id\/\d+\?\d+\-\d+\.IBehaviorListener\.0\-browseForm\-enterPageSubmit)'
    reRes = re.match(urlPattern, rawHeaders)
    if (reRes == None):
        sg.popup_error(
            "Error code: 1-01; Header request input not appropriate")
        return
    url = 'https://elib.maruzen.co.jp' + reRes.group(1)
    paramPattern = '\n\s*?([^:]+)\s*?:\s*?([^\s][^\n]+)'
    resultList = re.findall(paramPattern, rawHeaders, re.S)
    arr = {}
    for res in resultList:
        arr[res[0]] = res[1]
    return url, arr
