export default function RecommendationCard({ rec, onRate, index }) {
  const {
    dish_name, restaurant_name, restaurant_area, score,
    first_bite, true_cost, price, delivery_fee, platform_fee,
    is_veg, is_community, cuisine_type, order_links,
  } = rec;

  return (
    <div className="glass-card fade-in-up" style={{
      padding: 22,
      animationDelay: `${index * 0.1}s`,
      opacity: 0,
    }}>
      {/* Top row: Score + badges */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 12, flexWrap: 'wrap' }}>
        <span className="score-badge">{score}% match</span>
        {is_community && <span className="community-badge">📍 Local spot</span>}
        {is_veg && (
          <span style={{
            background: 'rgba(16, 185, 129, 0.1)',
            border: '1px solid rgba(16, 185, 129, 0.25)',
            color: 'var(--khao-green)',
            fontSize: '0.75rem',
            fontWeight: 600,
            padding: '3px 10px',
            borderRadius: 20,
          }}>
            🌿 Veg
          </span>
        )}
        {cuisine_type && (
          <span style={{
            fontSize: '0.75rem',
            color: 'var(--khao-text-muted)',
            background: 'var(--khao-dark-surface)',
            padding: '3px 10px',
            borderRadius: 20,
          }}>
            {cuisine_type}
          </span>
        )}
      </div>

      {/* Dish + Restaurant */}
      <h3 style={{ fontSize: '1.15rem', fontWeight: 700, marginBottom: 4 }}>{dish_name}</h3>
      <p style={{ fontSize: '0.88rem', color: 'var(--khao-text-muted)', marginBottom: 14 }}>
        {restaurant_name} · {restaurant_area}
      </p>

      {/* First Bite */}
      <div className="first-bite-card" style={{ marginBottom: 14 }}>
        <div style={{ fontSize: '0.78rem', fontWeight: 700, color: 'var(--khao-gold)', marginBottom: 4 }}>
          👅 First Bite Preview
        </div>
        <p style={{ fontSize: '0.9rem', color: 'var(--khao-text-secondary)', lineHeight: 1.5 }}>
          {first_bite}
        </p>
      </div>

      {/* True Cost */}
      <div style={{ marginBottom: 16 }}>
        <span style={{ fontSize: '1.1rem', fontWeight: 800 }}>₹{true_cost}</span>
        <span style={{ fontSize: '0.8rem', color: 'var(--khao-text-muted)', marginLeft: 8 }}>
          (₹{price} + ₹{delivery_fee} delivery + ₹{platform_fee} fees)
        </span>
      </div>

      {/* Order Buttons */}
      <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginBottom: 14 }}>
        {order_links?.zomato && (
          <a href={order_links.zomato} target="_blank" rel="noopener noreferrer"
            className="order-btn zomato">
            🔴 Zomato
          </a>
        )}
        {order_links?.swiggy && (
          <a href={order_links.swiggy} target="_blank" rel="noopener noreferrer"
            className="order-btn swiggy">
            🟠 Swiggy
          </a>
        )}
        {order_links?.google_maps && (
          <a href={order_links.google_maps} target="_blank" rel="noopener noreferrer"
            className="order-btn maps">
            📍 Maps
          </a>
        )}
      </div>

      {order_links?.note && (
        <p style={{ fontSize: '0.8rem', color: 'var(--khao-gold)', marginBottom: 12 }}>
          ⚡ {order_links.note}
        </p>
      )}

      {/* Rating Buttons */}
      <div style={{
        display: 'flex',
        gap: 8,
        paddingTop: 12,
        borderTop: '1px solid var(--khao-dark-border)',
      }}>
        <span style={{ fontSize: '0.8rem', color: 'var(--khao-text-muted)', alignSelf: 'center', marginRight: 4 }}>
          Tried it?
        </span>
        {[
          { emoji: '😍', label: 'Loved', rating: 1 },
          { emoji: '😐', label: 'Okay', rating: 2 },
          { emoji: '😕', label: 'Nah', rating: 3 },
        ].map(r => (
          <button
            key={r.rating}
            onClick={() => onRate(r.rating)}
            style={{
              background: 'var(--khao-dark-surface)',
              border: '1px solid var(--khao-dark-border)',
              borderRadius: 10,
              padding: '6px 14px',
              cursor: 'pointer',
              fontSize: '0.82rem',
              color: 'var(--khao-text-secondary)',
              transition: 'all 0.25s ease',
              display: 'flex',
              alignItems: 'center',
              gap: 4,
            }}
            onMouseEnter={e => {
              e.currentTarget.style.borderColor = 'var(--khao-orange)';
              e.currentTarget.style.color = 'var(--khao-text-primary)';
            }}
            onMouseLeave={e => {
              e.currentTarget.style.borderColor = 'var(--khao-dark-border)';
              e.currentTarget.style.color = 'var(--khao-text-secondary)';
            }}
          >
            {r.emoji} {r.label}
          </button>
        ))}
      </div>
    </div>
  );
}
