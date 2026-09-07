import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { api } from '../../api/client';
import { Trophy, ArrowLeft, Calendar, Users, FileText, Gamepad2, Sparkles, CheckCircle } from 'lucide-react';

const COMPETITION_CATEGORIES = [
    { label: 'Sports', type: 'sports', icon: '⚽' },
    { label: 'Quiz / Trivia', type: 'quiz', icon: '🧠' },
    { label: 'Coding / Tech', type: 'coding', icon: '💻' },
    { label: 'Chess & Strategy', type: 'chess', icon: '♟️' },
    { label: 'Gaming / Esports', type: 'gaming', icon: '🎮' },
    { label: 'Custom / Other', type: 'custom', icon: '⚡' },
];

const CreateEvent = () => {
    const [formData, setFormData] = useState({
        name: '',
        description: '',
        event_type: '',
        participant_limit: 100,
        start_date: '',
        end_date: ''
    });
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSelectPreset = (type) => {
        setFormData(prev => ({ ...prev, event_type: type }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setIsLoading(true);

        try {
            const payload = { ...formData };
            if (payload.start_date) payload.start_date = new Date(payload.start_date).toISOString();
            if (payload.end_date) payload.end_date = new Date(payload.end_date).toISOString();
            if (!payload.participant_limit) payload.participant_limit = null;

            const newEvent = await api.createEvent(payload);
            navigate(`/creator/events/${newEvent.id}/rules`);
        } catch (err) {
            setError(err.response?.data?.detail || err.message || 'Failed to create event');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="py-3" style={{ maxWidth: '820px', margin: '0 auto' }}>
            {/* Navigation back */}
            <div className="mb-4">
                <Link to="/creator/dashboard" className="text-decoration-none text-muted small d-inline-flex align-items-center gap-1 mb-2 hover-primary">
                    <ArrowLeft size={16} /> Back to Dashboard
                </Link>
                <h1 className="h3 fw-bold mb-1">Create New Tournament</h1>
                <p className="text-muted small mb-0">
                    Set up your tournament details, game format, capacity limits, and scoring schedule.
                </p>
            </div>

            {error && (
                <div className="alert alert-danger rounded-3 d-flex align-items-center mb-4">
                    {error}
                </div>
            )}

            <div className="card-modern">
                <div className="card-modern-header d-flex justify-content-between align-items-center">
                    <div className="d-flex align-items-center gap-2">
                        <div className="stat-icon-wrapper stat-icon-green" style={{ width: '36px', height: '36px', margin: 0, borderRadius: '10px' }}>
                            <Trophy size={18} />
                        </div>
                        <div>
                            <h2 className="h6 fw-bold mb-0">Tournament Configuration</h2>
                            <small className="text-muted">Step 1 of 2: Basic Info</small>
                        </div>
                    </div>
                    <span className="badge-soft-primary">
                        <Sparkles size={12} className="me-1" /> Dynamic Engine
                    </span>
                </div>

                <div className="p-4 p-md-5">
                    <form onSubmit={handleSubmit}>
                        {/* Event Name */}
                        <div className="mb-4">
                            <label className="form-label small fw-bold text-muted text-uppercase letter-spacing-1">
                                Tournament Name <span className="text-danger">*</span>
                            </label>
                            <input 
                                type="text" 
                                className="form-control" 
                                name="name"
                                value={formData.name}
                                onChange={handleChange}
                                placeholder="e.g. National Championship 2026 / Winter Tournament"
                                required 
                            />
                            <div className="form-text small text-muted">A clear, recognizable title for participants to identify.</div>
                        </div>

                        {/* Competition Category / Discipline */}
                        <div className="mb-4">
                            <label className="form-label small fw-bold text-muted text-uppercase letter-spacing-1">
                                Category / Discipline <span className="text-danger">*</span>
                            </label>
                            
                            {/* Category Chips */}
                            <div className="d-flex flex-wrap gap-2 mb-2">
                                {COMPETITION_CATEGORIES.map(preset => (
                                    <button
                                        key={preset.type}
                                        type="button"
                                        className={`btn btn-sm ${formData.event_type.toLowerCase() === preset.type.toLowerCase() ? 'btn-primary' : 'btn-outline-secondary'}`}
                                        style={{ borderRadius: '8px', fontSize: '0.8rem', padding: '0.35rem 0.75rem' }}
                                        onClick={() => handleSelectPreset(preset.type)}
                                    >
                                        <span className="me-1">{preset.icon}</span> {preset.label}
                                    </button>
                                ))}
                            </div>

                            <input 
                                type="text" 
                                className="form-control mt-2" 
                                name="event_type"
                                value={formData.event_type}
                                onChange={handleChange}
                                placeholder="Select a category above or type custom discipline (e.g. Sports, Quiz, Hackathon, Chess, etc.)..."
                                required 
                            />
                        </div>

                        {/* Description */}
                        <div className="mb-4">
                            <label className="form-label small fw-bold text-muted text-uppercase letter-spacing-1">
                                Description & Format
                            </label>
                            <textarea 
                                className="form-control" 
                                name="description"
                                value={formData.description}
                                onChange={handleChange}
                                rows="3"
                                placeholder="Provide context, match format (e.g. 6v6, Best of 3), prize pool, or special rules..."
                            ></textarea>
                        </div>

                        {/* Participant Limit */}
                        <div className="row g-3 mb-4">
                            <div className="col-md-6">
                                <label className="form-label small fw-bold text-muted text-uppercase letter-spacing-1">
                                    Max Participants
                                </label>
                                <div className="input-group">
                                    <span className="input-group-text bg-light border-end-0">
                                        <Users size={16} className="text-muted" />
                                    </span>
                                    <input 
                                        type="number" 
                                        className="form-control border-start-0 ps-0" 
                                        name="participant_limit"
                                        value={formData.participant_limit || ''}
                                        onChange={handleChange}
                                        placeholder="Leave empty for unlimited"
                                        min="2"
                                    />
                                </div>
                                <div className="form-text small text-muted">Leave blank for open unlimited registrations.</div>
                            </div>

                            <div className="col-md-6">
                                <label className="form-label small fw-bold text-muted text-uppercase letter-spacing-1">
                                    Scoring System
                                </label>
                                <div className="p-2 border rounded-3 bg-light d-flex align-items-center gap-2">
                                    <CheckCircle size={18} className="text-success flex-shrink-0 ms-1" />
                                    <span className="small text-muted">Dynamic points customizable in the next step</span>
                                </div>
                            </div>
                        </div>

                        {/* Schedule Dates */}
                        <div className="row g-3 mb-5">
                            <div className="col-md-6">
                                <label className="form-label small fw-bold text-muted text-uppercase letter-spacing-1">
                                    Start Date & Time (Optional)
                                </label>
                                <div className="input-group">
                                    <span className="input-group-text bg-light border-end-0">
                                        <Calendar size={16} className="text-muted" />
                                    </span>
                                    <input 
                                        type="datetime-local" 
                                        className="form-control border-start-0 ps-0" 
                                        name="start_date"
                                        value={formData.start_date}
                                        onChange={handleChange}
                                    />
                                </div>
                            </div>

                            <div className="col-md-6">
                                <label className="form-label small fw-bold text-muted text-uppercase letter-spacing-1">
                                    End Date & Time (Optional)
                                </label>
                                <div className="input-group">
                                    <span className="input-group-text bg-light border-end-0">
                                        <Calendar size={16} className="text-muted" />
                                    </span>
                                    <input 
                                        type="datetime-local" 
                                        className="form-control border-start-0 ps-0" 
                                        name="end_date"
                                        value={formData.end_date}
                                        onChange={handleChange}
                                    />
                                </div>
                            </div>
                        </div>

                        {/* Submit Actions */}
                        <div className="d-flex justify-content-between align-items-center pt-3 border-top">
                            <button 
                                type="button" 
                                className="btn btn-outline-secondary px-4" 
                                onClick={() => navigate('/creator/dashboard')}
                            >
                                Cancel
                            </button>
                            <button type="submit" className="btn btn-primary px-4 py-2" disabled={isLoading}>
                                {isLoading ? (
                                    <>
                                        <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                                        Setting up...
                                    </>
                                ) : (
                                    'Create & Configure Rules →'
                                )}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default CreateEvent;
