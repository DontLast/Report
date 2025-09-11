from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
import database
import models
from typing import List
import os

# Создаем таблицы
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Blog System API")

# Обслуживаем статические файлы
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Модели Pydantic
class UserCreate(BaseModel):
    email: str
    username: str
    password: str
    full_name: str


class UserLogin(BaseModel):
    identifier: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: str

    class Config:
        from_attributes = True


class PostCreate(BaseModel):
    title: str
    content: str
    author_id: int


class PostUpdate(BaseModel):
    title: str
    content: str


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    author_name: str
    created_at: datetime

    class Config:
        from_attributes = True


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# User endpoints
@app.post("/register/", response_model=UserResponse)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    print(f"Получен запрос на регистрацию: {user}")

    # Проверяем обязательные поля
    if not all([user.email, user.username, user.password, user.full_name]):
        raise HTTPException(status_code=400, detail="Все поля обязательны для заполнения")

    db_user_email = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user_email:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")

    db_user_username = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user_username:
        raise HTTPException(status_code=400, detail="Имя пользователя уже занято")

    db_user = models.User(
        email=user.email,
        username=user.username,
        password=user.password,
        full_name=user.full_name
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    print(f"Пользователь успешно создан: {db_user.id}")
    return db_user


@app.post("/login/", response_model=UserResponse)
async def login_user(login_data: UserLogin, db: Session = Depends(get_db)):
    print(f"Попытка входа: {login_data.identifier}")

    user = db.query(models.User).filter(
        (models.User.email == login_data.identifier) |
        (models.User.username == login_data.identifier)
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")

    if user.password != login_data.password:
        raise HTTPException(status_code=401, detail="Неверный пароль")

    print(f"Успешный вход: {user.username}")
    return user


@app.get("/users/", response_model=List[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    print(f"Запрошен список пользователей: {len(users)} пользователей")
    return users


@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    db.delete(user)
    db.commit()

    print(f"Пользователь удален: {user_id}")
    return {"message": "Пользователь успешно удален"}


# Post endpoints
@app.post("/posts/", response_model=PostResponse)
async def create_post(post: PostCreate, db: Session = Depends(get_db)):
    print(f"Создание поста: {post.title}")

    user = db.query(models.User).filter(models.User.id == post.author_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    db_post = models.Post(
        title=post.title,
        content=post.content,
        author_id=post.author_id,
        created_at=datetime.now()
    )

    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    print(f"Пост создан: {db_post.id}")
    return {
        "id": db_post.id,
        "title": db_post.title,
        "content": db_post.content,
        "author_id": db_post.author_id,
        "author_name": user.username,
        "created_at": db_post.created_at
    }


@app.get("/posts/", response_model=List[PostResponse])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).order_by(models.Post.created_at.desc()).all()

    result = []
    for post in posts:
        user = db.query(models.User).filter(models.User.id == post.author_id).first()
        result.append({
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "author_id": post.author_id,
            "author_name": user.username if user else "Неизвестный автор",
            "created_at": post.created_at
        })

    print(f"Запрошены посты: {len(result)} постов")
    return result


@app.get("/posts/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")

    user = db.query(models.User).filter(models.User.id == post.author_id).first()

    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "author_id": post.author_id,
        "author_name": user.username if user else "Неизвестный автор",
        "created_at": post.created_at
    }


@app.put("/posts/{post_id}", response_model=PostResponse)
async def update_post(post_id: int, post_data: PostUpdate, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")

    post.title = post_data.title
    post.content = post_data.content

    db.commit()
    db.refresh(post)

    user = db.query(models.User).filter(models.User.id == post.author_id).first()

    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "author_id": post.author_id,
        "author_name": user.username if user else "Неизвестный автор",
        "created_at": post.created_at
    }


@app.delete("/posts/{post_id}")
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")

    db.delete(post)
    db.commit()

    return {"message": "Пост успешно удален"}


# Main endpoint
@app.get("/")
async def serve_frontend():
    return FileResponse("../frontend/index.html")


@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Server is running"}


# Эндпоинт для проверки соединения
@app.get("/test")
async def test_connection():
    return {"message": "Сервер работает", "timestamp": datetime.now().isoformat()}