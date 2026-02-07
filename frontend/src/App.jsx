import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from './components/navabar.jsx';
import DashboardPage from './pages/DashboardPage.jsx';

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<DashboardPage />} />
      </Routes>
    </Router>
  );
}

export default App