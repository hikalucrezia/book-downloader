from multiprocessing import current_process
import PySimpleGUI as sg
import requestSender
import os
import re
import shutil
import requests
from PIL import Image
import io
from glob import glob

def handleEvents(window):
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event == "Go":
            if requestSender.checkValidations(values):
                imgPattern='^.*(\/kikan\_info\/GetImg\.jpg\?id\=\d+)[^\d]*'
                folderName=os.getcwd() + "/"+values["-foldername"]
                os.makedirs(folderName, exist_ok=False)
                firstpage, finalpage=int(values["-firstpage"]), int(values["-finalpage"])
                for i in range(firstpage, finalpage+1):
                    responce = requestSender.sendRequest(values, i)
                    if responce == None:
                        sg.popup_error("Error code: 2-02; Responce not returned at all. Try reloading the page and follow the instructions again")
                        break
                    elif not re.match(imgPattern, responce.text, re.S) == None:
                        imgUrl="https://elib.maruzen.co.jp"+re.match(imgPattern, responce.text, re.S).group(1)
                        res = requests.get(imgUrl, stream = True)
                        if res.status_code == 200:
                            fileName=str(i).zfill(5)+".jpg"
                            with open(folderName+"/"+fileName,'wb') as f:
                                shutil.copyfileobj(res.raw, f)
                        else:
                            sg.popup_error("Error code: 2-03; Responce denied. See if you are restricted from the website. If you can still access the website from your browser, then try reloading the page and follow the instructions again")
                            break
                        currentVal=i/(finalpage-firstpage)
                        window['progress'].UpdateBar(currentVal)
                        image = Image.open(folderName+"/"+fileName)
                        image.thumbnail((300, 500))
                        bio = io.BytesIO()
                        image.save(bio, format="PNG")
                        window["-image"].update(data=bio.getvalue())
                        if i==finalpage:
                            sg.popup("Succesfully downloaded all the images")
                            window['progress'].UpdateBar(0)
                    else:
                        sg.popup_error('Error code: 2-01; Desired responce not returned. Try reloading the page and follow the instructions again')
                        break
    window.close()
