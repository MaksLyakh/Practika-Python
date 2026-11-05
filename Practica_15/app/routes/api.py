from flask import Blueprint, jsonify, request, abort
from ..database import SessionLocal
from ..repositories import MedicineRepository, CategoryRepository, PurchaseRepository
from ..services import PharmacyService, ValidationError, ConflictError
api=Blueprint('api',__name__)
def as_dict(m): return dict(id=m.id,name=m.name,price=float(m.price),stock=m.stock,category_id=m.category_id,category=m.category.name)
@api.get('/medicines')
def listing():
    with SessionLocal() as db:
        try:
            cat=int(request.args['category']) if request.args.get('category') else None
            lo=float(request.args['min_price']) if request.args.get('min_price') else None
            hi=float(request.args['max_price']) if request.args.get('max_price') else None
        except ValueError: abort(400)
        return jsonify([as_dict(m) for m in MedicineRepository(db).list(request.args.get('search',''),cat,lo,hi,request.args.get('sort','name'))])
@api.get('/medicines/<int:ident>')
def one(ident):
    with SessionLocal() as db:
        m=MedicineRepository(db).get(ident)
        if not m: abort(404)
        return jsonify(as_dict(m))
@api.post('/medicines')
def create():
    with SessionLocal() as db:
        try: m=PharmacyService(db).create(request.get_json(silent=True) or {})
        except ValidationError as e: return jsonify(error=str(e)),400
        return jsonify(as_dict(m)),201
@api.route('/medicines/<int:ident>',methods=['PUT','PATCH'])
def update(ident):
    with SessionLocal() as db:
        m=MedicineRepository(db).get(ident)
        if not m: abort(404)
        data=request.get_json(silent=True) or {}
        if request.method=='PATCH': data={**dict(name=m.name,price=m.price,stock=m.stock,category_id=m.category_id),**data}
        try: PharmacyService(db).update(m,data)
        except ValidationError as e: return jsonify(error=str(e)),400
        return jsonify(as_dict(m))
@api.delete('/medicines/<int:ident>')
def delete(ident):
    with SessionLocal() as db:
        m=MedicineRepository(db).get(ident)
        if not m: abort(404)
        try: PharmacyService(db).delete(m)
        except ConflictError as e: return jsonify(error=str(e)),409
        return jsonify(message='Удалено'),200
@api.get('/categories')
def categories():
    with SessionLocal() as db: return jsonify([dict(id=c.id,name=c.name) for c in CategoryRepository(db).list()])
@api.get('/purchases')
def purchases():
    with SessionLocal() as db: return jsonify([dict(id=p.id,medicine_id=p.medicine_id,quantity=p.quantity,total=float(p.total)) for p in PurchaseRepository(db).list()])
@api.post('/purchases')
def buy():
    data=request.get_json(silent=True) or {}
    with SessionLocal() as db:
        try: ident=int(data['medicine_id'])
        except (KeyError,TypeError,ValueError): return jsonify(error='Укажите medicine_id'),400
        m=MedicineRepository(db).get(ident)
        if not m: abort(404)
        try: p=PharmacyService(db).purchase(m,data.get('quantity'))
        except ValidationError as e: return jsonify(error=str(e)),400
        except ConflictError as e: return jsonify(error=str(e)),409
        return jsonify(id=p.id,medicine_id=p.medicine_id,quantity=p.quantity,total=float(p.total)),201
