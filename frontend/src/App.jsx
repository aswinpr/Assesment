import { useEffect, useState } from "react";
import api from "./api/client";

function App() {
  const [status, setStatus] = useState("loading...");

  useEffect(() => {
    api.get("/health")
      .then(res => {
        setStatus(res.data.status);
      })
      .catch(err => {
        console.error(err);
        setStatus("error");
      });
  }, []);

  return (
    <div style={{ padding: "20px", backgroundColor: "#3d66e3", minWidth: "100px", color: "white", }}>
      <h1>Assessment</h1>
      <p>Backend status: <b>{status}</b></p>
    </div>
  );
}

export default App;
