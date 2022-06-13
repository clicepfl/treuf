from app import create_app, db
from app.models import User, Borrowing, Item, Role

# creates the app instance to be used when launching with flask run
app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Borrowing": Borrowing, "Item": Item, "Role": Role}
