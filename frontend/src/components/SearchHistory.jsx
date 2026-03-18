export default function SearchHistory({ history, activeId, onSelect }) {
  const formatDate = (isoString) => {
    const d = new Date(isoString);
    return d.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  return (
    <aside className="sidebar">
      <h3 className="sidebar__title">Search History</h3>

      {history.length === 0 ? (
        <div className="sidebar__empty">
          <div className="sidebar__empty-icon">🔍</div>
          <p>No searches yet.<br />Describe your event to get started!</p>
        </div>
      ) : (
        history.map((item) => (
          <div
            key={item._id}
            className={`history-item ${item._id === activeId ? "active" : ""}`}
            onClick={() => onSelect(item)}
          >
            <div className="history-item__venue">
              {item.proposal?.venue_name || "Venue"}
            </div>
            <div className="history-item__desc">{item.description}</div>
            <div className="history-item__meta">
              <span className="history-item__cost">
                {item.proposal?.estimated_cost}
              </span>
              <span className="history-item__date">
                {formatDate(item.created_at)}
              </span>
            </div>
          </div>
        ))
      )}
    </aside>
  );
}
