import { useEffect, useState } from "react";
import api from "../api/api";

function Leaderboard() {
  const [tests, setTests] = useState([]);
  const [selectedTest, setSelectedTest] = useState("");
  const [leaders, setLeaders] = useState([]);

  useEffect(() => {
    api.get("/analytics/test-summary").then(res => {
      setTests(res.data);
    });
  }, []);

  const fetchLeaderboard = async (testId) => {
    const res = await api.get("/analytics/leaderboard", {
      params: { test_id: testId }
    });
    setLeaders(res.data);
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Leaderboard</h2>

      <select
        onChange={(e) => {
          setSelectedTest(e.target.value);
          fetchLeaderboard(e.target.value);
        }}
      >
        <option>Select Test</option>
        {tests.map(t => (
          <option key={t.test_id} value={t.test_id}>
            {t.test_name}
          </option>
        ))}
      </select>

      <table border="1" cellPadding="8" style={{ marginTop: "20px" }}>
        <thead>
          <tr>
            <th>Rank</th>
            <th>Student</th>
            <th>Score</th>
          </tr>
        </thead>
        <tbody>
          {leaders.map(l => (
            <tr key={l.attempt_id}>
              <td>{l.rank}</td>
              <td>{l.student_name}</td>
              <td>{l.score}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Leaderboard;
