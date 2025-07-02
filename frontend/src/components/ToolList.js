/**
 * ToolList Component
 * ------------------
 * Displays a list of modules (tools) associated with a project.
 * Allows filtering tasks based on selected tool.
 * Admins/Managers can add or delete modules.
 *
 * Props:
 * - projectId: ID of the current project
 * - onToolClick: Callback to filter tasks by selected tool
 * - clearfilter: Function to clear the tool filter
 * - refresh: Function to re-fetch tasks when a tool is deleted
 *
 * State:
 * - tools: List of tools in the project
 * - newTool: Input value for adding a new tool
 *
 * Functions:
 * - fetchTools: Loads all tools for the project
 * - handleAddTool: Adds a new tool to the project
 * - handleDeleteTool: Deletes a tool by ID after confirmation
 *
 * Effects:
 * - Fetches tools when the projectId changes
 *
 * Usage:
 * Used in the project details page to filter and manage modules/tools.
 */

import { useEffect, useState } from "react";
import axios from "axios";
import { useAuth } from "../context/AuthContext";
import "./styles/ToolList.css";
import BASE_URL from "../config";

/**
 * ToolList Component
 * ------------------
 * Displays a list of modules associated with a project.
 * Allows filtering tasks based on selected tool.
 * Admins/Managers can add or delete modules.
 * 
 * Props:
 * - projectId: ID of the current project
 * - onToolClick: Callback to filter tasks by selected tool
 * - clearfilter: Function to clear the tool filter
 * - refresh: Function to re-fetch tasks when a tool is deleted
 */

export default function ToolList({projectId,onToolClick,clearfilter,refresh}) {
  const [tools,setTools] = useState([]); // List of tools in the project
  const [newTool, setNewTool] = useState(""); // Input for adding new tool
  
  const { token, user } = useAuth();

  // Fetches all modules for the current project from the API.
  const fetchTools = async () =>{
    /**
     * Loads all tools for the current project from the backend API.
     * Updates the tools state.
     */
    try {
      const res = await axios.get(`${BASE_URL}/tool/${projectId}/tools`);
      setTools(res.data);
      } catch (err) {
      alert('Error fetching modules');
      }
   };

   /**
     * Adds a new tool to the project.
     * Resets the input and refetches tool list.
     */
   const handleAddTool = async () => {
    if(!newTool.trim()) return;
    try {
      await axios.post(`${BASE_URL}/tool/${projectId}/tools`,{name: newTool },{
      headers: { Authorization: `Bearer ${token}` },
    });
      setNewTool("");
      await fetchTools();
    } catch (err) {
      alert('Error occured while adding modules');
    } 

   };

   /**
     * Deletes a tool by ID after confirmation.
     * Warns the user that deleting the tool will also delete related tasks.
     * Refetches both modules and tasks after deletion.
     *
     * @param {number} toolId - The ID of the tool to delete
     */
   const handleDeleteTool = async (toolId) => {
    if (!window.confirm("Deleting this tool will delete all the tasks using it.")) return;
    try {
      await axios.delete(`${BASE_URL}/tool/tools/${toolId}`,{
      headers: { Authorization: `Bearer ${token}` },
    });
    await fetchTools();
      clearfilter(); 
      setTools(tools.filter(t => t.id !== toolId))
      refresh();
      
    } catch (err) {
    alert('Could not delete tool');
    }
   };

  useEffect(() => {
    /**
     * Fetches tools when the projectId changes.
     */
    fetchTools();
  },[projectId]);

  
 return(
  <div className="tool-list-container">
    <h2 className="tool-list-heading">Modules</h2>

    {/* Only the admins or managers can add modules */}
    {(user.role === 'admin' || user.role === 'manager') && (
    <div className="tool-form">
      {/* Input for new tool */}
      <input
      type="text"
      value={newTool}
      onChange={(e) => setNewTool(e.target.value)}
      placeholder = "Module name"
      className="tool-input"
      />
      <button 
      onClick={handleAddTool}
      className = "tool-add-button"
      >
        +
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
      {tools.length === 0 && <p className="no-tools">No modules added</p>}
    </ul>
    {tools.length!== 0 && 
    <button className="clear-tool-filter" onClick={clearfilter}>Clear Filter</button>
    }
  </div>
 );
}


