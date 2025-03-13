from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Float, select, update, delete
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
import os
from pydantic import BaseModel

# Database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@db1:5432/api1_db")

# Create async engine and session
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# Pydantic model for creating a product
class ProductCreate(BaseModel):
    name: str
    price: float

# Pydantic model for updating a product
class ProductUpdate(BaseModel):
    name: str
    price: float
    
# Define Product model
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)

# Initialize DB and insert dummy data
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def seed_data():
    async with SessionLocal() as session:
        result = await session.execute(select(Product))
        products = result.scalars().all()
        if not products:
            sample_products = [
                Product(name="Laptop", price=1200.99),
                Product(name="Mouse", price=25.50),
                Product(name="Keyboard", price=45.99),
                Product(name="Monitor", price=300.00)
            ]
            session.add_all(sample_products)
            await session.commit()
            print("✅ Dummy products inserted!")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔄 Starting API...")
    await init_db()
    await seed_data()
    yield
    print("🛑 Shutting down API...")

app = FastAPI(lifespan=lifespan)



# Apply CORS middleware after defining the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Only allow your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
async def get_db():
    async with SessionLocal() as session:
        yield session

### 🔹 CRUD Endpoints
@app.get("/api/products")
async def get_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product))
    return result.scalars().all()

@app.get("/api/products/{product_id}")
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/api/products", status_code=201)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    new_product = Product(name=product.name, price=product.price)
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product

@app.put("/api/products/{product_id}")
async def update_product(product_id: int, product: ProductUpdate, db: AsyncSession = Depends(get_db)):
    existing_product = await db.get(Product, product_id)
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")

    existing_product.name = product.name
    existing_product.price = product.price

    await db.commit()
    await db.refresh(existing_product)
    return existing_product

@app.delete("/api/products/{product_id}", status_code=204)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    await db.delete(product)
    await db.commit()
    return {"message": "Product deleted successfully"}