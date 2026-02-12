import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import api from "../api/api";

function AttemptDetail() {
  const { id } = useParams();
  const [attempt, setAttempt] = useState(null);

  const fetchAttempt = async () => {
    const res = await api.get(`/attempts/${id}`);
    setAttempt(res.data);
  };

  useEffect(() => {
    fetchAttempt();
  }, []);

  const handleRecompute = async () => {
    await api.post(`/attempts/${id}/recompute`);
    fetchAttempt();
  };

  const handleFlag = async () => {
    await api.post(`/attempts/${id}/flag`, {
      reason: "Manual review from UI"
    });
    fetchAttempt();
  };

  if (!attempt) return <p>Loading...</p>;

  return (
    <div style={{ padding: "20px" }}>
      <h2>Attempt Detail</h2>

      <p>Status: {attempt.status}</p>
      <p>Score: {attempt.score?.final_score}</p>

      <button onClick={handleRecompute}>Recompute</button>
      <button onClick={handleFlag}>Flag</button>

      <h3>Raw Payload</h3>
      <pre>{JSON.stringify(attempt.raw_payload, null, 2)}</pre>
    </div>
  );
}

export default AttemptDetail;
