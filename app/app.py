from fastapi import FastAPI, Body, status
from fastapi.responses import JSONResponse, FileResponse
import asyncio


class Process(object):
    @classmethod
    async def create(cls, name: str):
        self = Process()
        self.name = name
        cmd = f"./{name}"
        self.proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
        self.stack = []
        return self

    async def read(self) -> str:
        return await self.proc.stdout.read()

    def exit(self):
        self.proc.kill()


app = FastAPI()

proc_db = {str: Process}


@app.post("/{proc_name}")
async def createProcess(proc_name: str, cmd: str):
    if (cmd == 'start'):
        if proc_name not in proc_db:
            p = await Process.create(proc_name)
        else:
            return {'status': "Already created"}
        proc_db[proc_name] = p
        return {'status': "Success"}
    elif (cmd == 'stop'):
        if proc_name in proc_db:
            proc_db[proc_name].exit()
            proc_db.pop(proc_name)
            return {'status': "Success"}
        else:
            return {'status': "Process not created"}
    else:
        return {'status': "Fail"}


@app.get("/{proc_name}/result")
async def getResult(proc_name: str):
    if proc_name in proc_db:
        return {'result': await proc_db[proc_name].proc.stdout.readline()}
    else:
        return {'result': "Process not created"}
