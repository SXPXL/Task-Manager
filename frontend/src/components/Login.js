import React, { useState } from "react";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";
import "./styles/Login.css"; 
import { useAuth } from "../context/AuthContext";
import GreenSpinner from "./Spinner";

function Login() {
  const [formData, setFormData] = useState({
    email:"",
    password: "",
  });
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const { login } = useAuth();
  const [loading,setLoading] = useState(false);

  const handleChange = (e) => {
    const {name,value } = e.target;
    setFormData((prev)=>({
      ...prev,
      [name]: value,
    }))
  };

  const handlesubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try{
      const res =await axios.post("http://localhost:8000/auth/login", formData);
       setError("");
       const token = res.data.access_token;
       login(token);
       navigate("/dashboard");

    } catch(err) {
      setError(err.response?.data?.detail || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };
  
  if (loading) return <GreenSpinner/>;


  return (
    <div className="wholepage">
    <div className="login-container">
      <h2>Login</h2>
      <form onSubmit={handlesubmit}>
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleChange}
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          required
        />
        {error && <p className="error">{error}</p>}
        <button type="submit">Login</button>
        <p style={{ marginTop: "10px", color: "blue" }}>New user? <Link to="/register">Register</Link></p>    
      </form>
    </div>
    </div>
    
  );
  }

  export default Login;