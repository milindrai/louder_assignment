export default function LoadingAnimation() {
  return (
    <div className="loading-container">
      <div className="loading-orb" />
      <div className="loading-text">
        AI is planning your event
        <span className="loading-dots">
          <span />
          <span />
          <span />
        </span>
      </div>
    </div>
  );
}
