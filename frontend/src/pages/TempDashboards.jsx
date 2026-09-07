import React from 'react';
import { ShieldCheck, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';

export const AdminDashboard = () => (
    <div className="py-4">
        <div className="dashboard-banner mb-4">
            <span className="badge-soft-primary mb-2 d-inline-block">System Administration</span>
            <h1 className="h2 fw-bold mb-2">Admin Dashboard</h1>
            <p className="text-muted mb-0">Platform overview, tournament moderation, and user management.</p>
        </div>
        <div className="card-modern p-5 text-center">
            <div className="stat-icon-wrapper stat-icon-green mx-auto mb-3" style={{ width: '56px', height: '56px' }}>
                <ShieldCheck size={28} />
            </div>
            <h4 className="fw-bold mb-2">Admin Portal Active</h4>
            <p className="text-muted small mb-4">You have global administrative privileges over all tournaments, rules, and participants.</p>
            <Link to="/creator/dashboard" className="btn btn-primary">
                Switch to Creator Studio <ArrowRight size={16} className="ms-1" />
            </Link>
        </div>
    </div>
);

