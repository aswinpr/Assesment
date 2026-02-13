import { useEffect, useState } from "react";
import api from "../api/api";

function Leaderboard() {
  const [tests, setTests] = useState([]);
  const [selectedTest, setSelectedTest] = useState("");
  const [leaders, setLeaders] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchTests = async () => {
    const res = await api.get("/analytics/test-summary");
    setTests(res.data);
  };

  const fetchLeaderboard = async (testId) => {
    if (!testId) return;
    setLoading(true);
    try {
      const res = await api.get("/analytics/leaderboard", {
        params: { test_id: testId }
      });
      setLeaders(res.data);
    } catch (err) {
      console.error("Leaderboard error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTests();
  }, []);

  const handleTestChange = (e) => {
    const testId = e.target.value;
    setSelectedTest(testId);
    fetchLeaderboard(testId);
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.heading}>Leaderboard</h2>

      <div style={styles.filterBox}>
        <select
          value={selectedTest}
          onChange={handleTestChange}
          style={styles.select}
        >
          <option value="">Select Test</option>
          {tests.map((t) => (
            <option key={t.test_id} value={t.test_id}>
              {t.test_name}
            </option>
          ))}
        </select>
      </div>

      {loading && <p style={styles.loading}>Loading leaderboard...</p>}

      {!loading && leaders.length > 0 && (
        <div style={styles.tableWrapper}>
          
{/* Table */}
{!loading && leaders.length > 0 && (
  <table style={styles.table}>
    <thead>
      <tr>
        <th style={styles.th}>Rank</th>
        <th style={styles.th}>Student</th>
        <th style={styles.th}>Score</th>
        <th style={styles.th}>Correct</th>
        <th style={styles.th}>Incorrect</th>
        <th style={styles.th}>Skipped</th>
        <th style={styles.th}>Accuracy</th>
      </tr>
    </thead>
    <tbody>
      {leaders.map((l) => (
        <tr key={l.attempt_id} style={styles.tr}>
          <td style={styles.td}>
            <span style={styles.rankBadge}>{l.rank}</span>
          </td>

          <td style={{ ...styles.td, fontWeight: "600" }}>
            {l.student_name}
          </td>

          <td style={{ ...styles.td, fontWeight: "700" }}>
            {l.score}
          </td>

          <td style={{ ...styles.td, color: "#15803d", fontWeight: "600" }}>
            {l.correct}
          </td>

          <td style={{ ...styles.td, color: "#dc2626", fontWeight: "600" }}>
            {l.incorrect}
          </td>

          <td style={{ ...styles.td, color: "#a16207", fontWeight: "600" }}>
            {l.skipped}
          </td>

          <td style={{ ...styles.td, fontWeight: "600" }}>
            {l.accuracy?.toFixed(2)}%
          </td>
        </tr>
      ))}
    </tbody>
  </table>
)}


        </div>
      )}

      {!loading && selectedTest && leaders.length === 0 && (
        <p style={styles.noData}>No leaderboard data available</p>
      )}
    </div>
  );
}

const styles = {
  container: {
    padding: "40px",
    minHeight: "100vh",
    background: "#f4f7f6",
    fontFamily: "'Inter', sans-serif",
    color: "#1a1a1a"
  },
  heading: {
    fontSize: "26px",
    fontWeight: "700",
    marginBottom: "25px",
    color: "#111827"
  },
  filterBox: {
    marginBottom: "25px"
  },
  select: {
    padding: "12px 16px",
    borderRadius: "8px",
    border: "2px solid #e5e7eb",
    fontSize: "15px",
    minWidth: "250px",
    background: "#ffffff",
    color: "#374151",
    outline: "none"
  },
  loading: {
    color: "#4b5563",
    fontWeight: "500"
  },
  tableWrapper: {
    width: "100%",
    overflowX: "auto", // Enables horizontal scrolling
    borderRadius: "12px",
    boxShadow: "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
    background: "#ffffff",
    border: "1px solid #e5e7eb"
  },
  table: {
    width: "100%",
    borderCollapse: "collapse",
    minWidth: "800px", // Ensures scrollbar triggers on smaller screens
  },
  th: {
    textAlign: "left",
    padding: "16px",
    background: "#f8fafc",
    color: "#475569",
    fontSize: "12px",
    letterSpacing: "0.05em",
    textTransform: "uppercase",
    fontWeight: "700",
    borderBottom: "2px solid #e2e8f0",
    whiteSpace: "nowrap"
  },
  td: {
    padding: "16px",
    borderBottom: "1px solid #f1f5f9",
    fontSize: "14px",
    color: "#334155",
    whiteSpace: "nowrap"
  },
  tr: {
    transition: "background 0.2s"
  },
  rankBadge: {
    background: "#f1f5f9",
    padding: "4px 8px",
    borderRadius: "6px",
    fontWeight: "700",
    color: "#475569"
  },
  noData: {
    color: "#6b7280",
    marginTop: "20px"
  }
};

export default Leaderboard;