from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# Initialize the MongoDB client and specify the database and collection
client = MongoClient('mongodb://root:your-root-password@mongo-mongodb:27017/')
db = client.furnituredb
collection = db.furnitures

def initialize_database():
    # Default furniture items
    default_furnitures = [
        {"name": "Sofa", "description": "Comfortable leather sofa", "price": "499"},
        {"name": "Dining Table", "description": "Wooden dining table for six", "price": "299"},
        {"name": "Chair", "description": "Ergonomic office chair", "price": "89"},
        {"name": "Bed", "description": "King size bed with storage", "price": "799"},
        {"name": "Coffee Table", "description": "Glass top coffee table", "price": "149"}
    ]
    
    # Insert default items if the collection is empty
    if collection.count_documents({}) == 0:
        collection.insert_many(default_furnitures)
        print("Default furniture items added to the database.")

# Call the function to initialize the database
initialize_database()

# Route to view all furniture
@app.route('/')
def index():
    furnitures = list(collection.find())
    return render_template('index.html', furnitures=furnitures)

# Route to add new furniture
@app.route('/add', methods=['GET', 'POST'])
def add_furniture():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        furniture = {'name': name, 'description': description, 'price': price}
        collection.insert_one(furniture)
        return redirect(url_for('index'))
    return render_template('add_furniture.html')

# Route to update furniture
@app.route('/update/<id>', methods=['GET', 'POST'])
def update_furniture(id):
    furniture = collection.find_one({"_id": ObjectId(id)})
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        collection.update_one({"_id": ObjectId(id)}, {"$set": {'name': name, 'description': description, 'price': price}})
        return redirect(url_for('index'))
    return render_template('update_furniture.html', furniture=furniture)

# Route to delete furniture
@app.route('/delete/<id>')
def delete_furniture(id):
    collection.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
