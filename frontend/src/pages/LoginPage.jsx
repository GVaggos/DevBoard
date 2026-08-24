import { useState } from "react"
import {
  ArrowRight,
  CheckCircle2,
  LockKeyhole,
  UserRound,
} from "lucide-react"
import { Link, useNavigate } from "react-router-dom"

function Login() {const navigate = useNavigate()
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (event) => {
    event.preventDefault()

    setError("")
    setLoading(true)

    try {
      const response = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username,
          password,
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || "Login failed")
      }

      localStorage.setItem("access_token", data.access_token)
      localStorage.setItem("user", JSON.stringify(data.user))

      navigate("/dashboard")
    } catch (error) {
      setError(error.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="auth-page">
      <section className="auth-shell">
        <div className="auth-hero">
          <div className="brand">
            <div className="brand-mark">D</div>
            <span>DevBoard</span>
          </div>

          <div className="auth-hero-content">
            <span className="eyebrow">WORK SMARTER</span>

            <h1>
              Keep your projects
              <br />
              moving forward.
            </h1>

            <p>
              A clean workspace for organizing projects,
              managing tasks and staying focused.
            </p>

            <div className="feature-list">
              <div>
                <CheckCircle2 size={18} />
                Organize projects in one place
              </div>

              <div>
                <CheckCircle2 size={18} />
                Track tasks and priorities
              </div>

              <div>
                <CheckCircle2 size={18} />
                Focus on what matters
              </div>
            </div>
          </div>

          <p className="auth-hero-footer">
            Simple. Focused. Productive.
          </p>
        </div>

        <div className="auth-form-side">
          <div className="mobile-brand">
            <div className="brand-mark">D</div>
            <span>DevBoard</span>
          </div>

          <div className="auth-card">
            <div className="auth-heading">
              <span className="auth-label">WELCOME BACK</span>
              <h2>Sign in to DevBoard</h2>
              <p>
                Enter your details to continue to your workspace.
              </p>
            </div>

            <form
              className="auth-form"
              onSubmit={handleSubmit}
            >
              <label>
                Username

                <div className="input-wrapper">
                  <UserRound size={18} />

                  <input
                    type="text"
                    placeholder="Enter your username"
                    value={username}
                    onChange={(event) =>
                      setUsername(event.target.value)
                    }
                    required
                  />
                </div>
              </label>

              <label>
                Password

                <div className="input-wrapper">
                  <LockKeyhole size={18} />

                  <input
                    type="password"
                    placeholder="Enter your password"
                    value={password}
                    onChange={(event) =>
                      setPassword(event.target.value)
                    }
                    required
                  />
                </div>
              </label>

              {error && (
                <p className="auth-error">
                  {error}
                </p>
              )}

              <button
                className="primary-button"
                type="submit"
                disabled={loading}
              >
                {loading ? "Signing in..." : "Sign in"}

                {!loading && <ArrowRight size={18} />}
              </button>
            </form>

            <p className="auth-switch">
  New to DevBoard?{" "}
  <Link to="/register">Create an account</Link>
              </p>
          </div>
        </div>
      </section>
    </main>
  )
}

export default Login