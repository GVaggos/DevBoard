import { Routes, Route, Navigate } from "react-router-dom"
import Login from "./pages/LoginPage.jsx"
import Register from "./pages/RegisterPage.jsx"
import Dashboard from "./pages/DashboardPage.jsx"

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      <Route
        path="/"
        element={<Navigate to="/login" replace />}
      />
      <Route path="/dashboard" element={<Dashboard />} />
    </Routes>
  )
}

export default App