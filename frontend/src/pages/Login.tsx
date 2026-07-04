import "./Login.css"
import Button from "../components/Button/Button"
import { Lock, ShieldCheck, LockOpen, ShieldOff } from 'lucide-react'
import {useState} from "react"

type loginProps =  {
  accessToken: string | null;
  setAccessToken: (token: string | null) => void;
};

function LoginPage({accessToken, setAccessToken}: loginProps) {

  const [username, setUsername] = useState<string>("")
  const [password, setPassword] = useState<string>("")
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
  e.preventDefault();
  setError(null);
  setLoading(true);

  const body = new URLSearchParams({
    grant_type: "password",
    username: username,
    password: password,
  });

  try {
    const res = await fetch("/api/auth/login", {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
      },
      body: body.toString(),
    });

    if (!res.ok) {
      const errData = await res.json().catch(() => null);
      setError(errData?.detail ?? "Invalid username or password");
      return;
    }

    const data = await res.json();
    setAccessToken(data.access_token);
  } catch (err) {
    setError("Unable to reach the server. Check your connection.");
  } finally {
    setLoading(false);
  }
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
        {error && <p style={{ color: "var(--color-danger)" }}>{error}</p>}
        <div>
          <label htmlFor="username">Username</label>
          <input onChange={(e: React.ChangeEvent<HTMLInputElement>) => setUsername(e.target.value)} type="text" id="username" name="username" required />
        </div>
        <div>
          <label htmlFor="password">Password</label>
          <input onChange={(e:React.ChangeEvent<HTMLInputElement>) => setPassword(e.target.value)} type="password" id="password" name="password" required />
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