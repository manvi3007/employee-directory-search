import { useEffect, useState } from "react";
import { Users, Building2, RefreshCw } from "lucide-react";

import SearchBar from "./components/SearchBar";
import EmployeeList from "./components/EmployeeList";
import useDebounce from "./hooks/useDebounce";
import { searchEmployees } from "./services/employeeService";
import "./App.css";

export default function App() {
  const [search, setSearch] = useState("");
  const debouncedSearch = useDebounce(search.trim(), 300);

  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [retryCount, setRetryCount] = useState(0);

  useEffect(() => {
    const controller = new AbortController();
    let active = true;

    async function loadEmployees() {
      setLoading(true);
      setError(null);

      try {
        const data = await searchEmployees(debouncedSearch, controller.signal);

        if (active) {
          setEmployees(data);
        }
      } catch (err) {
        if (err.name !== "AbortError" && active) {
          const message =
            err.message === "Failed to fetch"
              ? "We couldn't connect to the server. Please check your connection and try again."
              : err.message || "Something went wrong. Please try again.";

          setError(message);
          setEmployees([]);
        }
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    }

    loadEmployees();

    return () => {
      active = false;
      controller.abort();
    };
  }, [debouncedSearch, retryCount]);

  return (
    <main className="app-shell">
      <header className="topbar">
        <a className="brand" href="/" aria-label="People Directory home">
          <span className="brand-icon">
            <Users size={21} />
          </span>

          <span>
            People<span className="brand-light">Directory</span>
          </span>
        </a>

        <span className="topbar-label">EMPLOYEE MANAGEMENT</span>
      </header>

      <section className="hero">
        <div className="eyebrow">
          <span className="eyebrow-dot" />
          YOUR TEAM, AT A GLANCE
        </div>

        <h1>Find your people.</h1>

        <p className="hero-description">
          Search your employee directory by name or department.
        </p>

        <SearchBar value={search} onChange={setSearch} />

        <p className="search-hint">Search by employee name or department</p>
      </section>

      <section
        className="directory-section"
        aria-live="polite"
        aria-busy={loading}
      >
        <div className="section-heading">
          <div>
            <h2>Our people</h2>
            <p>Explore your organization's team directory.</p>
          </div>

          {!loading && !error && (
            <span className="result-count">
              {employees.length}{" "}
              {employees.length === 1 ? "employee" : "employees"}
            </span>
          )}
        </div>

        {loading && (
          <div className="state-panel" role="status">
            <span className="spinner" />
            <p>Finding your people...</p>
          </div>
        )}

        {!loading && error && (
          <div className="state-panel error-panel" role="alert">
            <div className="state-icon">
              <RefreshCw size={22} />
            </div>

            <h3>We couldn't load the directory</h3>
            <p>{error}</p>

            <button
              type="button"
              className="retry-button"
              onClick={() => setRetryCount((count) => count + 1)}
            >
              Try again
            </button>
          </div>
        )}

        {!loading && !error && employees.length === 0 && (
          <div className="state-panel">
            <div className="state-icon">
              <Building2 size={22} />
            </div>

            <h3>
              {debouncedSearch
                ? "No employees found"
                : "Your directory is empty"}
            </h3>

            <p>
              {debouncedSearch
                ? "Try another name or department."
                : "There are no employees to display right now."}
            </p>
          </div>
        )}

        {!loading && !error && employees.length > 0 && (
          <EmployeeList employees={employees} />
        )}
      </section>

      <footer className="footer">
        <span>People Directory</span>
        <span>Employee search made simple.</span>
      </footer>
    </main>
  );
}
