from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Sample data for subscriptions and friends list
subscriptions = []
friends_list = []


class SubscriptionCreate(BaseModel):
    user_id: int
    content: str


@app.get("/")
def Homepage():
    with open("./templates/index.html") as html:
        return HTMLResponse(content=html.read())


@app.post("/subscriptions/", response_model=SubscriptionCreate)
async def create_subscription(subscription: SubscriptionCreate):
    subscriptions.append(subscription)
    return subscription


@app.get("/subscriptions/", response_model=List[SubscriptionCreate])
async def get_subscriptions():
    return subscriptions

