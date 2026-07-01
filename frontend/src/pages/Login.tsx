import "./Login.css"
import Button from "../components/Button/Button"
import { Lock, ShieldCheck, LockOpen, ShieldOff } from 'lucide-react'
import {useState} from "react"

type loginProps =  {
  accessToken: string | null;
  setAccessToken: (token: string | null) => void;
  refreshToken: string | null;
  setRefreshToken: (token: string | null) => void;
};

function LoginPage({accessToken, setAccessToken, refreshToken, setRefreshToken}: loginProps) {

  const [username, setUsername] = useState<string>("")
  const [password, setPassword] = useState<string>("")

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
  e.preventDefault();

  const body = new URLSearchParams({
    grant_type: "password",
    username: username,
    password: password,
  });

  const res = await fetch("/api/auth/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      "Accept": "application/json",
    },
    body: body.toString(),
  });

  const data = await res.json();

  if (data.access_token) {
    setAccessToken(data.access_token);
  }
  if (data.refresh_token) {
    setRefreshToken(data.refresh_token);
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