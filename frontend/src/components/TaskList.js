/**
 * TaskListPage Component
 * ----------------------
 * Displays a list of tasks based on their status (e.g., "due_soon", "overdue").
 * Fetches tasks from the backend and allows navigation to individual task details.
 *
 * State:
 * - tasks: List of fetched tasks
 * - loading: Whether the task list is loading
 *
 * Functions:
 * - fetchTasks: Loads tasks from backend based on status and optional user_id
 * - handleTaskClick: Navigates to the details page for a selected task
 *
 * Effects:
 * - Fetches tasks when the component mounts or status/token changes
 *
 * Usage:
 * Used to show filtered task lists from the dashboard or summary cards.
 */

import { useParams, useNavigate, useLocation } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";
import { useAuth } from "../context/AuthContext";
import GreenSpinner from "./Spinner";
import './styles/TaskListPage.css'; 
import BASE_URL from "../config";

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
  const location = useLocation();
  

  //To fetch tasks based on the status from the backend when the component mounts or status changes
  useEffect(() => {
    /**
     * Fetches tasks from the backend API based on status and optional user_id.
     * Updates the tasks state and loading state.
     */
    if (!token) return;
    const searchParams = new URLSearchParams(location.search);
    const userId = searchParams.get("user_id");

    // Fetch tasks from the backend API
    const fetchTasks = async () => {
      try {
        const response = await axios.get(`${BASE_URL}/summary/tasks/${status}${userId ? `?user_id=${userId}` : ''}`, {
          headers: { Authorization: `Bearer ${token}` }
        });

        // Update task list state with fetched tasks
        setTasks(response.data);
      } catch (err) {
        alert("Failed to fetch tasks");
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
  }, [status, token]);

  // Handle task click to navigate to task details page
  const handleTaskClick = (taskId,projectId) => {
    /**
     * Navigates to the details page for the selected task.
     * @param {number} taskId - The ID of the task
     * @param {number} projectId - The ID of the project the task belongs to
     */
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
