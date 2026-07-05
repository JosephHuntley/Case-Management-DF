import "./Login.css"
import Button from "../components/Button/Button"
import { Lock, ShieldCheck, LockOpen, ShieldOff } from 'lucide-react'
import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import { useAuth } from "../context/AuthContext"

function LoginPage() {
  const { login, isAuthenticated, error } = useAuth();
  const [username, setUsername] = useState<string>("")
  const [password, setPassword] = useState<string>("")
  const [submitting, setSubmitting] = useState<boolean>(false);
  const navigate = useNavigate();

  useEffect(() => {
    if (isAuthenticated) {
      navigate("/", { replace: true });
    }
  }, [isAuthenticated, navigate]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await login(username, password);
      navigate('/dashboard');
    } catch {
      // AuthContext already set `error` with a user-facing message
      // (invalid credentials vs. rate-limited). Nothing else to do here.
    } finally {
      setSubmitting(false);
    }
  };

  const isSecure = window.location.protocol === 'https:'

  return (
    <section id="login-page">
      {isSecure ? (
        <div className="login-icon-badge" aria-label="Lock icon indicating secure login">
          <ShieldCheck size={48} color="var(--color-primary)" />
        </div>
      ) : (
        <div className="login-icon-badge" aria-label="Lock icon indicating insecure login">
          <ShieldOff size={48} color="var(--color-danger)" />
        </div>
      )}
      <div className="login-header">
        <h1 className="primary-text">Case Management DF</h1>
        <p className="secondary-text">Sign in to your account</p>
      </div>
      <form id="login-form" onSubmit={handleSubmit}>
        {error && <p style={{ color: "var(--color-danger)" }}>{error}</p>}
        <div>
          <label htmlFor="username">Username</label>
          <input onChange={(e: React.ChangeEvent<HTMLInputElement>) => setUsername(e.target.value)} type="text" id="username" name="username" required />
        </div>
        <div>
          <label htmlFor="password">Password</label>
          <input onChange={(e: React.ChangeEvent<HTMLInputElement>) => setPassword(e.target.value)} type="password" id="password" name="password" required />
        </div>
        <button type="button" id="forgot-password">Forgot password?</button>
        <Button text={submitting ? "Signing in…" : "Sign in"} type="submit" />
      </form>
      {
        isSecure ? (
          <div id="secured-connection">
            <Lock size={14} color="var(--text-secondary)" />
            <span>Secured connection over HTTPS</span>
          </div>
        ) : (
          <div id="secured-connection">
            <LockOpen size={14} color="var(--color-danger)" />
            <span style={{ color: "var(--color-danger)" }}>Insecure connection over HTTP</span>
          </div>
        )
      }
      <p className="secondary-text">Access restricted to authorized users only</p>
    </section>
  )
}
export default LoginPage