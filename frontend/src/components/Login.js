import React, { useState } from "react";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";
import "./styles/Login.css"; 
import { useAuth } from "../context/AuthContext";
import GreenSpinner from "./Spinner";

function Login() {

  // State for input values
  const [formData, setFormData] = useState({
    email:"",
    password: "",
  });
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const { login } = useAuth();
  const [loading,setLoading] = useState(false);

  // Handles changes to input fields and update state accordingly
  const handleChange = (e) => {
    const {name,value } = e.target;
    setFormData((prev)=>({
      ...prev,
      [name]: value,
    }))
  };

  // Handle form submission
  const handlesubmit = async (e) => {
    e.preventDefault(); // To prevent default form submit refresh
    setLoading(true);
    try{

      // POST request to backend 
      const res =await axios.post("http://localhost:8000/auth/login", formData);
       setError("");

       // extract access token from response
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
        {/* Email input field */}
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleChange}
          required
        />

        {/* Password input field */}
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
        {/* Link to register page for new users */}
        <p style={{ marginTop: "10px", color: "blue" }}>New user? <Link to="/register">Register</Link></p>    
      </form>
    </div>
    </div>
    
  );
  }

  export default Login;