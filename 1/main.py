from fastapi import FastAPI

app = FastAPI()

# Sample WebID profile data
webid_profile = [
    {
        "id": 1,
        "name": "John",
        "email": "john@example.com",
        "location": "New York"
    },
    {
        "id": 2,
        "name": "Doe",
        "email": "doe@example.com",
        "location": "New York"
    }
]


@app.get("/profile")
async def get_webid_profile():
    return webid_profile


@app.get("/profile/{webid}")
async def get_webid_profile(webid: str):
    for profile in webid_profile:
        if profile["id"] == int(webid):
            return [profile]
