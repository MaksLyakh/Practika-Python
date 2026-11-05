import pytest
from app.services import PharmacyService, ValidationError

def test_invalid_price():
    class Dummy:
        def get(self,*args): return object()
    with pytest.raises(ValidationError):
        PharmacyService(Dummy()).parse(dict(name='Тест',price=-1,stock=1,category_id=1))

def test_invalid_stock():
    class Dummy:
        def get(self,*args): return object()
    with pytest.raises(ValidationError):
        PharmacyService(Dummy()).parse(dict(name='Тест',price=10,stock=-1,category_id=1))
