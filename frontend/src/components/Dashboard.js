import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import './styles/Dashboard.css';
import CreateProject from './CreateProject';
import GreenSpinner from './Spinner';

const Dashboard = () => {
  const { user, token, logout } = useAuth();
  const username = user?.username;
  const role = user?.role;
  const [projects, setProjects] = useState([]);
  const [showCreateProject, setShowCreateProject] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  // Fetch projects from backend using JWT
  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const response = await axios.get('http://localhost:8000/project/get-projects', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        console.log('Projects:', response.data);
        setProjects(response.data);
      } catch (error) {
        console.error('Error fetching projects:', error);
      }
    };
    if (token) {
    fetchProjects();
    }
  }, [token]);

  const handleDelete = async (projectId) => {
    if(!window.confirm("Are you sure you want to delete this project?")) 
      return;
    try {
      await axios.delete(`http://localhost:8000/project/delete-project/${projectId}`,{
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setProjects((prev) => prev.filter((project) => project.id !== projectId));
      setMessage("Project deleted successfully!");
      console.log("Deleting project ID:", projectId);

    } catch (err) {
      setMessage(`${err.response?.data?.detail || "Error deleting project"}`);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };
  const toggleCreateProject = () => {
    setShowCreateProject(!showCreateProject);
  }
  const goToProject = (projectId) => {
    navigate(`/project/${projectId}`);
  };

  return (
    <div className='wholepage'>
    <div className="dashboard-container">
      <div className="top-bar">
        <button className="hamburger" onClick={() => setMenuOpen(!menuOpen)}>
          ☰
        </button>
        <div className="welcome-text"><h2>Welcome, {username}!</h2></div>
        <button className="logout-btn" onClick={handleLogout}>Logout</button>
      </div>

      {menuOpen && <div className="overlay" onClick={() => setMenuOpen(false)} />}
  <div className={`hamburger-menu ${menuOpen ? 'open' : ''}`}>
    <div className='profile'>
      <h3>{username}</h3>
      <p>{user?.email}</p>
      <p>{role}</p>
    </div>
    <hr></hr>
    {/* Add role-based options here later */}
    
  </div>

      <div className="project-section">
        <div className="project-header">
          <h2>Your Projects</h2>
          {(role === 'admin' || role === 'manager') && (
          <button className="create-project-btn" onClick={toggleCreateProject}>
             {showCreateProject ? 'Close' : 'Create New Project'}
          </button>
          )}
          
        </div>
        {showCreateProject && (
          <div className="create-project-form">
            <CreateProject onClose={toggleCreateProject} token={token} 
            onProjectCreated={(newProject) => setProjects((prev)=> [
                ...prev, newProject])}/>
            </div>
        )}

        <div className="project-list">
          {projects.length === 0 ? (
            <p>No projects yet.</p>
          ) : (
            projects.map((project) => (
              <div
                key={project.id}
                className="project-item"
                onClick={() => goToProject(project.id)}
              >
              <span className="project-title">{project.title}</span>
               {(role === 'admin' || role === 'manager') && (
                <button
                  className="delete-btn"
                  onClick={(e) => {
                    e.stopPropagation();
                     handleDelete(project.id)}}
                >
                  Delete
                </button>
              )}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
    </div>
  );
};

export default Dashboard;
