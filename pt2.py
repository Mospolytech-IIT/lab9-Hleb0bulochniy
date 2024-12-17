'''Файл содержит задание из второй части лабораторной работы 9'''

from sqlalchemy.orm import Session
from pt1 import (User, Post)

# Напишите программу, которая добавляет в таблицу Users несколько записей
# с разными значениями полей username, email и password.
def add_users(db: Session):
    '''Добавляет нескольких пользователей в таблицу Users'''
    users = [
        User(username="test1", email="test1@mail.ru", password="123"),
        User(username="test2", email="test2@mail.ru", password="456"),
        User(username="test3", email="test3y@mail.ru", password="789")
    ]
    db.add_all(users)
    db.commit()


# Напишите программу, которая добавляет в таблицу Posts несколько записей,
# связанных с пользователями из таблицы Users.
def add_posts(db: Session):
    '''Добавляет в Posts несколько записей вместе с данными об их создателе'''
    users = db.query(User).all()
    posts = [
        Post(title="post1", content="First", user_id=users[0].id),
        Post(title="post2", content="Second",
             user_id=users[1].id),
        Post(title="post3", content="Third",
             user_id=users[2].id),
        Post(title="post4", content="Fourth", user_id=users[1].id),
    ]
    db.add_all(posts)
    db.commit()


# Напишите программу, которая извлекает все записи из таблицы Users.
def get_all_users(db: Session):
    '''Извлекает все записи из таблицы Users'''
    users = db.query(User).all()
    for user in users:
        print(f"ID: {user.id}, Username: {user.username}, " +
              f"Email: {user.email}, Password: {user.password}")
    return users


# Напишите программу, которая извлекает все записи из таблицы Posts,
# включая информацию о пользователях, которые их создали.
def get_all_posts_with_users(db: Session):
    '''Извлекает все посты из таблицы Posts'''
    posts = db.query(Post).join(User).all()
    for post in posts:
        print(f"ID: {post.id}, Title: {post.title}, Content: {post.content}, " +
              f"UserId: {post.user_id}, Username: {post.user.username}")
    return posts


# Напишите программу, которая извлекает записи из таблицы Posts,
# созданные конкретным пользователем.
def get_posts_by_user(db: Session, user_id):
    '''Извлекает все посты из таблицы Posts, связанные с пользователем по id'''
    posts = db.query(Post).filter(Post.user_id == user_id).all()
    for post in posts:
        print(f"Title: {post.title}, Content: {post.content}")
    return posts


# Напишите программу, которая обновляет поле email у одного из пользователей.
def update_user_email(db: Session, user_id, new_email):
    '''Меняет поле Email у пользователя по его id'''
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.email = new_email
        db.commit()


# Напишите программу, которая обновляет поле content у одного из постов.
def update_post_content(db: Session, post_id, new_content):
    '''Обновляет поле content у поста по его id'''
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        post.content = new_content
        db.commit()


# Напишите программу, которая удаляет один из постов.
def delete_post(db: Session, post_id):
    '''Удаляет пост из таблицы Posts по его ID'''
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        db.delete(post)
        db.commit()


# Напишите программу, которая удаляет пользователя и все его посты.
def delete_user(db: Session, user_id):
    '''Удаляет пользователя из Users и все его посты из Posts'''
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.query(Post).filter(Post.user_id == user_id).delete()
        db.delete(user)
        db.commit()
