import pytest
from flask import Flask
from flask.testing import FlaskClient
from pymongo import MongoClient
from bson.objectid import ObjectId
from app import app, initialize_database, collection  # Importing the app and initialize_database function

# Fixture to create a test client and set up the initial database state
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            # Set up the database with default data before each test
            initialize_database()
        yield client

# Fixture to track and remove added or updated items after each test
@pytest.fixture
def track_changes():
    added_ids = []
    updated_ids = []
    yield added_ids, updated_ids

    # Remove added items
    for item_id in added_ids:
        collection.delete_one({"_id": ObjectId(item_id)})
    
    # Optionally, restore original state of updated items (not shown here for simplicity)
    # You would need to track the original state and update the items back to that state

def test_index(client: FlaskClient):
    """Test the index route to ensure it returns the default furniture items."""
    rv = client.get('/')
    assert rv.status_code == 200
    assert b"Furniture Shop" in rv.data

def test_add_furniture(client: FlaskClient, track_changes):
    """Test adding a new furniture item."""
    new_furniture = {
        'name': 'Bookshelf',
        'description': 'Wooden bookshelf with 5 shelves',
        'price': '199'
    }
    rv = client.post('/add', data=new_furniture, follow_redirects=True)
    assert rv.status_code == 200
    assert b"Bookshelf" in rv.data

    # Track added furniture ID
    added_furniture = collection.find_one({'name': 'Bookshelf'})
    track_changes[0].append(added_furniture['_id'])

def test_update_furniture(client: FlaskClient, track_changes):
    """Test updating an existing furniture item."""
    # Insert a test furniture item
    furniture_id = collection.insert_one({
        'name': 'Desk',
        'description': 'Office desk with drawers',
        'price': '299'
    }).inserted_id

    # Track added furniture ID
    track_changes[0].append(furniture_id)

    updated_furniture = {
        'name': 'Office Desk',
        'description': 'Updated office desk with drawers',
        'price': '349'
    }
    rv = client.post(f'/update/{furniture_id}', data=updated_furniture, follow_redirects=True)
    assert rv.status_code == 200
    assert b"Office Desk" in rv.data

    # Track updated furniture ID
    track_changes[1].append(furniture_id)

def test_delete_furniture(client: FlaskClient, track_changes):
    """Test deleting an existing furniture item."""
    # Insert a test furniture item
    furniture_id = collection.insert_one({
        'name': 'Lamp',
        'description': 'Desk lamp with adjustable arm',
        'price': '49'
    }).inserted_id

    # Track added furniture ID
    track_changes[0].append(furniture_id)

    rv = client.get(f'/delete/{furniture_id}', follow_redirects=True)
    assert rv.status_code == 200
    assert b"Lamp" not in rv.data

if __name__ == '__main__':
    pytest.main()
