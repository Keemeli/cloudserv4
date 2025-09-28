import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [name, setName] = useState('');
  const [info, setInfo] = useState(null);
  const [projects, setProjects] = useState(null);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState({});
  const [activeTab, setActiveTab] = useState('home');

  // API base URL - use relative path for production (proxied by nginx)
  const API_BASE = '/api';

  const fetchData = async (endpoint, setter, loadingKey) => {
    setLoading(prev => ({ ...prev, [loadingKey]: true }));
    try {
      const response = await axios.get(`${API_BASE}${endpoint}`);
      setter(response.data);
    } catch (error) {
      console.error(`Error fetching ${endpoint}:`, error);
      setter(null);
    } finally {
      setLoading(prev => ({ ...prev, [loadingKey]: false }));
    }
  };

  const fetchName = () => fetchData('/name', setName, 'name');
  const fetchInfo = () => fetchData('/info', setInfo, 'info');
  const fetchProjects = () => fetchData('/projects', setProjects, 'projects');
  const fetchStats = () => fetchData('/stats', setStats, 'stats');

  useEffect(() => {
    // Fetch initial data
    fetchName();
    fetchStats();
  }, []);

  const TabButton = ({ id, label, active, onClick }) => (
    <button
      className={`tab-button ${active ? 'active' : ''}`}
      onClick={() => onClick(id)}
    >
      {label}
    </button>
  );

  const LoadingSpinner = () => (
    <div className="loading">Loading...</div>
  );

  return (
    <div className="App">
      <header className="App-header">
        <h1>🚀 Eemeli Karjalainen's CSC Rahti Demo</h1>
        <p>Personal Multi-Container Application on OpenShift</p>
      </header>

      <nav className="tab-navigation">
        <TabButton id="home" label="🏠 Home" active={activeTab === 'home'} onClick={setActiveTab} />
        <TabButton id="info" label="ℹ️ Info" active={activeTab === 'info'} onClick={setActiveTab} />
        <TabButton id="projects" label="📁 Projects" active={activeTab === 'projects'} onClick={setActiveTab} />
        <TabButton id="api" label="🔗 API Test" active={activeTab === 'api'} onClick={setActiveTab} />
      </nav>

      <main className="main-content">
        {activeTab === 'home' && (
          <div className="tab-content">
            <div className="welcome-section">
              <h2>Welcome to my personal demonstration!</h2>
              <div className="name-card">
                <h3>👋 My Name</h3>
                {name ? (
                  <div className="name-result">
                    <p><strong>{name.name || name}</strong></p>
                    {name.message && <p className="message">{name.message}</p>}
                    {name.timestamp && (
                      <p className="timestamp">Retrieved: {new Date(name.timestamp).toLocaleString()}</p>
                    )}
                  </div>
                ) : (
                  <p>Click "Get My Name" to retrieve via API</p>
                )}
                <button 
                  onClick={fetchName} 
                  disabled={loading.name}
                  className="api-button"
                >
                  {loading.name ? 'Loading...' : '🔄 Get My Name via API'}
                </button>
              </div>

              <div className="features-grid">
                <div className="feature-card">
                  <h4>🏗️ Multi-Container</h4>
                  <p>Flask backend + React frontend + Redis coordination</p>
                </div>
                <div className="feature-card">
                  <h4>☁️ Cloud Native</h4>
                  <p>Deployed on CSC Rahti OpenShift platform</p>
                </div>
                <div className="feature-card">
                  <h4>🔄 Auto-Scaling</h4>
                  <p>Kubernetes HPA for handling traffic loads</p>
                </div>
                <div className="feature-card">
                  <h4>❤️ Health Monitoring</h4>
                  <p>Built-in health checks and readiness probes</p>
                </div>
              </div>
            </div>

            {stats && (
              <div className="stats-section">
                <h3>📊 Application Statistics</h3>
                <div className="stats-grid">
                  <div className="stat-item">
                    <span className="stat-label">Name API Calls:</span>
                    <span className="stat-value">{stats.name_requests}</span>
                  </div>
                  <div className="stat-item">
                    <span className="stat-label">Redis Status:</span>
                    <span className={`stat-value ${stats.redis_status === 'connected' ? 'success' : 'error'}`}>
                      {stats.redis_status}
                    </span>
                  </div>
                  <div className="stat-item">
                    <span className="stat-label">Last Name Request:</span>
                    <span className="stat-value">
                      {stats.last_name_request 
                        ? new Date(stats.last_name_request).toLocaleString() 
                        : 'Never'
                      }
                    </span>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'info' && (
          <div className="tab-content">
            <button onClick={fetchInfo} disabled={loading.info} className="refresh-button">
              {loading.info ? 'Loading...' : '🔄 Refresh System Info'}
            </button>
            
            {loading.info ? <LoadingSpinner /> : info && (
              <div className="info-sections">
                <div className="info-section">
                  <h3>👤 Personal Information</h3>
                  <div className="info-grid">
                    <div><strong>Name:</strong> {info.personal.name}</div>
                    <div><strong>Role:</strong> {info.personal.role}</div>
                    <div><strong>Course:</strong> {info.personal.course}</div>
                    <div><strong>University:</strong> {info.personal.university}</div>
                  </div>
                </div>

                <div className="info-section">
                  <h3>💻 System Information</h3>
                  <div className="info-grid">
                    <div><strong>Hostname:</strong> {info.system.hostname}</div>
                    <div><strong>Platform:</strong> {info.system.platform} {info.system.platform_release}</div>
                    <div><strong>Architecture:</strong> {info.system.architecture}</div>
                    <div><strong>Python Version:</strong> {info.system.python_version}</div>
                    <div><strong>Memory:</strong> {info.system.memory_available_gb}GB / {info.system.memory_total_gb}GB ({info.system.memory_percent}% used)</div>
                    <div><strong>Disk:</strong> {info.system.disk_free_gb}GB free / {info.system.disk_total_gb}GB total</div>
                  </div>
                </div>

                <div className="info-section">
                  <h3>🚀 Application Details</h3>
                  <div className="info-grid">
                    <div><strong>App Name:</strong> {info.application.name}</div>
                    <div><strong>Version:</strong> {info.application.version}</div>
                    <div><strong>Port:</strong> {info.application.port}</div>
                    <div><strong>Environment:</strong> {info.application.environment}</div>
                    <div><strong>Redis Connected:</strong> {info.application.redis_connected ? '✅ Yes' : '❌ No'}</div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'projects' && (
          <div className="tab-content">
            <button onClick={fetchProjects} disabled={loading.projects} className="refresh-button">
              {loading.projects ? 'Loading...' : '🔄 Load My Projects'}
            </button>
            
            {loading.projects ? <LoadingSpinner /> : projects && (
              <div className="projects-sections">
                <div className="projects-section">
                  <h3>🚀 My Projects</h3>
                  {projects.projects.map((project, index) => (
                    <div key={index} className="project-card">
                      <h4>{project.name}</h4>
                      <p>{project.description}</p>
                      <div className="tech-tags">
                        {project.technologies.map((tech, techIndex) => (
                          <span key={techIndex} className="tech-tag">{tech}</span>
                        ))}
                      </div>
                      <div className="project-status">Status: <span className="status-badge">{project.status}</span></div>
                      {project.achievements && (
                        <div className="achievements">
                          <h5>🏆 Achievements:</h5>
                          <ul>
                            {project.achievements.map((achievement, achIndex) => (
                              <li key={achIndex}>{achievement}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                      {project.topics && (
                        <div className="topics">
                          <h5>📚 Learning Topics:</h5>
                          <ul>
                            {project.topics.map((topic, topicIndex) => (
                              <li key={topicIndex}>{topic}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  ))}
                </div>

                <div className="skills-section">
                  <h3>🛠️ Skills & Technologies</h3>
                  <div className="skills-grid">
                    {projects.skills.map((skill, index) => (
                      <span key={index} className="skill-tag">{skill}</span>
                    ))}
                  </div>
                </div>

                <div className="contact-section">
                  <h3>📞 Contact</h3>
                  <p><strong>Name:</strong> {projects.contact.name}</p>
                  <p><em>{projects.contact.note}</em></p>
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'api' && (
          <div className="tab-content">
            <h3>🔗 API Testing Interface</h3>
            <div className="api-testing">
              <div className="api-buttons">
                <button onClick={fetchName} disabled={loading.name} className="api-button">
                  GET /api/name {loading.name && '(Loading...)'}
                </button>
                <button onClick={fetchInfo} disabled={loading.info} className="api-button">
                  GET /api/info {loading.info && '(Loading...)'}
                </button>
                <button onClick={fetchProjects} disabled={loading.projects} className="api-button">
                  GET /api/projects {loading.projects && '(Loading...)'}
                </button>
                <button onClick={fetchStats} disabled={loading.stats} className="api-button">
                  GET /api/stats {loading.stats && '(Loading...)'}
                </button>
              </div>

              <div className="api-endpoints">
                <h4>📋 Available Endpoints</h4>
                <div className="endpoint-list">
                  <div className="endpoint"><code>GET /api/name</code> - Returns "Eemeli Karjalainen"</div>
                  <div className="endpoint"><code>GET /api/info</code> - Personal and system information</div>
                  <div className="endpoint"><code>GET /api/projects</code> - My projects and achievements</div>
                  <div className="endpoint"><code>GET /api/health</code> - Health check endpoint</div>
                  <div className="endpoint"><code>GET /api/stats</code> - Application statistics</div>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>

      <footer className="App-footer">
        <p>
          Created by <strong>Eemeli Karjalainen</strong> for CSC Rahti demonstration | 
          Cloud Services Course | Multi-Container Architecture
        </p>
        <p>
          <a href="/api/health" target="_blank" rel="noopener noreferrer">Health Check</a> | 
          <a href="/api/name" target="_blank" rel="noopener noreferrer">Name API</a>
        </p>
      </footer>
    </div>
  );
}

export default App;
