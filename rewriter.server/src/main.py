from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio

from .rewriter import rewrite_by_personality_streamed


origins = [
    "http://localhost:5585/",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>Text rewriter by personality description</h1>
        <form action="" onsubmit="sendMessage(event)">
            <p><label for="text-fragment">Text Fragment:</label> <p/>
            <textarea id="text-fragment" name="Text Fragment" rows="7" cols="150">The rain had just stopped, leaving the streets slick and shimmering under the glow of streetlamps. Puddles mirrored the sky, still heavy with clouds that refused to move on. I walked slowly, the quiet drip of water from rooftops the only sound for blocks. There was a strange comfort in the emptiness, like the world had decided to whisper instead of shout.</textarea>
            <p><label for="personality-description">Personality Description:</label><p/>
            <textarea id="personality-description" name="Personality Description" rows="3" cols="150"></textarea>
            <br /><br />
            <button>Send</button>
        </form>
        <p><label for="rewritten-text">Rewritten text based on the personality description:</label><p/>
        <textarea id="rewritten-text" name="Rewritten text" rows="7" cols="150"></textarea>
        <script>
            var ws = new WebSocket("ws://localhost:5583/rewriter");
            var resultField = document.getElementById("rewritten-text");
            ws.onmessage = function(event) {
                resultField.value = resultField.value + event.data;
            };
            function sendMessage(event) {
                const input = {
                    fragment: document.getElementById("text-fragment").value,
                    personality: document.getElementById("personality-description").value
                };
                message = JSON.stringify(input);
                console.log(message);
                ws.send(message);
                resultField.value = "";
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


class RewritingInput(BaseModel):
    fragment: str
    personality: str


@app.websocket("/socket-echo")
async def websocket_test_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    try:
        data = await websocket.receive_text()
        for item in data.split():
            await websocket.send_text(f"{item}")
            await asyncio.sleep(0.5)
        websocket.close()
    except WebSocketDisconnect:
        print(f"WebSocket '{websocket.client.host}:{websocket.client.port}' disconnected")


@app.websocket("/rewriter")
async def rewriter(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_json()
            input = RewritingInput.model_validate(data)
            if input.fragment and input.personality:
                res = rewrite_by_personality_streamed(input.fragment, input.personality)
                for chunk in res:
                    await websocket.send_text(chunk)
                    await asyncio.sleep(1)
                    websocket.client.host
    except WebSocketDisconnect:
        print(f"WebSocket '{websocket.client.host}:{websocket.client.port}' disconnected")


@app.get("/health-check")
def health_check():
    return {"status": "ok"}
