import React, { useState } from 'react';
import './App.css';

function App() {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [pages, setPages] = useState([]);
  const [formData, setFormData] = useState({
    description: '',
    image_url: '',
    affiliate_url: '',
    hook_title: ''
  });
  const [loading, setLoading] = useState(false);

  const API_URL = 'http://localhost:5000';

  // Generate AI Hook Title
  const generateHook = async () => {
    if (!formData.description) {
      alert('Please enter a description');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/generate-hook`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ description: formData.description })
      });

      const data = await response.json();
      if (response.ok) {
        setFormData({ ...formData, hook_title: data.hook_title });
      } else {
        alert('Error generating hook: ' + data.error);
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Error generating hook');
    } finally {
      setLoading(false);
    }
  };

  // Create Hook Page
  const createPage = async () => {
    if (!formData.hook_title || !formData.description || !formData.image_url || !formData.affiliate_url) {
      alert('Please fill in all fields');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/pages`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      const data = await response.json();
      if (response.ok) {
        setPages([...pages, data]);
        alert(`✅ Page created!\n\nCopy this link to share:\n${data.page_url}`);
        setFormData({
          description: '',
          image_url: '',
          affiliate_url: '',
          hook_title: ''
        });
        setCurrentPage('dashboard');
        fetchPages();
      } else {
        alert('Error creating page: ' + data.error);
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Error creating page');
    } finally {
      setLoading(false);
    }
  };

  // Fetch all pages
  const fetchPages = async () => {
    try {
      const response = await fetch(`${API_URL}/api/pages`);
      const data = await response.json();
      setPages(data);
    } catch (error) {
      console.error('Error fetching pages:', error);
    }
  };

  React.useEffect(() => {
    fetchPages();
  }, []);

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    alert('✅ Copied to clipboard!');
  };

  return (
    <div className="App">
      <nav className="navbar">
        <div className="nav-container">
          <h1 className="logo">🎣 Hook Page Builder</h1>
          <div className="nav-buttons">
            <button
              className={`nav-btn ${currentPage === 'dashboard' ? 'active' : ''}`}
              onClick={() => setCurrentPage('dashboard')}
            >
              📊 Dashboard
            </button>
            <button
              className={`nav-btn ${currentPage === 'create' ? 'active' : ''}`}
              onClick={() => setCurrentPage('create')}
            >
              ➕ Create New
            </button>
          </div>
        </div>
      </nav>

      <div className="container">
        {/* Dashboard Page */}
        {currentPage === 'dashboard' && (
          <div className="dashboard">
            <h2>📊 Your Hook Pages</h2>
            {pages.length === 0 ? (
              <div className="empty-state">
                <p>No pages created yet</p>
                <button className="btn-primary" onClick={() => setCurrentPage('create')}>
                  Create Your First Page
                </button>
              </div>
            ) : (
              <div className="pages-grid">
                {pages.map((page) => (
                  <div key={page.page_id || page.id} className="page-card">
                    <img src={page.image_url} alt={page.hook_title} className="page-image" />
                    <div className="page-info">
                      <h3>{page.hook_title}</h3>
                      <p className="description">{page.description}</p>
                      <div className="page-stats">
                        <span>📧 Emails: {page.emails_captured || 0}</span>
                        <span>📅 {new Date(page.created_at).toLocaleDateString()}</span>
                      </div>
                      <div className="page-actions">
                        <button
                          className="btn-copy"
                          onClick={() => copyToClipboard(page.copy_url || page.page_url)}
                        >
                          📋 Copy Link
                        </button>
                        <a
                          href={page.copy_url || page.page_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="btn-preview"
                        >
                          👁️ Preview
                        </a>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Create Page */}
        {currentPage === 'create' && (
          <div className="create-page">
            <h2>➕ Create New Hook Page</h2>
            <div className="form-container">
              <div className="form-group">
                <label>Affiliate Link *</label>
                <input
                  type="url"
                  placeholder="https://example.com/affiliate?id=123"
                  value={formData.affiliate_url}
                  onChange={(e) => setFormData({ ...formData, affiliate_url: e.target.value })}
                />
              </div>

              <div className="form-group">
                <label>Image URL *</label>
                <input
                  type="url"
                  placeholder="https://example.com/image.jpg"
                  value={formData.image_url}
                  onChange={(e) => setFormData({ ...formData, image_url: e.target.value })}
                />
              </div>

              <div className="form-group">
                <label>Description *</label>
                <textarea
                  placeholder="Brief description of what you're promoting"
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  rows="4"
                />
              </div>

              <div className="form-group">
                <label>AI-Generated Hook Title *</label>
                <div className="hook-input-group">
                  <input
                    type="text"
                    placeholder="Click 'Generate Hook' to create title"
                    value={formData.hook_title}
                    onChange={(e) => setFormData({ ...formData, hook_title: e.target.value })}
                    disabled
                  />
                  <button
                    className="btn-generate"
                    onClick={generateHook}
                    disabled={loading}
                  >
                    {loading ? '⏳ Generating...' : '🤖 Generate Hook'}
                  </button>
                </div>
              </div>

              <div className="form-actions">
                <button
                  className="btn-primary"
                  onClick={createPage}
                  disabled={loading}
                >
                  {loading ? '⏳ Creating...' : '✅ Create Page'}
                </button>
                <button
                  className="btn-secondary"
                  onClick={() => {
                    setFormData({
                      description: '',
                      image_url: '',
                      affiliate_url: '',
                      hook_title: ''
                    });
                    setCurrentPage('dashboard');
                  }}
                >
                  ❌ Cancel
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
