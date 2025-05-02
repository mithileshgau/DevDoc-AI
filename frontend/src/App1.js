import React, { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

const defaultMarkdown = `
# Heading 1

## Heading 2

**Bold text**

*Italic text*

- List item 1
- List item 2

| Table | Example |
|-------|---------|
| Cell  | Cell    |

[GitHub](https://github.com)
`;

export default function App() {
  const [markdown, setMarkdown] = useState(defaultMarkdown);

  return (
    <div style={{ maxWidth: 700, margin: "2rem auto", fontFamily: "sans-serif" }}>
      <textarea
        style={{ width: "100%", height: 200, marginBottom: 20 }}
        value={markdown}
        onChange={e => setMarkdown(e.target.value)}
      />
      <div style={{ border: "1px solid #ccc", padding: 20, borderRadius: 8 }}>
        <ReactMarkdown remarkPlugins={[remarkGfm]}>
          {markdown}
        </ReactMarkdown>
      </div>
    </div>
  );
}
