import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { Trophy, User, Mail, Lock, ChevronDown, ArrowRight } from 'lucide-react';

const Register = () => {
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        password: '',
        role: 'player'
    });
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const { register } = useAuth();
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setIsLoading(true);

        try {
            await register(formData);
            navigate('/login');
        } catch (err) {
            setError(err.response?.data?.detail || err.message || 'Registration failed');
        } finally {
            setIsLoading(false);
        }
    };

    const inputStyle = {
        width: '100%',
        padding: '0.8rem 0.8rem 0.8rem 2.75rem',
        border: '1px solid #e0e0e0',
        borderRadius: '12px',
        fontSize: '0.95rem',
        outline: 'none',
        transition: 'border-color 0.2s',
        boxSizing: 'border-box',
    };

    const labelStyle = {
        display: 'block',
        fontSize: '0.8rem',
        fontWeight: 600,
        color: '#555',
        textTransform: 'uppercase',
        letterSpacing: '0.5px',
        marginBottom: '0.5rem',
    };

    const iconStyle = {
        position: 'absolute',
        left: '14px',
        top: '50%',
        transform: 'translateY(-50%)',
        color: '#aaa',
    };

    return (
        <div style={{
            minHeight: '80vh',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '2rem 1rem',
            background: 'linear-gradient(135deg, #fafbf8 0%, #f0f4ed 100%)',
        }}>
            <div style={{ width: '100%', maxWidth: '420px' }}>
                {/* Logo */}
                <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
                    <Link to="/" style={{
                        textDecoration: 'none',
                        color: '#1a1a1a',
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '0.5rem',
                        fontWeight: 700,
                        fontSize: '1.25rem',
                    }}>
                        <Trophy size={24} style={{ color: '#4a5d23' }} />
                        Mini Leaderboard
                    </Link>
                </div>

                {/* Card */}
                <div style={{
                    background: '#fff',
                    borderRadius: '20px',
                    boxShadow: '0 8px 32px rgba(0,0,0,0.06)',
                    padding: '2.5rem',
                }}>
                    <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
                        <h2 style={{
                            fontFamily: "'Playfair Display', serif",
                            fontSize: '1.8rem',
                            fontWeight: 700,
                            marginBottom: '0.5rem',
                        }}>
                            Create account
                        </h2>
                        <p style={{ color: '#888', fontSize: '0.9rem', margin: 0 }}>
                            Join Mini Leaderboard and start competing
                        </p>
                    </div>

                    {error && (
                        <div style={{
                            background: '#fff5f5',
                            border: '1px solid #fecaca',
                            borderRadius: '10px',
                            padding: '0.75rem 1rem',
                            fontSize: '0.85rem',
                            color: '#dc2626',
                            marginBottom: '1.5rem',
                        }}>
                            {error}
                        </div>
                    )}

                    <form onSubmit={handleSubmit}>
                        {/* Name */}
                        <div style={{ marginBottom: '1.25rem' }}>
                            <label style={labelStyle}>Full Name</label>
                            <div style={{ position: 'relative' }}>
                                <User size={18} style={iconStyle} />
                                <input
                                    type="text"
                                    name="name"
                                    value={formData.name}
                                    onChange={handleChange}
                                    required
                                    placeholder="John Doe"
                                    style={inputStyle}
                                    onFocus={(e) => e.target.style.borderColor = '#4a5d23'}
                                    onBlur={(e) => e.target.style.borderColor = '#e0e0e0'}
                                />
                            </div>
                        </div>

                        {/* Email */}
                        <div style={{ marginBottom: '1.25rem' }}>
                            <label style={labelStyle}>Email Address</label>
                            <div style={{ position: 'relative' }}>
                                <Mail size={18} style={iconStyle} />
                                <input
                                    type="email"
                                    name="email"
                                    value={formData.email}
                                    onChange={handleChange}
                                    required
                                    placeholder="you@example.com"
                                    style={inputStyle}
                                    onFocus={(e) => e.target.style.borderColor = '#4a5d23'}
                                    onBlur={(e) => e.target.style.borderColor = '#e0e0e0'}
                                />
                            </div>
                        </div>

                        {/* Role */}
                        <div style={{ marginBottom: '1.25rem' }}>
                            <label style={labelStyle}>Account Type</label>
                            <div style={{ position: 'relative' }}>
                                <ChevronDown size={18} style={{
                                    ...iconStyle,
                                    left: 'auto',
                                    right: '14px',
                                    pointerEvents: 'none',
                                }} />
                                <select
                                    name="role"
                                    value={formData.role}
                                    onChange={handleChange}
                                    style={{
                                        ...inputStyle,
                                        paddingLeft: '1rem',
                                        appearance: 'none',
                                        cursor: 'pointer',
                                        backgroundColor: '#fff',
                                    }}
                                    onFocus={(e) => e.target.style.borderColor = '#4a5d23'}
                                    onBlur={(e) => e.target.style.borderColor = '#e0e0e0'}
                                >
                                    <option value="player">Player</option>
                                    <option value="creator">Tournament Creator</option>
                                </select>
                            </div>
                        </div>

                        {/* Password */}
                        <div style={{ marginBottom: '1.75rem' }}>
                            <label style={labelStyle}>Password</label>
                            <div style={{ position: 'relative' }}>
                                <Lock size={18} style={iconStyle} />
                                <input
                                    type="password"
                                    name="password"
                                    value={formData.password}
                                    onChange={handleChange}
                                    required
                                    minLength="6"
                                    placeholder="••••••••"
                                    style={inputStyle}
                                    onFocus={(e) => e.target.style.borderColor = '#4a5d23'}
                                    onBlur={(e) => e.target.style.borderColor = '#e0e0e0'}
                                />
                            </div>
                        </div>

                        <button
                            type="submit"
                            disabled={isLoading}
                            style={{
                                width: '100%',
                                padding: '0.85rem',
                                backgroundColor: '#4a5d23',
                                color: '#fff',
                                border: 'none',
                                borderRadius: '12px',
                                fontSize: '0.95rem',
                                fontWeight: 600,
                                cursor: isLoading ? 'not-allowed' : 'pointer',
                                opacity: isLoading ? 0.7 : 1,
                                transition: 'background-color 0.2s',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                gap: '0.5rem',
                            }}
                            onMouseEnter={(e) => { if (!isLoading) e.currentTarget.style.backgroundColor = '#3b4a1c'; }}
                            onMouseLeave={(e) => { e.currentTarget.style.backgroundColor = '#4a5d23'; }}
                        >
                            {isLoading ? 'Creating account...' : <>Create Account <ArrowRight size={18} /></>}
                        </button>
                    </form>
                </div>

                {/* Bottom link */}
                <p style={{
                    textAlign: 'center',
                    marginTop: '1.5rem',
                    color: '#888',
                    fontSize: '0.9rem',
                }}>
                    Already have an account?{' '}
                    <Link to="/login" style={{
                        color: '#4a5d23',
                        fontWeight: 600,
                        textDecoration: 'none',
                    }}>
                        Sign in
                    </Link>
                </p>
            </div>
        </div>
    );
};

export default Register;
