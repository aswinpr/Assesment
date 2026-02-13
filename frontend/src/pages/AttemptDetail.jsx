import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../api/api";

function AttemptDetail() {
  const { id } = useParams();
  const [attempt, setAttempt] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showPayload, setShowPayload] = useState(false);
  const [flagReason, setFlagReason] = useState("");

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

  const handleRecompute = async () => {
    await api.post(`/attempts/${id}/recompute`);
    fetchAttempt();
  };

  const handleFlag = async () => {
    await api.post(`/attempts/${id}/flag`, {
      reason: flagReason || "Manual review"
    });
    setFlagReason("");
    fetchAttempt();
  };

  if (loading) return <div style={styles.statusMsg}>Loading...</div>;
  if (!attempt) return <div style={styles.statusMsg}>Attempt not found</div>;

  return (
    <div style={styles.container}>
      <h2 style={styles.heading}>Attempt Detail</h2>

      {/* Basic Info */}
      <div style={styles.card}>
        <p style={styles.text}><strong>Student:</strong> {attempt.student_name}</p>
        <p style={styles.text}><strong>Test:</strong> {attempt.test_name}</p>
        <p style={styles.text}><strong>Status:</strong> <span style={styles.badge}>{attempt.status}</span></p>
        <p style={styles.text}><strong>Score:</strong> {attempt.score ?? "-"}</p>
      </div>

      {/* Score Breakdown */}
      <div style={styles.card}>
        <h3 style={styles.subHeading}>Score Breakdown</h3>
        <pre style={styles.codeBlock}>
          {JSON.stringify(attempt.raw_payload?.answers, null, 2)}
        </pre>
      </div>

      {/* Duplicate Thread */}
      <div style={styles.card}>
        <h3 style={styles.subHeading}>Duplicate Thread</h3>
        {attempt.duplicate_thread?.length === 0 ? (
          <p style={styles.mutedText}>No duplicates</p>
        ) : (
          attempt.duplicate_thread?.map(d => (
            <div key={d.id} style={styles.listItem}>
              ID: <strong>{d.id}</strong> — Status: {d.status}
            </div>
          ))
        )}
      </div>

      {/* Flags */}
      <div style={styles.card}>
        <h3 style={styles.subHeading}>Flags</h3>
        {attempt.flags.length === 0 ? (
          <p style={styles.mutedText}>No flags</p>
        ) : (
          attempt.flags.map(f => (
            <div key={f.id} style={styles.listItem}>
              <span style={styles.flagReason}>{f.reason}</span> — {new Date(f.created_at).toLocaleString()}
            </div>
          ))
        )}
      </div>

      {/* Raw Payload Collapsible */}
      <div style={styles.card}>
        <button
          style={{ ...styles.button, background: "#495057" }}
          onClick={() => setShowPayload(!showPayload)}
        >
          {showPayload ? "Hide Raw Payload" : "Show Raw Payload"}
        </button>

        {showPayload && (
          <pre style={{ ...styles.codeBlock, marginTop: "15px" }}>
            {JSON.stringify(attempt.raw_payload, null, 2)}
          </pre>
        )}
      </div>

      {/* Action Buttons */}
      <div style={styles.card}>
        <button
          style={{ ...styles.button, background: "#0056b3" }}
          onClick={handleRecompute}
        >
          Recompute
        </button>

        <input
          placeholder="Flag reason"
          value={flagReason}
          onChange={(e) => setFlagReason(e.target.value)}
          style={styles.input}
        />

        <button
          style={{ ...styles.button, background: "#c82333" }}
          onClick={handleFlag}
        >
          Flag
        </button>
      </div>
    </div>
  );
}

// Refined Styles for Readability
const styles = {
  container: {
    padding: "40px",
    background: "#f4f7f6",
    minHeight: "100vh",
    fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
    color: "#212529"
  },
  heading: { color: "#1a1d20", marginBottom: "20px" },
  subHeading: { marginTop: 0, color: "#343a40", borderBottom: "1px solid #eee", paddingBottom: "10px" },
  statusMsg: { padding: "40px", fontSize: "1.2rem", color: "#6c757d" },
  card: {
    background: "#ffffff",
    padding: "25px",
    borderRadius: "10px",
    marginBottom: "20px",
    boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
    border: "1px solid #e9ecef"
  },
  text: { margin: "8px 0", fontSize: "1rem", lineHeight: "1.5" },
  mutedText: { color: "#6c757d", fontStyle: "italic" },
  listItem: { padding: "8px 0", borderBottom: "1px solid #f8f9fa" },
  flagReason: { fontWeight: "600", color: "#d63384" },
  badge: { background: "#e7f1ff", color: "#007bff", padding: "2px 8px", borderRadius: "4px", fontWeight: "bold" },
  codeBlock: {
    background: "#212529",
    color: "#f8f9fa",
    padding: "15px",
    borderRadius: "6px",
    overflowX: "auto",
    fontSize: "0.9rem"
  },
  button: {
    padding: "10px 24px",
    borderRadius: "6px",
    border: "none",
    cursor: "pointer",
    fontWeight: "600",
    color: "#fff",
    marginRight: "12px",
    transition: "opacity 0.2s"
  },
  input: {
    padding: "10px",
    marginRight: "10px",
    borderRadius: "6px",
    border: "1px solid #ced4da",
    width: "250px"
  }
};

export default AttemptDetail;