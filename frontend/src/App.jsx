import { BrowserRouter, Routes, Route } from "react-router-dom";
import AttemptsList from "./pages/AttemptsList";
import AttemptDetail from "./pages/AttemptDetail";
import Leaderboard from "./pages/Leaderboard";
import Navbar from "./components/Navbar";

function App() {
  return (
    <BrowserRouter>

      <Navbar />
      <Routes>
        
        <Route path="/" element={<AttemptsList />} />
        <Route path="/attempt/:id" element={<AttemptDetail />} />
        <Route path="/leaderboard" element={<Leaderboard />} />

      </Routes>
    </BrowserRouter>
  );
}

export default App;
