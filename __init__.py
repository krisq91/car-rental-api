from flask import Flask
import click
from .database.db import setup_db

app = Flask(__name__)


@click.command('init_db', short_help='Initialize the database.')
def init_db():
    print('Initializing the database...')
    setup_db()

if __name__ == '__main__':
    setup_db()
    app.run(debug=True)
