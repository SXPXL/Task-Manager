import { useEffect, useState } from "react";
import axios from "axios";
import { useAuth } from "../context/AuthContext";
import "./styles/ToolList.css";

/**
 * ToolList Component
 * ------------------
 * Displays a list of tools associated with a project.
 * Allows filtering tasks based on selected tool.
 * Admins/Managers can add or delete tools.
 * 
 * Props:
 * - projectId: ID of the current project
 * - onToolClick: Callback to filter tasks by selected tool
 * - clearfilter: Function to clear the tool filter
 * - fetchTasks: Function to re-fetch tasks when a tool is deleted
 */

export default function ToolList({projectId,onToolClick,clearfilter,fetchTasks}) {
  const [tools,setTools] = useState([]); // List of tools in the project
  const [newTool, setNewTool] = useState(""); // Input for adding new tool
  
  const { token, user } = useAuth();

  // Fetches all tools for the current project from the API.
const fetchTools = async () =>{

try {
  const res = await axios.get(`http://localhost:8000/tool/${projectId}/tools`);
  setTools(res.data);
  } catch (err) {
  
  }
 };

 /**
   * Adds a new tool to the project.
   * Resets the input and refetches tool list.
   */
 const handleAddTool = async () => {
  if(!newTool.trim()) return;
  try {
    
    await axios.post(`http://localhost:8000/tool/${projectId}/tools`,{name: newTool },{
    headers: { Authorization: `Bearer ${token}` },
  });
    setNewTool("");
    await fetchTools();
  } catch (err) {
    
  } finally {
    
  }

 };

 /**
   * Deletes a tool by ID after confirmation.
   * Warns the user that deleting the tool will also delete related tasks.
   * Refetches both tools and tasks after deletion.
   * 
   */
 const handleDeleteTool = async (toolId) => {
  window.confirm("Deleting this tool will delete all the tasks using it.")
  try {
    await axios.delete(`http://localhost:8000/tool/tools/${toolId}`,{
    headers: { Authorization: `Bearer ${token}` },
  });
    setTools(tools.filter(t => t.id !== toolId))
    fetchTools();
    fetchTasks();
  } catch (err) {
    

  }
 };

  useEffect(() => {
    fetchTools();
  },[projectId]);

  
 return(
  <div className="tool-list-container">
    <h2 className="tool-list-heading">Tools</h2>

    {/* Only the admins or managers can add tools */}
    {(user.role === 'admin' || user.role === 'manager') && (
    <div className="tool-form">
      {/* Input for new tool */}
      <input
      type="text"
      value={newTool}
      onChange={(e) => setNewTool(e.target.value)}
      placeholder = "Tool name"
      className="tool-input"
      />
      <button 
      onClick={handleAddTool}
      className = "tool-add-button"
      >
        Add
      </button>
    </div>
    )}

    <ul className="tool-items">
      {tools.map((tool)=>(
      <li
      key={tool.id}
      className="tool-item"
      onClick={() => onToolClick(tool.id)}
      >
        <span className="tool-name">
          {tool.name}
        </span>
        {(user.role === 'admin' || user.role === 'manager') && (
        <button
        className="tool-delete-button"
        onClick={() => handleDeleteTool(tool.id)}
        >
          X
        </button>
        )}
      </li>
      ))}
      {tools.length === 0 && <p className="no-tools">No tools added</p>}
    </ul>
    {tools.length!== 0 && 
    <button className="clear-tool-filter" onClick={clearfilter}>Clear Filter</button>
    }
  </div>
 );
}


