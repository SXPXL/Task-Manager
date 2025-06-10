import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import CreateTask from './CreateTask';
import './styles/ProjectDetail.css';
import UpdateTaskForm from './UpdateTask';
import GreenSpinner from './Spinner';
import ToolList from './ToolList.js';
import BASE_URL from '../config.js';


/**
 * Project Detail Page
 * -------------------
 * Displays detailed information about a single project.
 * Shows the task list with filtering and sorting options.
 * Allows creating, updating, and deleting tasks for admins/managers.
 * Includes a print feature for the project report.
 */
const ProjectDetail = () => {
  const { projectId } = useParams(); // Project ID from URL parameters
  const { token, user } = useAuth(); // Auth token and currrent user info
  const navigate = useNavigate(); 
  const [project, setProject] = useState(null); // Current project details
  const [tasks, setTasks] = useState([]); // List of tasks for the project
  const [allTasks,setAllTasks] = useState([]);
  const [showCreateTask, setShowCreateTask] = useState(false); 
  const [selectedTool,setSelectedTool] = useState(null);
  const [filterStatus, setFilterStatus] = useState('all'); // Filter to show tasks by status
  const [editingTask, setEditingTask] = useState(null); // Task currently being edited
  const [users, setUsers] = useState([]); // List of Users
  const [assignedUser, setAssignedUser] = useState('all'); // Filter to show tasks based on the user

  // Fetch project details
  const fetchProject = async () => {
    try {
      const res = await axios.get(`${BASE_URL}/project/get-projects`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const found = res.data.find((p) => String(p.id) === projectId);
      setProject(found || null);
    } catch (err) {
      alert('Error fetching project');
    }
  };

  // Fetch all tasks within the project
  const fetchTasks = async () => {
    try {
      const res = await axios.get(`${BASE_URL}/project/${projectId}/tasks`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setAllTasks(res.data);
      setTasks(res.data);
    } catch (err) {
      alert('Error fetching tasks');
    }
  };

  // Fetch all users
  const fetchUsers = async () => {
      try {
        const res =await axios.get(`${BASE_URL}/auth/get-users`, 
          {
        headers: { Authorization: `Bearer ${token}` },
      }
        );
        setUsers(res.data);
      } catch (err) {
        alert('Error fetching users');
      }
    }

  // Intital data fetch when tokke or projectId changes
  useEffect(() => {
    if (token) {
      fetchProject();
      fetchTasks();
      fetchUsers();
    }
  }, [token, projectId]);

  // To get a username by user id
  const getUserName = (userId) => {
    const user = users.find((u) => u.id === userId);
    return user ? user.username : 'Unknown';
  }
  

  // To navigate to respective task detail page
  const handleTaskClick = (taskId) => {
    navigate(`/project/${projectId}/tasks/${taskId}`);
  };

  // CallBack when a new task is created
  const handleTaskCreated = () => {
    setShowCreateTask(false);
    fetchTasks();
  };

  // Start editing task
  const handleUpdateTask = (taskId, e) => {
    e.stopPropagation();
    const taskToEdit = tasks.find((task) => task.id === taskId);
    setEditingTask(taskToEdit);
    
  };

  // Closes form and refresh after task update
  const handleTaskUpdated = () => {
    setEditingTask(null);
    fetchTasks();
  };
 
  // delete a task after confirmation
  const handleDeleteTask = async (taskId, e) => {
    e.stopPropagation();
    if(!window.confirm("Are you sure you want to delete this task?")) 
      return;
    try {
      await axios.delete(`${BASE_URL}/project/delete-task/${taskId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setTasks((prevTasks) => prevTasks.filter((task) => task.id !== taskId));
    } catch (error) {
      alert('Error deleting task');
    }
  };
  
  // To filter tasks based on selected tool
  const handleToolClick = (toolId) => {
  setSelectedTool(toolId); 
};

  // Print the filtered project report
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

      {/* Task headers with filters and create button */}
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
        
        {/* Create Task Form */}
        {showCreateTask && (
          <CreateTask 
          projectId={projectId}
          token={token} 
          onTaskCreated={handleTaskCreated}
          onClose={()=>setShowCreateTask(false)}
           />
        )}

        {/* Update Task Form */}
        {editingTask && (
        <UpdateTaskForm
          task={editingTask}
          token={token}
          onClose={() => setEditingTask(null)}
          onUpdate={handleTaskUpdated}
        />
      )}
      <div className='lists-wrapper'>
       
       {/* Adding the ToolLIst component */}
       <ToolList 
        projectId={projectId} 
        onToolClick={handleToolClick} 
        clearfilter={() => setSelectedTool(null)}
        fetchTasks={fetchTasks}
       />
        
        {/* Task list with filtering */}
        <div className="task-list">
          {tasks.length === 0 ? (
            <p className="no-task">No tasks for this project.</p>
          
          ) : (
            tasks
              .filter(
                (task) =>
                  ( filterStatus === 'all' || task.status === filterStatus)&&
                  (assignedUser === 'all' || String(task.assigned_to) === assignedUser)&&
                  (!selectedTool || task.tool_id === selectedTool)
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
        </div>
        
       
        {/* Hidden printable section */}
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
