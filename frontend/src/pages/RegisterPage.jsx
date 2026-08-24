import { useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import {
  ArrowRight,
  CheckCircle2,
  LockKeyhole,
  Mail,
  UserRound,
} from "lucide-react"

function Register() {
  const navigate = useNavigate()

  const [username, setUsername] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (event) => {
    event.preventDefault()

    setError("")
    setLoading(true)

    try {
      const response = await fetch("http://127.0.0.1:8000/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username,
          email,
          password,
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || "Registration failed")
      }

      alert("Account created successfully!")
      navigate("/login")
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
            <span className="eyebrow">GET STARTED</span>

            <h1>
              Turn your ideas
              <br />
              into progress.
            </h1>

            <p>
              Create your workspace and keep your projects,
              tasks and priorities organized.
            </p>

            <div className="feature-list">
              <div>
                <CheckCircle2 size={18} />
                Create and manage projects
              </div>

              <div>
                <CheckCircle2 size={18} />
                Organize your daily tasks
              </div>

              <div>
                <CheckCircle2 size={18} />
                Track your progress
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
              <span className="auth-label">JOIN DEVBOARD</span>
              <h2>Create your account</h2>
              <p>
                Start organizing your projects in one clean workspace.
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
                    placeholder="Choose a username"
                    value={username}
                    onChange={(event) =>
                      setUsername(event.target.value)
                    }
                    required
                  />
                </div>
              </label>

              <label>
                Email

                <div className="input-wrapper">
                  <Mail size={18} />

                  <input
                    type="email"
                    placeholder="Enter your email"
                    value={email}
                    onChange={(event) =>
                      setEmail(event.target.value)
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
                    placeholder="Create a password"
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
                {loading ? "Creating account..." : "Create account"}

                {!loading && <ArrowRight size={18} />}
              </button>
            </form>

            <p className="auth-switch">
              Already have an account?{" "}
              <Link to="/login">Sign in</Link>
            </p>
          </div>
        </div>
      </section>
    </main>
  )
}

export default Register