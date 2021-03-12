from typing import Optional
from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

from pathlib import Path
import json
import subprocess
import datetime

store = Path("./synced-with-remnote")
store.mkdir(exist_ok=True)

HTTP_SERVER = "http://localhost:8080"


class Rem(BaseModel):
    name: str
    content: Optional[str]


@app.get("/rem/{rem_id}")
async def read_rem(rem_id: str):
    rem_file = store / rem_id
    if rem_file.exists():
        rem = rem_file.read_text().split("::")
        return Rem(name=rem[0], content=rem[1] if len(rem) > 1 else None)
    else:
        return {rem_id: None}


@app.put("/rem/{rem_id}")
async def write_rem(rem_id: str, rem: Rem):
    rem_file = store / rem_id
    rem_file.write_text(rem.name + (f"::{rem.content}" if rem.content else ""))
    return rem


@app.put("/send-page")
async def send_page(request: Request):
    rem = await request.json()
    Path("stats.html").write_text(
        f"""
<h1>RemNote Companion - A dashboard for knowledge workers</h1>
<h2>Stats about the current page</h2>
<p>Number of visible rem: {len(rem['visibleRemOnDocument'])}</p>
<p>Created: {datetime.datetime.fromtimestamp(rem['createdAt']//1000)}
<p>...</p>
<h2>Your Local Graph View could be here since 2020</h2>
😉
<h2>Raw data of the document</h2>
<pre>
{json.dumps(rem, sort_keys=True, indent=2)}
</pre>
"""
    )
    return 200


class Command(BaseModel):
    command: str


class CompletedProcessModel(BaseModel):
    args: str
    returncode: int
    stdout: str
    stderr: str


@app.post("/run-command")
async def run_command(command: Command):
    # WARNING: Running unknown commands is dangerous!
    ret = subprocess.run(
        command.command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return ret


class PythonCode(BaseModel):
    remId: str
    code: str


@app.post("/eval-python")
async def eval_python(code: PythonCode):
    return {"output": eval(code.code)}


local_variables = {}


@app.post("/exec-python")
async def exec_python(code: PythonCode):
    return {"output": exec(code.code, local_variables)}


images = Path("./images")
images.mkdir(exist_ok=True)


@app.post("/make-diagram")
def exec_python(code: PythonCode):
    exec(code.code, local_variables)
    # Assuming the variable fig is defined in the diagram code
    fig = local_variables["fig"]
    image_path = images / f"{code.remId}.svg"
    fig.write_image(str(image_path))
    return {"output": f"![diagram]({HTTP_SERVER}/{image_path})"}
