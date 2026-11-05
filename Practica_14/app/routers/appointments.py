from datetime import date
from pathlib import Path
from uuid import uuid4
from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, Query, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.cache import AppointmentCache, get_cache
from app.database import get_db
from app.models.appointment import Attachment
from app.repositories.appointment import AppointmentRepository, SORT_FIELDS
from app.schemas.appointment import (AppointmentCreate, AppointmentUpdate, AppointmentPatch,
    AppointmentResponse, AppointmentListResponse, AppointmentStatistics)
from app.security import current_user, require_admin
from app.services.appointment import AppointmentService

router = APIRouter(prefix="/appointments", tags=["Записи на приём"])
UPLOAD_DIR = Path(__file__).resolve().parents[2] / "uploads"
MAX_FILE_BYTES = 2 * 1024 * 1024
ALLOWED_EXTENSIONS = {".pdf", ".txt", ".png", ".jpg", ".jpeg"}

def get_service(db: Session = Depends(get_db), cache: AppointmentCache = Depends(get_cache)):
    return AppointmentService(AppointmentRepository(db), cache)

def log_event(message: str):
    import logging
    logging.getLogger("clinic14.audit").info(message)

@router.get("", response_model=AppointmentListResponse, summary="Список, фильтрация, сортировка и пагинация")
def list_appointments(limit: int = Query(20, ge=1, le=100), offset: int = Query(0, ge=0),
                      sort: str = Query("date"), order: str = Query("asc", pattern="^(asc|desc)$"),
                      specialty: str | None = None, status: str | None = Query(None, pattern="^(scheduled|completed|cancelled)$"),
                      doctor: str | None = None, db: Session = Depends(get_db), user=Depends(current_user)):
    if sort not in SORT_FIELDS:
        raise HTTPException(422, f"sort должен быть одним из {sorted(SORT_FIELDS)}")
    total, items = AppointmentRepository(db).list(limit=limit, offset=offset, sort=sort, order=order,
                                                    specialty=specialty, status=status, doctor=doctor)
    return {"total": total, "limit": limit, "offset": offset, "items": items}

@router.get("/search", response_model=AppointmentListResponse, summary="Поиск по пациенту или врачу")
def search(q: str = Query(min_length=1), limit: int = Query(20, ge=1, le=100),
           offset: int = Query(0, ge=0), db: Session = Depends(get_db), user=Depends(current_user)):
    total, items = AppointmentRepository(db).list(q=q, limit=limit, offset=offset)
    return {"total": total, "limit": limit, "offset": offset, "items": items}

@router.get("/statistics", response_model=AppointmentStatistics, summary="Статистика приёмов")
def statistics(db: Session = Depends(get_db), user=Depends(current_user)):
    return AppointmentRepository(db).statistics()

@router.get("/{appointment_id}", response_model=AppointmentResponse, summary="Получить запись с Redis Cache-Aside")
def get_appointment(appointment_id: int, service: AppointmentService = Depends(get_service), user=Depends(current_user)):
    return service.get(appointment_id)

@router.post("", response_model=AppointmentResponse, status_code=201, summary="Создать запись")
def create_appointment(data: AppointmentCreate, tasks: BackgroundTasks,
                       service: AppointmentService = Depends(get_service), admin=Depends(require_admin)):
    result = service.create(data)
    tasks.add_task(log_event, f"Создан приём {result.id}")
    return result

@router.put("/{appointment_id}", response_model=AppointmentResponse, summary="Полностью заменить запись")
def put_appointment(appointment_id: int, data: AppointmentUpdate,
                    service: AppointmentService = Depends(get_service), admin=Depends(require_admin)):
    return service.update(appointment_id, data.model_dump())

@router.patch("/{appointment_id}", response_model=AppointmentResponse, summary="Частично изменить запись")
def patch_appointment(appointment_id: int, data: AppointmentPatch,
                      service: AppointmentService = Depends(get_service), admin=Depends(require_admin)):
    return service.update(appointment_id, data.model_dump(exclude_unset=True))

@router.delete("/{appointment_id}", status_code=204, summary="Удалить запись")
def delete_appointment(appointment_id: int, service: AppointmentService = Depends(get_service), admin=Depends(require_admin)):
    service.delete(appointment_id)

@router.post("/{appointment_id}/file", status_code=201, summary="Загрузить вложение до 2 МБ")
async def upload_file(appointment_id: int, file: UploadFile = File(...),
                      db: Session = Depends(get_db), admin=Depends(require_admin)):
    if AppointmentRepository(db).get(appointment_id) is None:
        raise HTTPException(404, "Запись на приём не найдена")
    extension = Path(file.filename or "").suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(422, "Недопустимое расширение файла")
    content = await file.read(MAX_FILE_BYTES + 1)
    if len(content) > MAX_FILE_BYTES:
        raise HTTPException(413, "Файл больше 2 МБ")
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    stored = uuid4().hex + extension
    (UPLOAD_DIR / stored).write_bytes(content)
    attachment = Attachment(appointment_id=appointment_id, original_name=Path(file.filename).name,
                            stored_name=stored)
    db.add(attachment)
    db.commit()
    db.refresh(attachment)
    return {"file_id": attachment.id, "filename": attachment.original_name}

@router.get("/{appointment_id}/file/{file_id}", summary="Скачать вложение")
def download_file(appointment_id: int, file_id: int, db: Session = Depends(get_db), user=Depends(current_user)):
    attachment = db.get(Attachment, file_id)
    if attachment is None or attachment.appointment_id != appointment_id:
        raise HTTPException(404, "Вложение не найдено")
    path = UPLOAD_DIR / attachment.stored_name
    if not path.is_file():
        raise HTTPException(404, "Файл не найден на диске")
    return FileResponse(path, filename=attachment.original_name)
