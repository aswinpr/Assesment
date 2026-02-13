import { useEffect, useState } from "react";
import api from "../api/api";
import { Link } from "react-router-dom";

function AttemptsList() {
  const [attempts, setAttempts] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  const [filters, setFilters] = useState({
    test_id: "",
    status: "",
    has_duplicates: "",
    search: ""
  });

  const fetchAttempts = async () => {
    const res = await api.get("/attempts", {
      params: {
        ...filters,
        page,
        per_page: 20
      }
    });

    const total = res.data.total;
    const perPage = 20;
    const computedTotalPages = Math.ceil(total / perPage);

    setAttempts(res.data.data);
    setTotalPages(computedTotalPages);
  };

  useEffect(() => {
    fetchAttempts();
  }, [page]);

  const handleChange = (e) => {
    setFilters({ ...filters, [e.target.name]: e.target.value });
  };

  // --- Readability-Focused Styling ---
  const containerStyle = {
    padding: "40px",
    backgroundColor: "#f8f9fa",
    minHeight: "100vh",
    fontFamily: "'Inter', -apple-system, sans-serif",
  };

  const headerStyle = {
    fontSize: "26px",
    fontWeight: "700",
    color: "#1a1a1a",
    marginBottom: "24px",
  };

  const filterContainerStyle = {
    display: "flex",
    gap: "15px",
    marginBottom: "30px",
    alignItems: "center",
    backgroundColor: "#ffffff",
    padding: "20px",
    borderRadius: "12px",
    boxShadow: "0 2px 4px rgba(0,0,0,0.04)",
  };

  const inputStyle = {
    padding: "12px 16px",
    borderRadius: "8px",
    border: "1px solid #d1d5db",
    backgroundColor: "#ffffff", 
    outline: "none",
    fontSize: "15px",
    width: "300px",
    color: "#374151",
  };

  const selectStyle = {
    padding: "12px 16px",
    borderRadius: "8px",
    border: "1px solid #d1d5db",
    backgroundColor: "#ffffff", 
    fontSize: "15px",
    cursor: "pointer",
    color: "#374151",
    minWidth: "160px",
  };

  const buttonStyle = {
    padding: "12px 24px",
    backgroundColor: "#007bff",
    color: "#ffffff",
    border: "none",
    borderRadius: "8px",
    fontWeight: "600",
    fontSize: "15px",
    cursor: "pointer",
    transition: "background 0.2s ease",
  };

  const tableStyle = {
    width: "100%",
    borderCollapse: "separate",
    borderSpacing: "0",
    backgroundColor: "#ffffff",
    borderRadius: "12px",
    boxShadow: "0 10px 15px -3px rgba(0, 0, 0, 0.1)",
    overflow: "hidden",
    border: "1px solid #e5e7eb",
  };

  const thStyle = {
    padding: "18px 24px",
    backgroundColor: "#f9fafb",
    color: "#4b5563",
    textAlign: "left",
    fontSize: "13px",
    textTransform: "uppercase",
    fontWeight: "700",
    letterSpacing: "0.05em",
    borderBottom: "2px solid #f3f4f6",
  };

  const tdStyle = {
    padding: "18px 24px",
    borderBottom: "1px solid #f3f4f6",
    fontSize: "15px",
    color: "#1f2937", // Darker text for better contrast
    lineHeight: "1.5",
  };

  const paginationButtonStyle = (disabled) => ({
    padding: "10px 20px",
    backgroundColor: disabled ? "#e5e7eb" : "#ffffff",
    color: disabled ? "#9ca3af" : "#374151",
    border: "1px solid #d1d5db",
    borderRadius: "8px",
    cursor: disabled ? "not-allowed" : "pointer",
    fontWeight: "600",
    fontSize: "14px",
    transition: "all 0.2s",
  });

  const statusBadgeStyle = (status) => {
    const colors = {
      SCORED: { bg: "#dcfce7", text: "#166534" },
      DEDUPED: { bg: "#fef9c3", text: "#854d0e" },
      FLAGGED: { bg: "#fee2e2", text: "#991b1b" },
    };
    const current = colors[status] || { bg: "#f3f4f6", text: "#374151" };
    return {
      padding: "6px 12px",
      borderRadius: "6px",
      fontSize: "12px",
      fontWeight: "700",
      backgroundColor: current.bg,
      color: current.text,
      display: "inline-block",
    };
  };

  const linkStyle = {
    color: "#2563eb",
    textDecoration: "none",
    fontWeight: "600",
  };

  return (
    <div style={containerStyle}>
      <h2 style={headerStyle}>Attempts List</h2>

      {/* Filters */}
      <div style={filterContainerStyle}>
        <input
          style={inputStyle}
          placeholder="Search student name..."
          name="search"
          onChange={handleChange}
        />

        <select style={selectStyle} name="status" onChange={handleChange}>
          <option value="">All Status</option>
          <option value="SCORED">SCORED</option>
          <option value="DEDUPED">DEDUPED</option>
          <option value="FLAGGED">FLAGGED</option>
        </select>

        <button
          style={buttonStyle}
          onClick={() => {
            setPage(1);
            fetchAttempts();
          }}
          onMouseOver={(e) => (e.target.style.backgroundColor = "#0056b3")}
          onMouseOut={(e) => (e.target.style.backgroundColor = "#007bff")}
        >
          Apply Filters
        </button>
      </div>

      {/* Table */}
      <div style={{ overflowX: "auto" }}>
        <table style={tableStyle}>
          <thead>
            <tr>
              <th style={thStyle}>Student</th>
              <th style={thStyle}>Test</th>
              <th style={thStyle}>Status</th>
              <th style={thStyle}>Score</th>
              <th style={thStyle}>Duplicate</th>
            </tr>
          </thead>
          <tbody>
            {attempts.map((a) => (
              <tr key={a.attempt_id} style={{ transition: "background 0.2s" }} 
                  onMouseOver={(e) => (e.currentTarget.style.backgroundColor = "#f9fafb")}
                  onMouseOut={(e) => (e.currentTarget.style.backgroundColor = "transparent")}>
                <td style={tdStyle}>
                  <Link to={`/attempt/${a.attempt_id}`} style={linkStyle}>
                    {a.student_name}
                  </Link>
                </td>
                <td style={tdStyle}>{a.test_name}</td>
                <td style={tdStyle}>
                  <span style={statusBadgeStyle(a.status)}>
                    {a.status}
                  </span>
                </td>
                <td style={{ ...tdStyle, fontWeight: "700", color: "#111827" }}>
                  {a.score ?? "-"}
                </td>
                <td style={tdStyle}>
                  {a.duplicate_of_attempt_id ? (
                    <span style={{ color: "#dc2626", fontWeight: "600", display: "flex", alignItems: "center", gap: "4px" }}>
                      ⚠️ Yes
                    </span>
                  ) : (
                    <span style={{ color: "#9ca3af" }}>No</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      <div style={{ marginTop: "30px", display: "flex", alignItems: "center", gap: "20px", justifyContent: "center" }}>
        <button
          style={paginationButtonStyle(page === 1)}
          disabled={page === 1}
          onClick={() => setPage(page - 1)}
        >
          ← Previous
        </button>

        <span style={{ fontWeight: "600", color: "#374151", fontSize: "15px" }}>
          Page {page} <span style={{ color: "#9ca3af", fontWeight: "400" }}>of</span> {totalPages}
        </span>

        <button
          style={paginationButtonStyle(page >= totalPages)}
          disabled={page >= totalPages}
          onClick={() => setPage(page + 1)}
        >
          Next →
        </button>
      </div>
    </div>
  );
}

export default AttemptsList;