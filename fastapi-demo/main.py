from fastapi import Depends, FastAPI
from models import Product
from database import session,engine
import database_models
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return "Hi, Deepanker this side!"

products = [
    Product(id=1,name="Phone",description="Smartphone",price=99,quantity=10),
    Product(id=2,name="Laptop",description="Gaming Laptop",price=44,quantity=6),
    Product(id=3,name="Tablet",description="Tablet",price=299,quantity=5),
    Product(id=4,name="Watch",description="Smartwatch",price=199,quantity=8)
]


def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()


def init_db():
    db=session()

    count=db.query(database_models.Product).count()
    
    if count ==0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
    
        db.commit()

init_db()

@app.get("/products")
def get_all_products(db:Session=Depends(get_db)):

    db_products=db.query(database_models.Product).all()

    return db_products


@app.get("/products/{id}")
def get_product_by_id(id: int,db:Session=Depends(get_db)):
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        return db_product
    return {"error": "Product not found"}



@app.post("/products")
def add_product(product:Product,db:Session=Depends(get_db)):
   
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product


@app.put("/products/{id}")
def update_product(id:int,product:Product,db:Session=Depends(get_db)):
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        db_product.name=product.name
        db_product.description=product.description
        db_product.price=product.price
        db_product.quantity=product.quantity
        db.commit()
        return "Product Updated Successfully"
    else:
        return "No Product found"
        
    return {"error": "Product not found"}


@app.delete("/products/{id}")
def delete_product(id:int,db:Session=Depends(get_db)):
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product Deleted Successfully"
    else:
        return "No Product found"
    return {"error": "Product not found"}

