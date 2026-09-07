import React from 'react';
import { Trophy, Mail, Phone, ExternalLink } from 'lucide-react';
import { Link } from 'react-router-dom';

const LinkedinIcon = ({ size = 18 }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor">
        <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
    </svg>
);

const GithubIcon = ({ size = 18 }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/>
    </svg>
);


const Footer = () => {
    return (
        <footer className="bg-white border-top py-5 mt-auto">
            <div className="container">
                <div className="row g-4 mb-4">
                    {/* Brand & Description */}
                    <div className="col-lg-5">
                        <Link className="d-flex align-items-center text-dark text-decoration-none fw-bold mb-3 fs-5" to="/">
                            <Trophy className="me-2 text-accent" size={24} /> Mini Leaderboard
                        </Link>
                        <p className="text-muted small pe-lg-5">
                            The premium platform for turning raw results into beautiful, real-time leaderboards. Make every competition professional.
                        </p>
                    </div>

                    {/* Contact Info */}
                    <div className="col-lg-4 col-md-6">
                        <h6 className="fw-bold mb-3">Contact</h6>
                        <ul className="list-unstyled small">
                            <li className="mb-2 d-flex align-items-center">
                                <Mail size={15} className="me-2 text-muted" />
                                <a href="mailto:pjssmukesh@mail.com" className="text-muted text-decoration-none">
                                    pjssmukesh@mail.com
                                </a>
                            </li>
                            <li className="mb-2 d-flex align-items-center">
                                <Phone size={15} className="me-2 text-muted" />
                                <a href="tel:+919030166122" className="text-muted text-decoration-none">
                                    +91 9030166122
                                </a>
                            </li>
                        </ul>
                    </div>

                    {/* Social Links */}
                    <div className="col-lg-3 col-md-6">
                        <h6 className="fw-bold mb-3">Connect</h6>
                        <div className="d-flex gap-3">
                            <a
                                href="https://www.linkedin.com/in/p-j-s-s-mukesh-8149a52bb/"
                                target="_blank"
                                rel="noopener noreferrer"
                                className="d-flex align-items-center justify-content-center rounded-circle"
                                style={{
                                    width: '40px',
                                    height: '40px',
                                    backgroundColor: '#f0f4ed',
                                    color: '#4a5d23',
                                    transition: 'all 0.2s ease',
                                }}
                                title="LinkedIn"
                                onMouseEnter={(e) => {
                                    e.currentTarget.style.backgroundColor = '#4a5d23';
                                    e.currentTarget.style.color = '#fff';
                                }}
                                onMouseLeave={(e) => {
                                    e.currentTarget.style.backgroundColor = '#f0f4ed';
                                    e.currentTarget.style.color = '#4a5d23';
                                }}
                            >
                                <LinkedinIcon size={18} />
                            </a>
                            <a
                                href="https://github.com/pjssmukesh-collab"
                                target="_blank"
                                rel="noopener noreferrer"
                                className="d-flex align-items-center justify-content-center rounded-circle"
                                style={{
                                    width: '40px',
                                    height: '40px',
                                    backgroundColor: '#f0f4ed',
                                    color: '#4a5d23',
                                    transition: 'all 0.2s ease',
                                }}
                                title="GitHub"
                                onMouseEnter={(e) => {
                                    e.currentTarget.style.backgroundColor = '#4a5d23';
                                    e.currentTarget.style.color = '#fff';
                                }}
                                onMouseLeave={(e) => {
                                    e.currentTarget.style.backgroundColor = '#f0f4ed';
                                    e.currentTarget.style.color = '#4a5d23';
                                }}
                            >
                                <GithubIcon size={18} />
                            </a>
                            <a
                                href="mailto:pjssmukesh@mail.com"
                                className="d-flex align-items-center justify-content-center rounded-circle"
                                style={{
                                    width: '40px',
                                    height: '40px',
                                    backgroundColor: '#f0f4ed',
                                    color: '#4a5d23',
                                    transition: 'all 0.2s ease',
                                }}
                                title="Email"
                                onMouseEnter={(e) => {
                                    e.currentTarget.style.backgroundColor = '#4a5d23';
                                    e.currentTarget.style.color = '#fff';
                                }}
                                onMouseLeave={(e) => {
                                    e.currentTarget.style.backgroundColor = '#f0f4ed';
                                    e.currentTarget.style.color = '#4a5d23';
                                }}
                            >
                                <Mail size={18} />
                            </a>
                            <a
                                href="tel:+919030166122"
                                className="d-flex align-items-center justify-content-center rounded-circle"
                                style={{
                                    width: '40px',
                                    height: '40px',
                                    backgroundColor: '#f0f4ed',
                                    color: '#4a5d23',
                                    transition: 'all 0.2s ease',
                                }}
                                title="Phone"
                                onMouseEnter={(e) => {
                                    e.currentTarget.style.backgroundColor = '#4a5d23';
                                    e.currentTarget.style.color = '#fff';
                                }}
                                onMouseLeave={(e) => {
                                    e.currentTarget.style.backgroundColor = '#f0f4ed';
                                    e.currentTarget.style.color = '#4a5d23';
                                }}
                            >
                                <Phone size={18} />
                            </a>
                        </div>
                    </div>
                </div>
                <div className="border-top pt-4 text-center text-muted small">
                    &copy; {new Date().getFullYear()} Mini Leaderboard System. All rights reserved.
                </div>
            </div>
        </footer>
    );
};

export default Footer;
