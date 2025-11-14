type Props = {
  total: number;
  submitted: number;
  inProgress: number;
  resolved: number;
};

export function Stats({ total, submitted, inProgress, resolved }: Props) {
  const cards = [
    { label: "Total Complaints", value: total },
    { label: "Submitted", value: submitted },
    { label: "In Progress", value: inProgress },
    { label: "Resolved", value: resolved }
  ];

  return (
    <div className="card">
      <div className="stats-grid">
        {cards.map((card) => (
          <div className="stat-card" key={card.label}>
            <h4>{card.label}</h4>
            <div className="value">{card.value}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

