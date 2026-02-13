import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../api/api";

function AttemptDetail() {
  const { id } = useParams();
  const [attempt, setAttempt] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchAttempt = async () => {
    try {
      const res = await api.get(`/attempts/${id}`);
      setAttempt(res.data);
    } catch (err) {
      console.error("Error fetching attempt:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAttempt();
  }, [id]);

  if (loading) return <div style={{ padding: 40 }}>Loading...</div>;

  if (!attempt) return <div style={{ padding: 40 }}>Attempt not found</div>;

  return (
    <div style={{ padding: 40 }}>
      <h2>Attempt Detail</h2>

      <p><strong>Student:</strong> {attempt.student_name}</p>
      <p><strong>Test:</strong> {attempt.test_name}</p>
      <p><strong>Status:</strong> {attempt.status}</p>
      <p><strong>Score:</strong> {attempt.score ?? "-"}</p>

      <h3>Raw Payload</h3>
      <pre style={{
        background: "#434445",
        padding: 15,
        borderRadius: 8,
        overflowX: "auto"
      }}>
        {JSON.stringify(attempt.raw_payload, null, 2)}
      </pre>
    </div>
  );
}

export default AttemptDetail;
