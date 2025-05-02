import React, { useState } from "react";
import logo from "./images/logo1.png";
import FileUpload from "./components/FileUpload";
import DocumentationAccordion from "./components/DocumentationAccordion";
import useBackendUrl from "./hooks/useBackendUrl";
import styles from "./styles/styles";

function App() {
  const [zipFile, setZipFile] = useState(null);
  const [documentation, setDocumentation] = useState({});
  const [loading, setLoading] = useState(false);

  const backendUrl = useBackendUrl();

  const handleFileChange = (file) => setZipFile(file);

  const handleGenerateDocs = async () => {
    if (!zipFile) {
      alert("Please upload a ZIP file first.");
      return;
    }
    setLoading(true);
    const formData = new FormData();
    formData.append("file", zipFile);

    try {
      const response = await fetch(`${backendUrl}/upload`, {
        method: "POST",
        body: formData,
      });
      if (!response.ok) throw new Error("Failed to generate documentation");
      const docs = await response.json();
      console.log("Generated documentation:", docs);
      
      setDocumentation(docs);
    } catch (error) {
      console.error("Error generating documentation:", error);
      alert("Failed to generate documentation");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div style={styles.pageBackground}></div>
      <div style={styles.container}>
        <img src={logo} alt="DevDoc AI" style={styles.logo} />
        <p style={styles.intro}>
          Upload a ZIP file containing your source code, and DevDoc AI will
          generate detailed documentation for your project. You can preview the
          documentation here and download it as a Markdown (.md) file.
        </p>
        <FileUpload
          onFileChange={handleFileChange}
          loading={loading}
          onGenerate={handleGenerateDocs}
        />
        {Object.keys(documentation).length > 0 && (
          <DocumentationAccordion documentation={documentation} />
        )}
      </div>
    </>
  );
}

export default App;
