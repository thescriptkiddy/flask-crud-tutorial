import random
import uuid
import app
from flask import Flask, jsonify
from app.extensions import db
from uuid import UUID, uuid4
from test_data import random_names, random_cities


# Define the User model
class User(db.Model):
    id = db.Column(db.UUID, primary_key=True)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    city = db.Column(db.String(50))


class Post(db.Model):
    id = db.Column(db.UUID, primary_key=True)
    title = db.Column(db.String(250))
    body = db.Column(db.Text)


# CRUD Helper Functions, for Database operations.
def create_record(model, **kwargs):
    """Creates a new record"""
    print(f"Creating record with data: {kwargs}")
    record = model(**kwargs)
    db.session.add(record)
    db.session.commit()
    return record


def read_records(model, *identifier):
    """Returns either all existing records or specific records if identifier(s) has been passed"""
    if identifier:
        try:
            record = db.get_or_404(model, identifier)
            # print(record.name)
            return record
        except Exception as err:
            print(f"An error occurred: {err}")
            return None
    elif not identifier:
        try:
            records = db.session.execute(db.select(model)).scalars()
            # print(records)
            return records
        except Exception as err:
            print(f"An error occurred: {err}")
            return None


def update_records(model, identifier, **kwargs):
    """Updates an database object"""
    try:
        print(f"Updating record id: {identifier} with data: {kwargs}")
        record = db.get_or_404(model, uuid.UUID(identifier))
        if record:
            for key, value in kwargs.items():
                setattr(record, key, value)
            db.session.commit()
            return record
    except Exception as err:
        print(f"Error occurred: {err}")
        return None


def delete_record(model, identifier):
    """Deletes an database object"""
    print(f"Deleting record id: {identifier}")
    result = db.session.execute(db.select(model).where(model.id == uuid.UUID(identifier)))
    record = result.scalar_one_or_none()
    if record:
        db.session.delete(record)
        db.session.commit()
        return True
    return False


# CRUD USER MODEL
def create_new_user(**kwargs):
    """Creates a new user object and returns it as json"""
    data = kwargs
    user = create_record(User, **data)
    return jsonify(user.id), 201


def get_users(*identifier):
    """Returns user objects. If no identifier has been provided it returns all existing user objects"""
    try:
        if identifier:
            if len(identifier) == 1:
                user = read_records(User, uuid.UUID(identifier[0]))
                print(f"User from get_user: {user.name}")
                return user
            else:
                users = [read_records(User, uuid.UUID(id)) for id in identifier]
                print(f"List of users {users}")
                for user in users:
                    print(f"Usernames from get_users {user.name}")
                return users
        else:
            users = read_records(User)
            print(users)
            return users
    except Exception as err:
        print(f"An error occurred: {err}")


def delete_user_by_id(identifier):
    """Deletes a user by its id (uuid)"""
    user_to_be_deleted = delete_record(User, identifier)
    print(user_to_be_deleted)
    return user_to_be_deleted


# CRUD Post Model
def create_new_post(**kwargs):
    data = kwargs
    post = create_record(Post, **data)
    return jsonify(post.id), 201


def get_posts(*identifier):
    """Returns all post object or specific posts if optional identifiers(post_id) have been passed"""
    try:
        if identifier:
            if len(identifier) == 1:
                post = read_records(Post, uuid.UUID(identifier[0]))
                print(f"Post from get_posts: {post.title}")
                return post
            else:
                posts = [read_records(Post, uuid.UUID(id)) for id in identifier]
                print(f"List of posts {posts}")
                for post in posts:
                    print(f"Post titles from get_posts {post.title}")
                return posts
        else:
            posts = read_records(Post)
            print(posts)
            # TODO Need to check how I return all posts as json data
            all_posts = [post for post in posts]
            print(all_posts)

            return all_posts
    except Exception as err:
        print(f"An error occurred: {err}")


def delete_post_by_id(identifier):
    post_to_be_deleted = delete_record(Post, identifier)
    return post_to_be_deleted


# Testing
def generate_random_posts():
    for _ in range(0, 10):
        random_number = random.randint(0, 1000)
        new_post = create_new_post(id=uuid4(),
                                   title=f"My new Title+{random_number}",
                                   body=f"My body text+{random_number}")

        print(new_post)


def generate_random_user():
    for _ in range(0, 10):
        random_number = random.randint(1, 99)
        new_user = create_new_user(id=uuid4(),
                                   name=random.choice(random_names),
                                   age=random_number,
                                   city=random.choice(random_cities))
        print(new_user)
