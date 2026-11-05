import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.database import make_engine, make_session_factory, init_db
from app.models import Customer, Medicine, Purchase, PurchaseItem
from app.service import PharmacyService, PharmacyError


@pytest.fixture
def setup(tmp_path):
    engine = make_engine(f"sqlite:///{tmp_path / 'test.db'}")
    init_db(engine)
    factory = make_session_factory(engine)
    service = PharmacyService(factory)
    customer_id = service.add_customer("Тестовый покупатель", "89991112233")
    first = service.add_medicine("Аспирин", "A001", "120.50", 10)
    second = service.add_medicine("Бинт", "B001", "40", 5)
    yield service, factory, customer_id, first, second
    engine.dispose()


def test_add_customer(setup):
    service, factory, *_ = setup
    assert service.add_customer("Другой", "89990000009") == 2


def test_duplicate_customer(setup):
    service, *_ = setup
    with pytest.raises(PharmacyError):
        service.add_customer("Дубликат", "89991112233")


def test_add_medicine(setup):
    service, *_ = setup
    assert service.add_medicine("Новый", "C001", 15, 3) == 3


def test_duplicate_article(setup):
    service, *_ = setup
    with pytest.raises(PharmacyError):
        service.add_medicine("Другой", "A001", 15, 3)


def test_invalid_price(setup):
    service, *_ = setup
    with pytest.raises(PharmacyError):
        service.add_medicine("Неверный", "C001", -10, 3)


def test_get_by_id(setup):
    service, _, _, first, _ = setup
    assert service.read(lambda r: r.get_medicine(first)).name == "Аспирин"


def test_search_filter(setup):
    service, *_ = setup
    result = service.read(lambda r: r.medicines(search="асп", max_price=150, min_stock=6))
    assert len(result) == 1


def test_sort(setup):
    service, *_ = setup
    result = service.read(lambda r: r.medicines(sort="price_desc"))
    assert result[0].name == "Аспирин"


def test_pagination(setup):
    service, *_ = setup
    assert len(service.read(lambda r: r.medicines(page=2, page_size=1))) == 1


def test_update(setup):
    service, _, _, first, _ = setup
    service.update_medicine(first, price=200, stock=7)
    assert service.read(lambda r: r.get_medicine(first)).stock == 7


def test_delete(setup):
    service, _, _, first, _ = setup
    service.delete_medicine(first)
    assert service.read(lambda r: r.get_medicine(first)) is None


def test_missing_delete(setup):
    service, *_ = setup
    with pytest.raises(PharmacyError):
        service.delete_medicine(999)


def test_purchase_total_and_stock(setup):
    service, _, cid, first, second = setup
    pid, total = service.buy(cid, [(first, 2), (second, 3)])
    assert total == 361
    assert service.read(lambda r: r.get_medicine(first)).stock == 8
    assert len(service.read(lambda r: r.get_purchase(pid)).items) == 2


def test_purchase_many_to_many(setup):
    service, factory, cid, first, second = setup
    service.buy(cid, [(first, 1), (second, 1)])
    with factory() as session:
        assert len(session.scalars(select(PurchaseItem)).all()) == 2


def test_rollback_when_insufficient(setup):
    service, factory, cid, first, second = setup
    with pytest.raises(PharmacyError):
        service.buy(cid, [(first, 2), (second, 999)])
    assert service.read(lambda r: r.get_medicine(first)).stock == 10
    with factory() as session:
        assert session.scalar(select(Purchase)) is None


def test_missing_customer_rollback(setup):
    service, *_ = setup
    with pytest.raises(PharmacyError):
        service.buy(999, [(1, 1)])


def test_duplicate_lines_combined(setup):
    service, _, cid, first, _ = setup
    _, total = service.buy(cid, [(first, 1), (first, 2)])
    assert total == 361.5
    assert service.read(lambda r: r.get_medicine(first)).stock == 7


def test_cancel_restores_stock(setup):
    service, _, cid, first, _ = setup
    pid, _ = service.buy(cid, [(first, 3)])
    service.cancel_purchase(pid)
    assert service.read(lambda r: r.get_medicine(first)).stock == 10
    assert service.read(lambda r: r.get_purchase(pid)).status == "cancelled"


def test_cancel_twice_error(setup):
    service, _, cid, first, _ = setup
    pid, _ = service.buy(cid, [(first, 1)])
    service.cancel_purchase(pid)
    with pytest.raises(PharmacyError):
        service.cancel_purchase(pid)


def test_statistics(setup):
    service, _, cid, first, _ = setup
    service.buy(cid, [(first, 2)])
    stats = service.read(lambda r: r.statistics())
    assert stats["count"] == 1
    assert stats["total"] == 241


def test_related_purchases(setup):
    service, _, cid, first, _ = setup
    service.buy(cid, [(first, 1)])
    assert len(service.read(lambda r: r.purchases(cid))) == 1


def test_foreign_key(setup):
    service, factory, *_ = setup
    with pytest.raises(IntegrityError):
        with factory.begin() as session:
            session.add(Purchase(customer_id=999, total=0))
