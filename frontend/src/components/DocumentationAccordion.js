import React, { useState } from "react";
import MarkdownPreview from "./MarkdownPreview";
import downloadMarkdown from "../utils/downloadMarkdown";
import styles from "../styles/styles";

function DocumentationAccordion({ documentation }) {
  const [activeFile, setActiveFile] = useState(null);

  const toggleFile = (filename) => {
    setActiveFile(activeFile === filename ? null : filename);
  };

  return (
    <div style={styles.accordion}>
      <h2>Generated Documentation:</h2>
      {Object.entries(documentation).map(([filename, doc], index) => (
        <div key={index} style={styles.accordionItem}>
          <div
            style={styles.accordionHeader}
            onClick={() => toggleFile(filename)}
          >
            {activeFile === filename ? "▼" : "▶"} {filename}
          </div>
          {activeFile === filename && (
            <div style={{...styles.accordionContent, backgroundColor: "white"}}>
              <MarkdownPreview doc={doc} />
            </div>
          )}
        </div>
      ))}
      <button
        onClick={() => downloadMarkdown(documentation)}
        style={styles.button}
      >
        Download Documentation (Markdown File)
      </button>
    </div>
  );
}

export default DocumentationAccordion;
