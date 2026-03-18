import { useState, useEffect } from "react";
import { submitEvent, getHistory } from "./api/client";
import SearchBar from "./components/SearchBar";
import LoadingAnimation from "./components/LoadingAnimation";
import ProposalCard from "./components/ProposalCard";
import SearchHistory from "./components/SearchHistory";

export default function App() {
  const [history, setHistory] = useState([]);
  const [activeItem, setActiveItem] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Load history on mount (persistence across refreshes)
  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const data = await getHistory();
      setHistory(data);
      // Show the latest result by default
      if (data.length > 0 && !activeItem) {
        setActiveItem(data[0]);
      }
    } catch (err) {
      console.error("Failed to fetch history:", err);
    }
  };

  const handleSubmit = async (description) => {
    setIsLoading(true);
    setError(null);
    setActiveItem(null);

    try {
      const result = await submitEvent(description);
      setActiveItem(result);
      // Refresh history
      const updatedHistory = await getHistory();
      setHistory(updatedHistory);
    } catch (err) {
      const message =
        err.response?.data?.error ||
        "Something went wrong. Please try again.";
      setError(message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSelectHistory = (item) => {
    setActiveItem(item);
    setError(null);
  };

  return (
    <div className="app-container">
      <main className="main-content">
        <header className="header">
          <div className="header__badge">
            <span className="header__badge-dot" />
            AI-Powered
          </div>
          <h1 className="header__title">Event Concierge</h1>
          <p className="header__subtitle">
            Describe your corporate event and let AI find the perfect venue for
            your team.
          </p>
        </header>

        <SearchBar onSubmit={handleSubmit} isLoading={isLoading} />

        {error && (
          <div className="error-message">
            <span>⚠️</span> {error}
          </div>
        )}

        {isLoading && <LoadingAnimation />}

        {!isLoading && activeItem && (
          <ProposalCard proposal={activeItem.proposal} />
        )}
      </main>

      <SearchHistory
        history={history}
        activeId={activeItem?._id}
        onSelect={handleSelectHistory}
      />
    </div>
  );
}
