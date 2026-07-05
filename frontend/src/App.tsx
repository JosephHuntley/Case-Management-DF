import { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import LoginPage from "./pages/Login";
import ProtectedRoute from "./components/ProtectedRoute/ProtectedRoute";
import DashboardWrapper from "./components/DashboardWrapper/DashboardWrapper";
import Dashboard from "./pages/dashboard/Dashboard";
import Cases from "./pages/cases/Cases"
import Evidence from "./pages/evidence/Evidence";
import ChainOfCustody from "./pages/chainOfCustody/ChainOfCustody";
import Reports from "./pages/reports/Reports"
import UsersRoles from "./pages/Users_Roles/UsersRoles";

function App() {
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [authChecked, setAuthChecked] = useState(false);

  useEffect(() => {
    const tryRefresh = async () => {
      try {
        const res = await fetch("/api/auth/refresh", {
          method: "POST",
          credentials: "include",
        });
        if (res.ok) {
          const data = await res.json();
          setAccessToken(data.access_token);
        }
      } finally {
        setAuthChecked(true);
      }
    };
    tryRefresh();
  }, []);

  useEffect(() => {
    if (!accessToken) return;

    const fetchCases = async () => {
      try {
        const res = await fetch("/api/cases/", {
          credentials: "include",
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        if (!res.ok) {
          console.error("Failed to fetch cases:", res.status);
          return;
        }
        const data = await res.json();
        console.log("Cases:", data);
      } catch (err) {
        console.error("Error fetching cases:", err);
      }
    };

    fetchCases();
  }, [accessToken]);

  if (!authChecked) {
    return <div>Loading...</div>; 
  }

  return (
    // AuthProvider must wrap the Router: Sidebar (and anything else using
    // useAuth()) renders inside these routes, so the context needs to be
    // above them in the tree or useAuth() throws.
    //
    // NOTE: this file still tracks its own accessToken/authChecked state
    // and calls /api/auth/refresh directly (above), which now duplicates
    // what AuthContext already does internally. ProtectedRoute currently
    // takes accessToken as a prop — once you're ready, it's worth switching
    // ProtectedRoute to read { isAuthenticated, isLoading } from useAuth()
    // instead, and removing the accessToken/authChecked state and the two
    // useEffects above entirely. Left as-is here since I haven't seen
    // ProtectedRoute.tsx yet.
    <AuthProvider>
      <Router>
        <Routes>
          <Route
            path="/login"
            element={<LoginPage />}
          />
          <Route
            path="/"
            element={
              <ProtectedRoute accessToken={accessToken}>
                <DashboardWrapper>
                  <Dashboard/>
                </DashboardWrapper>
              </ProtectedRoute>
            }
          />

         <Route 
          path="/cases"
          element={
            <ProtectedRoute accessToken={accessToken}>
              <DashboardWrapper>
                <Cases/>
              </DashboardWrapper>
            </ProtectedRoute>
          }
          />

          <Route 
          path="/evidence"
          element={
            <ProtectedRoute accessToken={accessToken}>
              <DashboardWrapper>
                <Evidence/>
              </DashboardWrapper>
            </ProtectedRoute>
          }
          />

          <Route 
          path="/chainofcustody"
          element={
            <ProtectedRoute accessToken={accessToken}>
              <DashboardWrapper>
                <ChainOfCustody/>
              </DashboardWrapper>
            </ProtectedRoute>
          }
          />

          <Route 
          path="/reports"
          element={
            <ProtectedRoute accessToken={accessToken}>
              <DashboardWrapper>
                <Reports/>
              </DashboardWrapper>
            </ProtectedRoute>
          }
          />

          <Route 
          path="/users-roles"
          element={
            <ProtectedRoute accessToken={accessToken}>
              <DashboardWrapper>
                <UsersRoles/>
              </DashboardWrapper>
            </ProtectedRoute>
          }
          />

        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;