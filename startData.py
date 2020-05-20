import subprocess
import time
from subprocess import check_output

def getStart():
    # subprocess.call('venv\\Scripts\\activate',shell=True)
    time.sleep(5)
    subprocess.call('venv\Scripts\python main.py', shell=True)

getStart()