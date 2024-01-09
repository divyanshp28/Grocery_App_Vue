from src import app, db, models, celery_workers, celery, celery_config
from src.models import User, Cart, CartItem, Category, Product, Order, Request, create_admin

if __name__ == '__main__':
    # with app.app_context():
    #     print("Inside the application context")
    #     db.create_all()
    #     create_admin()
    #     print("Database tables created successfully")

    app.run(debug = True, host = '0.0.0.0')