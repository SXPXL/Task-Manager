import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './styles/UpdateTask.css';
import BASE_URL from '../config';

/**
 * UpdateTaskForm Component
 * ------------------------
 * A modal form used to update an existing task.
 * 
 * Props:
 * - task: the task object to be updated
 * - token: authentication token (string)
 * - onClose: function to close the modal
 * - onUpdate: callback to notify parent when task is updated
 * */
const UpdateTaskForm = ({ task, token, onClose, onUpdate }) => {
  // Local state to hold form data
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    status: '',
    due_date: '',
  });

  // Effect to populate form data when 'task' prop changes
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

  // Handles changes to input fields and updates state accordingly
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // Send PUT request to update the task
      const response = await axios.put(
        `${BASE_URL}/project/update-task/${task.id}`,
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
      alert('Error updating task');
    }
  };

  return (
    <div className="modal">
      {/* Form UI for updating tasks */}
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

        {/* Drop down for task status */}
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
