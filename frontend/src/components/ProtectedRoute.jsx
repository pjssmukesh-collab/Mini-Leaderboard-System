import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const ProtectedRoute = ({ allowedRoles }) => {
    const { user } = useAuth();

    if (!user) {
        return <Navigate to="/login" replace />;
    }

    if (allowedRoles && !allowedRoles.includes(user.role)) {
        // Send to appropriate dashboard if wrong role
        if (user.role === 'creator') return <Navigate to="/creator/dashboard" replace />;
        if (user.role === 'admin') return <Navigate to="/admin/dashboard" replace />;
        return <Navigate to="/player/dashboard" replace />;
    }

    return <Outlet />;
};

export default ProtectedRoute;
