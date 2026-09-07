import React, { useState } from 'react';

const categories = [
    { name: 'Gaming', icon: '🎮', desc: 'Battle Royale, FPS, Chess & more', gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' },
    { name: 'Coding', icon: '💻', desc: 'Hackathons & coding challenges', gradient: 'linear-gradient(135deg, #00b894 0%, #00cec9 100%)' },
    { name: 'Quiz', icon: '🧠', desc: 'Trivia, knowledge & academic', gradient: 'linear-gradient(135deg, #fdcb6e 0%, #e17055 100%)' },
    { name: 'Sports', icon: '⚽', desc: 'Football, cricket, athletics', gradient: 'linear-gradient(135deg, #0984e3 0%, #6c5ce7 100%)' },
];

const EventTypesSection = () => {
    const [hoveredIdx, setHoveredIdx] = useState(null);

    return (
        <section id="events" style={{ padding: '6rem 0', backgroundColor: '#fafbf8' }}>
            <div className="container">
                <div className="text-center mb-5">
                    <span style={{
                        fontSize: '0.75rem',
                        textTransform: 'uppercase',
                        letterSpacing: '2px',
                        color: '#888',
                        fontWeight: 600,
                    }}>
                        Event Categories
                    </span>
                    <h2 style={{
                        fontFamily: "'Playfair Display', serif",
                        fontSize: '3rem',
                        fontWeight: 700,
                        marginTop: '0.75rem',
                    }}>
                        One platform. Any competition.
                    </h2>
                    <p style={{ color: '#888', maxWidth: '500px', margin: '1rem auto 0' }}>
                        From gaming tournaments to academic quizzes — create leaderboards for any type of event.
                    </p>
                </div>

                <div className="row g-4 justify-content-center">
                    {categories.map((cat, idx) => (
                        <div className="col-6 col-md-3" key={idx}>
                            <div
                                style={{
                                    background: '#fff',
                                    borderRadius: '16px',
                                    padding: '2rem 1.5rem',
                                    textAlign: 'center',
                                    cursor: 'pointer',
                                    transition: 'all 0.3s ease',
                                    transform: hoveredIdx === idx ? 'translateY(-8px)' : 'translateY(0)',
                                    boxShadow: hoveredIdx === idx
                                        ? '0 16px 40px rgba(0,0,0,0.1)'
                                        : '0 2px 12px rgba(0,0,0,0.04)',
                                    border: '1px solid #f0f0f0',
                                }}
                                onMouseEnter={() => setHoveredIdx(idx)}
                                onMouseLeave={() => setHoveredIdx(null)}
                            >
                                <div style={{
                                    width: '64px',
                                    height: '64px',
                                    borderRadius: '16px',
                                    background: hoveredIdx === idx ? cat.gradient : '#f5f5f5',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    margin: '0 auto 1.25rem',
                                    fontSize: '1.75rem',
                                    transition: 'background 0.3s ease',
                                }}>
                                    {cat.icon}
                                </div>
                                <h5 style={{
                                    fontWeight: 700,
                                    fontSize: '1.05rem',
                                    marginBottom: '0.4rem',
                                    color: '#1a1a1a',
                                }}>
                                    {cat.name}
                                </h5>
                                <p style={{
                                    color: '#999',
                                    fontSize: '0.8rem',
                                    margin: 0,
                                    lineHeight: 1.4,
                                }}>
                                    {cat.desc}
                                </p>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
};

export default EventTypesSection;
