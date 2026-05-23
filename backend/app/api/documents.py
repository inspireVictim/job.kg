from __future__ import annotations

import os
import shutil
import uuid
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, Response, UploadFile, status
from fastapi.responses import FileResponse

from app.api.deps import CurrentUser, DbSession, require_roles
from app.core.config import settings
from app.models.document import Document
from app.models.user import User
from app.schemas.document import DocumentOut


router = APIRouter(prefix="/documents", tags=["Документы"])


def _to_out(doc: Document) -> DocumentOut:
    return DocumentOut(
        id=doc.id,
        title=doc.title,
        description=doc.description,
        original_filename=doc.original_filename,
        size_bytes=doc.size_bytes,
        uploaded_by=doc.uploaded_by,
        uploader_name=doc.uploader.full_name if doc.uploader else None,
        uploaded_at=doc.uploaded_at,
    )


@router.get("/", response_model=List[DocumentOut])
def list_documents(db: DbSession, current_user: CurrentUser) -> List[DocumentOut]:
    items = db.query(Document).order_by(Document.uploaded_at.desc()).all()
    return [_to_out(d) for d in items]


@router.post(
    "/",
    response_model=DocumentOut,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    db: DbSession,
    title: str = Form(..., min_length=2, max_length=255),
    description: Optional[str] = Form(default=None, max_length=512),
    file: UploadFile = File(...),
    current_user: User = Depends(require_roles("admin", "hr")),
) -> DocumentOut:
    if file.filename is None or file.filename.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Имя файла не указано",
        )

    safe_name = Path(file.filename).name
    suffix = Path(safe_name).suffix
    stored_name = f"{uuid.uuid4().hex}{suffix}"
    stored_path = settings.UPLOAD_DIR / stored_name

    size = 0
    with stored_path.open("wb") as buffer:
        while True:
            chunk = await file.read(1024 * 1024)
            if not chunk:
                break
            size += len(chunk)
            if size > settings.MAX_UPLOAD_SIZE:
                buffer.close()
                stored_path.unlink(missing_ok=True)
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail="Размер файла превышает допустимый предел (20 МБ)",
                )
            buffer.write(chunk)

    doc = Document(
        title=title,
        description=description,
        file_path=str(stored_path.relative_to(settings.UPLOAD_DIR.parent)),
        original_filename=safe_name,
        size_bytes=size,
        uploaded_by=current_user.id,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return _to_out(doc)


@router.get("/{document_id}/download")
def download_document(document_id: int, db: DbSession, current_user: CurrentUser) -> FileResponse:
    doc = db.query(Document).filter(Document.id == document_id).first()
    if doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Документ не найден")

    absolute_path = (settings.UPLOAD_DIR.parent / doc.file_path).resolve()
    if not absolute_path.exists():
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Файл документа отсутствует на сервере",
        )
    return FileResponse(
        path=str(absolute_path),
        filename=doc.original_filename,
        media_type="application/octet-stream",
    )


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_document(
    document_id: int,
    db: DbSession,
    current_user: User = Depends(require_roles("admin", "hr")),
):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Документ не найден")

    absolute_path = (settings.UPLOAD_DIR.parent / doc.file_path).resolve()
    if absolute_path.exists():
        try:
            os.remove(absolute_path)
        except OSError:
            pass

    db.delete(doc)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
