import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './styles/CreateTask.css';

/**
 * CreateTask Component
 * --------------------
 * A modal form used to create a new task within a specific project.
 * 
 * Props:
 * - token: authentication token (string)
 * - onTaskCreated: callback to notify parent when task is created
 * - onClose: function to close the modal
 * - projectId: ID of the project this task belongs to
 */
const CreateTask = ({ token, onTaskCreated, onClose, projectId }) => {
  const [users, setUsers] = useState([]);

  // State for form inputs
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    start_date: '',
    due_date: '',
    assigned_to: '',  
  });

  /**
   * useEffect to fetch all users from the backend
   * so the task can be assigned to one of them
   */
  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const res = await axios.get('http://localhost:8000/auth/get-users', {
          headers: { Authorization: `Bearer ${token}` },
        });
        setUsers(res.data);
      } catch (err) {
        console.error('Failed to fetch users:', err);
      }
    };
    fetchUsers();
  }, [token]);

  // Updates the form data when the user changes any input field
  const handleChange = (e) => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  /**
   * Handles form submission
   * - Validates dates
   * - Sends POST request to create task
   * - Calls onTaskCreated() and onClose() if successful
   */
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (new Date(formData.start_date) > new Date(formData.due_date)) {
      alert('Due date cannot be before start date.');
      return;
    }
    try {
      const dataToSend = {
        ...formData,
        project_id: projectId,  // include project ID
      };
      const response = await axios.post(
        `http://localhost:8000/project/create-tasks`,
        dataToSend,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      onTaskCreated(response.data);
      onClose();
    } catch (err) {
      console.error('Error creating task:', err);
    }
  };
  

  return (
    <div className="modal-overlay" onClick={onClose}> 
     {/* Stop propagation so clicking inside modal doesn't close it */}
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
    <form className="create-task-form" onSubmit={handleSubmit}>
      <h3>Create Task</h3>

      {/* Input fields */}
      <input 
        name="title"
        placeholder="Title"
        value={formData.title}
        onChange={handleChange}
        required
      />
      <textarea
        name="description"
        placeholder="Description"
        value={formData.description}
        onChange={handleChange}
        required
      />
      <label>
        Start date
      <input
        name="start_date"
        type="date"
        value={formData.start_date}
        onChange={handleChange}
        required
      />
      </label>
      <label>
        Due date
      <input
        name="due_date"
        type="date"
        value={formData.due_date}
        onChange={handleChange}
        required
      />
      </label>

      <select
        name="assigned_to"
        value={formData.assigned_to}
        onChange={handleChange}
        required
      >
        {/* User dropdown */}
        <option value="">Assign to...</option>
        {users.map(user => (
          <option key={user.id} value={user.id}>
            {user.username} ({user.role})
          </option>
        ))}
      </select>
      <button type="submit" className='submitform'>Create Task</button>
      <button type="button" onClick={onClose}>Cancel</button>
    </form>
    </div>
    </div>
  );
};

export default CreateTask;
