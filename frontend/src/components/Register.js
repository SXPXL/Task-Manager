import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./styles/Register.css"; // Import external CSS
import { Link } from "react-router-dom";

/**
 * Register Component
 * ------------------
 * Handles user registration by collecting username, email, and password.
 * Submits the form data to backend API to create a new user.
 * Displays error messages on failure and navigates to login page on success.
 */
function Register() {
  // State to hold form input values
  const [formdata, setFormData] = useState({
    username: "",
    email: "",
    password: "",
  });

  const navigate = useNavigate(); 

  // Error message state
  const [error, setError] = useState("");

  // Handle input field changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  // Handle form submit
  const handleSubmit = async (e) => {
    e.preventDefault(); // prevent page reload
    setError(""); // clear previous error

    try {
      const res = await axios.post("http://localhost:8000/auth/register", formdata);
      alert('Registration Successfull')

      // Clear form after successful registration
      setFormData({
        username: "",
        email: "",
        password: "",
      });
      navigate("/login");
    } catch (err) {
      setError(err.response?.data?.detail || "Something went wrong");
    }
  };

  return (
    <div className="wholepage">
    <div className="register-container">
      <h2>Register</h2>
      {/* Register form */}
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="username"
          placeholder="Username"
          value={formdata.username}
          onChange={handleChange}
        />
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={formdata.email}
          onChange={handleChange}
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formdata.password}
          onChange={handleChange}
        />

        {/* Show error message */}
        {error && <div className="error">{error}</div>}

        <button type="submit">Register</button>

        {/* Link to Login if already registered */}
        <p> <Link to="/login">Already registered? Click here to login</Link></p> 
      </form>
    </div>
    </div>
  );
}

export default Register;
