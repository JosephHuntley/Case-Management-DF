import { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LoginPage from "./pages/Login";

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

  // TEMP: test fetch to confirm access token works end-to-end
  useEffect(() => {
    if (!accessToken) return;

    const fetchCases = async () => {
      try {
        const res = await fetch("/api/cases", {
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
    <Router>
      <Routes>
        <Route
          path="/login"
          element={<LoginPage accessToken={accessToken} setAccessToken={setAccessToken} />}
        />
        {/* protected routes go here, gated on accessToken */}
      </Routes>
    </Router>
  );
}

export default App;