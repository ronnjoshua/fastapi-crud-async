# FastAPI Product API with PostgreSQL & Docker 🐳🚀

This is a simple FastAPI-based REST API for managing products. The API is backed by **PostgreSQL** and uses **SQLAlchemy** for database interactions. The project is containerized with **Docker** to ensure easy setup and deployment.

---

## 📌 Features
- 📝 **CRUD Operations** for products (Create, Read, Update, Delete)
- 🔄 **Asynchronous SQLAlchemy** integration
- 🌍 **CORS enabled** for frontend communication
- 🐳 **Docker Compose** support for easy deployment

## 🛠 Technologies Used
- **FastAPI** (Backend)
- **React (Vite)** (Frontend)
- **PostgreSQL** (Database)
- **Docker** (Containerization)

## 🚀 How to Run

### 1️⃣ Backend (FastAPI)
cd fastapi_env/api1  # or fastapi_env/api2

# Run with Docker
docker build -t api1 .  # For API1
docker run -p 8000:8000 api1

### 2️⃣ Frontend (React)
cd frontend/crud-dashboard

# Install dependencies
npm install

# Start development server
npm run dev

## 📌 API Endpoints (Example)
- GET /api/products → Get all products
- POST /api/products → Add a new product
- PUT /api/products/{id} → Update a product
- DELETE /api/products/{id} → Delete a product

## 📦 Running with Docker Compose
docker-compose up --build

## 📜 License
This project is for learning purposes.

