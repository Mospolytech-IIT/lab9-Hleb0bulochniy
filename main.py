'''Главный файл для лабораторной работы 9'''

from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import FastAPI, Depends
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pt1 import (Base, User, Post, SessionLocal, engine)


app = FastAPI()
app.mount("/static", StaticFiles(directory="files", html=True))

class UserModel(BaseModel):
    '''Модель для пользователя'''
    username: str
    email: str
    password: str

class PostModel(BaseModel):
    '''Модель для поста'''
    title: str
    content: str
    user_id: int

Base.metadata.create_all(bind=engine)

def get_db():
    '''Получение сессии базы данных'''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    """Корневой маршрут для отображения index.html."""
    return FileResponse("files/index.html")


@app.get("/users/")
def get_all_users(db: Session = Depends(get_db)):
    '''Отправляет список всех пользователей'''
    users = db.query(User).all()
    if not users:
        return {"status": "error", "message": "Пользователи не найдены"}
    return {"status": "success", "users": users}


@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    '''Отправляет данные одного пользователя по id'''
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"status": "error", "message": "Пользователь не найден"}
    return {"status": "success", "user": user}


@app.post("/users/")
def create_user(user: UserModel, db: Session = Depends(get_db)):
    '''Добавляет нового пользователя'''
    if db.query(User).filter(
        or_(User.username == user.username, User.email == user.email)).first():
        return {"status": "error", "message": "Пользователь уже существует"}
    db_user = User(username=user.username, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"status": "success", "user": db_user}


@app.put("/users/{user_id}")
def update_user(user_id: int, updated_user: UserModel, db: Session = Depends(get_db)):
    '''Обновляет данные пользователя по id'''
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"status": "error", "message": "Пользователь не найден"}
    user.username = updated_user.username
    user.email = updated_user.email
    user.password = updated_user.password
    db.commit()
    db.refresh(user)
    return {"status": "success", "user": user}


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    '''Удаляет пользователя по id'''
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"status": "error", "message": "Пользователь не найден"}
    db.query(Post).filter(Post.user_id == user_id).delete()
    db.delete(user)
    db.commit()
    return {"status": "success", "message": "Пользователь удалён"}


@app.get("/posts/")
def get_all_posts(db: Session = Depends(get_db)):
    '''Отправляет все посты'''
    posts = db.query(Post).all()
    if not posts:
        return {"status": "error", "message": "Постов нет"}
    return {"status": "success", "posts": posts}


@app.get("/posts/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    '''Отправляет один пост'''
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return {"status": "error", "message": "Пост не найден"}
    return {"status": "success", "post": post}


@app.post("/posts/")
def create_post(post: PostModel, db: Session = Depends(get_db)):
    '''Добавляет новый пост'''
    if not db.query(User).filter(User.id == post.user_id).first():
        return {"status": "error", "message": "Создатель поста не найден"}
    db_post = Post(title=post.title, content=post.content, user_id=post.user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return {"status": "success", "post": db_post}


@app.put("/posts/{post_id}")
def update_post(post_id: int, updated_post: PostModel, db: Session = Depends(get_db)):
    '''Обновляет поля поста'''
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return {"status": "error", "message": "Пост не найден"}
    if not db.query(User).filter(User.id == updated_post.user_id).first():
        return {"status": "error", "message": "Создатель поста не найден"}
    post.title = updated_post.title
    post.content = updated_post.content
    post.user_id = updated_post.user_id
    db.commit()
    db.refresh(post)
    return {"status": "success", "post": post}


@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    '''Удаляет пост'''
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return {"status": "error", "message": "Пост не найден"}
    db.delete(post)
    db.commit()
    return {"status": "success", "message": "Пост  удалён"}
