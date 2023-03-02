#coding=utf-8
from flask_cors import CORS
from selenium import webdriver
from flask import Flask
from flask import request
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import socket
import pyautogui
import time
import pandas as pd
import os
import urllib.request
import json
import shutil
import win32gui
import win32con
import wget
import re
import zipfile
app = Flask(__name__)
hwnd = ''
chrome_options=Options()
# chrome_options.add_argument("--kiosk")
chrome_options.add_experimental_option('useAutomationExtension',False)
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation']);
chrome_options.add_argument("--allow-file-access-from-files")

@app.route('/playVideo', methods=['POST'])
def playVideo():
    position = request.json
    time.sleep(3)
    print(position)
    pyautogui.click(x=position['x'], y=position['y'])
    return 'success'


@app.route('/openChrome')
def openChrome():
    global hwnd
    global driver
    try:
        driver = webdriver.Chrome(options=chrome_options)
        time.sleep(3)
        hwnd = win32gui.FindWindow(None, "data:, - Google Chrome")
        time.sleep(1)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 1700, 1500, win32con.SWP_SHOWWINDOW)
        pyautogui.moveTo(279, 364)
        pyautogui.click()
        time.sleep(1)
        pyautogui.hotkey('F11')
        return 'success'
    except Exception as e:
        err_info = str(e)
        print('err:', err_info)
        level = re.findall(r"Current browser version is (\d+)\.", err_info)[0]
        print(level)
        resp = urllib.request.urlopen('https://registry.npmmirror.com/-/binary/chromedriver/')
        versionList = json.loads(resp.read())
        url = ""
        print('ver:', versionList)
        for item in versionList:
            if item["name"][:3] == level:
                url = item["url"] + 'chromedriver_win32.zip'
                break
        print("url: ", url)
        if(url == ''):
            return 'error'
        os.remove('chromedriver.exe')
        wget.download(url)
        while not os.path.exists('chromedriver_win32.zip'):
            time.sleep(0.5)
        zfile = zipfile.ZipFile('chromedriver_win32.zip')
        for file in zfile.namelist():
            zfile.extract(file)
        zfile.close()
        time.sleep(1)
        os.remove('chromedriver_win32.zip')
        time.sleep(2)
        driver = webdriver.Chrome(options=chrome_options)
        time.sleep(3)
        hwnd = win32gui.FindWindow(None, "data:, - Google Chrome")
        time.sleep(1)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 1700, 1500, win32con.SWP_SHOWWINDOW)
        pyautogui.moveTo(279, 364)
        pyautogui.click()
        time.sleep(3)
        pyautogui.hotkey('F11')
        return 'success'

@app.route('/url/<pageName>')
def getOrder(pageName):
    resp = urllib.request.urlopen('http://10.72.100.6:8887/content_map')
    dic = json.loads(resp.read())
    driver.get(dic[pageName])
    return 'success'


@app.route('/volume/<order>')
def setVolume(order):
    if order=='up':
        pyautogui.keyDown('volumeup')
    elif order=='down':
        pyautogui.keyDown('volumedown')
    elif order=='mute':
        pyautogui.press('volumemute')

@app.route('/scroll/<order>')
def setScroll(order):
    if order=='front':
        pyautogui.scroll(1)
    elif order=='back':
        pyautogui.scroll(-1)

@app.route('/shutdown')
def shutdown():
    os.system('shutdown -s -t 00')

@app.route('/music')
def music():
    pyautogui.press('space')

@app.route('/test')
def test():
    global hwnd
    print(hwnd)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 500, 1000, win32con.SWP_SHOWWINDOW)
    time.sleep(3)
    pyautogui.moveTo(1000, 1080)
    pyautogui.click()
    return 'success'


if __name__=='__main__':
    openChrome()
    CORS(app,supports_credential=True)
    hostname = socket.gethostname()
    # 获取本机IP1111
    ip = socket.gethostbyname(hostname)
    app.run(host=ip,port=7777,debug=False)


#https://registry.npmmirror.com/binary.html?path=chromedriver/ chromedriver获取列表