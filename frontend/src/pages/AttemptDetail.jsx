import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../api/api";

function AttemptDetail() {
  const { id } = useParams();
  const [attempt, setAttempt] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showPayload, setShowPayload] = useState(false);
  const [flagReason, setFlagReason] = useState("");

  // ✅ NEW STATES
  const [recomputing, setRecomputing] = useState(false);
  const [flagging, setFlagging] = useState(false);
  const [toast, setToast] = useState("");

  const showToast = (message) => {
    setToast(message);
    setTimeout(() => setToast(""), 3000);
  };

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

  // ✅ UPDATED RECOMPUTE
  const handleRecompute = async () => {
    const confirmAction = window.confirm(
      "Are you sure you want to recompute this attempt?"
    );
    if (!confirmAction) return;

    try {
      setRecomputing(true);
      await api.post(`/attempts/${id}/recompute`);
      showToast("✅ Recomputed successfully");
      fetchAttempt();
    } catch (err) {
      showToast("❌ Failed to recompute");
    } finally {
      setRecomputing(false);
    }
  };

  const handleFlag = async () => {
    if (!flagReason.trim()) {
      showToast("⚠️ Please enter a reason");
      return;
    }

    try {
      setFlagging(true);
      await api.post(`/attempts/${id}/flag`, {
        reason: flagReason
      });
      setFlagReason("");
      showToast("🚩 Attempt flagged successfully");
      fetchAttempt();
    } catch (err) {
      showToast("❌ Failed to flag");
    } finally {
      setFlagging(false);
    }
  };

  if (loading) return <div style={styles.statusMsg}>Loading...</div>;
  if (!attempt) return <div style={styles.statusMsg}>Attempt not found</div>;

  return (
    <div style={styles.container}>
      <h2 style={styles.heading}>Attempt Detail</h2>

      {/* ✅ Toast */}
      {toast && <div style={styles.toast}>{toast}</div>}

      {/* Basic Info */}
      <div style={styles.card}>
        <p style={styles.text}><strong>Student:</strong> {attempt.student_name}</p>
        <p style={styles.text}><strong>Test:</strong> {attempt.test_name}</p>
        <p style={styles.text}>
          <strong>Status:</strong>{" "}
          <span style={styles.badge}>{attempt.status}</span>
        </p>
        <p style={styles.text}>
          <strong>Score:</strong> {attempt.score ?? "-"}
        </p>

        {/* ✅ RECOMPUTE BUTTON MOVED HERE */}
        <button
          style={{
            ...styles.button,
            background: "#0056b3",
            opacity: recomputing ? 0.6 : 1,
            cursor: recomputing ? "not-allowed" : "pointer"
          }}
          disabled={recomputing}
          onClick={handleRecompute}
        >
          {recomputing ? "Recomputing..." : "Recompute"}
        </button>
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
        {attempt.duplicate_of_attempt_id ? (
          <p>Duplicate of: {attempt.duplicate_of_attempt_id}</p>
        ) : (
          <p style={styles.mutedText}>No duplicates</p>
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
              <span style={styles.flagReason}>{f.reason}</span> —{" "}
              {new Date(f.created_at).toLocaleString()}
            </div>
          ))
        )}

        {/* Flag Action */}
        <div style={{ marginTop: "15px" }}>
          <input
            placeholder="Flag reason"
            value={flagReason}
            onChange={(e) => setFlagReason(e.target.value)}
            style={styles.input}
            disabled={flagging}
          />

          <button
            style={{
              ...styles.button,
              background: "#c82333",
              opacity: flagging ? 0.6 : 1,
              cursor: flagging ? "not-allowed" : "pointer"
            }}
            disabled={flagging}
            onClick={handleFlag}
          >
            {flagging ? "Flagging..." : "Flag"}
          </button>
        </div>
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
    </div>
  );
}

const styles = {
  container: {
    padding: "40px",
    background: "#f4f7f6",
    minHeight: "100vh",
    fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
    color: "#212529"
  },
  heading: { marginBottom: "20px" },
  subHeading: { borderBottom: "1px solid #eee", paddingBottom: "10px" },
  statusMsg: { padding: "40px", fontSize: "1.2rem", color: "#6c757d" },
  card: {
    background: "#ffffff",
    padding: "25px",
    borderRadius: "10px",
    marginBottom: "20px",
    boxShadow: "0 2px 8px rgba(0,0,0,0.08)"
  },
  text: { margin: "8px 0" },
  mutedText: { color: "#6c757d", fontStyle: "italic" },
  listItem: { padding: "8px 0", borderBottom: "1px solid #f8f9fa" },
  flagReason: { fontWeight: "600", color: "#d63384" },
  badge: {
    background: "#e7f1ff",
    color: "#007bff",
    padding: "2px 8px",
    borderRadius: "4px",
    fontWeight: "bold"
  },
  codeBlock: {
    background: "#212529",
    color: "#f8f9fa",
    padding: "15px",
    borderRadius: "6px",
    overflow: "auto",
    fontSize: "0.9rem",
    maxHeight: "400px",     
    scrollbarWidth: "thin" 
  },
  button: {
    padding: "10px 24px",
    borderRadius: "6px",
    border: "none",
    fontWeight: "600",
    color: "#fff",
    marginRight: "12px"
  },
  input: {
    padding: "10px",
    marginRight: "10px",
    borderRadius: "6px",
    border: "1px solid #ced4da",
    width: "250px"
  },
  toast: {
    background: "#212529",
    color: "#fff",
    padding: "10px 20px",
    borderRadius: "6px",
    marginBottom: "15px",
    display: "inline-block"
  }
};

export default AttemptDetail;
