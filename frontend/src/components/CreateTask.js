import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './styles/CreateTask.css';

const CreateTask = ({ token, onTaskCreated, onClose, projectId }) => {
  const [users, setUsers] = useState([]);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    due_date: '',
    assigned_to: '',  // store selected user id
  });

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

  const handleChange = (e) => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
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
    <form className="create-task-form" onSubmit={handleSubmit}>
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
      <input
        name="due_date"
        type="date"
        value={formData.due_date}
        onChange={handleChange}
        required
      />
      <select
        name="assigned_to"
        value={formData.assigned_to}
        onChange={handleChange}
        required
      >
        <option value="">Assign to...</option>
        {users.map(user => (
          <option key={user.id} value={user.id}>
            {user.username} ({user.role})
          </option>
        ))}
      </select>
      <button type="submit">Create Task</button>
      <button type="button" onClick={onClose}>Cancel</button>
    </form>
  );
};

export default CreateTask;
