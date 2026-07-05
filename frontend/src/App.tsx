import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
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
  return (
    <AuthProvider>
      <Router>
        <AppRoutes />
      </Router>
    </AuthProvider>
  );
}

function AppRoutes() {
  const { isLoading } = useAuth();

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <Routes>
      <Route
        path="/login"
        element={<LoginPage />}
      />
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <DashboardWrapper>
              <Dashboard/>
            </DashboardWrapper>
          </ProtectedRoute>
        }
      />

     <Route 
      path="/cases"
      element={
        <ProtectedRoute>
          <DashboardWrapper>
            <Cases/>
          </DashboardWrapper>
        </ProtectedRoute>
      }
      />

      <Route 
      path="/evidence"
      element={
        <ProtectedRoute>
          <DashboardWrapper>
            <Evidence/>
          </DashboardWrapper>
        </ProtectedRoute>
      }
      />

      <Route 
      path="/chainofcustody"
      element={
        <ProtectedRoute>
          <DashboardWrapper>
            <ChainOfCustody/>
          </DashboardWrapper>
        </ProtectedRoute>
      }
      />

      <Route 
      path="/reports"
      element={
        <ProtectedRoute>
          <DashboardWrapper>
            <Reports/>
          </DashboardWrapper>
        </ProtectedRoute>
      }
      />

      <Route 
      path="/users-roles"
      element={
        <ProtectedRoute>
          <DashboardWrapper>
            <UsersRoles/>
          </DashboardWrapper>
        </ProtectedRoute>
      }
      />

    </Routes>
  );
}

export default App;