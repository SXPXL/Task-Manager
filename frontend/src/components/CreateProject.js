import React, { useState } from "react";
import axios from "axios";
import { useAuth } from "../context/AuthContext";
import "./styles/CreateProject.css";

function CreateProject({ onClose, onProjectCreated }) {
  const { token } = useAuth();

  const [formData, setFormData] = useState({
    title: "",
    description: "",
    due_date: "", // Include due_date in state
  });

  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post(
        "http://localhost:8000/project/create-projects",
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setMessage(`Project "${res.data.title}" created successfully!`);
      setFormData({
        title: "",
        description: "",
       
      });
      if (onProjectCreated) {
        onProjectCreated(res.data);
      }
    } catch (err) {
      setMessage(err.response?.data?.detail || "Error creating project");
    }
  };

  return (
    <div className="modal-overlay">
    <div className="modal-content">
      <form onSubmit={handleSubmit} className="create-form">
        <h3>Create New Project</h3>
        <input
          type="text"
          name="title"
          placeholder="Project Title"
          value={formData.title}
          onChange={handleChange}
          required
        />
        <br />
        <textarea
          name="description"
          placeholder="Project Description"
          value={formData.description}
          onChange={handleChange}
          required
        />
        
        <br />
        <button type="submit" className="Submit">Create Project</button>
        {onClose && (
          <button type="button" className="close" onClick={onClose} >
            Close
          </button>
        )}
      </form>
      {message && <p style={{ marginTop: "10px" }}>{message}</p>}
    </div>
    </div>
  );

}
export default CreateProject;
