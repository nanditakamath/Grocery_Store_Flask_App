from flask import Flask, render_template,make_response, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, func 
import bcrypt
from datetime import datetime,date
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'


db = SQLAlchemy(app)
app.app_context().push()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    
class Manager(db.Model):
    __tablename__ = 'manager'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)

class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    unit = db.Column(db.String(50), nullable=False)
    rate = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    quantity_sold = db.Column(db.Integer, default=0)
    date = db.Column(db.DateTime, default=date.today())  
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)


class OrderHistory(db.Model):
    __tablename__ = 'order_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    quantity_sold = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # item = db.relationship('Item', backref=db.backref('order_history', lazy=True))

class Cart(db.Model):
    _tablename_ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    # product = db.relationship('Item', backref='cart_items')

db.create_all()

@app.after_request
def add_cache_headers(response):
    if request.path.startswith('/static/'):
        response.cache_control.no_cache = True
        response.cache_control.no_store = True
        response.cache_control.must_revalidate = True
        response.cache_control.max_age = 0
        response.cache_control.private = True
    return response
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        try:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            new_user = User(name=name, username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login'))
        except:
            integrity_error = True
    else:
        integrity_error = False

    return render_template('signup.html',integrity_error=integrity_error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with app.app_context():
            user = User.query.filter_by(username=username).first()

            if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
                session['user_id'] = user.id
                session['username'] = user.username
                session['logged_in'] = True
                return redirect(url_for('products_page',uname=user.username))
            else:
                return render_template('login.html',invalid_credentials=True)

    return render_template('login.html')

@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with app.app_context():
            admin = Manager.query.filter_by(username=username).first()

            if admin and bcrypt.checkpw(password.encode('utf-8'), admin.password):
                session['user_id'] = admin.id
                session['username'] = admin.username
                session['logged_in'] = True
                return redirect(url_for('admindash', uname=admin.username))
            
            else:
                return 'Incorrect username or password'
            
    return render_template('adminlogin.html')

@app.route('/adminDashboard/<uname>', methods=['GET', 'POST'])
def admindash(uname):
    try:
        if session['logged_in'] == True:
            Categorydata = db.session.query(Category).all()
            Itemdata = db.session.query(Item).all()
            category_error = request.args.get('category_error')
            if request.method == 'POST':
                if "newItem" in request.form:
                    itemname = request.form['itemname']
                    unit = request.form['unit']
                    rate = request.form['rate']
                    quantity = request.form['quantity']
                    #mfgdate = request.form['date']
                    mfgdate = datetime.strptime(request.form['date'], '%Y-%m-%d')
                    selected_category_id = request.form['category_id']
                    new_item = Item(
                    name=itemname,
                    unit=unit,
                    rate=rate,
                    quantity=quantity,
                    date=mfgdate,
                    category_id=selected_category_id  
                    )
                    db.session.add(new_item)
                    db.session.commit()
                    return redirect(url_for('admindash', uname=uname))
                
                elif "newCategory" in request.form:
                    new_category_name = request.form['category']
                    existing_category = Category.query.filter(Category.name == new_category_name).first()
                    if existing_category:
                        category_error = 'Category already exists'
                    else:
                        new_category = Category(name=new_category_name)
                        db.session.add(new_category)
                        db.session.commit()
                        return redirect(url_for('admindash', uname=uname))
                    
            return render_template('adminDashboard.html', data1=Categorydata, data2=Itemdata, category_error=category_error, uname=uname)
    except Exception as e:
        return str(e)


@app.route('/edit_category/<uname>', methods=['POST'])
def edit_category(uname):
    if request.method == 'POST':
        category_id = request.form.get('category_id')
        new_category_name = request.form.get('edit_category_name')
        
        if category_id is not None and new_category_name is not None:
            try:
                category = Category.query.get(category_id)
                if category:
                    existing_category = Category.query.filter(Category.name == new_category_name).first()
                    if existing_category and existing_category.id != category_id:
                        error_message = 'Category already exists'
                        return redirect(url_for('admindash',uname=uname, category_error=error_message))
                    
                    print(f"Editing category: {category.name} -> {new_category_name}")
                    category.name = new_category_name
                    db.session.commit()
                    return redirect(url_for('admindash',uname=uname))
                else:
                    return jsonify({'success': False, 'message': 'Category not found'}), 404
            except Exception as e:
                return jsonify({'success': False, 'message': str(e)}), 500
        
    return jsonify({'success': False})

@app.route('/edit_item/<uname>', methods=['POST'])
def edit_item(uname):
    if request.method == 'POST':
        item_id = request.form.get('item_id')
        new_item_name = request.form.get('editItemName')
        new_item_rate = request.form.get('rate')
        new_item_unit = request.form.get('unit')
        new_item_quantity = request.form.get('quantity')
        new_item_mfgdate = datetime.strptime(request.form.get('date'), '%Y-%m-%d')
        if item_id is not None and new_item_name is not None:
            try:
                item = Item.query.get(item_id)
                if item:

                    item.name = new_item_name
                    item.rate = new_item_rate
                    item.unit = new_item_unit
                    item.quantity = new_item_quantity
                    item.date = new_item_mfgdate
                    db.session.commit()
                    return redirect(url_for('admindash',uname=uname))
                else:
                    return jsonify({'success': False, 'message': 'Item not found'}), 404
            except Exception as e:
                return jsonify({'success': False, 'message': str(e)}), 500
        
    return jsonify({'success': False})

@app.route('/delete_category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    try:
        category = Category.query.get(category_id)
        if category:
            Item.query.filter_by(category_id=category_id).delete()
            db.session.delete(category)
            db.session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Category not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 200

@app.route('/delete_item/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        item = Item.query.get(item_id)
        if item:
            Item.query.filter_by(id=item_id).delete()
            db.session.delete(item)
            db.session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Category not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 200

@app.route('/products/<uname>')
def products_page(uname):
    try:
        if session['logged_in'] == True:
            categories = Category.query.all()
            items = Item.query.order_by(desc(Item.id)).all()
            return render_template('userDashboard.html', categories=categories, products=items, uname=uname)
    except Exception as e:
        return str(e)

@app.route('/buy_product/<string:uname>/<int:product_id>/<int:quantity>', methods=['POST'])
def buy_product(uname,product_id, quantity):
    try:
        user = User.query.filter_by(username=uname).first()
        product = Item.query.get(product_id)
        if product:
            if product.quantity >= quantity:
                product.quantity -= quantity
                product.quantity_sold += quantity
                db.session.commit()
                
                new_order = OrderHistory(user_id=user.id,item_id=product_id, quantity_sold=quantity, order_date=datetime.utcnow())

                db.session.add(new_order)
                db.session.commit()
                return jsonify({'success': True})
            else:
                return jsonify({'success': False, 'message': 'Not enough quantity available'}), 400
        else:
            return jsonify({'success': False, 'message': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/summary')
def summary():
    categories_count = db.session.query(func.count(Category.id)).scalar()
    if categories_count == 0:
        category_empty = 'Data is empty'
    else:
        category_empty = None
    item_count = db.session.query(func.count(Item.id)).scalar()
    if item_count == 0:
        item_empty = 'Data is empty'
    else:
        item_empty = None
    items_data1 = db.session.query(Item.name, Item.quantity_sold).order_by(desc(Item.id)).limit(5).all()
    items_data2 = db.session.query(Category.name, Item.quantity_sold).join(Item).order_by(desc(Item.quantity_sold)).limit(5).all()
    product_sold = [[item_name, quantity] for item_name, quantity in items_data1]
    category_sold = [[category_name, quantity] for category_name, quantity in items_data2]
    return render_template('summary.html', data1=product_sold, data2=category_sold, category_empty=category_empty, item_empty=item_empty,uname=session['username'])

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/login')

@app.route('/add_to_cart/<string:uname>/<int:product_id>/<int:quantity>', methods=['POST'])
def add_to_cart(uname, product_id, quantity):
    try:
        # Get user_id based on uname
        user = User.query.filter_by(username=uname).first()
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        user_id = user.id

        product = Item.query.get(product_id)
        if product:
            if product.quantity >= quantity:
                # Check if the item already exists in the cart
                cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()

                if cart_item:
                    cart_item.quantity += quantity
                else:
                    cart_item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)

                db.session.add(cart_item)
                db.session.commit()
                return jsonify({'success': True})
            else:
                return jsonify({'success': False, 'message': 'Not enough quantity available'}), 400
        else:
            return jsonify({'success': False, 'message': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    
@app.route('/view_cart/<string:uname>', methods=['GET'])
def view_cart(uname):
    try:
        user = User.query.filter_by(username=uname).first()
        if user:
            cart_items = Cart.query.filter_by(user_id=user.id).all()

            cart_data = []
            total_amount = 0

            for cart_item in cart_items:
                product = Item.query.get(cart_item.product_id)
                if product:
                    cart_data.append({
                        'id': cart_item.id,
                        'item_name': product.name,
                        'product_id': product.id,
                        'quantity': cart_item.quantity,
                        'cost': product.rate * cart_item.quantity
                    })
                    total_amount += product.rate * cart_item.quantity

            return render_template('view_cart.html', uname=uname, cart_items=cart_data, total_amount=total_amount)
        else:
            return redirect(url_for('login')), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/checkout/<string:uname>', methods=['POST'])
def checkout(uname):
    try:
        user = User.query.filter_by(username=uname).first()
        if user:
            cart_items = request.json  # Assuming the data sent is in JSON format

            cart_data = []
            for cart_item in cart_items:
                product_id = int(cart_item['productId'])
                quantity = int(cart_item['quantity'])
                print('product_id = '+str(product_id))
                print('quantity = '+str(quantity))

                product = Item.query.get(product_id)
                if product and product.quantity >= quantity:
                    product.quantity -= quantity
                    product.quantity_sold += quantity

                    new_order = OrderHistory(user_id=user.id, item_id=product_id, quantity_sold=quantity, order_date=datetime.utcnow())
                    db.session.add(new_order)
                else:
                    db.session.rollback()
                    return jsonify({'success': False, 'message': 'Not enough quantity available'}), 400
            cart_items = Cart.query.filter_by(user_id=user.id).all()
            for cart_item in cart_items:
                cart_data.append(cart_item) 
            for cart_item in cart_data:
                db.session.delete(cart_item)
            db.session.commit()
            return jsonify({'success': True, 'goto': url_for('products_page', uname=user.username)})
        else:
            return jsonify({'success': False, 'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/remove_cart_item/<string:uname>/<int:item_id>', methods=['POST'])
def remove_cart_item(uname, item_id):
    try:
        user = User.query.filter_by(username=uname).first()
        if user:
            cart_item = Cart.query.filter_by(user_id=user.id, product_id=item_id).first()
            if cart_item:
                db.session.delete(cart_item)
                db.session.commit()
                return jsonify({'success': True})
            else:
                return jsonify({'success': False, 'message': 'Cart item not found'}), 404
        else:
            return jsonify({'success': False, 'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


def create_manager(username, password):
    existing_manager = Manager.query.filter_by(username=username).first()
    
    if existing_manager:
        return  # Return early if manager already exists
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_manager = Manager(username=username, password=hashed_password)
    db.session.add(new_manager)
    db.session.commit()


if __name__ == '__main__':
    create_manager('admin', 'admin123')
    app.run(host='0.0.0.0',debug=True)
