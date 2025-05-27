import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './styles/AdminDashboard.css';
import { useAuth } from '../context/AuthContext';
import GreenSpinner from './Spinner';

const roles = ['member', 'manager', 'admin'];

const AdminDashboard = () => {
  const [users, setUsers] = useState([]);
  const { token } = useAuth();
  const [expandedUserId, setExpandedUserId] = useState(null);
  const [editingRoleUserId, setEditingRoleUserId] = useState(null);
  const [selectedRoles, setSelectedRoles] = useState({});

  useEffect(() => {
    fetchUsers(); 
  }, [token]);

  const fetchUsers = async () => {
    try {
      
      const res = await axios.get('http://localhost:8000/auth/get-users');
      setUsers(res.data);
    } catch (err) {
      console.error('Error fetching users:', err);
    }
  };

  const handleDelete = async (userId) => {
  if (!window.confirm('Do you want to delete this user?')) return;

  try {
    await axios.delete(`http://localhost:8000/auth/users/${userId}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    setUsers(users.filter((user) => user.id !== userId));
  } catch (err) {
    console.error('Error deleting user:', err);
  }
};


  const toggleExpand = (userId) => {
    setExpandedUserId(expandedUserId === userId ? null : userId);
  };

  const toggleEditRole = (userId, currentRole) => {
    setEditingRoleUserId(editingRoleUserId === userId ? null : userId);
    setSelectedRoles({ ...selectedRoles, [userId]: currentRole });
  };

  const handleChangeRole = async (userId) => {
    const newRole = selectedRoles[userId];
    try {
      await axios.put(`http://localhost:8000/auth/change-role/${userId}?role=${newRole}`, { 
        
        headers: {
        Authorization: `Bearer ${token}`,
          },
      });
      fetchUsers(); // refresh after update
      setEditingRoleUserId(null);
    } catch (err) {
      console.error('Error updating role:', err);
    }
  };
  if(!token) return <GreenSpinner/>
  return (
    <div className="admin-dashboard">
      <h2>All Users</h2>
      {users.map((user) => (
        <div
          key={user.id}
          className="user-container"
          onClick={() => toggleExpand(user.id)}
        >
          <div className="user-header">
            <span>{user.username}</span>
            {(user.role != 'admin') && (
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
                {roles.map((role) => (
                  <option key={role} value={role}>
                    {role}
                  </option>
                ))}
              </select>
              <button className='update-role' onClick={() => handleChangeRole(user.id)}>Update</button>
            </div>
          )}

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
