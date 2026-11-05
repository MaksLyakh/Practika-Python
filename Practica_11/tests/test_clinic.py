import pytest
from database import init_database, connect
from repository import AppointmentRepository
from service import ClinicService
from exceptions import ValidationError, NotFoundError
from app import create_app


@pytest.fixture
def prepared(tmp_path):
    path = tmp_path / 'test.db'
    init_database(path)
    with connect(path) as db:
        db.execute("INSERT INTO doctors(id,name,specialty) VALUES (1,'Врач','Терапевт')")
        db.execute("INSERT INTO patients(id,name,phone) VALUES (1,'Пациент','123')")
    repo = AppointmentRepository(path)
    return repo, ClinicService(repo), create_app(path).test_client()


def payload(time='2026-12-20 09:00'):
    return {'doctor_id': 1, 'patient_id': 1, 'appointment_time': time, 'price': 1500}


def test_empty(prepared):
    repo, _, _ = prepared
    assert repo.all() == []


def test_create(prepared):
    _, service, _ = prepared
    assert service.create(payload())['id'] == 1


def test_get(prepared):
    repo, service, _ = prepared
    service.create(payload())
    assert repo.get(1)['price'] == 1500


def test_missing(prepared):
    repo, _, _ = prepared
    with pytest.raises(NotFoundError):
        repo.get(999)


def test_invalid_price(prepared):
    _, service, _ = prepared
    with pytest.raises(ValidationError):
        service.create({**payload(), 'price': -1})


def test_invalid_date(prepared):
    _, service, _ = prepared
    with pytest.raises(ValidationError):
        service.create({**payload(), 'appointment_time': 'abc'})


def test_duplicate_slot(prepared):
    _, service, _ = prepared
    service.create(payload())
    with pytest.raises(ValidationError):
        service.create(payload())


def test_update(prepared):
    repo, service, _ = prepared
    service.create(payload())
    assert service.update(1, {'status': 'completed'}, partial=True)['status'] == 'completed'


def test_delete(prepared):
    repo, service, _ = prepared
    service.create(payload())
    repo.delete(1)
    assert repo.all() == []


def test_slots(prepared):
    repo, service, _ = prepared
    service.create(payload())
    assert '2026-12-20 09:00' not in repo.available_slots(1, '2026-12-20')


def test_api_list(prepared):
    _, _, client = prepared
    assert client.get('/appointments').status_code == 200


def test_api_create(prepared):
    _, _, client = prepared
    assert client.post('/appointments', json=payload()).status_code == 201


def test_api_bad_request(prepared):
    _, _, client = prepared
    assert client.post('/appointments', json={'price': 5}).status_code == 400


def test_api_404(prepared):
    _, _, client = prepared
    assert client.get('/appointments/123').status_code == 404


def test_api_patch(prepared):
    _, _, client = prepared
    client.post('/appointments', json=payload())
    assert client.patch('/appointments/1', json={'status': 'cancelled'}).json['status'] == 'cancelled'


def test_api_put(prepared):
    _, _, client = prepared
    client.post('/appointments', json=payload())
    assert client.put('/appointments/1', json={**payload(), 'price': 2000}).json['price'] == 2000


def test_api_delete(prepared):
    _, _, client = prepared
    client.post('/appointments', json=payload())
    assert client.delete('/appointments/1').status_code == 200


def test_transaction_rollback(prepared):
    repo, service, _ = prepared
    with pytest.raises(ValidationError):
        service.book({'patient_name': 'Новый', 'phone': '999', 'doctor_id': 999,
                      'appointment_time': '2026-12-20 09:00', 'price': 1000})
    with connect(repo.path) as db:
        assert db.execute("SELECT COUNT(*) FROM patients WHERE phone='999'").fetchone()[0] == 0


def test_api_slots(prepared):
    _, _, client = prepared
    result = client.get('/doctors/1/slots?date=2026-12-20')
    assert result.status_code == 200
    assert len(result.json['slots']) == 9


def test_static_cache_header(prepared):
    _, _, client = prepared
    result = client.get('/static-files/doctor1.svg')
    assert result.status_code == 200
    assert 'max-age=3600' in result.headers['Cache-Control']
