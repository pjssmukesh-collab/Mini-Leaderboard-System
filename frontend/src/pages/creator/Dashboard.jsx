import React, { useState, useEffect, useMemo } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../../api/client';
import { useAuth } from '../../contexts/AuthContext';
import { PlusCircle, Trophy, Users, Sliders, UploadCloud, ExternalLink, Search, Gamepad2, Sparkles, Activity, Edit3, Trash2, X, Check, AlertTriangle } from 'lucide-react';

const CreatorDashboard = () => {
    const { user } = useAuth();
    const [events, setEvents] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedType, setSelectedType] = useState('all');

    // Edit and Delete Modal State
    const [editingEvent, setEditingEvent] = useState(null);
    const [editFormData, setEditFormData] = useState({
        name: '',
        description: '',
        event_type: 'gaming',
        participant_limit: 100,
        status: 'active'
    });
    const [editLoading, setEditLoading] = useState(false);
    const [editError, setEditError] = useState('');

    const [deleteEventTarget, setDeleteEventTarget] = useState(null);
    const [deleteLoading, setDeleteLoading] = useState(false);

    const [actionAlert, setActionAlert] = useState(null); // { type: 'success' | 'danger', text: '' }

    useEffect(() => {
        const fetchEvents = async () => {
            if (!user) return;
            try {
                // If the user is a creator, filter by their own creator_id. Admins see all events.
                const params = user.role === 'admin' ? {} : { creator_id: user.id };
                const data = await api.getEvents(params);
                setEvents(data || []);
            } catch (error) {
                console.error("Failed to fetch events", error);
            } finally {
                setIsLoading(false);
            }
        };
        fetchEvents();
    }, [user]);

    // Open Edit Modal
    const handleOpenEdit = (event) => {
        setEditingEvent(event);
        setEditFormData({
            name: event.name || '',
            description: event.description || '',
            event_type: (event.event_type || 'gaming').toLowerCase(),
            participant_limit: event.participant_limit || 100,
            status: event.status || 'active'
        });
        setEditError('');
    };

    // Save Edited Event
    const handleSaveEdit = async (e) => {
        e.preventDefault();
        if (!editingEvent) return;
        setEditLoading(true);
        setEditError('');

        try {
            const payload = {
                name: editFormData.name,
                description: editFormData.description,
                event_type: editFormData.event_type,
                participant_limit: editFormData.participant_limit ? parseInt(editFormData.participant_limit, 10) : null,
                status: editFormData.status
            };
            const updated = await api.updateEvent(editingEvent.id, payload);
            setEvents(prev => prev.map(ev => ev.id === editingEvent.id ? { ...ev, ...updated } : ev));
            setEditingEvent(null);
            setActionAlert({ type: 'success', text: `Tournament "${updated.name}" updated successfully!` });
            setTimeout(() => setActionAlert(null), 4000);
        } catch (err) {
            setEditError(err.response?.data?.detail || err.message || 'Failed to update tournament');
        } finally {
            setEditLoading(false);
        }
    };

    // Confirm Delete Event
    const handleConfirmDelete = async () => {
        if (!deleteEventTarget) return;
        setDeleteLoading(true);
        try {
            await api.deleteEvent(deleteEventTarget.id);
            setEvents(prev => prev.filter(ev => ev.id !== deleteEventTarget.id));
            const deletedName = deleteEventTarget.name;
            setDeleteEventTarget(null);
            setActionAlert({ type: 'success', text: `Tournament "${deletedName}" deleted successfully.` });
            setTimeout(() => setActionAlert(null), 4000);
        } catch (err) {
            setActionAlert({ type: 'danger', text: err.response?.data?.detail || err.message || 'Failed to delete tournament' });
            setTimeout(() => setActionAlert(null), 5000);
        } finally {
            setDeleteLoading(false);
        }
    };

    // Extract unique event types for filtering
    const eventTypes = useMemo(() => {
        const types = new Set(events.map(e => e.event_type).filter(Boolean));
        return ['all', ...Array.from(types)];
    }, [events]);

    // Filter events by search and type
    const filteredEvents = useMemo(() => {
        return events.filter(e => {
            const matchesSearch = (e.name || '').toLowerCase().includes(searchQuery.toLowerCase()) ||
                                  (e.description || '').toLowerCase().includes(searchQuery.toLowerCase()) ||
                                  (e.event_type || '').toLowerCase().includes(searchQuery.toLowerCase());
            const matchesType = selectedType === 'all' || (e.event_type || '').toLowerCase() === selectedType.toLowerCase();
            return matchesSearch && matchesType;
        });
    }, [events, searchQuery, selectedType]);


    return (
        <div className="py-2">
            {/* Creator Header Banner */}
            <div className="dashboard-banner mb-4">
                <div className="row align-items-center">
                    <div className="col-lg-8 mb-3 mb-lg-0">
                        <div className="d-inline-flex align-items-center gap-2 mb-2">
                            <span className="badge-soft-primary">
                                <Trophy size={13} className="me-1" /> Tournament Creator Portal
                            </span>
                            <span className="badge-live-pulse">
                                <span className="pulse-dot"></span> System Live
                            </span>
                        </div>
                        <h1 className="h2 fw-bold mb-2">Creator Dashboard</h1>
                        <p className="text-muted mb-0" style={{ fontSize: '0.95rem', maxWidth: '600px' }}>
                            Manage your competitions, customize dynamic scoring rules, upload match data, and publish live leaderboards.
                        </p>
                    </div>
                    <div className="col-lg-4 text-lg-end">
                        <Link to="/creator/events/create" className="btn btn-primary px-4 py-2">
                            <PlusCircle className="me-2" size={18} /> Create Tournament
                        </Link>
                    </div>
                </div>
            </div>

            {/* Stats Overview Grid */}
            <div className="row g-3 mb-4">
                <div className="col-sm-6 col-xl-3">
                    <div className="stat-card">
                        <div className="stat-icon-wrapper stat-icon-green">
                            <Trophy size={24} />
                        </div>
                        <div>
                            <div className="stat-value">{events.length}</div>
                            <div className="stat-label">Total Tournaments</div>
                        </div>
                    </div>
                </div>

                <div className="col-sm-6 col-xl-3">
                    <div className="stat-card">
                        <div className="stat-icon-wrapper stat-icon-blue">
                            <Activity size={24} />
                        </div>
                        <div>
                            <div className="stat-value">{events.length}</div>
                            <div className="stat-label">Active Competitions</div>
                        </div>
                    </div>
                </div>

                <div className="col-sm-6 col-xl-3">
                    <div className="stat-card">
                        <div className="stat-icon-wrapper stat-icon-amber">
                            <Gamepad2 size={24} />
                        </div>
                        <div>
                            <div className="stat-value">{new Set(events.map(e => e.event_type).filter(Boolean)).size}</div>
                            <div className="stat-label">Game Disciplines</div>
                        </div>
                    </div>
                </div>

                <div className="col-sm-6 col-xl-3">
                    <div className="stat-card">
                        <div className="stat-icon-wrapper stat-icon-purple">
                            <Sparkles size={24} />
                        </div>
                        <div>
                            <div className="stat-value" style={{ fontSize: '1.25rem', color: '#7c3aed' }}>Automated</div>
                            <div className="stat-label">Scoring Engine</div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Tournaments Header & Filters */}
            <div className="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3 mb-4">
                <div>
                    <h3 className="h5 fw-bold mb-1 d-flex align-items-center gap-2">
                        My Tournaments
                        <span className="badge bg-light text-dark border px-2 py-1" style={{ fontSize: '0.75rem' }}>
                            {filteredEvents.length}
                        </span>
                    </h3>
                    <p className="text-muted small mb-0">Browse and manage all competitions under your organization</p>
                </div>

                <div className="d-flex flex-wrap gap-2">
                    {/* Search Bar */}
                    <div className="position-relative" style={{ minWidth: '220px' }}>
                        <Search size={16} className="position-absolute text-muted" style={{ left: '12px', top: '50%', transform: 'translateY(-50%)' }} />
                        <input
                            type="text"
                            className="form-control form-control-sm ps-5"
                            placeholder="Search tournament..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                        />
                    </div>

                    {/* Filter selector */}
                    {eventTypes.length > 2 && (
                        <select
                            className="form-select form-select-sm"
                            value={selectedType}
                            onChange={(e) => setSelectedType(e.target.value)}
                            style={{ width: 'auto' }}
                        >
                            {eventTypes.map(type => (
                                <option key={type} value={type}>
                                    {type === 'all' ? 'All Games' : type.toUpperCase()}
                                </option>
                            ))}
                        </select>
                    )}
                </div>
            </div>

            {/* Action Notification Alert */}
            {actionAlert && (
                <div className={`alert alert-${actionAlert.type} alert-dismissible fade show rounded-3 mb-4 d-flex align-items-center justify-content-between`} role="alert">
                    <div className="d-flex align-items-center gap-2">
                        {actionAlert.type === 'success' ? <Check size={18} /> : <AlertTriangle size={18} />}
                        <span>{actionAlert.text}</span>
                    </div>
                    <button type="button" className="btn-close" onClick={() => setActionAlert(null)}></button>
                </div>
            )}

            {/* Events Content */}
            {isLoading ? (
                <div className="text-center py-5">
                    <div className="spinner-border text-primary" role="status"></div>
                    <p className="text-muted mt-2 small">Loading tournaments...</p>
                </div>
            ) : filteredEvents.length === 0 ? (
                <div className="card-modern p-5 text-center my-3">
                    <div className="stat-icon-wrapper stat-icon-green mx-auto mb-3" style={{ width: '64px', height: '64px' }}>
                        <Trophy size={32} />
                    </div>
                    <h4 className="fw-bold mb-2">No Tournaments Found</h4>
                    <p className="text-muted small mb-4" style={{ maxWidth: '400px', margin: '0 auto' }}>
                        {searchQuery ? "No tournaments match your search criteria. Try a different query." : "You haven't created any tournaments yet. Launch your first tournament in seconds."}
                    </p>
                    <div>
                        <Link to="/creator/events/create" className="btn btn-primary">
                            <PlusCircle size={16} className="me-1" /> Create First Tournament
                        </Link>
                    </div>
                </div>
            ) : (
                <div className="row g-4">
                    {filteredEvents.map(event => {
                        const isOwner = user?.role === 'admin' || event.creator_id === user?.id;
                        return (
                        <div key={event.id} className="col-md-6 col-lg-4">
                            <div className="event-card">
                                <div className="event-card-body">
                                    {/* Top Bar: Game Badge & Status & Edit/Delete actions */}
                                    <div className="d-flex justify-content-between align-items-center mb-2">
                                        <span className="badge-soft-primary">
                                            {event.event_type || 'General'}
                                        </span>
                                        <div className="d-flex align-items-center gap-2">
                                            <span className="badge-live-pulse" style={{ fontSize: '0.7rem', padding: '0.2rem 0.55rem' }}>
                                                <span className="pulse-dot" style={{ width: '6px', height: '6px' }}></span> {event.status || 'Active'}
                                            </span>
                                            {isOwner && (
                                                <>
                                                    <button
                                                        className="btn btn-sm btn-light border p-1 text-muted"
                                                        style={{ width: '28px', height: '28px', display: 'inline-flex', alignItems: 'center', justifyContent: 'center', borderRadius: '6px' }}
                                                        onClick={() => handleOpenEdit(event)}
                                                        title="Edit Tournament"
                                                    >
                                                        <Edit3 size={13} />
                                                    </button>
                                                    <button
                                                        className="btn btn-sm btn-light border p-1 text-danger"
                                                        style={{ width: '28px', height: '28px', display: 'inline-flex', alignItems: 'center', justifyContent: 'center', borderRadius: '6px' }}
                                                        onClick={() => setDeleteEventTarget(event)}
                                                        title="Delete Tournament"
                                                    >
                                                        <Trash2 size={13} />
                                                    </button>
                                                </>
                                            )}
                                        </div>
                                    </div>

                                    {/* Organizer Info (if Admin viewing other's tournament) */}
                                    {event.creator && event.creator_id !== user?.id && (
                                        <div className="badge bg-light text-muted border mb-2" style={{ fontSize: '0.72rem' }}>
                                            Organizer: <span className="fw-semibold text-dark">{event.creator.name}</span>
                                        </div>
                                    )}

                                    {/* Title */}
                                    <h4 className="event-card-title text-capitalize">
                                        {event.name}
                                    </h4>

                                    {/* Description */}
                                    <p className="event-card-desc">
                                        {event.description || 'No additional tournament details provided.'}
                                    </p>

                                    {/* Meta Chips */}
                                    <div className="event-meta-chips">
                                        <span className="meta-chip">
                                            <Users size={13} className="text-muted" />
                                            Max: <strong>{event.participant_limit || 'Unlimited'}</strong>
                                        </span>
                                        <span className="meta-chip">
                                            <Gamepad2 size={13} className="text-muted" />
                                            {event.event_type || 'Standard'}
                                        </span>
                                    </div>
                                </div>

                                {/* Footer Action Bar */}
                                <div className="event-card-footer">
                                    <Link
                                        to={`/creator/events/${event.id}/rules`}
                                        className="btn btn-sm btn-outline-primary"
                                        title="Configure scoring rules"
                                    >
                                        <Sliders size={14} className="me-1" /> Rules
                                    </Link>
                                    
                                    <div className="d-flex gap-2">
                                        <Link
                                            to={`/player/leaderboard/${event.id}`}
                                            className="btn btn-sm btn-outline-secondary d-flex align-items-center"
                                            title="View public live leaderboard"
                                        >
                                            <ExternalLink size={14} />
                                        </Link>
                                        <Link
                                            to={`/creator/events/${event.id}/results`}
                                            className="btn btn-sm btn-primary"
                                            title="Upload results & calculate scores"
                                        >
                                            <UploadCloud size={14} className="me-1" /> Process
                                        </Link>
                                    </div>
                                </div>
                            </div>
                        </div>
                    ); })}
                </div>
            )}

            {/* Edit Tournament Modal */}
            {editingEvent && (
                <div className="modal show d-block" style={{ backgroundColor: 'rgba(15, 23, 42, 0.65)', backdropFilter: 'blur(4px)', zIndex: 1050 }} tabIndex="-1">
                    <div className="modal-dialog modal-dialog-centered">
                        <div className="modal-content border-0 shadow-lg rounded-4 overflow-hidden">
                            <div className="modal-header border-bottom py-3 px-4 bg-light">
                                <div className="d-flex align-items-center gap-2">
                                    <div className="stat-icon-wrapper stat-icon-green" style={{ width: '32px', height: '32px', margin: 0 }}>
                                        <Edit3 size={16} />
                                    </div>
                                    <h5 className="modal-title fw-bold fs-6 mb-0">Edit Tournament Details</h5>
                                </div>
                                <button type="button" className="btn-close" onClick={() => setEditingEvent(null)} disabled={editLoading}></button>
                            </div>
                            <form onSubmit={handleSaveEdit}>
                                <div className="modal-body p-4">
                                    {editError && (
                                        <div className="alert alert-danger py-2 px-3 small rounded-3 mb-3">
                                            {editError}
                                        </div>
                                    )}

                                    <div className="mb-3">
                                        <label className="form-label small fw-semibold text-muted">Tournament Name *</label>
                                        <input
                                            type="text"
                                            className="form-control form-control-sm"
                                            required
                                            value={editFormData.name}
                                            onChange={(e) => setEditFormData({ ...editFormData, name: e.target.value })}
                                            placeholder="e.g. Annual Championship / Rapid Tournament"
                                        />
                                    </div>

                                    <div className="mb-3">
                                        <label className="form-label small fw-semibold text-muted">Description</label>
                                        <textarea
                                            className="form-control form-control-sm"
                                            rows="3"
                                            value={editFormData.description}
                                            onChange={(e) => setEditFormData({ ...editFormData, description: e.target.value })}
                                            placeholder="Overview of the competition rules and structure..."
                                        ></textarea>
                                    </div>

                                    <div className="row g-2 mb-3">
                                        <div className="col-md-6">
                                            <label className="form-label small fw-semibold text-muted">Category / Discipline</label>
                                            <input
                                                type="text"
                                                className="form-control form-control-sm"
                                                required
                                                value={editFormData.event_type}
                                                onChange={(e) => setEditFormData({ ...editFormData, event_type: e.target.value })}
                                                placeholder="e.g. Sports, Quiz, Coding, Chess, etc."
                                            />
                                        </div>
                                        <div className="col-md-6">
                                            <label className="form-label small fw-semibold text-muted">Max Capacity</label>
                                            <input
                                                type="number"
                                                min="1"
                                                className="form-control form-control-sm"
                                                value={editFormData.participant_limit}
                                                onChange={(e) => setEditFormData({ ...editFormData, participant_limit: e.target.value })}
                                                placeholder="e.g. 12"
                                            />
                                        </div>
                                    </div>

                                    <div className="mb-2">
                                        <label className="form-label small fw-semibold text-muted">Status</label>
                                        <select
                                            className="form-select form-select-sm"
                                            value={editFormData.status}
                                            onChange={(e) => setEditFormData({ ...editFormData, status: e.target.value })}
                                        >
                                            <option value="active">Active (Open for joining)</option>
                                            <option value="draft">Draft</option>
                                            <option value="completed">Completed</option>
                                            <option value="archived">Archived</option>
                                        </select>
                                    </div>
                                </div>
                                <div className="modal-footer border-top py-2 px-4 bg-light">
                                    <button type="button" className="btn btn-sm btn-outline-secondary" onClick={() => setEditingEvent(null)} disabled={editLoading}>
                                        Cancel
                                    </button>
                                    <button type="submit" className="btn btn-sm btn-primary px-3" disabled={editLoading}>
                                        {editLoading ? (
                                            <>
                                                <span className="spinner-border spinner-border-sm me-1" role="status"></span>
                                                Saving...
                                            </>
                                        ) : 'Save Changes'}
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            )}

            {/* Delete Confirmation Modal */}
            {deleteEventTarget && (
                <div className="modal show d-block" style={{ backgroundColor: 'rgba(15, 23, 42, 0.65)', backdropFilter: 'blur(4px)', zIndex: 1050 }} tabIndex="-1">
                    <div className="modal-dialog modal-dialog-centered">
                        <div className="modal-content border-0 shadow-lg rounded-4 overflow-hidden">
                            <div className="modal-header border-bottom py-3 px-4 bg-light">
                                <div className="d-flex align-items-center gap-2 text-danger">
                                    <AlertTriangle size={18} />
                                    <h5 className="modal-title fw-bold fs-6 mb-0">Delete Tournament?</h5>
                                </div>
                                <button type="button" className="btn-close" onClick={() => setDeleteEventTarget(null)} disabled={deleteLoading}></button>
                            </div>
                            <div className="modal-body p-4">
                                <p className="mb-2">
                                    Are you sure you want to delete <strong className="text-dark">"{deleteEventTarget.name}"</strong>?
                                </p>
                                <p className="text-muted small mb-0">
                                    This action is permanent and will remove all associated scoring rules, participants, match results, and leaderboard data.
                                </p>
                            </div>
                            <div className="modal-footer border-top py-2 px-4 bg-light">
                                <button type="button" className="btn btn-sm btn-outline-secondary" onClick={() => setDeleteEventTarget(null)} disabled={deleteLoading}>
                                    Cancel
                                </button>
                                <button type="button" className="btn btn-sm btn-danger px-3" onClick={handleConfirmDelete} disabled={deleteLoading}>
                                    {deleteLoading ? (
                                        <>
                                            <span className="spinner-border spinner-border-sm me-1" role="status"></span>
                                            Deleting...
                                        </>
                                    ) : (
                                        <>
                                            <Trash2 size={13} className="me-1" /> Delete Permanently
                                        </>
                                    )}
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default CreatorDashboard;

