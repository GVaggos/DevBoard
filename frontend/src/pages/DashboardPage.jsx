import { useNavigate } from "react-router-dom"
import {
  LayoutDashboard,
  FolderKanban,
  CheckSquare2,
  Plus,
  LogOut,
} from "lucide-react"

function Dashboard() {
  const navigate = useNavigate()
  const user = JSON.parse(localStorage.getItem("user") || "null")

  const handleLogout = () => {
    localStorage.removeItem("access_token")
    localStorage.removeItem("user")
    navigate("/login")
  }

  return (
    <main className="dashboard-page">

      <aside className="sidebar">
        <div>
          <div className="sidebar-brand">
            <div className="sidebar-brand-mark">D</div>
            <span>DevBoard</span>
          </div>

          <nav className="sidebar-nav">
            <button className="sidebar-link active">
              <LayoutDashboard size={19} />
              Dashboard
            </button>

            <button className="sidebar-link">
              <FolderKanban size={19} />
              Projects
            </button>

            <button className="sidebar-link">
              <CheckSquare2 size={19} />
              Tasks
            </button>
          </nav>
        </div>

        <button
          className="sidebar-link logout-link"
          onClick={handleLogout}
        >
          <LogOut size={19} />
          Log out
        </button>
      </aside>


      <section className="dashboard-content">

        <header className="dashboard-header">
          <div>
            <span className="dashboard-eyebrow">
              OVERVIEW
            </span>

            <h1>
              Welcome back, {user?.username || "User"}
            </h1>

            <p>
              Manage your projects and keep your work moving forward.
            </p>
          </div>

          <button className="new-project-button">
            <Plus size={18} />
            New Project
          </button>
        </header>


        <section className="stats-grid">
          <div className="stat-card">
            <span>Total projects</span>
            <strong>0</strong>
            <p>Your active workspaces</p>
          </div>

          <div className="stat-card">
            <span>Open tasks</span>
            <strong>0</strong>
            <p>Tasks waiting for you</p>
          </div>

          <div className="stat-card">
            <span>Completed</span>
            <strong>0</strong>
            <p>Tasks completed</p>
          </div>
        </section>


        <section className="projects-section">
          <div className="section-heading">
            <div>
              <h2>Your projects</h2>
              <p>Everything you're currently working on.</p>
            </div>
          </div>

          <div className="empty-projects">
            <div className="empty-icon">
              <FolderKanban size={26} />
            </div>

            <h3>No projects yet</h3>

            <p>
              Create your first project and start organizing your tasks.
            </p>

            <button className="empty-project-button">
              <Plus size={17} />
              Create project
            </button>
          </div>
        </section>

      </section>

    </main>
  )
}

export default Dashboard