import React, { useState, useRef, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Trophy, User, ChevronDown, LogOut } from 'lucide-react';

const navLinkStyle = (isActive) => ({
    color: isActive ? '#4a5d23' : '#555',
    textDecoration: 'none',
    fontSize: '0.9rem',
    fontWeight: isActive ? 600 : 500,
    padding: '0.4rem 0.75rem',
    borderRadius: '8px',
    transition: 'all 0.15s',
    backgroundColor: isActive ? '#f0f4ed' : 'transparent',
});

const Navbar = () => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();
    const location = useLocation();
    const [profileOpen, setProfileOpen] = useState(false);
    const dropdownRef = useRef(null);

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    // Close dropdown on outside click
    useEffect(() => {
        const handleClickOutside = (e) => {
            if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
                setProfileOpen(false);
            }
        };
        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    const isActive = (path) => location.pathname.startsWith(path);

    // Role-based navigation links
    const getNavLinks = () => {
        if (!user) return [];

        if (user.role === 'player') {
            return [
                { to: '/player/dashboard', label: 'Events' },
            ];
        }

        if (user.role === 'creator') {
            return [
                { to: '/creator/dashboard', label: 'Dashboard' },
                { to: '/creator/events/create', label: 'My Events', match: '/creator/events' },
            ];
        }

        if (user.role === 'admin') {
            return [
                { to: '/admin/dashboard', label: 'Dashboard' },
            ];
        }

        return [];
    };

    const navLinks = getNavLinks();

    return (
        <nav style={{
            backgroundColor: '#fff',
            borderBottom: '1px solid #f0f0f0',
            padding: '0.75rem 0',
            position: 'sticky',
            top: 0,
            zIndex: 1000,
            boxShadow: '0 1px 8px rgba(0,0,0,0.03)',
        }}>
            <div className="container d-flex align-items-center justify-content-between">
                {/* Logo */}
                <Link to="/" style={{
                    textDecoration: 'none',
                    color: '#1a1a1a',
                    fontFamily: "'Inter', sans-serif",
                    fontWeight: 700,
                    fontSize: '1.15rem',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem',
                }}>
                    <Trophy size={20} style={{ color: '#4a5d23' }} />
                    Mini Leaderboard
                </Link>

                {/* Center Nav Links (role-based) */}
                {user && navLinks.length > 0 && (
                    <div className="d-none d-md-flex align-items-center gap-1">
                        {navLinks.map((link) => (
                            <Link
                                key={link.to}
                                to={link.to}
                                style={navLinkStyle(isActive(link.match || link.to))}
                                onMouseEnter={(e) => {
                                    if (!isActive(link.match || link.to)) {
                                        e.currentTarget.style.backgroundColor = '#f8f8f8';
                                    }
                                }}
                                onMouseLeave={(e) => {
                                    if (!isActive(link.match || link.to)) {
                                        e.currentTarget.style.backgroundColor = 'transparent';
                                    }
                                }}
                            >
                                {link.label}
                            </Link>
                        ))}
                    </div>
                )}

                {/* Right Side */}
                <div className="d-flex align-items-center gap-3">
                    {user ? (
                        /* Profile Dropdown */
                        <div ref={dropdownRef} style={{ position: 'relative' }}>
                            <button
                                onClick={() => setProfileOpen(!profileOpen)}
                                style={{
                                    backgroundColor: profileOpen ? '#f0f4ed' : 'transparent',
                                    border: '1px solid #e8e8e8',
                                    borderRadius: '50px',
                                    padding: '0.4rem 1rem 0.4rem 0.6rem',
                                    fontSize: '0.85rem',
                                    color: '#333',
                                    cursor: 'pointer',
                                    fontWeight: 500,
                                    display: 'flex',
                                    alignItems: 'center',
                                    gap: '0.5rem',
                                    transition: 'all 0.15s',
                                }}
                                onMouseEnter={(e) => {
                                    e.currentTarget.style.borderColor = '#c0c0c0';
                                }}
                                onMouseLeave={(e) => {
                                    e.currentTarget.style.borderColor = '#e8e8e8';
                                }}
                            >
                                <div style={{
                                    width: '26px',
                                    height: '26px',
                                    borderRadius: '50%',
                                    backgroundColor: '#4a5d23',
                                    color: '#fff',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    fontSize: '0.7rem',
                                    fontWeight: 700,
                                }}>
                                    {(user.name || user.username || 'U').charAt(0).toUpperCase()}
                                </div>
                                {user.name || user.username}
                                <ChevronDown size={14} style={{
                                    transform: profileOpen ? 'rotate(180deg)' : 'rotate(0)',
                                    transition: 'transform 0.2s',
                                }} />
                            </button>

                            {profileOpen && (
                                <div style={{
                                    position: 'absolute',
                                    top: 'calc(100% + 8px)',
                                    right: 0,
                                    backgroundColor: '#fff',
                                    borderRadius: '12px',
                                    boxShadow: '0 8px 30px rgba(0,0,0,0.1)',
                                    border: '1px solid #f0f0f0',
                                    minWidth: '200px',
                                    overflow: 'hidden',
                                    zIndex: 1001,
                                }}>
                                    {/* User info */}
                                    <div style={{
                                        padding: '1rem',
                                        borderBottom: '1px solid #f0f0f0',
                                    }}>
                                        <div style={{ fontWeight: 600, fontSize: '0.9rem' }}>
                                            {user.name || user.username}
                                        </div>
                                        <div style={{ color: '#888', fontSize: '0.8rem' }}>
                                            {user.email}
                                        </div>
                                        <div style={{
                                            marginTop: '0.4rem',
                                            fontSize: '0.7rem',
                                            textTransform: 'uppercase',
                                            letterSpacing: '1px',
                                            color: '#4a5d23',
                                            fontWeight: 600,
                                        }}>
                                            {user.role}
                                        </div>
                                    </div>

                                    {/* Mobile nav links */}
                                    <div className="d-md-none" style={{ borderBottom: '1px solid #f0f0f0' }}>
                                        {navLinks.map((link) => (
                                            <Link
                                                key={link.to}
                                                to={link.to}
                                                onClick={() => setProfileOpen(false)}
                                                style={{
                                                    display: 'block',
                                                    padding: '0.7rem 1rem',
                                                    color: '#333',
                                                    textDecoration: 'none',
                                                    fontSize: '0.85rem',
                                                    fontWeight: 500,
                                                    transition: 'background-color 0.15s',
                                                }}
                                                onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#f8f8f8'}
                                                onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'transparent'}
                                            >
                                                {link.label}
                                            </Link>
                                        ))}
                                    </div>

                                    {/* Logout */}
                                    <button
                                        onClick={handleLogout}
                                        style={{
                                            width: '100%',
                                            padding: '0.75rem 1rem',
                                            border: 'none',
                                            backgroundColor: 'transparent',
                                            color: '#dc2626',
                                            fontSize: '0.85rem',
                                            fontWeight: 500,
                                            cursor: 'pointer',
                                            textAlign: 'left',
                                            display: 'flex',
                                            alignItems: 'center',
                                            gap: '0.5rem',
                                            transition: 'background-color 0.15s',
                                        }}
                                        onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#fff5f5'}
                                        onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'transparent'}
                                    >
                                        <LogOut size={16} />
                                        Logout
                                    </button>
                                </div>
                            )}
                        </div>
                    ) : (
                        <>
                            <Link to="/login" style={{
                                color: '#555',
                                textDecoration: 'none',
                                fontSize: '0.9rem',
                                fontWeight: 500,
                            }}>
                                Login
                            </Link>
                            <Link to="/register" style={{
                                backgroundColor: '#4a5d23',
                                color: '#fff',
                                textDecoration: 'none',
                                borderRadius: '50px',
                                padding: '0.5rem 1.5rem',
                                fontSize: '0.85rem',
                                fontWeight: 500,
                                transition: 'background-color 0.2s',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '0.35rem',
                            }}>
                                Get Started <span>→</span>
                            </Link>
                        </>
                    )}
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
