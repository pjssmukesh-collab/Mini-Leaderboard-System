import React from 'react';
import homeImage from '../../assets/home__.png';

const DashboardPreview = () => {
    return (
        <div className="dashboard-mockup text-center" style={{ perspective: '1200px' }}>
            <div
                style={{
                    transform: 'rotateY(-12deg) rotateX(5deg) rotateZ(2deg)',
                    transformStyle: 'preserve-3d',
                    transition: 'transform 0.5s ease',
                    borderRadius: '20px',
                    boxShadow: '30px 30px 60px rgba(0,0,0,0.15), -5px -5px 20px rgba(0,0,0,0.03)',
                    overflow: 'hidden',
                    display: 'inline-block',
                }}
                onMouseEnter={(e) => {
                    e.currentTarget.style.transform = 'rotateY(0deg) rotateX(0deg) rotateZ(0deg) scale(1.02)';
                }}
                onMouseLeave={(e) => {
                    e.currentTarget.style.transform = 'rotateY(-12deg) rotateX(5deg) rotateZ(2deg)';
                }}
            >
                <img
                    src={homeImage}
                    alt="Dashboard Preview"
                    className="img-fluid"
                    style={{
                        maxHeight: '600px',
                        objectFit: 'cover',
                        objectPosition: 'top center',
                        display: 'block',
                        borderRadius: '20px',
                    }}
                />
            </div>
        </div>
    );
};

export default DashboardPreview;
