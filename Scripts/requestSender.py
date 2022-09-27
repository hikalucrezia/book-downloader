from array import array
from socket import gethostbyaddr
from webbrowser import get
import requests
import re
import json


def sendRequest(values: array):
    checkValidations(values)
    arr = makeHeadersArray(values["-headers"])
    url = arr["url"]
    postHeaders: array = arr["data"]
    postRes = requests.post(url, headers=postHeaders, data={
        "id": "", "changeScale": "1", "pageNumEditor": 5, "enterPageSubmit": 1})
    return postRes, "A"


def checkValidations(values: array):
    if (values["-firstpage"] == '' or values["-finalpage"] == '' or int(values["-firstpage"]) >= int(values["-finalpage"]) or int(values["-firstpage"]) < 1):
        raise Exception("Error code: 1-02; Page number is illegal")


def makeHeadersArray(rawHeaders) -> array:
    urlPattern = '.*?(\/elib/html\/Viewer\/Id\/\d+\?\d+\-\d+\.IBehaviorListener\.0\-browseForm\-enterPageSubmit)'
    reRes = re.match(urlPattern, rawHeaders)
    if (reRes == None):
        raise Exception(
            "Error code: 1-01; Header request input not appropriate")
    url = 'https://elib.maruzen.co.jp' + reRes.group(1)
    paramPattern = '\n\s*?([^:]+)\s*?:\s*?([^\s][^\n]+)'
    resultList = re.findall(paramPattern, rawHeaders, re.S)
    arr = {}
    for res in resultList:
        arr[res[0]] = res[1]
    return {"url": url, "data": arr}
