import os


def redis_demo():
    import redis
    r = redis.Redis.from_url(os.getenv('REDIS_URL', 'redis://localhost:6379/0'), decode_responses=True)
    r.ping()
    r.set('doctor:1:schedule', '09:00,10:00,11:00')  # SET
    print('GET:', r.get('doctor:1:schedule'))         # GET
    r.expire('doctor:1:schedule', 60)                # EXPIRE
    print('TTL:', r.ttl('doctor:1:schedule'))
    print('INCR:', r.incr('clinic:requests'))         # INCR
    r.delete('doctor:1:schedule')                    # DELETE
    print('DELETE:', r.get('doctor:1:schedule'))


def mongo_demo():
    from pymongo import MongoClient
    with MongoClient(os.getenv('MONGO_URL', 'mongodb://localhost:27017'), serverSelectionTimeoutMS=2000) as client:
        collection = client.lab11.doctor_schedule
        collection.delete_many({'demo': True})
        collection.insert_one({'doctor_id': 1, 'hours': ['09:00', '10:00'], 'demo': True})
        print('FIND:', collection.find_one({'doctor_id': 1, 'demo': True}, {'_id': 0}))
        collection.update_one({'doctor_id': 1, 'demo': True}, {'$push': {'hours': '11:00'}})
        print('UPDATE:', collection.find_one({'doctor_id': 1, 'demo': True}, {'_id': 0}))
        print('COUNT:', collection.count_documents({'demo': True}))
        collection.delete_many({'demo': True})
        print('DELETE:', collection.count_documents({'demo': True}))


if __name__ == '__main__':
    try:
        redis_demo()
    except Exception as error:
        print('Redis недоступен:', error)
    try:
        mongo_demo()
    except Exception as error:
        print('MongoDB недоступна:', error)
