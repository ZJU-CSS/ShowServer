import subprocess
from subprocess import check_output

def getStart():
    subprocess.call('yarn start', shell=True)

getStart()