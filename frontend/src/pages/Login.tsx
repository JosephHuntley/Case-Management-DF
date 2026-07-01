import "./Login.css"
import Button from "../components/Button/Button"
import { Lock, ShieldCheck, LockOpen, ShieldOff } from 'lucide-react'

function LoginPage() {
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    // Handle form submission logic here
  };

  const isSecure = window.location.protocol === 'https:'

  return (
    <section id="login-page">

      {isSecure? (
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
        <div>
          <label htmlFor="username">Username</label>
          <input type="text" id="username" name="username" required />
        </div>
        <div>
          <label htmlFor="password">Password</label>
          <input type="password" id="password" name="password" required />
        </div>
        <button type="button" id="forgot-password">Forgot password?</button>
        <Button text="Sign in" type="submit" />
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