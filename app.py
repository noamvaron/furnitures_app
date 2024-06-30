from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ZtGMMCF67D@my-postgresql:5432/furnituredb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Furniture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Integer, nullable=False)

def initialize_database():
    db.create_all()
    default_furnitures = [
        {"name": "Sofa", "description": "Comfortable leather sofa", "price": 499},
        {"name": "Dining Table", "description": "Wooden dining table for six", "price": 299},
        {"name": "Chair", "description": "Ergonomic office chair", "price": 89},
        {"name": "Bed", "description": "King size bed with storage", "price": 799},
        {"name": "Coffee Table", "description": "Glass top coffee table", "price": 149}
    ]
    if Furniture.query.count() == 0:
        for item in default_furnitures:
            db.session.add(Furniture(**item))
        db.session.commit()

initialize_database()

@app.route('/')
def index():
    furnitures = Furniture.query.all()
    return render_template('index.html', furnitures=furnitures)

@app.route('/add', methods=['GET', 'POST'])
def add_furniture():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        furniture = Furniture(name=name, description=description, price=price)
        db.session.add(furniture)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_furniture.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_furniture(id):
    furniture = Furniture.query.get_or_404(id)
    if request.method == 'POST':
        furniture.name = request.form['name']
        furniture.description = request.form['description']
        furniture.price = request.form['price']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update_furniture.html', furniture=furniture)

@app.route('/delete/<int:id>')
def delete_furniture(id):
    furniture = Furniture.query.get_or_404(id)
    db.session.delete(furniture)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)
