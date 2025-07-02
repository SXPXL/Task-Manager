/**
 * UpdateTaskForm Component
 * ------------------------
 * Modal form for updating an existing task's details.
 *
 * Props:
 * - task: The task object to update
 * - token: Authentication token for API requests
 * - onClose: Function to close the modal
 * - onUpdate: Callback to notify parent after successful update
 *
 * State:
 * - formData: Holds updated task field values
 * - reason: Reason for due date change (if applicable)
 * - error: Error message for validation or API errors
 * - initialDueDate: Ref to store the original due date
 *
 * Functions:
 * - handleChange: Updates formData and resets reason if due date changes
 * - handleSubmit: Validates input, sends PUT request, and handles response
 *
 * Effects:
 * - Loads task data into form fields when task prop changes
 *
 * Usage:
 * Used as a modal in the project/task details page for editing tasks.
 */

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
    /**
     * Loads task data into form fields when the task prop changes.
     */
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
    /**
     * Updates formData state and resets reason if due date changes.
     * @param {object} e - The input change event
     */
    setFormData({ ...formData, [e.target.name]: e.target.value });
    if (e.target.name === 'due_date' && e.target.value !== initialDueDate.current) {
      setReason('');
    }
  };

  const handleSubmit = async (e) => {
    /**
     * Validates input, sends PUT request to update the task, and handles response.
     * @param {object} e - The form submit event
     */
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