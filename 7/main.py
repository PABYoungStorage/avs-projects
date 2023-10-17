from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

# Simulated REST API data store
data_store = []

# Simulated WebSocket connections
websocket_connections = []

# REST API endpoint for writing data


@app.get("/api/data")
async def get_date():
    return {"message": data_store}

# REST API endpoint for writing data


@app.post("/api/data")
async def write_data(data: str):
    data_store.append(data)
    return {"message": "Data added to REST API"}

# WebSocket endpoint for writing data


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    websocket_connections.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            data_store.append(data)
            await websocket.send_text(f"Data written to WebSocket: {data}")
    except Exception:
        websocket_connections.remove(websocket)


@app.get("/")
async def get_index():
    with open("./templates/index.html", "r") as html:
        return HTMLResponse(content=html.read())
