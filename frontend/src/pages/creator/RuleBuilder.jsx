import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { api } from '../../api/client';
import { Trash2, Plus, Sliders, ArrowLeft, CheckCircle2, Sparkles, HelpCircle } from 'lucide-react';

const RuleBuilder = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    
    const [event, setEvent] = useState(null);
    const [rules, setRules] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [isSaving, setIsSaving] = useState(false);
    const [error, setError] = useState('');

    const [newRule, setNewRule] = useState({
        metric: '',
        condition: '',
        operator: 'each',
        value: '',
        points: '',
        priority: 0
    });

    useEffect(() => {
        const fetchData = async () => {
            try {
                const eventData = await api.getEvent(id);
                setEvent(eventData);
                const rulesData = await api.getRules(id);
                setRules(rulesData || []);
            } catch (err) {
                setError('Failed to load tournament or rules.');
            } finally {
                setIsLoading(false);
            }
        };
        fetchData();
    }, [id]);

    const handleAddRule = async (e) => {
        e.preventDefault();
        setError('');
        setIsSaving(true);
        try {
            const payload = {
                ...newRule,
                points: parseFloat(newRule.points),
                priority: parseInt(newRule.priority) || 0,
                value: newRule.operator === 'each' ? null : newRule.value
            };
            const createdRule = await api.createRule(id, payload);
            setRules([...rules, createdRule]);
            
            // Reset form
            setNewRule({
                metric: '',
                condition: '',
                operator: 'each',
                value: '',
                points: '',
                priority: 0
            });
        } catch (err) {
            setError(err.response?.data?.detail || err.message || 'Failed to add rule');
        } finally {
            setIsSaving(false);
        }
    };

    if (isLoading) return (
        <div className="text-center py-5">
            <div className="spinner-border text-primary" role="status"></div>
            <p className="text-muted small mt-2">Loading scoring engine...</p>
        </div>
    );
    
    if (!event) return (
        <div className="alert alert-danger my-4 rounded-3">Tournament not found or unauthorized.</div>
    );

    return (
        <div className="py-2">
            {/* Header */}
            <div className="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3 mb-4">
                <div>
                    <Link to="/creator/dashboard" className="text-decoration-none text-muted small d-inline-flex align-items-center gap-1 mb-2 hover-primary">
                        <ArrowLeft size={16} /> Back to Dashboard
                    </Link>
                    <div className="d-flex align-items-center gap-2">
                        <h1 className="h3 fw-bold mb-0">Rule Builder & Scoring Engine</h1>
                        <span className="badge-soft-primary text-uppercase">{event.event_type || 'General'}</span>
                    </div>
                    <p className="text-muted small mb-0 mt-1">Configuring rules for tournament: <strong>{event.name}</strong></p>
                </div>
                <div className="d-flex gap-2">
                    <button className="btn btn-outline-secondary" onClick={() => navigate('/creator/dashboard')}>
                        Back
                    </button>
                    <button className="btn btn-primary" onClick={() => navigate(`/creator/events/${id}/results`)}>
                        Proceed to Results →
                    </button>
                </div>
            </div>

            {error && <div className="alert alert-danger rounded-3 mb-4">{error}</div>}

            <div className="row g-4">
                {/* Active Rules List */}
                <div className="col-lg-8">
                    <div className="card-modern h-100">
                        <div className="card-modern-header d-flex justify-content-between align-items-center">
                            <div className="d-flex align-items-center gap-2">
                                <Sliders size={18} className="text-primary" />
                                <h2 className="h6 fw-bold mb-0">Active Scoring Rules</h2>
                            </div>
                            <span className="badge bg-light text-dark border px-2 py-1" style={{ fontSize: '0.75rem' }}>
                                {rules.length} Configured
                            </span>
                        </div>
                        
                        <div className="p-0">
                            {rules.length === 0 ? (
                                <div className="p-5 text-center">
                                    <div className="stat-icon-wrapper stat-icon-green mx-auto mb-3" style={{ width: '56px', height: '56px' }}>
                                        <Sparkles size={28} />
                                    </div>
                                    <h5 className="fw-bold mb-1">No Scoring Rules Defined Yet</h5>
                                    <p className="text-muted small mb-0" style={{ maxWidth: '400px', margin: '0 auto' }}>
                                        Define rules like points per kill, placement multipliers, or bonus thresholds using the panel on the right.
                                    </p>
                                </div>
                            ) : (
                                <div className="table-responsive">
                                    <table className="table table-hover align-middle mb-0">
                                        <thead className="table-light">
                                            <tr>
                                                <th className="ps-4">Metric</th>
                                                <th>Condition</th>
                                                <th>Target Value</th>
                                                <th>Points Awarded</th>
                                                <th>Priority</th>
                                                <th className="pe-4 text-end">Action</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {rules.map(rule => (
                                                <tr key={rule.id}>
                                                    <td className="ps-4 fw-bold text-dark">{rule.metric}</td>
                                                    <td>
                                                        <span className="badge bg-light text-dark border">
                                                            {rule.operator === 'each' ? '✖ Each unit' : rule.operator}
                                                        </span>
                                                    </td>
                                                    <td>{rule.value || <span className="text-muted">-</span>}</td>
                                                    <td>
                                                        <span className={`badge ${rule.points >= 0 ? 'bg-success' : 'bg-danger'} px-2 py-1`}>
                                                            {rule.points > 0 ? `+${rule.points}` : rule.points} pts
                                                        </span>
                                                    </td>
                                                    <td><span className="text-muted small">{rule.priority}</span></td>
                                                    <td className="pe-4 text-end">
                                                        <button className="btn btn-sm btn-outline-danger border-0" title="Delete rule">
                                                            <Trash2 size={16} />
                                                        </button>
                                                    </td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            )}
                        </div>
                    </div>
                </div>

                {/* Add Rule Form */}
                <div className="col-lg-4">
                    <div className="card-modern">
                        <div className="card-modern-header">
                            <h2 className="h6 fw-bold mb-0 d-flex align-items-center gap-2">
                                <Plus size={18} className="text-primary" /> Add New Rule
                            </h2>
                        </div>
                        <div className="p-4">
                            <form onSubmit={handleAddRule}>
                                <div className="mb-3">
                                    <label className="form-label small fw-bold text-muted text-uppercase">
                                        Metric Name <span className="text-danger">*</span>
                                    </label>
                                    <input 
                                        type="text" 
                                        className="form-control form-control-sm" 
                                        placeholder="e.g. kills, rank, placement, damage"
                                        value={newRule.metric} 
                                        onChange={e => setNewRule({...newRule, metric: e.target.value})} 
                                        required 
                                    />
                                </div>

                                <div className="mb-3">
                                    <label className="form-label small fw-bold text-muted text-uppercase">
                                        Rule Operation <span className="text-danger">*</span>
                                    </label>
                                    <select 
                                        className="form-select form-select-sm" 
                                        value={newRule.operator} 
                                        onChange={e => setNewRule({...newRule, operator: e.target.value})}
                                    >
                                        <option value="each">Each Unit (e.g. 1 kill = X pts)</option>
                                        <option value="equals">Exact Equals (==)</option>
                                        <option value=">">Greater Than (&gt;)</option>
                                        <option value="<">Less Than (&lt;)</option>
                                        <option value=">=">Greater or Equal (&gt;=)</option>
                                        <option value="<=">Less or Equal (&lt;=)</option>
                                    </select>
                                </div>

                                {newRule.operator !== 'each' && (
                                    <div className="mb-3">
                                        <label className="form-label small fw-bold text-muted text-uppercase">
                                            Condition Target Value <span className="text-danger">*</span>
                                        </label>
                                        <input 
                                            type="text" 
                                            className="form-control form-control-sm" 
                                            placeholder="e.g. 1 (for rank 1), or WIN"
                                            value={newRule.value} 
                                            onChange={e => setNewRule({...newRule, value: e.target.value})} 
                                            required 
                                        />
                                    </div>
                                )}

                                <div className="mb-3">
                                    <label className="form-label small fw-bold text-muted text-uppercase">
                                        Points Awarded <span className="text-danger">*</span>
                                    </label>
                                    <input 
                                        type="number" 
                                        className="form-control form-control-sm" 
                                        placeholder="e.g. 10, 5, or -2" 
                                        step="0.5"
                                        value={newRule.points} 
                                        onChange={e => setNewRule({...newRule, points: e.target.value})} 
                                        required 
                                    />
                                    <div className="form-text small text-muted">Use positive for bonus, negative for penalties.</div>
                                </div>

                                <div className="mb-4">
                                    <label className="form-label small fw-bold text-muted text-uppercase">
                                        Evaluation Priority
                                    </label>
                                    <input 
                                        type="number" 
                                        className="form-control form-control-sm" 
                                        value={newRule.priority} 
                                        onChange={e => setNewRule({...newRule, priority: e.target.value})} 
                                    />
                                </div>

                                <button 
                                    type="submit" 
                                    className="btn btn-primary w-100 py-2 d-flex align-items-center justify-content-center" 
                                    disabled={isSaving}
                                >
                                    {isSaving ? (
                                        'Saving Rule...'
                                    ) : (
                                        <><Plus size={16} className="me-1"/> Add Scoring Rule</>
                                    )}
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
            
            <div className="d-flex justify-content-end mt-4 pt-3 border-top">
                <button className="btn btn-primary px-4" onClick={() => navigate('/creator/dashboard')}>
                    <CheckCircle2 size={16} className="me-2" /> Finish Setup & Return
                </button>
            </div>
        </div>
    );
};

export default RuleBuilder;

