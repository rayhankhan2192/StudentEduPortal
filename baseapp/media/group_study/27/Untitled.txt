import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './StudyGroup.css';

function StudyGroup() {
  const [groups, setGroups] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [username, setUsername] = useState('User');
  const navigate = useNavigate();

  // Get username from localStorage (set during login)
  useEffect(() => {
    const storedUsername = localStorage.getItem('username');
    if (storedUsername) {
      setUsername(storedUsername);
    }
  }, []);

  // Function to fetch groups from the REST API
  const fetchGroups = async () => {
    const token = localStorage.getItem('token'); // Get the token from localStorage
    if (!token) {
      setError('No token found');
      setLoading(false);
      return;
    }

    try {
      const response = await fetch('http://127.0.0.1:8000/api/study/join-studygroup/list-all/', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`, // Include the token for authentication
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        setGroups(data); // Set the data returned by the API
      } else {
        setError('Failed to fetch groups');
      }
    } catch (error) {
      setError('An error occurred while fetching the groups');
    } finally {
      setLoading(false);
    }
  };

  // Fetch groups on component mount
  useEffect(() => {
    fetchGroups();
  }, []);

  // Function to handle copying the invite code
  const handleCopyInviteCode = (inviteCode) => {
    navigator.clipboard.writeText(inviteCode)
      .then(() => {
        alert('Invite code copied to clipboard!');
      })
      .catch((err) => {
        alert('Failed to copy invite code: ', err);
      });
  };

  if (loading) {
    return (
      <div className="study-group-loading">
        <div className="loading-spinner"></div>
        <p>Loading your study groups...</p>
      </div>
    );
  }

  return (
    <div className="study-group-page-container">
      {/* Sidebar */}
      <div className="study-group-sidebar">
        <div className="sidebar-header">
          <h3>Welcome, {username}</h3>
        </div>
        <nav className="sidebar-nav">
          <button 
            className="sidebar-btn"
            onClick={() => navigate('/user-dashboard')}
          >
            ← Back to Dashboard
          </button>
          <button 
            className="sidebar-btn active"
            onClick={() => navigate('/study-group')}
          >
            📚 My Study Groups
          </button>
          <button 
            className="sidebar-btn"
            onClick={() => navigate('/group-chat')}
          >
            💬 Group Chats
          </button>
        </nav>
      </div>

      {/* Main Content */}
      <div className="study-group-main-content">
        <div className="study-group-header">
          <h1>Study Groups</h1>
          <div className="group-buttons">
            <button 
              className="small-btn create-group-btn"
              onClick={() => navigate('/create-study-group')}
            >
              Create New Group
            </button>
            <button 
              className="small-btn join-group-btn"
              onClick={() => navigate('/join-study-group')}
            >
              Join Study Group
            </button>
          </div>
        </div>

        <div className="groups-list">
          {groups.map((group) => (
            <div key={group.id} className="group-card">
              <div className="group-info">
                <h3>{group.groupName}</h3>
                <span>🕒 Last Update {new Date(group.updated_at).toLocaleDateString()}</span>
                <div className="group-meta">
                  <span>👥 {group.members.length} members</span>
                  <span>🕒 Created {new Date(group.created_at).toLocaleDateString()}</span>
                </div>
              </div>
              <div className="group-actions">
                <button 
                  className="view-btn"
                  onClick={() => navigate(`/group-chat/${group.id}`)}
                >
                  View
                </button>
                <button 
                  className="copy-invite-btn"
                  onClick={() => handleCopyInviteCode(group.invite_code)}
                >
                  Copy Invite Code
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default StudyGroup;
