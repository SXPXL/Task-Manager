import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './styles/UpdateTask.css';

const UpdateTaskForm = ({ task, token, onClose, onUpdate }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    status: '',
    due_date: '',
  });

  useEffect(() => {
    if (task) {
      setFormData({
        title: task.title,
        description: task.description,
        status: task.status,
        due_date: task.due_date ? task.due_date.slice(0, 10) : '',
      });
    }
  }, [task]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.put(
        `http://localhost:8000/project/update-task/${task.id}`,
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      onUpdate(response.data);
      onClose();
    } catch (error) {
      console.error('Error updating task:', error);
    }
  };

  return (
    <div className="modal">
      <form onSubmit={handleSubmit} className="update-form">
        <h3>Update Task</h3>
        <input
          type="text"
          name="title"
          value={formData.title}
          onChange={handleChange}
          placeholder="Title"
          required
        />
        <textarea
          name="description"
          value={formData.description}
          onChange={handleChange}
          placeholder="Description"
        />
        <select
          name="status"
          value={formData.status}
          onChange={handleChange}
          required
        >
          <option value="">Select status</option>
          <option value="pending">Pending</option>
          <option value="in_progress">In Progress</option>
          <option value="completed">Completed</option>
        </select>
        <label>
          Due date
        <input
          type="date"
          name="due_date"
          value={formData.due_date}
          onChange={handleChange}
        />
        </label>
        <button type="submit">Save</button>
        <button type="button" onClick={onClose}>Cancel</button>
      </form>
    </div>
  );
};

export default UpdateTaskForm;
