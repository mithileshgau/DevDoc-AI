import React from "react";
import styles from "../styles/styles";

function FileUpload({ onFileChange, loading, onGenerate }) {
  const handleInputChange = (e) => {
    const files = e.target.files; // Get all selected files
    if (files.length > 0) {
      onFileChange(files); // Pass the files to the parent component
    } else {
      alert("Please upload at least one valid file.");
    }
  };

  return (
    <>
      <input
        type="file"
        accept=".py,.js,.ts,.java,.sql,.json,.yaml,.yml,.html,.xml" // Accept multiple code file types
        multiple // Allow multiple file selection
        onChange={handleInputChange}
        style={styles.input}
      />
      <button
        onClick={onGenerate}
        disabled={loading}
        style={styles.button}
      >
        {loading ? "Processing..." : "Generate Documentation"}
      </button>
    </>
  );
}

export default FileUpload;