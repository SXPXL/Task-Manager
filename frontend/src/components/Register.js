/**
 * Register Component
 * ------------------
 * Handles user registration by collecting username, email, and password.
 * Submits the form data to backend API to create a new user.
 * Displays error messages on failure and navigates to login page on success.
 *
 * State:
 * - formdata: Holds username, email, and password input values
 * - error: Error message to display on registration failure
 *
 * Functions:
 * - handleChange: Updates formdata when input fields change
 * - handleSubmit: Submits registration form, sends POST request, and handles response
 *
 * Usage:
 * Used as the registration page for the application.
 */

import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./styles/Register.css"; // Import external CSS
import { Link } from "react-router-dom";
import BASE_URL from "../config";

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
    /**
     * Updates formdata state when an input field changes.
     * @param {object} e - The input change event
     */
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  // Handle form submit
  const handleSubmit = async (e) => {
    /**
     * Handles registration form submission.
     * Sends POST request to backend, clears form, and navigates on success.
     * @param {object} e - The form submit event
     */
    e.preventDefault(); // prevent page reload
    setError(""); // clear previous error

    try {
      await axios.post(`${BASE_URL}/auth/register`, formdata);
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
        <p>Already registered? <Link to="/login">Click here to login</Link></p> 
      </form>
    </div>
    </div>
  );
}

export default Register;
