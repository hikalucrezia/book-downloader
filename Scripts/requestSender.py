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
    getHeaders = postHeaders
    getHeaders["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    getHeaders["Referrer"] = "https://elib.maruzen.co.jp/elib/html/BookListDetail/search/true"
    getHeaders["Cache-Control"] = "max-age=0"
    getHeaders["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    getHeaders["Upgrade-Insecure-Requests"] = "1"
    getHeaders["Sec-Fetch-User"] = "?1"
    getHeaders["Sec-Fetch-Site"] = "same-origin"
    getHeaders["Sec-Fetch-Mode"] = "navigate"
    getHeaders["Sec-Fetch-Dest"] = "document"
    del getHeaders["Content-Length"]
    del getHeaders["Content-Type"]
    del getHeaders["X-Requested-With"]
    getRes = requests.get(
        re.match("^[^\?]+", url).group(0), headers=getHeaders, timeout=5)
    print(getRes.text)
    name = re.match("\<title[^\>]*?\>([^｜]+)｜", getRes.text).group(1)
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
