import { ArrowRight, CheckCircle2, LockKeyhole, UserRound } from "lucide-react"

function Login() {
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

          <p className="auth-hero-footer">Simple. Focused. Productive.</p>
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
              <p>Enter your details to continue to your workspace.</p>
            </div>

            <form className="auth-form">
              <label>
                Username
                <div className="input-wrapper">
                  <UserRound size={18} />
                  <input
                    type="text"
                    placeholder="Enter your username"
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
                  />
                </div>
              </label>

              <button className="primary-button" type="submit">
                Sign in
                <ArrowRight size={18} />
              </button>
            </form>

            <p className="auth-switch">
              New to DevBoard? <span>Create an account</span>
            </p>
          </div>
        </div>

      </section>
    </main>
  )
}

export default Login