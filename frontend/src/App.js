import React, { useState } from 'react';
import JSZip from 'jszip';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import logo from './img/logo1.png'; // Import the logo

function App() {
  const [zipFile, setZipFile] = useState(null);
  const [documentation, setDocumentation] = useState({});
  const [loading, setLoading] = useState(false);
  const [activeFile, setActiveFile] = useState(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.name.endsWith('.zip')) {
      setZipFile(file);
    } else {
      alert('Please upload a valid ZIP file.');
    }
  };

  const handleGenerateDocs = async () => {
    if (!zipFile) {
      alert('Please upload a ZIP file first.');
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append('file', zipFile);

    try {
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to generate documentation');
      }

      const docs = await response.json();
      setDocumentation(docs);
    } catch (error) {
      console.error('Error generating documentation:', error);
      alert('Failed to generate documentation');
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = () => {
    const content = Object.entries(documentation)
      .map(([filename, doc]) => `## ${filename}\n\n${doc}`)
      .join('\n\n');

    const blob = new Blob([content], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'documentation.md';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const toggleFile = (filename) => {
    setActiveFile(activeFile === filename ? null : filename);
  };

  const styles = {
    container: {
      maxWidth: '800px',
      margin: '0 auto',
      padding: '50px 25px',
      fontFamily: 'Segoe UI, sans-serif',
      backgroundColor: '#ffffff',
      borderRadius: '16px',
      boxShadow: '0 8px 20px rgba(0, 0, 0, 0.1)',
      backgroundImage: 'linear-gradient(to bottom right, #f0f4f8, #e2ebf0)',
      position: 'relative',
      zIndex: 1,
    },
    pageBackground: {
      position: 'fixed',
      top: 0,
      left: 0,
      width: '100%',
      height: '100%',
      backgroundImage: 'linear-gradient(to bottom, #e2ebf0, #cbd5e0)',
      zIndex: 0,
    },
    logo: {
      display: 'block',
      margin: '0 auto 30px',
      width: '200px', // Increased size
      height: 'auto',
    },
    header: {
      textAlign: 'center',
      color: '#1a202c',
      fontSize: '32px',
      marginBottom: '30px',
    },
    input: {
      display: 'block',
      margin: '20px auto',
      padding: '12px',
      borderRadius: '6px',
      border: '1px solid #cbd5e0',
      backgroundColor: '#edf2f7',
      width: '100%',
      maxWidth: '400px',
    },
    button: {
      display: 'block',
      margin: '15px auto',
      padding: '12px 24px',
      backgroundColor: '#3182ce',
      color: '#fff',
      border: 'none',
      borderRadius: '6px',
      cursor: 'pointer',
      transition: 'background-color 0.3s ease',
    },
    buttonHover: {
      backgroundColor: '#2b6cb0',
    },
    accordion: {
      marginTop: '30px',
    },
    accordionItem: {
      marginBottom: '12px',
      border: '1px solid #cbd5e0',
      borderRadius: '6px',
      overflow: 'hidden',
      backgroundColor: '#f7fafc',
    },
    accordionHeader: {
      padding: '12px 16px',
      backgroundColor: '#e2e8f0',
      cursor: 'pointer',
      fontWeight: 'bold',
      transition: 'background-color 0.2s ease',
    },
    accordionContent: {
      padding: '14px 16px',
      backgroundColor: '#ffffff',
      whiteSpace: 'pre-wrap',
      fontFamily: 'monospace',
      fontSize: '14px',
      color: '#2d3748',
    },
  };

  return (
    <>
      <div style={styles.pageBackground}></div>
      <div style={styles.container}>
        <img src={logo} alt="DevDoc AI" style={styles.logo} />
        {/* <h1 style={styles.header}>DevDoc AI</h1> */}
        <p style={{ textAlign: 'center', color: '#4a5568', fontSize: '18px', marginBottom: '20px' }}>
          Upload a ZIP file containing your source code, and DevDoc AI will generate detailed documentation for your project. 
          You can preview the documentation here and download it as a Markdown (.md) file.
        </p>
        <input type="file" accept=".zip" onChange={handleFileChange} style={styles.input} />
        <button onClick={handleGenerateDocs} disabled={loading} style={styles.button}>
          {loading ? 'Processing...' : 'Generate Documentation'}
        </button>

        {Object.keys(documentation).length > 0 && (
          <div style={styles.accordion}>
            <h2>Generated Documentation:</h2>
            {Object.entries(documentation).map(([filename, doc], index) => (
              <div key={index} style={styles.accordionItem}>
                <div
                  style={styles.accordionHeader}
                  onClick={() => toggleFile(filename)}
                >
                  {activeFile === filename ? '▼' : '▶'} {filename}
                </div>
                {activeFile === filename && (
                  <div style={styles.accordionContent}>
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                      {doc}
                    </ReactMarkdown>
                  </div>
                )}
              </div>
            ))}
            <button onClick={handleDownload} style={styles.button}>
              Download Documentation (Markdown File)
            </button>
          </div>
        )}
      </div>
    </>
  );
}

export default App;