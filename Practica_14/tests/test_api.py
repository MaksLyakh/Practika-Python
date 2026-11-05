def test_health(client):
    assert client.get('/health').json() == {'status':'ok'}

def test_unauthorized(client):
    assert client.get('/appointments').status_code == 401

def test_register(client):
    r=client.post('/auth/register', json={'username':'newuser','password':'Password123!'})
    assert r.status_code == 201 and r.json()['role'] == 'USER'

def test_register_duplicate(client, user_headers):
    assert client.post('/auth/register',json={'username':'testuser','password':'Password123!'}).status_code == 409

def test_login_wrong_password(client):
    assert client.post('/auth/login',json={'username':'admin','password':'wrongpass'}).status_code == 401

def test_profile(client, admin_headers):
    assert client.get('/profile',headers=admin_headers).json()['role']=='ADMIN'

def test_invalid_token(client):
    assert client.get('/profile',headers={'Authorization':'Bearer invalid'}).status_code == 401

def test_user_cannot_write(client, user_headers, payload):
    assert client.post('/appointments',json=payload,headers=user_headers).status_code == 403

def test_post_created(client, admin_headers, payload):
    r=client.post('/appointments',json=payload,headers=admin_headers)
    assert r.status_code==201 and r.json()['patient']==payload['patient']

def test_post_invalid(client, admin_headers, payload):
    payload['room']=-1
    assert client.post('/appointments',json=payload,headers=admin_headers).status_code==422

def test_get_list(client, admin_headers, created):
    r=client.get('/appointments',headers=admin_headers)
    assert r.status_code==200 and r.json()['total']==1

def test_get_existing(client, admin_headers, created):
    r=client.get(f"/appointments/{created['id']}",headers=admin_headers)
    assert r.status_code==200 and r.json()['id']==created['id']

def test_get_missing(client, admin_headers):
    assert client.get('/appointments/999',headers=admin_headers).status_code==404

def test_put(client, admin_headers, created, payload):
    payload['patient']='Новый пациент'
    r=client.put(f"/appointments/{created['id']}",json=payload,headers=admin_headers)
    assert r.status_code==200 and r.json()['patient']=='Новый пациент'

def test_patch_preserves_other_fields(client, admin_headers, created):
    r=client.patch(f"/appointments/{created['id']}",json={'status':'completed'},headers=admin_headers)
    assert r.status_code==200 and r.json()['patient']==created['patient'] and r.json()['status']=='completed'

def test_patch_null_rejected(client, admin_headers, created):
    assert client.patch(f"/appointments/{created['id']}",json={'status':None},headers=admin_headers).status_code==422

def test_put_missing(client, admin_headers, payload):
    assert client.put('/appointments/999',json=payload,headers=admin_headers).status_code==404

def test_delete_and_repeat(client, admin_headers, created):
    path=f"/appointments/{created['id']}"
    assert client.delete(path,headers=admin_headers).status_code==204
    assert client.delete(path,headers=admin_headers).status_code==404

def test_filter(client, admin_headers, created):
    assert client.get('/appointments?specialty=Терапевт',headers=admin_headers).json()['total']==1
    assert client.get('/appointments?specialty=Хирург',headers=admin_headers).json()['total']==0

def test_sort(client, admin_headers, created, payload):
    payload['patient']='Борис'
    client.post('/appointments',json=payload,headers=admin_headers)
    r=client.get('/appointments?sort=patient&order=desc',headers=admin_headers)
    assert r.status_code==200 and r.json()['items'][0]['patient']=='Борис'

def test_pagination(client, admin_headers, created, payload):
    client.post('/appointments',json=payload,headers=admin_headers)
    r=client.get('/appointments?limit=1&offset=1',headers=admin_headers)
    assert r.status_code==200 and r.json()['total']==2 and len(r.json()['items'])==1

def test_search(client, admin_headers, created):
    assert client.get('/appointments/search?q=Алексей',headers=admin_headers).json()['total']==1

def test_statistics(client, admin_headers, created):
    r=client.get('/appointments/statistics',headers=admin_headers)
    assert r.status_code==200 and r.json()['total']==1 and r.json()['scheduled']==1 and r.json()['specialties']==1

def test_invalid_sort(client, admin_headers):
    assert client.get('/appointments?sort=not_a_column',headers=admin_headers).status_code==422

def test_cache_miss_hit(client, admin_headers, created):
    path=f"/appointments/{created['id']}"
    client.get(path,headers=admin_headers)
    client.get(path,headers=admin_headers)
    assert client.fake_cache.misses>=1 and client.fake_cache.hits>=1

def test_cache_invalidation_patch(client, admin_headers, created):
    aid=created['id']
    client.get(f'/appointments/{aid}',headers=admin_headers)
    assert aid in client.fake_cache.data
    client.patch(f'/appointments/{aid}',json={'status':'completed'},headers=admin_headers)
    assert aid not in client.fake_cache.data
    assert client.get(f'/appointments/{aid}',headers=admin_headers).json()['status']=='completed'

def test_cache_invalidation_delete(client, admin_headers, created):
    aid=created['id']
    client.get(f'/appointments/{aid}',headers=admin_headers)
    client.delete(f'/appointments/{aid}',headers=admin_headers)
    assert aid not in client.fake_cache.data

def test_pubsub_events(client, admin_headers, created):
    assert ('appointment.created',created['id']) in client.fake_cache.events

def test_openapi(client):
    r=client.get('/openapi.json')
    assert r.status_code==200 and '/appointments/search' in r.json()['paths']

def test_upload_invalid_extension(client, admin_headers, created):
    r=client.post(f"/appointments/{created['id']}/file",headers=admin_headers,
                  files={'file':('danger.exe',b'data','application/octet-stream')})
    assert r.status_code==422

def test_upload_too_large(client, admin_headers, created):
    r=client.post(f"/appointments/{created['id']}/file",headers=admin_headers,
                  files={'file':('big.txt',b'x'*(2*1024*1024+1),'text/plain')})
    assert r.status_code==413

def test_upload_download(client, admin_headers, created):
    aid=created['id']
    r=client.post(f'/appointments/{aid}/file',headers=admin_headers,
                  files={'file':('report.txt',b'Hello lab14','text/plain')})
    assert r.status_code==201, r.text
    file_id=r.json()['file_id']
    d=client.get(f'/appointments/{aid}/file/{file_id}',headers=admin_headers)
    assert d.status_code==200 and d.content==b'Hello lab14'

def test_async_health(client):
    assert client.get('/health').status_code==200
