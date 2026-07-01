import LoginPage from "./pages/Login"
import {useState} from "react"

function App() {
  const [accessToken, setAccessToken] = useState<string | null>(null)
  const [refreshToken, setRefreshToken] = useState<string | null>(null)

  const isLoggedIn = accessToken !== null || refreshToken !== null
  return (
    <div>
      {!isLoggedIn && (
        <LoginPage 
          accessToken={accessToken} 
          setAccessToken={setAccessToken} 
          refreshToken={refreshToken} 
          setRefreshToken={setRefreshToken} />
      )}

      {isLoggedIn && (
        <div>
          Logged in
        </div>
      )}

    </div>
  )
}

export default App
