import os
import pytest
from fastapi.testclient import TestClient
from main import app
from db.conn import Base, engine, Session
from datetime import datetime
from random import randint

os.environ["ENV"] = "test"
client = TestClient(app)

@pytest.fixture()
def test_db():
    yield
    Session.close_all()
    Base.metadata.drop_all(engine)

def test_get_events_with_no_events_returns_empty_list(test_db):
    response = client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data["result"], list)
    assert len(data["result"]) == 0
    assert data["page_token"] == None

def test_add_event_ok(test_db):
    uid = f"test_add_event_ok_uid_{datetime.now()}"
    response = client.post("/login", params={"uid": uid})
    assert response.status_code == 200

    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["result"], list)
    assert len(data["result"]) == 1

    event = data["result"][0]
    assert event["event_id"] == 1
    assert event["event_type"] == "login"
    assert event["user_id"] == uid

def test_add_event_error_invalid_event_type(test_db):
    uid = f"test_add_event_ok_uid_{datetime.now()}"
    response = client.post("/invalid", params={"uid": uid})
    assert response.status_code == 422

def test_add_event_error_missing_uid(test_db):
    response = client.post("/login")
    assert response.status_code == 422

def test_get_events_multiple_results_ok(test_db):
    uid_1 = f"test_get_events_multiple_results_ok_{datetime.now()}"
    response = client.post("/login", params={"uid": uid_1})
    assert response.status_code == 200

    uid_2 = f"test_get_events_multiple_results_ok_{datetime.now()}"
    response = client.post("/signup", params={"uid": uid_2})
    assert response.status_code == 200

    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["result"], list)
    assert len(data["result"]) == 2

    event = data["result"][0]
    assert event["event_id"] == 2
    assert event["event_type"] == "signup"
    assert event["user_id"] == uid_2

    event = data["result"][1]
    assert event["event_id"] == 1
    assert event["event_type"] == "login"
    assert event["user_id"] == uid_1

def test_get_stats(test_db):
    n_logins = randint(1, 10)
    n_signups = randint(1, 10)
    n_passwordresets = randint(1, 10)

    for _ in range(n_logins):
        uid_1 = f"test_get_stats_{datetime.now()}"
        response = client.post("/login", params={"uid": uid_1})
        assert response.status_code == 200
    
    for _ in range(n_signups):
        uid_1 = f"test_get_stats_{datetime.now()}"
        response = client.post("/signup", params={"uid": uid_1})
        assert response.status_code == 200
    
    for _ in range(n_passwordresets):
        uid_1 = f"test_get_stats_{datetime.now()}"
        response = client.post("/passwordReset", params={"uid": uid_1})
        assert response.status_code == 200
    
    response = client.get("/stats")
    assert response.status_code == 200
    data = response.json()

    result = data["result"]
    assert isinstance(result, dict)
    
    logins = result["login"]
    assert isinstance(logins, list)
    assert len(logins) == 1
    assert logins[0]["count"] == n_logins
    assert logins[0]["date"] == datetime.today().strftime("%Y-%m-%d")

    signups = result["signup"]
    assert isinstance(signups, list)
    assert len(signups) == 1
    assert signups[0]["count"] == n_signups
    assert signups[0]["date"] == datetime.today().strftime("%Y-%m-%d")

    passwordresets = result["passwordReset"]
    assert isinstance(passwordresets, list)
    assert len(passwordresets) == 1
    assert passwordresets[0]["count"] == n_passwordresets
    assert passwordresets[0]["date"] == datetime.today().strftime("%Y-%m-%d")

def test_get_users_summary(test_db):
    response = client.get("/usersSummary")
    assert response.status_code == 200
    data = response.json()

    result = data["result"]
    assert isinstance(result, dict)
    assert len(result.keys()) == 3
    assert isinstance(result["total_users"], int)
    assert isinstance(result["total_blocked_users"], int)
    assert isinstance(result["total_admins"], int)
