import React, { useState, useEffect, useMemo } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../../api/client';
import { useAuth } from '../../contexts/AuthContext';
import { Trophy, Users, LogIn, Search, Gamepad2, Award, ShieldCheck, Check, AlertCircle, CheckCircle2, Info, X } from 'lucide-react';

const PlayerDashboard = () => {
    const { user } = useAuth();
    const [events, setEvents] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [joinLoading, setJoinLoading] = useState(null);
    const [joinedEvents, setJoinedEvents] = useState(new Set());
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedType, setSelectedType] = useState('all');

    // In-App Status Popup (e.g. limit reached, already joined, success)
    const [statusPopup, setStatusPopup] = useState(null);

    useEffect(() => {
        const fetchDashboardData = async () => {
            try {
                const [eventsData, myParts] = await Promise.all([
                    api.getEvents(),
                    api.getMyParticipations().catch(err => {
                        console.warn("Could not fetch participations", err);
                        return [];
                    })
                ]);
                setEvents(eventsData || []);
                if (Array.isArray(myParts)) {
                    setJoinedEvents(new Set(myParts.map(p => p.event_id)));
                }
            } catch (error) {
                console.error("Failed to fetch dashboard data", error);
            } finally {
                setIsLoading(false);
            }
        };
        fetchDashboardData();
    }, []);

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

    const handleJoinEvent = async (eventId) => {
        setJoinLoading(eventId);
        try {
            await api.joinEvent(eventId);
            setJoinedEvents(prev => new Set(prev).add(eventId));
            setStatusPopup({
                type: 'success',
                title: 'Successfully Registered!',
                message: 'You have joined the tournament. Your starting score of 0 pts has been recorded on the official leaderboard.',
                eventId: eventId
            });
        } catch (err) {
            const errorDetail = err.response?.data?.detail || err.message || 'Failed to join event';
            const lower = typeof errorDetail === 'string' ? errorDetail.toLowerCase() : '';

            if (lower.includes('limit reached')) {
                setStatusPopup({
                    type: 'warning',
                    title: 'Tournament Full',
                    message: 'Event participant limit reached. All player slots have been filled for this tournament.',
                });
            } else if (lower.includes('already joined')) {
                setJoinedEvents(prev => new Set(prev).add(eventId));
                setStatusPopup({
                    type: 'info',
                    title: 'Already Registered',
                    message: 'You have already joined this event. Head over to the leaderboard to track your standing!',
                    eventId: eventId
                });
            } else {
                setStatusPopup({
                    type: 'error',
                    title: 'Unable to Join',
                    message: errorDetail,
                });
            }
        } finally {
            setJoinLoading(null);
        }
    };



    return (
        <div className="py-2">
            {/* Player Welcome Banner */}
            <div className="dashboard-banner mb-4">
                <div className="row align-items-center">
                    <div className="col-lg-8 mb-3 mb-lg-0">
                        <div className="d-inline-flex align-items-center gap-2 mb-2">
                            <span className="badge-soft-primary">
                                <Gamepad2 size={13} className="me-1" /> Player Arena
                            </span>
                            <span className="badge-live-pulse">
                                <span className="pulse-dot"></span> Live Tournaments
                            </span>
                        </div>
                        <h1 className="h2 fw-bold mb-2">Welcome back, {user?.name || user?.username || 'Player'}!</h1>
                        <p className="text-muted mb-0" style={{ fontSize: '0.95rem', maxWidth: '600px' }}>
                            Discover available tournaments, join the competition, and climb up the official live leaderboards.
                        </p>
                    </div>
                    <div className="col-lg-4 text-lg-end">
                        <div className="d-inline-flex align-items-center gap-2 px-3 py-2 bg-white rounded-pill border shadow-sm">
                            <div className="stat-icon-wrapper stat-icon-green" style={{ width: '32px', height: '32px', margin: 0 }}>
                                <ShieldCheck size={18} />
                            </div>
                            <div className="text-start pe-2">
                                <div className="fw-bold small">{user?.name || user?.username}</div>
                                <div className="text-muted" style={{ fontSize: '0.7rem' }}>Verified Player</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Player Stats Grid */}
            <div className="row g-3 mb-4">
                <div className="col-sm-6 col-xl-4">
                    <div className="stat-card">
                        <div className="stat-icon-wrapper stat-icon-green">
                            <Trophy size={24} />
                        </div>
                        <div>
                            <div className="stat-value">{events.length}</div>
                            <div className="stat-label">Open Tournaments</div>
                        </div>
                    </div>
                </div>

                <div className="col-sm-6 col-xl-4">
                    <div className="stat-card">
                        <div className="stat-icon-wrapper stat-icon-blue">
                            <Award size={24} />
                        </div>
                        <div>
                            <div className="stat-value">{joinedEvents.size}</div>
                            <div className="stat-label">Registered Events</div>
                        </div>
                    </div>
                </div>

                <div className="col-sm-6 col-xl-4">
                    <div className="stat-card">
                        <div className="stat-icon-wrapper stat-icon-amber">
                            <Gamepad2 size={24} />
                        </div>
                        <div>
                            <div className="stat-value">{new Set(events.map(e => e.event_type).filter(Boolean)).size}</div>
                            <div className="stat-label">Active Game Categories</div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Search & Filter Header */}
            <div className="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3 mb-4">
                <div>
                    <h3 className="h5 fw-bold mb-1 d-flex align-items-center gap-2">
                        Available Tournaments
                        <span className="badge bg-light text-dark border px-2 py-1" style={{ fontSize: '0.75rem' }}>
                            {filteredEvents.length}
                        </span>
                    </h3>
                    <p className="text-muted small mb-0">Join ongoing tournaments and compete for top ranks</p>
                </div>

                <div className="d-flex flex-wrap gap-2">
                    <div className="position-relative" style={{ minWidth: '220px' }}>
                        <Search size={16} className="position-absolute text-muted" style={{ left: '12px', top: '50%', transform: 'translateY(-50%)' }} />
                        <input
                            type="text"
                            className="form-control form-control-sm ps-5"
                            placeholder="Search by game or title..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                        />
                    </div>

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

            {/* Tournaments List */}
            {isLoading ? (
                <div className="text-center py-5">
                    <div className="spinner-border text-primary" role="status"></div>
                    <p className="text-muted mt-2 small">Fetching available competitions...</p>
                </div>
            ) : filteredEvents.length === 0 ? (
                <div className="card-modern p-5 text-center my-3">
                    <div className="stat-icon-wrapper stat-icon-amber mx-auto mb-3" style={{ width: '64px', height: '64px' }}>
                        <Trophy size={32} />
                    </div>
                    <h4 className="fw-bold mb-2">No Tournaments Found</h4>
                    <p className="text-muted small mb-0">
                        {searchQuery ? "No events match your search term. Try searching something else." : "There are currently no active tournaments open for registration. Check back soon!"}
                    </p>
                </div>
            ) : (
                <div className="row g-4">
                    {filteredEvents.map(event => {
                        const isJoined = joinedEvents.has(event.id);
                        return (
                            <div key={event.id} className="col-md-6 col-lg-4">
                                <div className="event-card">
                                    <div className="event-card-body">
                                        <div className="d-flex justify-content-between align-items-center mb-2">
                                            <span className="badge-soft-primary">
                                                {event.event_type || 'Tournament'}
                                            </span>
                                            <span className="badge-live-pulse" style={{ fontSize: '0.7rem', padding: '0.2rem 0.55rem' }}>
                                                <span className="pulse-dot" style={{ width: '6px', height: '6px' }}></span> Open
                                            </span>
                                        </div>

                                        <h4 className="event-card-title text-capitalize">
                                            {event.name}
                                        </h4>

                                        <p className="event-card-desc">
                                            {event.description || 'Join this competitive event, earn match points and rise to the top of the leaderboard.'}
                                        </p>

                                        <div className="event-meta-chips">
                                            <span className="meta-chip">
                                                <Users size={13} className="text-muted" />
                                                Capacity: <strong>{event.participant_limit || 'Unlimited'}</strong>
                                            </span>
                                            <span className="meta-chip">
                                                <Gamepad2 size={13} className="text-muted" />
                                                {event.event_type || 'Standard'}
                                            </span>
                                        </div>
                                    </div>

                                    <div className="event-card-footer">
                                        <Link 
                                            to={`/player/leaderboard/${event.id}`} 
                                            className="btn btn-sm btn-outline-primary"
                                        >
                                            <Trophy size={14} className="me-1" /> Leaderboard
                                        </Link>

                                        <button 
                                            className={`btn btn-sm ${isJoined ? 'btn-success text-white' : 'btn-primary'}`}
                                            onClick={() => handleJoinEvent(event.id)}
                                            disabled={joinLoading === event.id || isJoined}
                                        >
                                            {joinLoading === event.id ? (
                                                <>
                                                    <span className="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span>
                                                    Joining...
                                                </>
                                            ) : isJoined ? (
                                                <>
                                                    <Check size={15} className="me-1" /> Registered
                                                </>
                                            ) : (
                                                <>
                                                    <LogIn size={15} className="me-1" /> Join Event
                                                </>
                                            )}
                                        </button>
                                    </div>
                                </div>
                            </div>
                        );
                    })}
                </div>
            )}

            {/* Custom In-App Status Popup Modal */}
            {statusPopup && (
                <div 
                    className="modal show d-block" 
                    style={{ backgroundColor: 'rgba(15, 23, 42, 0.65)', backdropFilter: 'blur(5px)', zIndex: 1060 }}
                    onClick={() => setStatusPopup(null)}
                >
                    <div 
                        className="modal-dialog modal-dialog-centered" 
                        style={{ maxWidth: '420px' }}
                        onClick={(e) => e.stopPropagation()}
                    >
                        <div className="modal-content border-0 shadow-lg rounded-4 overflow-hidden text-center p-4">
                            <div className="d-flex justify-content-end">
                                <button 
                                    type="button" 
                                    className="btn-close" 
                                    aria-label="Close"
                                    onClick={() => setStatusPopup(null)}
                                ></button>
                            </div>

                            <div className="modal-body p-0 pt-1 pb-3">
                                <div 
                                    className={`stat-icon-wrapper mx-auto mb-3 ${
                                        statusPopup.type === 'success' ? 'stat-icon-green' :
                                        statusPopup.type === 'warning' ? 'stat-icon-amber' :
                                        statusPopup.type === 'info' ? 'stat-icon-blue' : 'stat-icon-amber'
                                    }`}
                                    style={{ width: '64px', height: '64px' }}
                                >
                                    {statusPopup.type === 'success' && <CheckCircle2 size={32} className="text-success" />}
                                    {statusPopup.type === 'warning' && <AlertCircle size={32} className="text-warning" />}
                                    {statusPopup.type === 'info' && <Info size={32} className="text-primary" />}
                                    {statusPopup.type === 'error' && <AlertCircle size={32} className="text-danger" />}
                                </div>

                                <h4 className="fw-bold mb-2 fs-5 text-dark">
                                    {statusPopup.title}
                                </h4>

                                <p className="text-muted small mb-4 px-2" style={{ lineHeight: '1.55' }}>
                                    {statusPopup.message}
                                </p>

                                <div className="d-flex gap-2 justify-content-center">
                                    {statusPopup.eventId && (
                                        <Link
                                            to={`/player/leaderboard/${statusPopup.eventId}`}
                                            className="btn btn-sm btn-outline-primary px-3"
                                            onClick={() => setStatusPopup(null)}
                                        >
                                            <Trophy size={14} className="me-1" /> View Leaderboard
                                        </Link>
                                    )}
                                    <button
                                        type="button"
                                        className="btn btn-sm btn-primary px-4"
                                        onClick={() => setStatusPopup(null)}
                                    >
                                        Understood
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default PlayerDashboard;

