import React from "react";
import styles from "../styles/styles";

function FileUpload({ onFileChange, loading, onGenerate }) {
  const handleInputChange = (e) => {
    const file = e.target.files[0];
    if (file && file.name.endsWith(".zip")) {
      onFileChange(file);
    } else {
      alert("Please upload a valid ZIP file.");
    }
  };

  return (
    <>
      <input
        type="file"
        accept=".zip"
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
