import click
from flask import Flask
from flask.cli import with_appcontext
from app.extensions import db


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'

    @click.command(name='init-db')
    @with_appcontext
    def init_db_command():
        with app.app_context():
            db.create_all()
            click.echo('Initialized the database.')

    # Register the CLI command
    app.cli.add_command(init_db_command)

    # Initialize Flask extensions here
    db.init_app(app)

    @app.route('/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app

