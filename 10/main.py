from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI()

# Sample user data
users = {
    1: {"id": 1, "username": "user1", "followers": [], "following": [2, 3]},
    2: {"id": 2, "username": "user2", "followers": [1], "following": [1, 3]},
    3: {"id": 3, "username": "user3", "followers": [1, 2], "following": [1, 2]},
    4: {"id": 4, "username": "user4", "followers": [], "following": []},
    5: {"id": 5, "username": "user5", "followers": [], "following": []},
}


def get_user(user_id):
    if user_id in users:
        return users[user_id]
    return None


@app.get("/")
def Homepage():
    with open("./templates/index.html") as html:
        return HTMLResponse(content=html.read())


@app.get("/users")
def UserList():
    return users


@app.get("/users/{user_id}")
def read_user(user_id: int):
    user = get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/follow/{user_id}/{followed_user_id}")
def follow_user(user_id: int, followed_user_id: int):
    user = get_user(user_id)
    followed_user = get_user(followed_user_id)
    if user is None or followed_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if followed_user_id not in user["following"]:
        user["following"].append(followed_user_id)
        followed_user["followers"].append(user_id)
    return {"message": "Followed successfully", "ok": True}


@app.post("/unfollow/{user_id}/{followed_user_id}")
def unfollow_user(user_id: int, followed_user_id: int):
    user = get_user(user_id)
    followed_user = get_user(followed_user_id)
    if user is None or followed_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if followed_user_id in user["following"]:
        user["following"].remove(followed_user_id)
        followed_user["followers"].remove(user_id)
    return {"message": "Unfollowed successfully"}
