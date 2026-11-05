import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.database import Base, get_db
from app.main import app
from app.cache import get_cache
from app.models.appointment import User
from app.security import hash_password

class FakeCache:
    def __init__(self):
        self.data = {}
        self.events = []
        self.hits = 0
        self.misses = 0
        self.invalidations = []
    def get(self, aid):
        if aid in self.data:
            self.hits += 1
            return self.data[aid]
        self.misses += 1
        return None
    def set(self, aid, value):
        self.data[aid] = value
    def invalidate(self, aid):
        self.data.pop(aid, None)
        self.invalidations.append(aid)
    def publish(self, event, aid):
        self.events.append((event, aid))

@pytest.fixture
def client():
    engine = create_engine('sqlite+pysqlite://', connect_args={'check_same_thread': False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(engine, expire_on_commit=False)
    cache = FakeCache()
    with session_factory() as db:
        db.add(User(username='admin', password_hash=hash_password('Admin123!'), role='ADMIN'))
        db.commit()
    def override_db():
        with session_factory() as db:
            yield db
    app.dependency_overrides[get_db] = override_db
    app.dependency_overrides[get_cache] = lambda: cache
    c = TestClient(app)
    c.fake_cache = cache
    yield c
    c.close()
    app.dependency_overrides.clear()
    engine.dispose()

@pytest.fixture
def admin_headers(client):
    response = client.post('/auth/login', json={'username':'admin','password':'Admin123!'})
    assert response.status_code == 200, response.text
    return {'Authorization': 'Bearer ' + response.json()['access_token']}

@pytest.fixture
def user_headers(client):
    assert client.post('/auth/register', json={'username':'testuser','password':'Password123!'}).status_code == 201
    token = client.post('/auth/login', json={'username':'testuser','password':'Password123!'}).json()['access_token']
    return {'Authorization': 'Bearer ' + token}

@pytest.fixture
def payload():
    return {'patient':'Алексей Иванов', 'doctor':'Иван Иванов', 'specialty':'Терапевт',
            'date':'2026-12-10', 'time':'10:00:00', 'room':101, 'status':'scheduled'}

@pytest.fixture
def created(client, admin_headers, payload):
    response = client.post('/appointments', json=payload, headers=admin_headers)
    assert response.status_code == 201, response.text
    return response.json()
