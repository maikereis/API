#async bug: "ValueError: set_wakeup_fd only works in main thread"
import sys, asyncio
if sys.platform == "win32" and (3, 8, 0) <= sys.version_info < (3, 9, 0):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"CashBack API": "Hello World!"}

def test_login():
    response = client.post(
        "/token",
        ## default x-www-form-urlencoded
        {
            "grant_type": "", 
            "username":'johndoe', 
            "password":"secret", 
            "scope":"", 
            "client_id":"", 
            "client_secret":""
        },
    )
    assert response.status_code == 200 
    assert response.json() == {'access_token': 'johndoe', 'token_type': 'bearer'}
