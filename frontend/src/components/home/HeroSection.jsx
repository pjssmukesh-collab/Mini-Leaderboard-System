import React from 'react';
import { Link } from 'react-router-dom';
import DashboardPreview from './DashboardPreview';

const HeroSection = () => {
    return (
        <section className="section-padding">
            <div className="container">
                <div className="row align-items-center">
                    <div className="col-lg-6 mb-5 mb-lg-0 pe-lg-5">
                        <h1 className="display-4 fw-bold mb-4" style={{ lineHeight: 1.2 }}>
                            Turn every result into a <span className="text-accent">leaderboard.</span>
                        </h1>
                        <p className="lead text-muted mb-5" style={{ fontSize: '1.2rem' }}>
                            A premium platform to effortlessly manage events, upload results, and generate beautiful real-time leaderboards for any competition.
                        </p>
                        <div className="d-flex flex-wrap gap-3">
                            <Link to="/register" className="btn-accent">Get Started Free</Link>
                        </div>


                    </div>
                    <div className="col-lg-6">
                        <DashboardPreview />
                    </div>
                </div>
            </div>
        </section>
    );
};

export default HeroSection;
