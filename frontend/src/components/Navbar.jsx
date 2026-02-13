import { Link, useLocation } from "react-router-dom";

export default function Navbar() {
  const location = useLocation();

  const linkStyle = (path) => ({
    padding: "10px 18px",
    textDecoration: "none",
    color: location.pathname === path ? "#ffffff" : "#495057",
    background: location.pathname === path ? "#007bff" : "transparent",
    borderRadius: "20px", 
    fontWeight: "500",
    transition: "all 0.3s ease", 
  });

  const navbarContainerStyle = {
    display: "flex",
    justifyContent: "center", 
    alignItems: "center",
    gap: "15px", 
    padding: "15px 30px",
    borderBottom: "1px solid #e9ecef", 
    backgroundColor: "#ffffff",
    boxShadow: "0 2px 4px rgba(0, 0, 0, 0.05)", 
  };

  return (
    <div style={navbarContainerStyle}>
      <Link to="/" style={linkStyle("/")}>
        Attempts
      </Link>

      <Link to="/leaderboard" style={linkStyle("/leaderboard")}>
        Leaderboard
      </Link>

    </div>
  );
}
