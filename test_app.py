import pytest
from flask import Flask
from flask.testing import FlaskClient
from app import app, db, Furniture, initialize_database

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            initialize_database()
        yield client
        with app.app_context():
            # Clean up any new data created during the tests
            db.session.query(Furniture).delete()
            initialize_database()
            db.session.commit()

def test_index(client: FlaskClient):
    """Test the index route to ensure it returns the default furniture items."""
    rv = client.get('/')
    assert rv.status_code == 200
    assert b"Furniture Shop" in rv.data

def test_add_furniture(client: FlaskClient):
    """Test adding a new furniture item."""
    new_furniture = {
        'name': 'Bookshelf',
        'description': 'Wooden bookshelf with 5 shelves',
        'price': 199
    }
    rv = client.post('/add', data=new_furniture, follow_redirects=True)
    assert rv.status_code == 200
    assert b"Bookshelf" in rv.data

def test_update_furniture(client: FlaskClient):
    """Test updating an existing furniture item."""
    furniture = Furniture(name='Desk', description='Office desk with drawers', price=299)
    db.session.add(furniture)
    db.session.commit()

    updated_furniture = {
        'name': 'Office Desk',
        'description': 'Updated office desk with drawers',
        'price': 349
    }
    rv = client.post(f'/update/{furniture.id}', data=updated_furniture, follow_redirects=True)
    assert rv.status_code == 200
    assert b"Office Desk" in rv.data

def test_delete_furniture(client: FlaskClient):
    """Test deleting an existing furniture item."""
    furniture = Furniture(name='Lamp', description='Desk lamp with adjustable arm', price=49)
    db.session.add(furniture)
    db.session.commit()

    rv = client.get(f'/delete/{furniture.id}', follow_redirects=True)
    assert rv.status_code == 200
    assert b"Lamp" not in rv.data

if __name__ == '__main__':
    pytest.main()
