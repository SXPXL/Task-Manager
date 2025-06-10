import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './styles/AdminDashboard.css';
import { useAuth } from '../context/AuthContext';
import GreenSpinner from './Spinner';
import BASE_URL from '../config';

// Available roles in the system
const roles = ['member', 'manager', 'admin'];

/**
 * AdminDashboard Component
 * -------------------------
 * Displays all users in the system for the admin.
 * Admin can:
 *  - View user details
 *  - Delete users (except other admins)
 *  - Change user roles via dropdown
 */
const AdminDashboard = () => {
  const [users, setUsers] = useState([]); // List of all users
  const { token } = useAuth(); // Auth token from context
  const [expandedUserId, setExpandedUserId] = useState(null); // Tracks expanded user toshow details
  const [editingRoleUserId, setEditingRoleUserId] = useState(null); // Tracks which user's role is beign edited
  const [selectedRoles, setSelectedRoles] = useState({}); // Stores selected role values for dropdown

 // Fetch users when component mounts or token changes
  useEffect(() => {
    fetchUsers(); 
  }, [token]);

  // Fetch users from the Backend
  const fetchUsers = async () => {
    try {
      
      const res = await axios.get(`${BASE_URL}/auth/get-users`);
      setUsers(res.data);
    } catch (err) {
      alert('Error fetching users');
    }
  };

  // Handles deletion of a user after confirmation
  const handleDelete = async (userId) => {
  if (!window.confirm('Do you want to delete this user?')) return;

  try {
    await axios.delete(`${BASE_URL}/auth/users/${userId}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    // Removes deleted user from local state
    setUsers(users.filter((user) => user.id !== userId));
  } catch (err) {
    console.error('Error deleting user:', err);
  }
};

  // Expand or collapse the user details section
  const toggleExpand = (userId) => {
    setExpandedUserId(expandedUserId === userId ? null : userId);
  };


  // Toggle the role editing mode for a user
  const toggleEditRole = (userId, currentRole) => {
    setEditingRoleUserId(editingRoleUserId === userId ? null : userId);
    setSelectedRoles({ ...selectedRoles, [userId]: currentRole });
  };


  // Sends a rewuest to the backend to update user's role
  const handleChangeRole = async (userId) => {
    const newRole = selectedRoles[userId];
    try {
      await axios.put(`${BASE_URL}/auth/change-role/${userId}?role=${newRole}`, { 
        
        headers: {
        Authorization: `Bearer ${token}`,
          },
      });
      fetchUsers(); // refresh user list after update
      setEditingRoleUserId(null);
    } catch (err) {
      alert('Error updating role');
    }
  };
  // Shows a loading spinner if the token is not yet available
  if(!token) return <GreenSpinner/>
  return (
    <div className="admin-dashboard">
      <h2>All Users</h2>

      {/* Loop through users and display each one */}
      {users.map((user) => (
        <div
          key={user.id}
          className="user-container"
          onClick={() => toggleExpand(user.id)}
        >
          <div className="user-header">
            <span>{user.username}</span>

            {/* Only allow delete/change role for non-admin users */}
            {(user.role !== 'admin') && (
            <div className="button-group">
              <button
                className="delete-btn"
                onClick={(e) => {
                  e.stopPropagation();
                  handleDelete(user.id);
                }}
              >
                Delete
              </button>
                
              <button
                className="change-role-btn"
                onClick={(e) => {
                  e.stopPropagation();
                  toggleEditRole(user.id, user.role);
                }}
              >
                Change Role
              </button>
            </div>
            )
          }
          </div>
            
          {/* Role dropdown shown only when editing */}
          {editingRoleUserId === user.id && (
            <div className="role-dropdown">
              <select
                value={selectedRoles[user.id] || user.role}
                onChange={(e) =>
                  setSelectedRoles({
                    ...selectedRoles,
                    [user.id]: e.target.value,
                  })
                }
              >
                {/* Role optioins */}
                {roles.map((role) => (
                  <option key={role} value={role}>
                    {role}
                  </option>
                ))}
              </select>
              <button className='update-role' onClick={() => handleChangeRole(user.id)}>Update</button>
            </div>
          )}
          {/* Expanded user details */}
          {expandedUserId === user.id && (
            <div className="user-details">
              <p><strong>Email:</strong> {user.email}</p>
              <p><strong>Role:</strong> {user.role}</p>

            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default AdminDashboard;
