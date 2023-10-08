from flask import Flask
import click
from .database.db import setup_db

app = Flask(__name__)


@click.command('init_db', short_help='Initialize the database.')
def init_db():
    print('Initializing the database...')
    setup_db()


from .controllers.user import UserAPI

app.add_url_rule("/user/create", view_func=UserAPI.as_view("user_create"), methods=['POST'])
app.add_url_rule("/user/get/<int:user_id>", view_func=UserAPI.as_view("user_list"), methods=['GET'])
app.add_url_rule("/user/update/<int:user_id>", view_func=UserAPI.as_view("user_update"), methods=['PUT'])
app.add_url_rule("/user/delete/<int:user_id>", view_func=UserAPI.as_view("user_delete"), methods=['DELETE'])
app.cli.add_command(init_db)

if __name__ == '__main__':
    setup_db()
    app.run(debug=True)
