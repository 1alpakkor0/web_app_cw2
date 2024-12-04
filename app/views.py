from app import app, db
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required, LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, Category, Product, CartItem
from app.forms import ChangePasswordForm, LoginForm, SignupForm, DeleteAccountForm
from sqlalchemy import or_


@app.context_processor ## This function is used for injecting the categories into the all templates
def inject_categories():
    categories = Category.query.all()
    cart_count = 0
    if current_user.is_authenticated:
        cart_count = CartItem.query.filter_by(user_id=current_user.id).count()
    return dict(categories=categories)





@app.route('/') ## This is the home page
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST']) ## This is the login page
def login():
    form = LoginForm() ## This is the login form which is imported from forms.py
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password): ## This is the login authentication
            login_user(user)
            flash('You have successfully logged in.')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Please check your email and password.')
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST']) ## This is the signup page where users can create an account
def signup():
    form = SignupForm() ## This is the signup form which is imported from forms.py
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256') ## This is the password hashing
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully.')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)
   


@app.route('/profile') ## This is the profile page
@login_required
def profile():
    return render_template('profile.html', user=current_user)
    ## return ('Profile Page')


@app.route('/cart') ## This is the cart page
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all() ## This is for getting all the items in the cart
    return render_template('cart.html', cart_items=cart_items)



@app.route('/add_to_cart', methods=['POST']) ## This is for adding items to the cart
@login_required
def add_to_cart():
    product_id = request.get_json().get('product_id')
    product = Product.query.get_or_404(product_id)
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product.id).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(user_id=current_user.id, product_id=product.id, quantity=1) 
        db.session.add(cart_item)
    db.session.commit()
    cart_count = CartItem.query.filter_by(user_id=current_user.id).count()
    return jsonify({'status': 'added', 'cart_count': cart_count}) ## This is for updating the cart count in the frontend



@app.route('/remove_from_cart', methods=['POST']) ## This is for removing items from the cart
@login_required
def remove_from_cart():
    item_id = request.get_json().get('item_id') 
    cart_item = CartItem.query.filter_by(id=item_id, user_id=current_user.id).first()
    if cart_item:
        db.session.delete(cart_item) 
        db.session.commit()
        cart_count = CartItem.query.filter_by(user_id=current_user.id).count()

        ## This is for calculating the total amount of the cart after removing an item
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        total_amount = sum([item.product.price * item.quantity for item in cart_items])
        return jsonify({'status': 'removed', 'cart_count': cart_count, 'total_amount': total_amount}) ## This is for updating the cart count and total amount
    else:
        return jsonify({'status': 'error'}), 404



@app.route('/search') ## This is the search page
def search():
    search_query = request.args.get('search_query', '') 
    if search_query:
        products = Product.query.filter(or_(Product.name.ilike(f'%{search_query}%'), Product.description.ilike(f'%{search_query}%'))).all() ## This is for searching the products with its name and description
    else:
        products = []
    return render_template('search.html', products=products, search_query=search_query)
    ## return ('Search Page')


@app.route('/logout') ## This is for logging out
@login_required
def logout():
    logout_user()
    flash('You have successfully logged out.')
    return redirect(url_for('home'))


@app.route('/change_password', methods=['GET', 'POST']) ## This is for changing the password
@login_required
def change_password():
    form = ChangePasswordForm() ## This is the change password form which is imported from forms.py
    if form.validate_on_submit():
        current_password = form.current_password.data
        new_password = form.new_password.data
        confirm_password = form.confirm_password.data

        if not check_password_hash(current_user.password, current_password): ## This is for checking the current password
            flash('Current password is incorrect. Please try again.')
            return redirect(url_for('change_password'))
        if new_password != confirm_password: ## This is for checking the new password and confirm password
            flash('Passwords do not match. Please try again.')
            return redirect(url_for('change_password'))
        
        current_user.password = generate_password_hash(new_password)
        db.session.commit()
        flash('Password successfully changed.')
        return redirect(url_for('profile'))
 
    return render_template('change_password.html', form=form)


@app.route('/delete_account', methods=['GET', 'POST']) ## This is for deleting the account
@login_required
def delete_account():
    form = DeleteAccountForm() ## This is the delete account form which is imported from forms.py
    if request.method == 'POST':
        if form.validate_on_submit():
            db.session.delete(current_user)
            db.session.commit()
            logout_user()
            flash('Account successfully deleted.')
            return redirect(url_for('home'))
        else:
            flash('Incorrect email or password. Please try again.')
            return redirect(url_for('delete_account'))
    ## return render_template('delete_account.html')
    return render_template('delete_account.html', form=form)




@app.route('/category/<int:category_id>') ## This is for viewing the products in a category with its id
def category_view(category_id):
    category = Category.query.get_or_404(category_id)
    products = Product.query.filter_by(category_id=category.id).all()
    return render_template('category.html', category=category, products=products)


@app.route('/like_product', methods=['POST']) ## This is for liking the product
@login_required
def like_product():
    product_id = request.get_json().get('product_id') ## This is for getting the product id from the script
    product = Product.query.get_or_404(product_id)
    if product in current_user.favorites:
        current_user.favorites.remove(product)
        db.session.commit()
        return jsonify({'status': 'unliked'})
    else:
        current_user.favorites.append(product)
        db.session.commit()
        return jsonify({'status': 'liked'})
    

@app.route('/wishlist') ## This is the wishlist page
@login_required
def wishlist():
    favorites = current_user.favorites
    return render_template('wishlist.html', favorites=favorites)


