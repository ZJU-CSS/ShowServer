from flask_cors import CORS
from flask import Flask
from selenium.webdriver.chrome.options import Options
import socket
import pyautogui
import time
import pandas as pd
import os
from selenium import webdriver
import subprocess
from subprocess import check_output
output = check_output('netsh wlan connect 公管107', shell=True)
print(output)
time.sleep(5)

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

chrome_options=Options()
# chrome_options.add_argument("--kiosk")
chrome_options.add_experimental_option('useAutomationExtension',False)
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation']);
chrome_options.add_argument("--allow-file-access-from-files")
dic={}
global musicDriver

# mdriver=webdriver.Chrome('chromedriver.exe', chrome_options=chrome_options)
# mdriver.get('file:///D:/Desktop/展示视频/backgroundmusic.html')
# mdriver.find_element()

# with webdriver.Edge() as IeDriver:

# print(socket.getfqdn(socket.gethostname()))

# os.system("net use z: \\MYPASSPORT\Storage\showserver")


def getList():
    # csv_data=pd.read_csv('https://raw.githubusercontent.com/HOOLoLo/webserver/master/content.csv')
    csv_data=pd.read_csv(r'\\MYPASSPORT\Storage\showserver\content.csv')
    # print(csv_data)
    for index,value in enumerate(csv_data['name']):
        dic[value]=csv_data['path'][index]
    print(dic)


# paths = os.listdir('z:')
# print(paths)
getList()
@app.route('/openChrome')
def openChrome():
    global driver
    driver = webdriver.Chrome('chromedriver.exe', chrome_options=chrome_options)
    time.sleep(3)
    pyautogui.hotkey('F11')



@app.route('/url/<pageName>')
def getOrder(pageName):
    print(pageName)
    getList()
    global musicDriver
    if pageName=='openMusic':
        musicDriver = webdriver.Edge()
        musicDriver.get(dic[pageName])
        musicDriver.minimize_window()
        return 'done'
    elif pageName=='stopMusic':

        musicDriver.close()
        return 'done'
    else:
        driver.get(dic[pageName])
        if pageName=='音乐' :
            time.sleep(1)
            pyautogui.click(x=0, y=500)
        if pageName == 'NASA':
            time.sleep(1)
            pyautogui.click(x=500, y=500)
        if pageName[-1]=='v':
            time.sleep(1)
            pyautogui.click(x=500, y=500)
        # driver.manage().window().fullscreen
        return 'done'


@app.route('/volume/<order>')
def setVolume(order):
    if order=='up':
        pyautogui.keyDown('volumeup')
    elif order=='down':
        pyautogui.keyDown('volumedown')

@app.route('/scroll/<order>')
def setScroll(order):
    if order=='front':
        pyautogui.scroll(1)
    elif order=='back':
        pyautogui.scroll(-1)



@app.route('/favicon.ico')
def favicon():
    return
@app.route('/shutdown')
def shutdown():
    os.system('shutdown -s -t 00')

@app.route('/cmd/<command>')
def cmd(command):
    subprocess.call(command,shell=True)




if __name__=='__main__':
    CORS(app,supports_credential=True)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))

    # hostname = socket.gethostname()
    # # 获取本机IP1111
    # ip = socket.gethostbyname(hostname)

    ip=s.getsockname()[0]
    print(ip)
    app.run(host=ip,port=7777,debug=False)


#复制命令：copy D:\Desktop\webserver\dist\main.exe D:\Desktop\webserver\ /Y
#如果是正在运行的情况应该怎么搞