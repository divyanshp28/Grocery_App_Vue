**Architecture & Features**

The backend has been made using Flask framework in a virtual environment *“venv”*. Api requests like get, post, put and delete has 
been written in restful manner. Route protection has been done using Json web token (JWT). Api for every endpoint is in a separate 
file in “src” folder. Frontend has been made using vue3 with CSS library Bootstrap for components and responsiveness and Font 
Awesome for icons. For frontend some reusable components are in components folder and views are views folder.

**Command to run backend server :** *python main.py (flask app)*
                                    *redis-server (redis server)*
                                    *celery -A src.celery_workers.celery worker --loglevel=info (Celery worker)*
                                    *celery -A src.celery_workers.celery beat --loglevel=info (Celery beat)*
**Command to run frontend :** *npm run dev* (Development server)

**Features Implemented**

**USER**
User can buy, search for products, filter products according to categories, see order history, get daily activity mail and monthly report 
mail.

**ADMIN**
Admin can perform CRUD on categories and view products in inventory and approve/reject requests from users to be store admin 
and requests from store admin to manage categories.

**STORE ADMIN**
Store admin can perform CRUD on products and request admin to manage categories.
