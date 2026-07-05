import { Navigate } from "react-router-dom";
import type { ReactNode } from "react";

type ProtectedRouteProps = {
  accessToken: string | null;
  children: ReactNode;
};

// Wrap any route element that requires auth: <ProtectedRoute accessToken={accessToken}><Dashboard /></ProtectedRoute>
// Redirects to /login if there's no accessToken. Since App.tsx doesn't render
// its <Routes> until the initial refresh-token check (authChecked) resolves,
// this never fires a false-positive redirect while that check is still in flight.
function ProtectedRoute({ accessToken, children }: ProtectedRouteProps) {
  if (!accessToken) {
    return <Navigate to="/login" replace />;
  }
  return <>{children}</>;
}

export default ProtectedRoute;