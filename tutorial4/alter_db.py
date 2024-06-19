from sqlalchemy import inspect
from website import db, create_app

def print_table_structure():
    app = create_app()
    with app.app_context():
        inspector = inspect(db.engine)
        for column in inspector.get_columns('recycling_effort'):
            print("Column: %s" % column['name'])

if __name__ == "__main__":
    print_table_structure()