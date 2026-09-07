import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { api } from '../../api/client';
import { Trophy, Medal, Download, Search, Users, ArrowLeft, Crown, Award, Activity } from 'lucide-react';
import { Bar } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const Leaderboard = () => {
    const { id } = useParams();
    const [event, setEvent] = useState(null);
    const [leaderboard, setLeaderboard] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        const fetchLeaderboard = async () => {
            try {
                const eventData = await api.getEvent(id);
                setEvent(eventData);
                const lbData = await api.getLeaderboard(id);
                setLeaderboard(lbData);
            } catch (err) {
                console.error('Failed to load leaderboard', err);
            } finally {
                setIsLoading(false);
            }
        };
        fetchLeaderboard();
    }, [id]);

    const handleSearch = async (e) => {
        e.preventDefault();
        try {
            const data = await api.getLeaderboard(id, { search: searchTerm });
            setLeaderboard(data);
        } catch (error) {
            console.error('Search failed', error);
        }
    };

    const handleExport = (format) => {
        if (!leaderboard) return;
        if (format === 'json') {
            const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(leaderboard, null, 2));
            const downloadAnchorNode = document.createElement('a');
            downloadAnchorNode.setAttribute("href", dataStr);
            downloadAnchorNode.setAttribute("download", `leaderboard_${id}.json`);
            document.body.appendChild(downloadAnchorNode);
            downloadAnchorNode.click();
            downloadAnchorNode.remove();
        } else if (format === 'csv') {
            const headers = ['Rank', 'Player ID', 'Username', 'Score'];
            const rows = leaderboard.rankings.map(r => [r.rank, r.external_player_id, r.username, r.score]);
            const csvContent = "data:text/csv;charset=utf-8," + [headers.join(','), ...rows.map(e => e.join(','))].join('\n');
            const downloadAnchorNode = document.createElement('a');
            downloadAnchorNode.setAttribute("href", encodeURI(csvContent));
            downloadAnchorNode.setAttribute("download", `leaderboard_${id}.csv`);
            document.body.appendChild(downloadAnchorNode);
            downloadAnchorNode.click();
            downloadAnchorNode.remove();
        }
    };

    if (isLoading) return (
        <div className="text-center py-5">
            <div className="spinner-border text-primary" role="status"></div>
            <p className="text-muted small mt-2">Loading official leaderboard...</p>
        </div>
    );

    if (!event || !leaderboard) return (
        <div className="alert alert-danger my-4 rounded-3">Failed to load leaderboard.</div>
    );

    // Chart Data prep (Top 10 max)
    const topPerformers = leaderboard.rankings.slice(0, 10);
    const chartData = {
        labels: topPerformers.map(r => r.username || r.external_player_id || `ID: ${r.participant_id}`),
        datasets: [{
            label: 'Total Score',
            data: topPerformers.map(r => r.score),
            backgroundColor: 'rgba(74, 93, 35, 0.85)',
            borderColor: '#4a5d23',
            borderWidth: 1,
            borderRadius: 6
        }]
    };

    const top1 = leaderboard.rankings.find(r => r.rank === 1);
    const top2 = leaderboard.rankings.find(r => r.rank === 2);
    const top3 = leaderboard.rankings.find(r => r.rank === 3);

    return (
        <div className="py-2">
            {/* Header */}
            <div className="dashboard-banner mb-4">
                <div className="row align-items-center">
                    <div className="col-lg-8 mb-3 mb-lg-0">
                        <div className="d-inline-flex align-items-center gap-2 mb-2">
                            <span className="badge-soft-primary text-uppercase">
                                {event.event_type || 'Tournament'}
                            </span>
                            <span className="badge-live-pulse">
                                <span className="pulse-dot"></span> Live Standings
                            </span>
                        </div>
                        <h1 className="h2 fw-bold mb-1 text-capitalize">{event.name}</h1>
                        <p className="text-muted mb-0" style={{ fontSize: '0.95rem' }}>
                            {event.description || 'Official live rankings and analytics updated in real-time.'}
                        </p>
                    </div>
                    <div className="col-lg-4 text-lg-end">
                        <div className="d-inline-flex gap-2">
                            <button className="btn btn-sm btn-outline-secondary" onClick={() => handleExport('csv')}>
                                <Download size={14} className="me-1"/> CSV
                            </button>
                            <button className="btn btn-sm btn-outline-secondary" onClick={() => handleExport('json')}>
                                <Download size={14} className="me-1"/> JSON
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            {/* Podium Showcase (Top 3) */}
            {leaderboard.rankings.length >= 2 && (
                <div className="row g-3 mb-4 justify-content-center">
                    {/* Rank 2 */}
                    {top2 && (
                        <div className="col-md-4 order-2 order-md-1">
                            <div className="card-modern p-3 text-center h-100" style={{ borderTop: '4px solid #94a3b8' }}>
                                <Medal size={28} className="text-secondary mb-1" />
                                <div className="badge bg-light text-secondary border mb-1">Rank 2</div>
                                <h4 className="h6 fw-bold mb-0 text-truncate">{top2.username || `Player #${top2.participant_id}`}</h4>
                                <div className="h4 fw-bold text-primary mt-1 mb-0">{top2.score.toLocaleString()} <span className="small text-muted" style={{ fontSize: '0.75rem' }}>pts</span></div>
                            </div>
                        </div>
                    )}

                    {/* Rank 1 */}
                    {top1 && (
                        <div className="col-md-4 order-1 order-md-2">
                            <div className="card-modern p-4 text-center h-100 shadow-md" style={{ borderTop: '4px solid #f59e0b', transform: 'scale(1.03)', zIndex: 2 }}>
                                <Crown size={36} className="text-warning mb-1" />
                                <div className="badge bg-warning text-dark mb-1">Champion - Rank 1</div>
                                <h3 className="h5 fw-bold mb-0 text-truncate">{top1.username || `Player #${top1.participant_id}`}</h3>
                                <div className="h3 fw-bold text-primary mt-1 mb-0">{top1.score.toLocaleString()} <span className="small text-muted" style={{ fontSize: '0.8rem' }}>pts</span></div>
                            </div>
                        </div>
                    )}

                    {/* Rank 3 */}
                    {top3 && (
                        <div className="col-md-4 order-3 order-md-3">
                            <div className="card-modern p-3 text-center h-100" style={{ borderTop: '4px solid #cd7f32' }}>
                                <Medal size={28} style={{ color: '#cd7f32' }} className="mb-1" />
                                <div className="badge bg-light border mb-1" style={{ color: '#cd7f32' }}>Rank 3</div>
                                <h4 className="h6 fw-bold mb-0 text-truncate">{top3.username || `Player #${top3.participant_id}`}</h4>
                                <div className="h4 fw-bold text-primary mt-1 mb-0">{top3.score.toLocaleString()} <span className="small text-muted" style={{ fontSize: '0.75rem' }}>pts</span></div>
                            </div>
                        </div>
                    )}
                </div>
            )}

            {/* Main Content Row */}
            <div className="row g-4 mb-5">
                {/* Rankings Table */}
                <div className="col-lg-8">
                    <div className="card-modern h-100">
                        <div className="card-modern-header d-flex justify-content-between align-items-center">
                            <div className="d-flex align-items-center gap-2">
                                <Trophy size={18} className="text-primary" />
                                <h2 className="h6 fw-bold mb-0">Official Rankings Table</h2>
                            </div>
                            <span className="badge-soft-primary">
                                Total Players: {leaderboard.total_participants}
                            </span>
                        </div>

                        <div className="p-3 bg-light border-bottom">
                            <form className="d-flex" onSubmit={handleSearch}>
                                <div className="position-relative flex-grow-1 me-2">
                                    <Search size={16} className="position-absolute text-muted" style={{ left: '12px', top: '50%', transform: 'translateY(-50%)' }} />
                                    <input 
                                        type="search" 
                                        className="form-control form-control-sm ps-5" 
                                        placeholder="Search by username or Player ID..." 
                                        value={searchTerm}
                                        onChange={(e) => setSearchTerm(e.target.value)}
                                    />
                                </div>
                                <button className="btn btn-sm btn-primary px-3" type="submit">Search</button>
                            </form>
                        </div>

                        <div className="table-responsive">
                            <table className="table table-hover align-middle mb-0">
                                <thead className="table-light">
                                    <tr>
                                        <th className="text-center" style={{ width: '80px' }}>Rank</th>
                                        <th>Competitor</th>
                                        <th className="text-end pe-4">Score</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {leaderboard.rankings.length === 0 ? (
                                        <tr>
                                            <td colSpan="3" className="text-center py-5 text-muted">
                                                No ranked records found. Match results will appear once uploaded.
                                            </td>
                                        </tr>
                                    ) : leaderboard.rankings.map((r) => (
                                        <tr key={r.id}>
                                            <td className="text-center">
                                                {r.rank === 1 ? <span className="badge bg-warning text-dark px-2 py-1">1st</span> :
                                                 r.rank === 2 ? <span className="badge bg-secondary px-2 py-1">2nd</span> :
                                                 r.rank === 3 ? <span className="badge px-2 py-1" style={{ backgroundColor: '#cd7f32', color: '#fff' }}>3rd</span> :
                                                 <span className="fw-bold text-muted">#{r.rank}</span>}
                                            </td>
                                            <td>
                                                <div className="d-flex align-items-center gap-2">
                                                    <div className="stat-icon-wrapper stat-icon-green" style={{ width: '32px', height: '32px', fontSize: '0.8rem', fontWeight: 'bold', margin: 0 }}>
                                                        {(r.username || 'P').charAt(0).toUpperCase()}
                                                    </div>
                                                    <div>
                                                        <div className="fw-bold text-dark">{r.username || `Player #${r.participant_id}`}</div>
                                                        {r.external_player_id && <small className="text-muted text-uppercase">UID: {r.external_player_id}</small>}
                                                    </div>
                                                </div>
                                            </td>
                                            <td className="text-end pe-4 fw-bold text-primary fs-6">
                                                {r.score.toLocaleString()} pts
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
                
                {/* Analytics & Summary */}
                <div className="col-lg-4">
                    <div className="card-modern mb-4">
                        <div className="card-modern-header">
                            <h2 className="h6 fw-bold mb-0">Top 10 Performers</h2>
                        </div>
                        <div className="p-3">
                            {topPerformers.length > 0 ? (
                                <Bar 
                                    data={chartData} 
                                    options={{ 
                                        responsive: true, 
                                        plugins: { legend: { display: false } },
                                        scales: {
                                            y: { beginAtZero: true, grid: { color: 'rgba(0,0,0,0.04)' } },
                                            x: { grid: { display: false } }
                                        }
                                    }} 
                                />
                            ) : (
                                <div className="text-center text-muted py-4 small">No data to display</div>
                            )}
                        </div>
                    </div>
                    
                    <div className="card-modern">
                        <div className="card-modern-header">
                            <h2 className="h6 fw-bold mb-0">Tournament Overview</h2>
                        </div>
                        <div className="p-3">
                            <div className="d-flex justify-content-between py-2 border-bottom">
                                <span className="text-muted small">Game Discipline</span>
                                <span className="fw-bold small text-capitalize">{event.event_type || 'Standard'}</span>
                            </div>
                            <div className="d-flex justify-content-between py-2 border-bottom">
                                <span className="text-muted small">Average Score</span>
                                <span className="fw-bold small">
                                    {leaderboard.rankings.length > 0 
                                        ? (leaderboard.rankings.reduce((a, b) => a + b.score, 0) / leaderboard.rankings.length).toFixed(1) 
                                        : '0'} pts
                                </span>
                            </div>
                            <div className="d-flex justify-content-between py-2">
                                <span className="text-muted small">Top Score</span>
                                <span className="fw-bold text-success small">
                                    {leaderboard.rankings.length > 0 ? `${leaderboard.rankings[0].score.toLocaleString()} pts` : '0 pts'}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Leaderboard;

