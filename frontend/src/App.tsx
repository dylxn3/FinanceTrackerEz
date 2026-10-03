import { useRef, useState } from "react";
import "./App.css";

import { importStatement, type Transaction } from "./api/transactions";

function App() {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [transactions, setTransactions] = useState<Transaction[]>([]);

  const [isImporting, setIsImporting] = useState(false);

  const [error, setError] = useState<string | null>(null);

  function handleImportClick() {
    fileInputRef.current?.click();
  }

  async function handleFileChange(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    setError(null);
    setIsImporting(true);

    try {
      const result = await importStatement(file);

      setTransactions(result.transactions);
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message);
      } else {
        setError("Something went wrong.");
      }
    } finally {
      setIsImporting(false);

      event.target.value = "";
    }
  }

  const totalSpending = transactions
    .filter((transaction) => transaction.type === "debit")
    .reduce((total, transaction) => total + transaction.amount, 0);

  const totalIncome = transactions
    .filter((transaction) => transaction.type === "credit")
    .reduce((total, transaction) => total + transaction.amount, 0);

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="logo">
          <h1>FinanceTrackerEz</h1>
        </div>

        <nav className="navigation">
          <button className="nav-button active">Dashboard</button>

          <button className="nav-button">Transactions</button>
        </nav>
      </aside>

      <main className="main-content">
        <header className="top-bar">
          <div>
            <h2>Dashboard</h2>

            <p>July 2026</p>
          </div>

          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,.csv"
            onChange={handleFileChange}
            hidden
          />

          <button
            className="import-button"
            onClick={handleImportClick}
            disabled={isImporting}
          >
            {isImporting ? "Importing..." : "Import Statement"}
          </button>
        </header>

        {error && <div className="error-message">{error}</div>}

        <section className="summary-grid">
          <div className="summary-card">
            <p className="card-label">Total Spending</p>

            <h3>${totalSpending.toFixed(2)}</h3>

            <p className="card-description">Total expenses imported</p>
          </div>

          <div className="summary-card">
            <p className="card-label">Total Income</p>

            <h3>${totalIncome.toFixed(2)}</h3>

            <p className="card-description">Total income imported</p>
          </div>

          <div className="summary-card">
            <p className="card-label">Transactions</p>

            <h3>{transactions.length}</h3>

            <p className="card-description">Transactions imported</p>
          </div>
        </section>

        <section className="content-card">
          <div className="section-header">
            <div>
              <h2>Recent Transactions</h2>

              <p>Your latest financial activity</p>
            </div>
          </div>

          {transactions.length === 0 ? (
            <div className="empty-state">
              <h3>No transactions yet</h3>

              <p>Import a bank statement to start tracking your spending.</p>

              <button className="import-button" onClick={handleImportClick}>
                Import Statement
              </button>
            </div>
          ) : (
            <div className="transaction-table">
              <div className="transaction-row table-header">
                <span>Date</span>

                <span>Description</span>

                <span>Type</span>

                <span>Amount</span>
              </div>

              {transactions.map((transaction, index) => (
                <div
                  className="transaction-row"
                  key={`${transaction.date}-${transaction.description}-${index}`}
                >
                  <span>{transaction.date}</span>

                  <span>{transaction.description}</span>

                  <span
                    className={
                      transaction.type === "credit" ? "credit" : "debit"
                    }
                  >
                    {transaction.type}
                  </span>

                  <span
                    className={
                      transaction.type === "credit" ? "credit" : "debit"
                    }
                  >
                    {transaction.type === "credit" ? "+" : "-"}$
                    {transaction.amount.toFixed(2)}
                  </span>
                </div>
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
