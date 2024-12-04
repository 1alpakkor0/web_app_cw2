from app import db, app
from app.models import Product, Category

with app.app_context():
    # List of categories representing the different types of products
    categories = [
        'Electronics',
        'Books',
        'Home and Garden',
        'Fashion',
        'Toys',
        'Beauty',
        'Sports and Outdoors',
        'Food and Drinks'
    ]

    # Create categories if they don't already exist
    for name in categories:
        category = Category.query.filter_by(name=name).first()
        if not category:
            category = Category(name=name)
            db.session.add(category)
    db.session.commit()

    # Hardcoded product data for each category
    products_by_category = {
        'Electronics': [
            {
                'name': 'Smartphone',
                'price': 1000,
                'description': 'A modern smartphone with the latest features.',
                'quantity': 10,
                'image': 'smartphone.jpg',
            },
            {
                'name': 'Laptop',
                'price': 1500,
                'description': 'A powerful laptop for professionals.',
                'quantity': 5,
                'image': 'laptop.jpg',
            },
            {
                'name': 'Wireless Earbuds',
                'price': 200,
                'description': 'Noise-cancelling wireless earbuds.',
                'quantity': 15,
                'image': 'earbuds.jpg',
            },
            
        ],
        'Books': [
            {
                'name': 'The Great Gatsby',
                'price': 15,
                'description': 'A classic novel by F. Scott Fitzgerald.',
                'quantity': 20,
                'image': 'great_gatsby.jpg',
            },
            {
                'name': '1984',
                'price': 12,
                'description': 'Dystopian novel by George Orwell.',
                'quantity': 18,
                'image': '1984.jpg',
            },
            
        ],
        'Home and Garden': [
            {
                'name': 'Garden Hose',
                'price': 25,
                'description': 'Durable garden hose 50ft.',
                'quantity': 30,
                'image': 'garden_hose.jpg',
            },
            {
                'name': 'LED Light Bulbs',
                'price': 10,
                'description': 'Energy-saving LED bulbs (pack of 4).',
                'quantity': 50,
                'image': 'led_bulbs.jpg',
            },
            
        ],
        
        'Fashion': [
            {
                'name': 'Men\'s T-Shirt',
                'price': 20,
                'description': '100% cotton t-shirt.',
                'quantity': 40,
                'image': 'mens_tshirt.jpg',
            },
            {
                'name': 'Women\'s Jeans',
                'price': 40,
                'description': 'Stylish denim jeans.',
                'quantity': 25,
                'image': 'womens_jeans.jpg',
            },
        ],
        'Toys': [
            {
                'name': 'Building Blocks Set',
                'price': 30,
                'description': '100-piece building blocks for kids.',
                'quantity': 35,
                'image': 'building_blocks.jpg',
            },
            {
                'name': 'RC Car',
                'price': 50,
                'description': 'Remote control racing car.',
                'quantity': 15,
                'image': 'rc_car.jpg',
            },
        ],
        'Beauty': [
            {
                'name': 'Lipstick',
                'price': 15,
                'description': 'Long-lasting matte lipstick.',
                'quantity': 60,
                'image': 'lipstick.jpg',
            },
            {
                'name': 'Moisturizer Cream',
                'price': 25,
                'description': 'Hydrating face cream.',
                'quantity': 40,
                'image': 'moisturizer.jpg',
            },
        ],
        'Sports and Outdoors': [
            {
                'name': 'Yoga Mat',
                'price': 35,
                'description': 'Non-slip yoga mat.',
                'quantity': 20,
                'image': 'yoga_mat.jpg',
            },
            {
                'name': 'Camping Tent',
                'price': 120,
                'description': '4-person camping tent.',
                'quantity': 10,
                'image': 'camping_tent.jpg',
            },
        ],
        'Food and Drinks': [
            {
                'name': 'Organic Coffee Beans',
                'price': 18,
                'description': 'Freshly roasted organic coffee.',
                'quantity': 25,
                'image': 'coffee_beans.jpg',
            },
            {
                'name': 'Gourmet Chocolate Box',
                'price': 22,
                'description': 'Assorted gourmet chocolates.',
                'quantity': 30,
                'image': 'chocolate_box.jpg',
            },
        ],
    }

    # Loop through the categories and add products
    for category_name, products in products_by_category.items():
        category = Category.query.filter_by(name=category_name).first()
        if category:
            for product_data in products:
                # Check if the product already exists
                existing_product = Product.query.filter_by(
                    name=product_data['name'],
                    category_id=category.id
                ).first()
                if not existing_product:
                    product = Product(
                        name=product_data['name'],
                        price=product_data['price'],
                        description=product_data['description'],
                        quantity=product_data['quantity'],
                        image=product_data['image'],
                        category=category
                    )
                    db.session.add(product)
    db.session.commit()



















    # product = Product(name='Smartphone', price=1000, description='A modern smartphone with latest features.', quantity=10, image='smartphone.jpg', category=electronics)
    # db.session.add(product)
    # db.session.commit()


    # electronics = Category.query.filter_by(name='Electronics').first()
    # product = Product(name='Laptop', price=1500, description='A modern laptop with latest features.', quantity=10, image='laptop.jpg', category=electronics)
    # db.session.add(product)
    # db.session.commit()