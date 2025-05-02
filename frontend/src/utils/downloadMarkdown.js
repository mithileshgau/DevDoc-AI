function downloadMarkdown(documentation) {
    // replace ``` with space
    const content = Object.entries(documentation)
      .map(([filename, doc]) => `## ${filename}\n\n${doc}`)
      .join("\n\n");

    // replace ``` with space
    const updatedContent = content.replace(/```/g, " ");
  
    const blob = new Blob([updatedContent], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "documentation.md";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
  
  export default downloadMarkdown;
  