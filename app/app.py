from fastapi import FastAPI, Body, status, HTTPException
from fastapi.responses import JSONResponse, FileResponse
import subprocess


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
        cmd = "./main"
        self.log = open("main.log", mode='w')
        try:
            self.proc = subprocess.Popen(cmd, stdout=self.log, stderr=self.log)
        except OSError as e:
            raise HTTPException(status_code=404, detail=e.strerror)

    def read(self) -> str:
        with open("main.log", "r") as f:
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
        return {'status': 'Active'}
    else:
        return {'status': 'Stopped'}
