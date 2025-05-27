import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";
import { useAuth } from "../context/AuthContext";
import GreenSpinner from "./Spinner";
import './styles/TaskListPage.css'; 

/**
 * TaskListPage Component
 * ----------------------
 * Displays a list of tasks based on their status (e.g., "due_soon", "overdue").
 * Fetches tasks from the backend and allows navigation to individual task details.
 */
export default function TaskListPage() {
  const { status } = useParams(); // Get status parameter from the URL
  const { token } = useAuth(); // Get JWT token from auth context
  const [tasks, setTasks] = useState([]); // State to store fetched tasks
  const [loading, setLoading] = useState(true); // State to control loading spinner
  const navigate = useNavigate();

  //To fetch tasks based on the status from the backend when the component mounts or status changes
  useEffect(() => {
    if (!token) return;

    // Fetch tasks from the backend API
    const fetchTasks = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/summary/tasks/${status}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        // Update task list state with fetched tasks
        setTasks(response.data);
        console.log(response.data);
      } catch (err) {
        console.error("Failed to fetch tasks:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
  }, [status, token]);

  // Handle task click to navigate to task details page
  const handleTaskClick = (taskId,projectId) => {
    navigate(`/project/${projectId}/tasks/${taskId}`);
  };

  return (
    <div>
    
    <div className="task-list-page">
      <button className="back" onClick={() => navigate(-1)}>← Back</button>
       <h2>{status.replace("_", " ").toUpperCase()}</h2>
       {/* Show loading spinner while data is beign fetched */}
      {loading ? (
        <GreenSpinner />
      ) : tasks.length > 0 ? (
        <ul className="task-list">
          {tasks.map((task) => (
            <li key={task.id}  onClick={() => handleTaskClick(task.id,task.project_id)} className="task-item">
              <h4>{task.title}</h4>
              
            </li>
          ))}
        </ul>
      ) : (
        <p>No tasks found.</p>
      )}
    </div>
    </div>
  );
}
