/**
 * Login Component
 * ---------------
 * Handles user login by collecting email and password, submitting to backend, and managing authentication state.
 *
 * State:
 * - formData: Holds email and password input values
 * - error: Error message to display on login failure
 * - loading: Whether the login request is in progress
 *
 * Functions:
 * - handleChange: Updates formData when input fields change
 * - handlesubmit: Submits login form, handles authentication, and redirects on success
 *
 * Usage:
 * Used as the login page for the application.
 */

import React, { useState } from "react";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";
import "./styles/Login.css"; 
import { useAuth } from "../context/AuthContext";
import GreenSpinner from "./Spinner";
import BASE_URL from "../config";

// Function for user login
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
    /**
     * Updates formData state when an input field changes.
     * @param {object} e - The input change event
     */
    const {name,value } = e.target;
    setFormData((prev)=>({
      ...prev,
      [name]: value,
    }))
  };

  // Handle form submission
  const handlesubmit = async (e) => {
    /**
     * Handles login form submission.
     * Sends POST request to backend, updates auth state, and navigates on success.
     * @param {object} e - The form submit event
     */
    e.preventDefault(); // To prevent default form submit refresh
    setLoading(true);
    try{

      // POST request to backend 
      const res =await axios.post(`${BASE_URL}/auth/login`, formData);
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
        <p>New user? <Link to="/register">Register</Link></p>    
      </form>
    </div>
    </div>
    
  );
  }

  export default Login;