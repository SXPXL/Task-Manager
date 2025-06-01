import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import './styles/TaskDetails.css'; 
import UpdateTaskForm from './UpdateTask';
import GreenSpinner from './Spinner';

/**
 * TaskDetails Component
 * ---------------------
 * Displays detailed information about a specific task in a project.
 * 
 * Features:
 * - Fetches and displays task details, assigned user, and comments.
 * - Allows authorized users (assignee, managers, and admins) to update the task.
 * - Enables uploading and viewing .eml email attachments grouped by date.
 * - Supports adding, editing, and deleting comments on the task.
 * - Allows downloading uploaded emails.
 * - Shows a spinner while data or files are loading.
 */

const TaskDetails = () => {
  const { projectId, taskId } = useParams(); // get project and task IDs from route params
  const { token, user } = useAuth(); // get token and user from auth context
  const navigate = useNavigate();
  const [task, setTask] = useState(null); // holds the current task object
  const [setAllTasks] = useState([]); // Store all tasks in the project
  const [comments, setComments] = useState([]); // Store list of comments
  const [newComment, setNewComment] = useState(''); // New comment input
  const [users, setUsers] = useState([]); // List of all users for displaying their name
  const [editingTask, setEditingTask] = useState(null); // Task objecct beign edited
  const [editCommentId, setEditCommentId] = useState(null); // ID of the comment beign edited
  const [editContent, setEditContent] = useState(''); // Content for editing a comment
  const [emlFile, setEmlFile] = useState(null); // .eml file selected for upload
  const [uploadMessage, setUploadMessage] = useState(''); // Feedback message for file upload
  const [showFileInput,setShowFileInput] = useState(false); // show/hide upload input
  const [emails,setEmails] = useState([]); // List of uploaded emails
  const [showEmails, setShowEmails] =useState(false); // Toggle email display
  const [uploading,setUploading] = useState(false); // Track if file is being uploaded
  const [tools,setTools] = useState([]);

  

  const authHeaders = {
    headers: { Authorization: `Bearer ${token}` },
  };

  // Fetch task detaisl from backend
  const fetchTask = async () => {
    try {
      const res = await axios.get(`http://localhost:8000/project/${projectId}/tasks`, authHeaders);
      const found = res.data.find((t) => String(t.id) === taskId);
      setTask(found);
      setAllTasks(res.data);
    } catch (err) {
      console.error('Error fetching task:', err);
    }
  };

  // Fetch comments related to the task
  const fetchComments = async () => {
    try {
      const res = await axios.get(`http://localhost:8000/comment/task/${taskId}`, authHeaders);
      setComments(res.data);
    } catch (err) {
      console.error('Error fetching comments:', err);
    }
  };

  // Fetch list of all users 
  const fecthUsers = async () => {
    try {
      const res =await axios.get('http://localhost:8000/auth/get-users', authHeaders);
      setUsers(res.data);
    } catch (err) {
      console.error('Error fetching users:', err);
    }
  }

  // Fetch email attachments related to the task
  const fetchEmails = async () => {
    try {
      const res = await axios.get(`http://localhost:8000/project/tasks/${taskId}/attachments/`, authHeaders)
      setEmails(res.data);
    } catch(err) {
      console.error('Error fetching emails:', err);
      alert(err);
    }
  };

  const fetchTools = async () =>{
  
  try {
    const res = await axios.get(`http://localhost:8000/tool/${projectId}/tools`);
    setTools(res.data);
    } catch (err) {
    console.error("Error fetching tools:", err);
    }
   };

  // Helper function to get username by user ID
  const getUserName = (userId) => {
    const user = users.find((u) => u.id === userId);
    return user ? user.username : 'Unknown';
  }

  const getToolName = (toolId) => {
    const tool = tools.find((t) => t.id === toolId);
    return tool ? tool.name : 'Unknown';
  }

  // Fetch all required data 
  useEffect(() => {
    if (token) {
      fetchTask();
      fetchComments();
      fecthUsers();
      fetchEmails();
      fetchTools();
    }
  }, [token, projectId, taskId]);

  // Validate of selected file ends with .eml
  const handleFileChange =(e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && !selectedFile.name.toLowerCase().endsWith('.eml')) {
      setUploadMessage('Only .eml files are allowed');
      setEmlFile(null);
    } else {
      setUploadMessage('File upload complete');
      setEmlFile(selectedFile)
    }
  };

  // Upload selected .eml file to the backend
  const handleFileUpload = async (e) => {
  if (!emlFile){
    alert('Only eml files are allowed.')
    return;
  }

  const formData = new FormData();
  formData.append('file', emlFile); // "file" must match what FastAPI expects
  setUploading(true);
  try {
     await axios.post(
      `http://localhost:8000/project/tasks/${taskId}/attachments`,
      formData,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "multipart/form-data",
        },
      }
    );
    setUploading(false);
    alert('Email uploaded!');
    setUploadMessage('');
    setShowFileInput(false);
    setEmlFile(null);
    fetchEmails();
    
  } catch (err) {
    console.error("Upload error:", err);

    setUploading(false);
    if (err.response && err.response.data && err.response.data.detail) {
      const detail = err.response.data.detail;

      
      const readableError = Array.isArray(detail)
        ? detail.map((d, i) => `${i + 1}. ${d.msg}`).join('\n')
        : JSON.stringify(detail);
      
      alert(`Upload failed:\n${readableError}`);
    } else {
      alert("Upload failed.");
    }
    
  }

  
};
if(uploading) return <GreenSpinner/>;

// Download email by ID
  const handleDownload = async (attachmentId, filename) => {
  try {
    const response = await axios.get(
      `http://localhost:8000/project/attachments/download/${attachmentId}`,
      {
        authHeaders, 
        responseType: 'blob', 
      }
    );

    const url = window.URL.createObjectURL(response.data);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error("Download error:", error);
    alert("Failed to download email.");
  }
};

  // Open task in edit form
  const handleUpdateTask = (taskId) => {
   if (task && task.id === taskId) {
    setEditingTask(task);
    
  }
};

  // Refresh task details after editing
  const handleTaskUpdated = () => {
    setEditingTask(null);
    fetchTask();
    alert('Task updated successfully!');
    
  };

  // Handle new comment submission
  const handleCommentSubmit = async (e) => {
    e.preventDefault();
    if (!newComment.trim()) return;

    try {
      const res = await axios.post(
        `http://localhost:8000/comment/task/${taskId}`,
        { content: newComment },
        authHeaders
        
      );
      
      setComments([res.data, ...comments]);
      setNewComment('');
      
    } catch (err) {
      alert('Failed to post comment');
    }
  };

  // Handle comment deletion
  const handleDeleteComment = async (commentId) => {
    try {
      await axios.delete(`http://localhost:8000/comment/${commentId}`, authHeaders);
      setComments(comments.filter((c) => c.id !== commentId));
    } catch (err) {
      alert('Not authorized to delete this comment.');
    }
  };

  // Handle comment editing submission
  const handleEditCommentSubmit = async (e, commentId) => {
  e.preventDefault();
  try {
    const res = await axios.put(
      `http://localhost:8000/comment/comments/${commentId}`,
      { content: editContent },
      authHeaders
    );
    setComments(
      comments.map((c) => (c.id === commentId ? res.data : c))
    );
    setEditCommentId(null);
    setEditContent('');
  } catch (err) {
    alert("Failed to edit comment");
  }
};


  if (!task) return <p><GreenSpinner/></p>;

  // Group email by creation date
  const groupedEmails = emails.reduce((acc, email) => {
  const date = new Date(email.created_at).toLocaleDateString("en-IN", {
    timeZone: "Asia/Kolkata",
  });

  if (!acc[date]) {
    acc[date] = [];
  }

  acc[date].push(email);
  return acc;
}, {});

  return (
    <div className="task-details-container">
      <div className="task-top-bar">
        <button className="back" onClick={() => navigate(-1)}>← Back</button>
        <div className="task-info">
          <h2>{task.title}</h2>
          <p>Description: {task.description}</p>
          <p>Start Date: {task.start_date}</p>
          <p>Due Date: {task.due_date}</p>
          <p>Tool Used: {getToolName(task.tool_id)}</p>
          <p>Assigned to: {getUserName(task.assigned_to)}</p>
        </div>
        {/* Only assigned user,manager or the admin can update the task */}
        {(user.user_id === task.assigned_to || ['admin','manager'].includes(user.role)) && (
              <button className="update-btn" onClick={() => handleUpdateTask(task.id)}>Update</button>
        )}
      </div>

      {editingTask && (
        <UpdateTaskForm
          task={editingTask}
          token={token}
          onClose={() => setEditingTask(null)}
          onUpdate={handleTaskUpdated}
        />
      )}

      {/* Email upload section */}
      <button className='add-mail'onClick={() => setShowFileInput(prev => !prev)}>{showFileInput ? 'Close' : 'Add Mails' }</button>
      {showFileInput && (
      <div>
        <h3>Upload Emails</h3>
        <input type='file' accept=".eml" onChange={handleFileChange}/>
        <button className='upload-mail' onClick={handleFileUpload}>
          Upload
        </button>
        <p>{uploadMessage}</p>
      </div>
      )}

      {/* Show/hide uploaded emails */}
      <button className='show-mail' onClick={() => setShowEmails(!showEmails)}>
        {showEmails ? 'Hide Mails' : 'Show Mails'}
      </button>

      <div>

      {/* Conditionally render grouped emails */}
      {showEmails && emails.length > 0 && (
        <div className="emails-list">
          <h3>Uploaded Emails</h3>
          {Object.entries(groupedEmails).map(([date, group]) => (
            <div key={date} className="email-group">
              <h4>{date}</h4>
              <ul>
                {group.map(email => (
                  <li key={email.id}>
                    <p className='download-email'  onClick={() => handleDownload(email.id,email.filename)}>{email.filename}</p></li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}
    </div>
      
      {/* Task comments section */}
      <div className="comment-section">
        <h3>Comments</h3>

        {/* Comment input form */}
        <form onSubmit={handleCommentSubmit} className="comment-form">
          <input
            type="text"
            placeholder="Add a comment..."
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
            className="comment-input"
          />
        </form>
        {/* Display comments */}
        <div className="comment-list">
          {comments.length === 0 ? (
            <p>No comments yet.</p>
          ) : (
            comments.map((comment) => (
              <div key={comment.id} className="comment-item">
                <div className="comment-content">
                  <p className="comment-author">{comment.user.username}</p>
                  <span className="comment-date"> - {new Date(comment.created_at).toLocaleDateString("en-IN", { timeZone: "Asia/Kolkata"} )}</span>
                  <p className="author-role"> - {comment.user.role}</p>

                  {/* Comment edit form */}
                  {editCommentId === comment.id ? (
                    <form onSubmit={(e) => handleEditCommentSubmit(e, comment.id)} className="edit-comment-form">
                      <input
                        type="text"
                        value={editContent}
                        onChange={(e) => setEditContent(e.target.value)}
                        className="comment-input"
                      />
                      <button type="submit" className="save-comment">Save</button>
                      <button onClick={() => setEditCommentId(null)} className="cancel-edit">Cancel</button>
                    </form>
                  ) : (
                    <p>{comment.content}</p>
                  )}

                </div>
                <div className='comment-actions'>
                {user.username === comment.user.username && (
                <button
                onClick={() => {
                  setEditCommentId(comment.id);
                  setEditContent(comment.content);
                }}
                className="edit-comment"
              >
                Edit
              </button>
                )}
                {/* Only the author,manager or adminn can delete the comment */}
                {(user.username === comment.user.username || ['admin','manager'].includes(user.role))&& (
                  <button
                    onClick={() => handleDeleteComment(comment.id)}
                    className="delete-comment"
                  >
                    Delete
                  </button>
                  
                )}
                
              </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default TaskDetails;
