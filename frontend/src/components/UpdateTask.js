import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './styles/UpdateTask.css';
import BASE_URL from '../config';

const UpdateTaskForm = ({ task, token, onClose, onUpdate }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    status: '',
    due_date: '',
  });
  const [reason, setReason] = useState('');
  const [error, setError] = useState('');
  const initialDueDate = useRef('');

  useEffect(() => {
    if (task) {
      setFormData({
        title: task.title,
        description: task.description,
        status: task.status,
        due_date: task.due_date ? task.due_date.slice(0, 10) : '',
      });
      initialDueDate.current = task.due_date ? task.due_date.slice(0, 10) : '';
      setReason('');
      setError('');
    }
  }, [task]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    if (e.target.name === 'due_date' && e.target.value !== initialDueDate.current) {
      setReason('');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    const dueDateChanged = formData.due_date !== initialDueDate.current;
    if (dueDateChanged && !reason.trim()) {
      setError('Reason for due date change is required.');
      return;
    }

    const payload = { ...formData };
    if (dueDateChanged) {
      payload.due_date_change_reason = reason;
    }

    try {
      const response = await axios.put(
        `${BASE_URL}/project/update-task/${task.id}`,
        payload, // <-- use payload, not formData
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      onUpdate(response.data);
      onClose();
    } catch (error) {
      setError('Error updating task');
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
        {formData.due_date !== initialDueDate.current && (
          <div>
            <label>Reason for Due Date Change</label>
            <input
              type="text"
              value={reason}
              onChange={(e) => setReason(e.target.value)}
              required
            />
          </div>
        )}
        {error && <div className="error">{error}</div>}
        <button type="submit">Save</button>
        <button type="button" onClick={onClose}>Cancel</button>
      </form>
    </div>
  );
};

export default UpdateTaskForm;