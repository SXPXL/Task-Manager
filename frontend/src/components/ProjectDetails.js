import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import CreateTask from './CreateTask';
import './styles/ProjectDetail.css';
import UpdateTaskForm from './UpdateTask';
import GreenSpinner from './Spinner';

const ProjectDetail = () => {
  const { projectId } = useParams();
  const { token, user } = useAuth();
  const navigate = useNavigate();

  const [project, setProject] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [showCreateTask, setShowCreateTask] = useState(false);
  const [filterStatus, setFilterStatus] = useState('all');
  const [errors, setErrors] = useState(null);
  const [editingTask, setEditingTask] = useState(null);
  const [users, setUsers] = useState([]);
  const [assignedUser, setAssignedUser] = useState('all');

  const fetchProject = async () => {
    try {
      const res = await axios.get('http://localhost:8000/project/get-projects', {
        headers: { Authorization: `Bearer ${token}` },
      });
      const found = res.data.find((p) => String(p.id) === projectId);
      setProject(found || null);
    } catch (err) {
      setErrors(err);
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
  const fetchUsers = async () => {
      try {
        const res =await axios.get('http://localhost:8000/auth/get-users', 
          {
        headers: { Authorization: `Bearer ${token}` },
      }
        );
        setUsers(res.data);
      } catch (err) {
        console.error('Error fetching users:', err);
      }
    }

  useEffect(() => {
    if (token) {
      fetchProject();
      fetchTasks();
      fetchUsers();
    }
  }, [token, projectId]);

  const getUserName = (userId) => {
    const user = users.find((u) => u.id === userId);
    return user ? user.username : 'Unknown';
  }

  const handleTaskClick = (taskId) => {
    navigate(`/project/${projectId}/tasks/${taskId}`);
  };

  const handleTaskCreated = () => {
    setShowCreateTask(false);
    fetchTasks();
  };

  const handleUpdateTask = (taskId, e) => {
    e.stopPropagation();
    const taskToEdit = tasks.find((task) => task.id === taskId);
    setEditingTask(taskToEdit);
    
  };

  const handleTaskUpdated = () => {
    setEditingTask(null);
    fetchTasks();
  };

  const handleDeleteTask = async (taskId, e) => {
    e.stopPropagation();
    if(!window.confirm("Are you sure you want to delete this task?")) 
      return;
    try {
      await axios.delete(`http://localhost:8000/project/delete-task/${taskId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setTasks((prevTasks) => prevTasks.filter((task) => task.id !== taskId));
    } catch (error) {
      console.error('Error deleting task:', error);
    }
  };

  const handlePrint = () => {
    const content = document.getElementById('print-section').innerHTML;

    const win = window.open('','','width=800,height=600');
    win.document.write('<html><head><Title>Project Report     </title></head><body');
    win.document.write(content);
    win.document.write('</body></html>');

    win.document.close();
    win.focus();
    win.print();
    win.close();
  };
  

  if(!project) return <GreenSpinner/>;
  console.log("comments",tasks.map(task => task.comments));
  

  return (
    <div className='wholepage'>
    <div className="project-detail-container">
      
      <div className="project-top-bar">
        <button className="back" onClick={() => navigate(-1)}>← Back</button>
        <div className="project-info">
          <h2>{project.title}</h2>
          <p>{project.description}</p>
        </div>
      </div>

      <div className="task-header-list">
        <div className="task-header">
          <h3>Tasks</h3>
          <div className="task-filter">
            
              <label htmlFor="userFilter">User: </label>
              <select
                id="userFilter"
                value={assignedUser}
                onChange={(e) => setAssignedUser(e.target.value)}
              >
                <option value="all">All</option>
                {users.map((user) => (
                  <option key={user.id} value={user.id}>
                    {user.username}
                  </option>
                ))}
              </select>
            
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
          {(user.role === 'admin' || user.role === 'manager') && (
            <button className="create-task" onClick={() => setShowCreateTask(!showCreateTask)}>
              {showCreateTask ? 'Close Task Form' : '+ Create Task'}
            </button>
          )}
        </div>

        {showCreateTask && (
          <CreateTask 
          projectId={projectId}
          token={token} 
          onTaskCreated={handleTaskCreated}
          onClose={()=>setShowCreateTask(false)}
           />
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
              .filter(
                (task) =>
                  ( filterStatus === 'all' || task.status === filterStatus)&&
               (assignedUser === 'all' || String(task.assigned_to) === assignedUser)
                  )
              .map((task) => (
                <div
                  key={task.id}
                  className="task-item"
                  onClick={() => handleTaskClick(task.id)}
                >
                  <div className="task-title-wrapper">
                    <span className={`status-circle ${task.status}`}></span>
                    <span className="task-title">{task.title}</span>
                    <span className="task-title-user">- {getUserName(task.assigned_to)}</span>
                  </div>
                  <div className="task-actions">
                    {(user.user_id === task.assigned_to || ['admin', 'manager'].includes(user.role)) && (
                      <button className="update-btn" onClick={(e) => handleUpdateTask(task.id, e)}>Update</button>
                    )}
                    {(user.role === 'admin' || user.role === 'manager') && (
                      <button className="delete-btn" onClick={(e) => handleDeleteTask(task.id, e)}>Delete</button>
                    )}
                  </div>
                </div>
              ))
          )}
        </div>
      
        <div className='print-section'>
          <button className='print' onClick={handlePrint}>
            Print Report
          </button>
          </div>
      
      </div>
    </div>
    
    <div style={{ display: 'none' }}>
  <div id="print-section">
    <h2>Project: {project?.title}</h2>
    <p>Filter: {filterStatus}</p>

    <table border="1" cellPadding="8" cellSpacing="0" style={{ width: '100%', borderCollapse: 'collapse' }}>
      <thead>
        <tr>
          <th>#</th>
          <th>Title</th>
          <th>Status</th>
          <th>Description</th>
          <th>Assigned To</th>
          <th>Due Date</th>
          
        </tr>
      </thead>
      <tbody>
        {tasks
          .filter(task => 
            (filterStatus === 'all' || task.status === filterStatus) &&
            (assignedUser === 'all' || String(task.assigned_to) === assignedUser)
          )
          .map((task, index) => {
              
            return (
              <tr key={task.id}>
                <td>{index + 1}</td>
                <td>{task.title}</td>
                <td>{task.status}</td>
                <td>{task.description || 'No description'}</td>
                <td>{getUserName(task.assigned_to) || 'Unassigned'}</td>
                <td>{task.due_date ? new Date(task.due_date).toLocaleDateString() : 'No due date'}</td>
                
                
              </tr>
            );
          })}
      </tbody>
    </table>
  </div>
</div>


    </div>

    
    
  );
};

export default ProjectDetail;
