from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Float, select
import httpx
import os

# Environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@db2:5432/api2_db")
API1_URL = os.getenv("API1_URL", "http://api1:8001/products")

# Create async engine & session
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

app = FastAPI()

# Define Product model
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)

# Create tables on startup
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def startup():
    await init_db()

# Dependency to get DB session
async def get_db():
    async with SessionLocal() as session:
        yield session

# Sync products from API1 to API2's database
@app.get("/sync-products")
async def sync_products(db: AsyncSession = Depends(get_db)):
    async with httpx.AsyncClient() as client:
        response = await client.get(API1_URL)
        if response.status_code != 200:
            return {"error": "Failed to fetch products"}

        products = response.json()

        # Insert fetched products into API2's database
        for product in products:
            existing_product = await db.execute(select(Product).where(Product.id == product["id"]))
            if existing_product.scalars().first() is None:  # Avoid duplicates
                new_product = Product(id=product["id"], name=product["name"], price=product["price"])
                db.add(new_product)

        await db.commit()
    return {"message": "Products synced successfully"}

# Fetch all products stored in API2's database
@app.get("/products")
async def get_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product))
    return result.scalars().all()