from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.api.deps import CurrentUser, DbSession, require_roles
from app.models.news import News
from app.models.user import User
from app.schemas.news import NewsCreate, NewsOut


router = APIRouter(prefix="/news", tags=["Корпоративные новости"])


def _to_out(news: News) -> NewsOut:
    return NewsOut(
        id=news.id,
        title=news.title,
        content=news.content,
        author_id=news.author_id,
        author_name=news.author.full_name if news.author else None,
        created_at=news.created_at,
    )


@router.get("/", response_model=List[NewsOut])
def list_news(db: DbSession, current_user: CurrentUser) -> List[NewsOut]:
    items = db.query(News).order_by(News.created_at.desc()).all()
    return [_to_out(n) for n in items]


@router.get("/{news_id}", response_model=NewsOut)
def get_news(news_id: int, db: DbSession, current_user: CurrentUser) -> NewsOut:
    news = db.query(News).filter(News.id == news_id).first()
    if news is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Новость не найдена")
    return _to_out(news)


@router.post(
    "/",
    response_model=NewsOut,
    status_code=status.HTTP_201_CREATED,
)
def create_news(
    payload: NewsCreate,
    db: DbSession,
    current_user: User = Depends(require_roles("admin", "hr")),
) -> NewsOut:
    item = News(
        title=payload.title,
        content=payload.content,
        author_id=current_user.id,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return _to_out(item)


@router.delete("/{news_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_news(
    news_id: int,
    db: DbSession,
    current_user: User = Depends(require_roles("admin", "hr")),
):
    item = db.query(News).filter(News.id == news_id).first()
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Новость не найдена")
    db.delete(item)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
