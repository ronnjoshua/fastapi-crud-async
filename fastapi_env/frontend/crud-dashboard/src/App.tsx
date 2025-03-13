import { useState, useEffect } from "react";
import axios from "axios";

const API1_URL = "http://localhost:8001/api/products";
console.log("Frontend is using API URL:", API1_URL);

type Product = {
  id: number;
  name: string;
  price: number;
};

export default function ProductDashboard() {
  const [products, setProducts] = useState<Product[]>([]);
  const [name, setName] = useState("");
  const [price, setPrice] = useState("");
  const [editingProduct, setEditingProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    setLoading(true);
    try {
      const response = await axios.get(API1_URL);
      setProducts(response.data);
      setError("");
    } catch (error) {
      console.error("Error fetching products", error);
      setError("Failed to load products.");
    } finally {
      setLoading(false);
    }
  };

  const addProduct = async () => {
    if (!name || !price) {
      setError("Product name and price are required.");
      return;
    }

    try {
      const response = await axios.post(`${API1_URL}`, {
        name,
        price: parseFloat(price),
      }, {
        headers: { "Content-Type": "application/json" }
      });

      setProducts([...products, response.data]);
      setName("");
      setPrice("");
      setError("");
    } catch (error) {
      console.error("Error adding product", error);
      setError("Failed to add product.");
    }
  };

  const deleteProduct = async (id: number) => {
    try {
      await axios.delete(`${API1_URL}/${id}`);
      setProducts(products.filter((p) => p.id !== id));
    } catch (error) {
      console.error("Error deleting product", error);
      setError("Failed to delete product.");
    }
  };

  const startEditing = (product: Product) => {
    setEditingProduct(product);
    setName(product.name);
    setPrice(product.price.toString());
  };

  const updateProduct = async () => {
    if (!editingProduct) return;
    if (!name || !price) {
      setError("Product name and price are required.");
      return;
    }

    try {
      await axios.put(`${API1_URL}/${editingProduct.id}`, { name, price: parseFloat(price) });
      setProducts(
        products.map((p) =>
          p.id === editingProduct.id ? { ...p, name, price: parseFloat(price) } : p
        )
      );
      setEditingProduct(null);
      setName("");
      setPrice("");
      setError("");
    } catch (error) {
      console.error("Error updating product", error);
      setError("Failed to update product.");
    }
  };

  return (
    <div style={{ maxWidth: "600px", margin: "auto", padding: "20px" }}>
      <h1>Product CRUD Dashboard</h1>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <div style={{ marginBottom: "20px" }}>
        <input
          type="text"
          placeholder="Product Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          style={{ marginRight: "10px", padding: "5px" }}
        />
        <input
          type="number"
          placeholder="Price"
          value={price}
          onChange={(e) => setPrice(e.target.value)}
          style={{ marginRight: "10px", padding: "5px" }}
        />
        {editingProduct ? (
          <button onClick={updateProduct} style={{ padding: "5px 10px", backgroundColor: "orange" }}>
            Update Product
          </button>
        ) : (
          <button onClick={addProduct} style={{ padding: "5px 10px" }}>Add Product</button>
        )}
      </div>

      <button onClick={fetchProducts} style={{ marginBottom: "10px", padding: "5px 10px", backgroundColor: "blue", color: "white" }}>
        Show All Products
      </button>

      {loading && <p>Loading products...</p>}

      <ul>
        {products.map((product) => (
          <li key={product.id} style={{ marginBottom: "10px" }}>
            {product.name} - ${product.price.toFixed(2)}
            <button onClick={() => startEditing(product)} style={{ marginLeft: "10px", color: "blue" }}>
              ✏️ Edit
            </button>
            <button onClick={() => deleteProduct(product.id)} style={{ marginLeft: "10px", color: "red" }}>
              ❌ Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
