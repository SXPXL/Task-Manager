import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";
import { useAuth } from "../context/AuthContext";
import GreenSpinner from "./Spinner";
import './styles/TaskListPage.css'; 

export default function TaskListPage() {
  const { status } = useParams();
  const { token } = useAuth();
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    if (!token) return;

    const fetchTasks = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/summary/tasks/${status}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
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

  const handleTaskClick = (taskId,projectId) => {
    navigate(`/project/${projectId}/tasks/${taskId}`);
  };

  return (
    <div>
    
    <div className="task-list-page">
      <button className="back" onClick={() => navigate(-1)}>← Back</button>
       <h2>{status.replace("_", " ").toUpperCase()}</h2>
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
