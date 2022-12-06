from flask.cli import FlaskGroup

from project.app import app
from project.modelos import db

cli = FlaskGroup(app)


# @cli.command("create_db")
# def create_db():
#     db.drop_all()
#     db.create_all()
#     db.session.commit()


# @cli.command("seed_db")
# def seed_db():
#     db.session.add(User(username= "usuario", password= "123", email="e.melara@uniandes.edu.co"))
#     db.session.commit()


if __name__ == "__main__":
    cli()

