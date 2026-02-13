import { useEffect, useState } from "react";
import api from "../api/api";

function Leaderboard() {
  const [tests, setTests] = useState([]);
  const [selectedTest, setSelectedTest] = useState("");
  const [leaders, setLeaders] = useState([]);

  useEffect(() => {
    api.get("/analytics/test-summary").then((res) => {
      setTests(res.data);
    });
  }, []);

  const fetchLeaderboard = async (testId) => {
    const res = await api.get("/analytics/leaderboard", {
      params: { test_id: testId },
    });
    setLeaders(res.data);
  };

  // --- Styling Logic ---
  const containerStyle = {
    padding: "40px",
    backgroundColor: "#f8f9fa",
    minHeight: "100vh",
    fontFamily: "'Inter', sans-serif",
  };

  const headerStyle = {
    fontSize: "24px",
    fontWeight: "600",
    color: "#212529",
    marginBottom: "20px",
  };

  const selectContainerStyle = {
    marginBottom: "25px",
  };

  const selectStyle = {
    padding: "10px 15px",
    borderRadius: "8px",
    border: "1px solid #ced4da",
    backgroundColor: "#626060",
    fontSize: "14px",
    cursor: "pointer",
    minWidth: "250px",
    outline: "none",
    boxShadow: "0 2px 4px rgba(0,0,0,0.02)",
  };

  const tableStyle = {
    width: "100%",
    maxWidth: "800px", // Leaderboards usually look better slightly narrower
    borderCollapse: "separate",
    borderSpacing: "0",
    backgroundColor: "#ffffff",
    borderRadius: "12px",
    boxShadow: "0 4px 6px rgba(0, 0, 0, 0.05)",
    overflow: "hidden",
    border: "1px solid #e9ecef",
  };

  const thStyle = {
    padding: "15px 20px",
    backgroundColor: "#f1f3f5",
    color: "#495057",
    textAlign: "left",
    fontSize: "13px",
    textTransform: "uppercase",
    fontWeight: "600",
    borderBottom: "1px solid #dee2e6",
  };

  const tdStyle = {
    padding: "15px 20px",
    borderBottom: "1px solid #f1f3f5",
    fontSize: "15px",
    color: "#495057",
  };

  const rankBadgeStyle = (rank) => {
    const isTopThree = rank <= 3;
    return {
      display: "inline-block",
      width: "28px",
      height: "28px",
      lineHeight: "28px",
      textAlign: "center",
      borderRadius: "50%",
      fontWeight: "bold",
      fontSize: "13px",
      backgroundColor: rank === 1 ? "#FFD700" : rank === 2 ? "#C0C0C0" : rank === 3 ? "#CD7F32" : "transparent",
      color: isTopThree ? "#fff" : "#495057",
      textShadow: isTopThree ? "0px 1px 2px rgba(0,0,0,0.2)" : "none",
    };
  };

  return (
    <div style={containerStyle}>
      <h2 style={headerStyle}>Leaderboard</h2>

      <div style={selectContainerStyle}>
        <select
          style={selectStyle}
          value={selectedTest}
          onChange={(e) => {
            setSelectedTest(e.target.value);
            fetchLeaderboard(e.target.value);
          }}
        >
          <option value="">Select Test to View Results</option>
          {tests.map((t) => (
            <option key={t.test_id} value={t.test_id}>
              {t.test_name}
            </option>
          ))}
        </select>
      </div>

      {leaders.length > 0 ? (
        <table style={tableStyle}>
          <thead>
            <tr>
              <th style={thStyle}>Rank</th>
              <th style={thStyle}>Student</th>
              <th style={thStyle}>Score</th>
            </tr>
          </thead>
          <tbody>
            {leaders.map((l) => (
              <tr key={l.attempt_id}>
                <td style={tdStyle}>
                  <span style={rankBadgeStyle(l.rank)}>{l.rank}</span>
                </td>
                <td style={{ ...tdStyle, fontWeight: l.rank <= 3 ? "600" : "400" }}>
                  {l.student_name}
                </td>
                <td style={{ ...tdStyle, fontWeight: "bold", color: "#007bff" }}>
                  {l.score}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <div style={{ color: "#adb5bd", fontStyle: "italic", marginTop: "20px" }}>
          {selectedTest ? "No data found for this test." : "Please select a test to see the rankings."}
        </div>
      )}
    </div>
  );
}

export default Leaderboard;