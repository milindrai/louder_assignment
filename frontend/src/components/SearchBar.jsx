import { useState } from "react";

export default function SearchBar({ onSubmit, isLoading }) {
  const [description, setDescription] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (description.trim() && !isLoading) {
      onSubmit(description.trim());
      setDescription("");
    }
  };

  return (
    <div className="search-container">
      <form className="search-form" onSubmit={handleSubmit}>
        <textarea
          className="search-textarea"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder='Describe your event... e.g. "A 10-person leadership retreat in the mountains for 3 days with a $4k budget"'
          disabled={isLoading}
        />
        <div className="search-actions">
          <span className="search-hint">
            Be specific — mention team size, budget, location preferences, and duration.
          </span>
          <button
            type="submit"
            className="search-btn"
            disabled={!description.trim() || isLoading}
          >
            <span className="search-btn__icon">✨</span>
            Find Venue
          </button>
        </div>
      </form>
    </div>
  );
}
