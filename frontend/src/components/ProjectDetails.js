import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import CreateTask from './CreateTask'; 
import UpdateTaskForm from './UpdateTask';
import './styles/ProjectDetail.css'; 


const ProjectDetail = () => {
  const { projectId } = useParams();
  const { token } = useAuth();
  const navigate = useNavigate();

  const [project, setProject] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [showCreateTask, setShowCreateTask] = useState(false);
  const [editingTask, setEditingTask] = useState(null);
  const [filterStatus, setFilterStatus] = useState('all');

  const fetchProject = async () => {
    try {
      const res = await axios.get('http://localhost:8000/project/get-projects', {
        headers: { Authorization: `Bearer ${token}` },
      });
      const found = res.data.find((p) => String(p.id) === projectId);
      setProject(found || null);
    } catch (err) {
      console.error('Error fetching project:', err);
    }
  };


  const fetchTasks = async () => {
    try {
      const res = await axios.get(`http://localhost:8000/project/${projectId}/tasks`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setTasks(res.data);
    } catch (err) {
      console.error('Error fetching tasks:', err);
    }
  };

  useEffect(() => {
    if (token) {
      fetchProject();
      fetchTasks();
    }
  }, [token, projectId]);

  const handleTaskClick = (taskId) => {
    navigate(`/task/${taskId}`);
  };

  const handleTaskCreated = () => {
    setShowCreateTask(false);
    fetchTasks(); // refresh tasks list after creation
  };

  if (!project) return <p>Loading project...</p>;

  const handleDeleteTask = async (taskId) => {
  try {
    await axios.delete(`http://localhost:8000/project/delete-task/${taskId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    // Remove the task from the local state
    setTasks((prevTasks) => prevTasks.filter((task) => task.id !== taskId));
  } catch (error) {
    console.error('Error deleting task:', error);
  }
};

const handleUpdateTask = (taskId) => {
  const taskToEdit = tasks.find(task => task.id === taskId);
  setEditingTask(taskToEdit);
};

const handleTaskUpdated = () => {
    setEditingTask(null);
    fetchTasks();
  };


  return (
    <div className="project-detail-container">
      <div className="project-top-bar">
        <button className="back" onClick={() => navigate(-1)}>← Back</button>
        <div className="project-info">
          <h2>{project.title}</h2>
          <p>{project.description}</p>
          
        </div>
      </div>

    <div className="task-header-list">
    <div className='task-header'>
      <h3>Tasks</h3>
      <div className="task-filter">
      <label htmlFor="statusFilter">Sort: </label>
      <select
        id="statusFilter"
        value={filterStatus}
        onChange={(e) => setFilterStatus(e.target.value)}
      >
        <option value="all">All</option>
        <option value="pending">Pending</option>
        <option value="in_progress">In Progress</option>
        <option value="completed">Completed</option>
      </select>
    </div>
     <button className="create-task" onClick={() => setShowCreateTask(!showCreateTask)}>
        {showCreateTask ? 'Close Task Form' : '+ Create Task'}
      </button>
      </div>
     

      {showCreateTask && (
        <CreateTask projectId={projectId} token={token} onTaskCreated={handleTaskCreated} />
      )}
      {editingTask && (
        <UpdateTaskForm
          task={editingTask}
          token={token}
          onClose={() => setEditingTask(null)}
          onUpdate={handleTaskUpdated}
        />
      )}

      <div className="task-list">
        {tasks.length === 0 ? (
          <p>No tasks for this project.</p>
        ) : (
          tasks
          .filter(task => filterStatus === 'all' || task.status === filterStatus)
          .map((task) => (

          <div key={task.id} className="task-item">
            <div className="task-title-wrapper" onClick={() => handleTaskClick(task.id)}>
              <span className={`status-circle ${task.status}`}></span>
              <span className="task-title">{task.title}</span>
            </div>
            <div className="task-actions">
              <button className="update-btn" onClick={() => handleUpdateTask(task.id)}>Update</button>
              <button className="delete-btn" onClick={() => handleDeleteTask(task.id)}>Delete</button>
            </div>
          </div>

        ))

        )}
      </div>
    </div>
    </div>
  );
};

export default ProjectDetail;
