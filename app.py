import uuid
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from uuid import UUID, uuid4

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db = SQLAlchemy(app)


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


def update_record(model, identifier, **kwargs):
    """Updates an database object"""
    try:
        print(f"Updating record id: {identifier} with data: {kwargs}")
        record = db.get_or_404(model, identifier)
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
    result = db.session.execute(db.select(model).where(model.id == identifier))
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


def get_posts():
    # TODO Refactor to use read_records with identifier. See get_users function
    posts = read_records(Post)
    for post in posts:
        print(post.title)
        print(post.id)


def delete_post_by_id(identifier):
    post_to_be_deleted = delete_record(Post, identifier)
    return post_to_be_deleted


# Ensure the database is created within the app context
with app.app_context():
    db.create_all()

    # create_new_user(
    #     id=uuid4(),
    #     name="Simon",
    #     age=20,
    #     city="Hamburg",)

    # get_user_by_id(identifier=uuid.UUID("722be9292cb24e179820914e96b2f2d2"))
    # update_record(User, identifier=uuid.UUID("722be9292cb24e179820914e96b2f2d2"), age=80, city="Hamburg")
    # delete_user_by_id(identifier=uuid.UUID("7100ee8921d146f2b49a0fe802a66d37"))

    # get_post_by_id(identifier=uuid.UUID("f0b9f2f074c948dca0f5bb1ee9a69c7c"))
    # delete_post_by_id(identifier=uuid.UUID("f0b9f2f074c948dca0f5bb1ee9a69c7c"))

    # read_records(User, uuid.UUID("b586eba81d394d86ac3e1d9935441e2a"))
    # get_users("669fb14a4513418388b7cc22ed47187e")
    # get_posts()