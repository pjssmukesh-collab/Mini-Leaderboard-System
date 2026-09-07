import React from 'react';
import { Link } from 'react-router-dom';

const CTASection = () => {
    return (
        <section className="section-padding bg-accent text-white text-center">
            <div className="container">
                <div className="mx-auto" style={{ maxWidth: '700px' }}>
                    <h2 className="display-4 fw-bold text-white mb-4">Ready to elevate your event?</h2>
                    <p className="lead text-white-50 mb-5">
                        Join thousands of organizers who use Mini Leaderboard to create professional, real-time rankings in minutes.
                    </p>
                    <Link to="/register" className="btn btn-light btn-lg px-5 py-3 rounded-pill fw-bold text-accent shadow-lg">
                        Create Your First Event
                    </Link>
                </div>
            </div>
        </section>
    );
};

export default CTASection;
