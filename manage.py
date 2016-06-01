from flask.ext.script import Manager, Server
from app import app, db

manager = Manager(app)

manager.add_command("runserver",
        Server(host = "0.0.0.0", port = 5000, use_debugger = True))

@manager.command
def create_all():
    """create db tables"""
    db.create_all()

if __name__ == '__main__':
    manager.run()