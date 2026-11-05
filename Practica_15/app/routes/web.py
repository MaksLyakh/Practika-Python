from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from ..database import SessionLocal
from ..models import Category
from ..repositories import MedicineRepository, CategoryRepository, PurchaseRepository
from ..services import PharmacyService, ValidationError, ConflictError
web=Blueprint('web',__name__)
@web.get('/')
def index():
    with SessionLocal() as db:
        return render_template('index.html',count=len(MedicineRepository(db).list()),purchases=len(PurchaseRepository(db).list()))
@web.get('/medicines')
def medicines():
    with SessionLocal() as db:
        try:
            category=int(request.args['category']) if request.args.get('category') else None
            min_price=float(request.args['min_price']) if request.args.get('min_price') else None
            max_price=float(request.args['max_price']) if request.args.get('max_price') else None
        except ValueError: abort(400)
        items=MedicineRepository(db).list(request.args.get('search',''),category,min_price,max_price,request.args.get('sort','name'))
        return render_template('list.html',items=items,categories=CategoryRepository(db).list(),filters=request.args)
@web.get('/medicines/<int:ident>')
def detail(ident):
    with SessionLocal() as db:
        item=MedicineRepository(db).get(ident)
        if not item: abort(404)
        return render_template('detail.html',item=item)
@web.route('/medicines/create',methods=['GET','POST'])
def create():
    with SessionLocal() as db:
        if request.method=='POST':
            try:
                item=PharmacyService(db).create(request.form)
                flash('Лекарство добавлено','success');return redirect(url_for('web.detail',ident=item.id))
            except ValidationError as e: flash(str(e),'error')
        return render_template('form.html',item=None,categories=CategoryRepository(db).list())
@web.route('/medicines/<int:ident>/edit',methods=['GET','POST'])
def edit(ident):
    with SessionLocal() as db:
        item=MedicineRepository(db).get(ident)
        if not item: abort(404)
        if request.method=='POST':
            try:
                PharmacyService(db).update(item,request.form)
                flash('Изменения сохранены','success');return redirect(url_for('web.detail',ident=ident))
            except ValidationError as e: flash(str(e),'error')
        return render_template('form.html',item=item,categories=CategoryRepository(db).list())
@web.post('/medicines/<int:ident>/delete')
def delete(ident):
    with SessionLocal() as db:
        item=MedicineRepository(db).get(ident)
        if not item: abort(404)
        try:
            PharmacyService(db).delete(item);flash('Лекарство удалено','success')
        except ConflictError as e: flash(str(e),'error')
        return redirect(url_for('web.medicines'))
@web.post('/medicines/<int:ident>/buy')
def buy(ident):
    with SessionLocal() as db:
        item=MedicineRepository(db).get(ident)
        if not item: abort(404)
        try:
            order=PharmacyService(db).purchase(item,request.form.get('quantity'))
            flash(f'Покупка №{order.id} оформлена','success')
        except (ValidationError,ConflictError) as e: flash(str(e),'error')
        return redirect(url_for('web.detail',ident=ident))
@web.get('/purchases')
def purchases():
    with SessionLocal() as db: return render_template('purchases.html',orders=PurchaseRepository(db).list())
