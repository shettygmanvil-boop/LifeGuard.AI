import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Predict from "./pages/Predict";
import Dashboard from "./pages/Dashboard";
import Hospitals from "./pages/Hospitals";
import Profile from "./pages/Profile";
import Smartwatch from "./pages/Smartwatch";

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <div className="min-h-screen bg-slate-900 text-slate-100">
          <Navbar />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/predict" element={<Predict />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/hospitals" element={<Hospitals />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/smartwatch" element={<Smartwatch />} />
          </Routes>
        </div>
      </BrowserRouter>
    </AuthProvider>
  );
}
