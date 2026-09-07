import React from 'react';

const stats = [
    { value: '100+', label: 'Events Created' },
    { value: '10K+', label: 'Participants' },
    { value: '95%', label: 'Faster Result Processing' },
];

const StatsSection = () => {
    return (
        <section style={{ padding: '3rem 0', borderBottom: '1px solid #f0f0f0' }}>
            <div className="container">
                <div className="row text-center">
                    {stats.map((stat, i) => (
                        <div className="col-md-4 mb-3 mb-md-0" key={i}>
                            <h3 style={{
                                fontFamily: "'Playfair Display', serif",
                                fontSize: '2.75rem',
                                fontWeight: 700,
                                color: '#1a1a1a',
                                marginBottom: '0.25rem',
                            }}>
                                {stat.value}
                            </h3>
                            <p style={{
                                color: '#888',
                                fontSize: '0.85rem',
                                textTransform: 'uppercase',
                                letterSpacing: '1.5px',
                                margin: 0,
                                fontFamily: "'Inter', sans-serif",
                            }}>
                                {stat.label}
                            </p>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
};

export default StatsSection;
