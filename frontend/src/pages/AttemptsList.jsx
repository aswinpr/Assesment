import { useEffect, useState } from "react";
import api from "../api/api";
import { Link } from "react-router-dom";

function AttemptsList() {
  const [attempts, setAttempts] = useState([]);
  const [filters, setFilters] = useState({
    test_id: "",
    status: "",
    has_duplicates: "",
    search: ""
  });

  const fetchAttempts = async () => {
    const params = { ...filters };
    const res = await api.get("/attempts", { params });
    setAttempts(res.data.data);
  };

  useEffect(() => {
    fetchAttempts();
  }, []);

  const handleChange = (e) => {
    setFilters({ ...filters, [e.target.name]: e.target.value });
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Attempts List</h2>

      {/* Filters */}
      <div>
        <input
          placeholder="Search student"
          name="search"
          onChange={handleChange}
        />
        <select name="status" onChange={handleChange}>
          <option value="">All Status</option>
          <option value="SCORED">SCORED</option>
          <option value="DEDUPED">DEDUPED</option>
          <option value="FLAGGED">FLAGGED</option>
        </select>
        <button onClick={fetchAttempts}>Apply</button>
      </div>

      <table border="1" cellPadding="8" style={{ marginTop: "20px" }}>
        <thead>
          <tr>
            <th>Student</th>
            <th>Test</th>
            <th>Status</th>
            <th>Score</th>
            <th>Duplicate</th>
          </tr>
        </thead>
        <tbody>
          {attempts.map((a) => (
            <tr key={a.id}>
              <td>
                <Link to={`/attempt/${a.id}`}>
                  {a.student_name}
                </Link>
              </td>
              <td>{a.test_name}</td>
              <td>{a.status}</td>
              <td>{a.score ?? "-"}</td>
              <td>{a.duplicate_of_attempt_id ? "Yes" : "No"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default AttemptsList;
