import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import {
  LayoutDashboard,
  FolderKanban,
  CheckSquare2,
  Plus,
  LogOut,
  LoaderCircle,
} from "lucide-react"

function Dashboard() {
  const navigate = useNavigate()

  const user = JSON.parse(localStorage.getItem("user") || "null")
  const token = localStorage.getItem("access_token")

  const [projects, setProjects] = useState([])
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  useEffect(() => {
    const loadDashboard = async () => {
      try {
        const projectsResponse = await fetch(
          "http://127.0.0.1:8000/projects",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        )

        if (projectsResponse.status === 401) {
          localStorage.removeItem("access_token")
          localStorage.removeItem("user")
          navigate("/login")
          return
        }

        if (!projectsResponse.ok) {
          throw new Error("Could not load projects")
        }

        const projectsData = await projectsResponse.json()
        setProjects(projectsData)

        const taskRequests = projectsData.map((project) =>
          fetch(
            `http://127.0.0.1:8000/projects/${project.id}/tasks`,
            {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            }
          ).then(async (response) => {
            if (!response.ok) {
              return []
            }

            return response.json()
          })
        )

        const taskGroups = await Promise.all(taskRequests)

        const allTasks = taskGroups.flat()
        setTasks(allTasks)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    loadDashboard()
  }, [navigate, token])

  const handleLogout = () => {
    localStorage.removeItem("access_token")
    localStorage.removeItem("user")
    navigate("/login")
  }

  const openTasks = tasks.filter(
    (task) => task.status !== "done"
  ).length

  const completedTasks = tasks.filter(
    (task) => task.status === "done"
  ).length

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
            <strong>{projects.length}</strong>
            <p>Your active workspaces</p>
          </div>

          <div className="stat-card">
            <span>Open tasks</span>
            <strong>{openTasks}</strong>
            <p>Tasks waiting for you</p>
          </div>

          <div className="stat-card">
            <span>Completed</span>
            <strong>{completedTasks}</strong>
            <p>Tasks completed</p>
          </div>
        </section>

        <section className="projects-section">
          <div className="section-heading">
            <div>
              <h2>Your projects</h2>
              <p>
                Everything you're currently working on.
              </p>
            </div>
          </div>

          {loading && (
            <div className="dashboard-loading">
              <LoaderCircle
                size={24}
                className="loading-spinner"
              />
              Loading your workspace...
            </div>
          )}

          {error && (
            <div className="dashboard-error">
              {error}
            </div>
          )}

          {!loading && !error && projects.length === 0 && (
            <div className="empty-projects">
              <div className="empty-icon">
                <FolderKanban size={26} />
              </div>

              <h3>No projects yet</h3>

              <p>
                Create your first project and start organizing
                your tasks.
              </p>

              <button className="empty-project-button">
                <Plus size={17} />
                Create project
              </button>
            </div>
          )}

          {!loading && !error && projects.length > 0 && (
            <div className="projects-grid">
              {projects.map((project) => {
                const projectTasks = tasks.filter(
                  (task) => task.project_id === project.id
                )

                const doneTasks = projectTasks.filter(
                  (task) => task.status === "done"
                ).length

                const progress =
                  projectTasks.length === 0
                    ? 0
                    : Math.round(
                        (doneTasks / projectTasks.length) * 100
                      )

                return (
                  <article
                    className="project-card"
                    key={project.id}
                  >
                    <div className="project-card-icon">
                      <FolderKanban size={20} />
                    </div>

                    <h3>{project.name}</h3>

                    <p>
                      {projectTasks.length}{" "}
                      {projectTasks.length === 1
                        ? "task"
                        : "tasks"}
                      {" · "}
                      {doneTasks} completed
                    </p>

                    <div className="project-progress">
                      <div className="project-progress-heading">
                        <span>Progress</span>
                        <span>{progress}%</span>
                      </div>

                      <div className="progress-track">
                        <div
                          className="progress-bar"
                          style={{
                            width: `${progress}%`,
                          }}
                        />
                      </div>
                    </div>
                  </article>
                )
              })}
            </div>
          )}
        </section>
      </section>
    </main>
  )
}

export default Dashboard