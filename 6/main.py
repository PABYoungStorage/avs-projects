from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/")
async def get_index():
    with open("./templates/index.html", "r") as html:
        return HTMLResponse(content=html.read())

@app.get("/api/data")
async def read_data():
    return {"data": "Data from REST API"}


# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Data from WebSocket: {data}")