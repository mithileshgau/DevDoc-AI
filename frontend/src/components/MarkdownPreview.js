import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import "github-markdown-css/github-markdown.css"; // Import GitHub CSS

function cleanMarkdown(md) {

    // replace ``` with space
    md = md.replace(/```/g, " ");
    return md;
}

function MarkdownPreview({ doc }) {
  const cleaned = cleanMarkdown(doc);
  return (
    <div className="markdown-body" style={{ padding: "16px" }}>
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{cleaned}</ReactMarkdown>
    </div>
  );
}

export default MarkdownPreview;
