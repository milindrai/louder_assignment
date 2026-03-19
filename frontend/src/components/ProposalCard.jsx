export default function ProposalCard({ proposal }) {
  if (!proposal) return null;

  const {
    venue_name,
    location,
    estimated_cost,
    capacity,
    duration,
    why_it_fits,
    amenities,
    event_type,
    image_url,
  } = proposal;

  const finalImage = image_url || `https://picsum.photos/seed/${encodeURIComponent(venue_name)}/800/400`;

  return (
    <div className="proposal-card" key={venue_name}>
      <div className="proposal-card__image-container">
        <img src={finalImage} alt={venue_name} className="proposal-card__image" loading="lazy" />
        <div className="proposal-card__image-overlay"></div>
      </div>
      
      <div className="proposal-card__content">
        <div className="proposal-card__header">
        <h2 className="proposal-card__venue">{venue_name}</h2>
        {event_type && (
          <span className="proposal-card__type">{event_type}</span>
        )}
      </div>

      <div className="proposal-card__grid">
        <div className="proposal-card__stat">
          <div className="proposal-card__stat-label">📍 Location</div>
          <div className="proposal-card__stat-value">{location}</div>
        </div>
        <div className="proposal-card__stat">
          <div className="proposal-card__stat-label">💰 Estimated Cost</div>
          <div className="proposal-card__stat-value">{estimated_cost}</div>
        </div>
        {capacity && (
          <div className="proposal-card__stat">
            <div className="proposal-card__stat-label">👥 Capacity</div>
            <div className="proposal-card__stat-value">{capacity}</div>
          </div>
        )}
        {duration && (
          <div className="proposal-card__stat">
            <div className="proposal-card__stat-label">🕐 Duration</div>
            <div className="proposal-card__stat-value">{duration}</div>
          </div>
        )}
      </div>

      {why_it_fits && (
        <div className="proposal-card__justification">
          <div className="proposal-card__justification-title">
            💡 Why It Fits
          </div>
          <p className="proposal-card__justification-text">{why_it_fits}</p>
        </div>
      )}

      {amenities && amenities.length > 0 && (
        <div className="proposal-card__amenities">
          {amenities.map((amenity, i) => (
            <span key={i} className="proposal-card__amenity">
              {amenity}
            </span>
          ))}
        </div>
      )}
      </div>
    </div>
  );
}
