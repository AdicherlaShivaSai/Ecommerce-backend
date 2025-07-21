# 📦 Ecommerce Backend API (FastAPI + MongoDB)

This is a sample **Ecommerce Backend Application** built with **FastAPI** and **MongoDB**, simulating core features of platforms like Flipkart or Amazon.  
It supports product creation, listing, and order placement with inventory management.

---

## 🚀 Live Demo (Render Deployed)

> 🔗 [https://your-app-name.onrender.com/docs](https://your-app-name.onrender.com/docs)  
> Replace with your actual deployed link

---

## 🛠 Tech Stack

- ✅ **Backend**: FastAPI (Python 3.10+)
- ✅ **Database**: MongoDB Atlas (used via `motor`)
- ✅ **Deployment**: Render
- ✅ **API Documentation**: Swagger UI (`/docs`)

---

## 📚 Features

### 📦 Products API

#### ✅ Create Product  
`POST /products`  
```json
{
  "name": "T-shirt",
  "price": 299.0,
  "sizes": [
    {
      "size": "M",
      "quantity": 10
    }
  ]
}
```

#### ✅ List Products  
`GET /products?name=shirt&size=M&limit=10&offset=0`  
Returns paginated product list with filters.

---

### 🛒 Orders API

#### ✅ Create Order  
`POST /orders`  
```json
{
  "userId": "user_1",
  "items": [
    {
      "productId": "<product_id>",
      "qty": 2
    }
  ]
}
```
- Automatically reduces product quantity.

#### ✅ Get Orders for User  
`GET /orders/user_1?limit=10&offset=0`  
Returns user’s orders with product details and total amount.

---

## 🧪 How to Run Locally

### 📋 Prerequisites
- Python 3.10+
- MongoDB Atlas URI

### 🔧 Setup

```bash
git clone https://github.com/yourusername/ecommerce-backend.git
cd ecommerce-backend
pip install -r requirements.txt
```

Set your MongoDB URI in `db/mongodb.py` or via environment variable:
```bash
export MONGO_URL="mongodb+srv://<user>:<pass>@cluster.mongodb.net/ecommerce_db"
```

### ▶️ Run the App

```bash
python main.py
```

Visit:  
> `http://localhost:8000/docs`

---

## 🌍 Deployment (Render)

1. Push this repo to GitHub.
2. Go to [https://render.com](https://render.com)
3. Click “New Web Service” → Connect your repo
4. Set:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Environment Variable**:  
     `MONGO_URL = your_mongodb_uri`
5. Deploy and access `/docs` for Swagger UI

---

## 📁 Project Structure

```
backend/
├── main.py
├── requirements.txt
├── models/
│   ├── product.py
│   └── order.py
├── routes/
│   ├── product_routes.py
│   └── order_routes.py
├── db/
│   └── mongodb.py
```

---

## 🙋‍♂️ Author

**Shiva Adicherla**  
_This project was part of a backend assignment to demonstrate FastAPI knowledge with MongoDB integration._

---

## 📄 License

MIT – Feel free to use and adapt for educational or personal use.