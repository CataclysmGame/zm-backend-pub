import base64
import math

from fastapi.testclient import TestClient

from app import app
from app.settings import settings
from app.util import get_timestamp

client = TestClient(app)


def test_get_ticket():
    ts = get_timestamp()
    res = client.get("/api/v1/ticket")
    assert res.status_code == 200
    ticket = res.json()
    ticket_bytes = base64.urlsafe_b64decode(ticket + '=')
    assert len(ticket_bytes) == settings.GAME_TICKET_LEN

    res = client.get(f"/api/v1/ticket/{ticket}")
    assert res.status_code == 200
    game = res.json()

    ts_delta = math.fabs(ts - game['ts'])
    assert ts_delta < 5

    assert game['client'] == 'testclient'
