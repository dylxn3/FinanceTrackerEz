import "./App.css"

function App() {
  return (
    <div className="app">
      <aside className="sidebar">
        <div className="logo">
          <h1>FinanceTrackerEz</h1>
        </div>

        <nav className="navigation">
          <button className="nav-button active">
            Dashboard
          </button>

          <button className="nav-button">
            Transactions
          </button>
        </nav>
      </aside>

      <main className="main-content">
        <header className="top-bar">
          <div>
            <h2>Dashboard</h2>
            <p>July 2026</p>
          </div>

          <button className="import-button">
            Import Statement
          </button>
        </header>

        <section className="summary-grid">
          <div className="summary-card">
            <p className="card-label">Total Spending</p>
            <h3>$0.00</h3>
            <p className="card-description">
              Total expenses this month
            </p>
          </div>

          <div className="summary-card">
            <p className="card-label">Total Income</p>
            <h3>$0.00</h3>
            <p className="card-description">
              Total income this month
            </p>
          </div>

          <div className="summary-card">
            <p className="card-label">Transactions</p>
            <h3>0</h3>
            <p className="card-description">
              Transactions this month
            </p>
          </div>
        </section>

        <section className="content-card">
          <div className="section-header">
            <div>
              <h2>Recent Transactions</h2>
              <p>Your latest financial activity</p>
            </div>

            <button className="view-button">
              View all
            </button>
          </div>

          <div className="empty-state">
            <h3>No transactions yet</h3>
            <p>
              Import a bank statement to start tracking your
              spending.
            </p>

            <button className="import-button">
              Import Statement
            </button>
          </div>
        </section>
      </main>
    </div>
  )
}

export default App