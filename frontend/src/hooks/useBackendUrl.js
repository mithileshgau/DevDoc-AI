function useBackendUrl() {
    return process.env.NODE_ENV === "development"
      ? "http://localhost:3001"
      : "https://devdoc-ai-backend.onrender.com";
  }
  
  export default useBackendUrl;
  