import React from 'react';

const players = [
    { rank: 1, name: 'Mukesh', event: 'Free Fire Tournament', score: 128, matches: 5, color: '#e8d44d' },
    { rank: 2, name: 'Rahul', event: 'Chess Championship', score: 115, matches: 5, color: '#c0c0c0' },
    { rank: 3, name: 'Ravi', event: 'Coding Contest', score: 102, matches: 4, color: '#cd7f32' },
    { rank: 4, name: 'Kiran', event: 'Quiz Challenge', score: 98, matches: 4, color: '#a0a0a0' },
];

const LeaderboardPreview = () => {
    return (
        <section id="leaderboard" style={{ padding: '6rem 0', backgroundColor: '#fafbf8' }}>
            <div className="container">
                <div className="text-center mb-5">
                    <span style={{
                        fontSize: '0.75rem',
                        textTransform: 'uppercase',
                        letterSpacing: '2px',
                        color: '#888',
                        fontWeight: 600,
                    }}>
                        Live Rankings
                    </span>
                    <h2 style={{
                        fontFamily: "'Playfair Display', serif",
                        fontSize: '3rem',
                        fontWeight: 700,
                        marginTop: '0.75rem',
                    }}>
                        Real-time leaderboards.<br />
                        Always up to date.
                    </h2>
                </div>

                <div style={{
                    background: '#fff',
                    borderRadius: '16px',
                    boxShadow: '0 4px 24px rgba(0,0,0,0.05)',
                    overflow: 'hidden',
                    maxWidth: '850px',
                    margin: '0 auto',
                }}>
                    {/* Header */}
                    <div className="d-flex justify-content-between align-items-center px-4 py-3"
                        style={{ borderBottom: '1px solid #f0f0f0' }}>
                        <h5 className="mb-0 fw-bold" style={{ fontFamily: "'Inter', sans-serif" }}>
                            Top Players
                        </h5>
                        <a href="#" style={{
                            color: '#4a5d23',
                            fontSize: '0.85rem',
                            textDecoration: 'none',
                            fontWeight: 500,
                        }}>
                            View All →
                        </a>
                    </div>

                    {/* Table Header */}
                    <div className="d-none d-md-flex px-4 py-2"
                        style={{
                            fontSize: '0.75rem',
                            textTransform: 'uppercase',
                            letterSpacing: '1px',
                            color: '#999',
                            borderBottom: '1px solid #f5f5f5',
                        }}>
                        <div style={{ width: '60px' }}>#</div>
                        <div style={{ flex: 1 }}>Player</div>
                        <div style={{ flex: 1 }}>Event</div>
                        <div style={{ width: '100px', textAlign: 'right' }}>Score</div>
                        <div style={{ width: '100px', textAlign: 'right' }}>Matches</div>
                    </div>

                    {/* Rows */}
                    {players.map((p) => (
                        <div key={p.rank}
                            className="d-flex align-items-center px-4 py-3 flex-wrap"
                            style={{
                                borderBottom: '1px solid #f5f5f5',
                                transition: 'background-color 0.15s',
                                cursor: 'default',
                            }}
                            onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#fafbf8'}
                            onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'transparent'}
                        >
                            <div style={{ width: '60px' }}>
                                <span style={{
                                    display: 'inline-flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    width: '28px',
                                    height: '28px',
                                    borderRadius: '50%',
                                    backgroundColor: p.rank <= 3 ? p.color : '#f0f0f0',
                                    color: p.rank <= 3 ? '#fff' : '#666',
                                    fontSize: '0.8rem',
                                    fontWeight: 700,
                                }}>
                                    {p.rank}
                                </span>
                            </div>
                            <div style={{ flex: 1, fontWeight: 600 }}>{p.name}</div>
                            <div className="d-none d-md-block" style={{ flex: 1, color: '#888', fontSize: '0.9rem' }}>
                                {p.event}
                            </div>
                            <div style={{ width: '100px', textAlign: 'right', fontWeight: 600, color: '#4a5d23' }}>
                                {p.score}
                            </div>
                            <div className="d-none d-md-block" style={{ width: '100px', textAlign: 'right', color: '#888' }}>
                                {p.matches}
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
};

export default LeaderboardPreview;
