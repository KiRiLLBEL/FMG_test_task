from fastapi import FastAPI, Body, status, HTTPException
from fastapi.responses import JSONResponse, FileResponse
import subprocess
import psutil
import os

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Process(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.proc = None

    def create(self):
        cmd = "./src/main"
        self.log = open("src/main_close.log", mode='w')
        try:
            self.proc = subprocess.Popen(cmd, stdout=self.log, stderr=self.log)
        except OSError as e:
            raise HTTPException(status_code=404, detail=e.strerror)

    def read(self) -> str:
        if not P.active():
            os.system("cat src/main_close.log > src/main.log")
        with open("src/main.log", "r") as f:
            return f.read()

    def exit(self):
        self.log.close()
        self.proc.kill()

    def started(self) -> bool:
        return self.proc is not None

    def active(self) -> bool:
        if self.started():
            if self.proc.poll() is None:
                return True
            else: 
                return False
        else:
            return False


app = FastAPI()

P = Process()
@app.post("/main")
def createProcess(cmd: str):
    if (cmd == 'start'):
        if P.active():
            return {'status': 'Already started'}
        else:
            P.create()
            return {'status': 'Success'}
    elif (cmd == 'stop'):
        if P.active():
            P.exit()
            return {'status': 'Success'}
        else:
            return {'status': 'Already stopped'}
    else:
        raise HTTPException(status_code=404, detail="Command not found")


@app.get("/main/result")
def getResult():
    if not P.started():
        raise HTTPException(status_code=404, detail="Not found")
    else:
        return P.read()


@app.get("/main")
def getStatus():
    if P.active():
        cmd = f"ps -p {P.proc.pid} -o etime"
        proc_data_time = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        ans = {'status': 'Active', 'time': proc_data_time.stdout.read().split()[1], 'mem': psutil.Process(P.proc.pid).memory_info().rss}
        proc_data_time.wait()
        return ans
    else:
        return {'status': 'Stopped'}
