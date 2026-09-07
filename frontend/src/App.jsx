import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute';

import Login from './pages/auth/Login';
import Register from './pages/auth/Register';
import { AdminDashboard } from './pages/TempDashboards';
import Home from './pages/Home';
import Footer from './components/Footer';

// Creator Pages
import CreatorDashboard from './pages/creator/Dashboard';
import CreateEvent from './pages/creator/CreateEvent';
import RuleBuilder from './pages/creator/RuleBuilder';

// Player Pages
import PlayerDashboard from './pages/player/Dashboard';
import Leaderboard from './pages/player/Leaderboard';

// Results Processing Flow
import UploadFlow from './pages/results/UploadFlow';

const App = () => {
    return (
        <div className="d-flex flex-column min-vh-100">
            <Navbar />
            <main className="container flex-grow-1 py-4">
                <Routes>
                    {/* Public Routes */}
                    <Route path="/" element={<Home />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />
                    
                    {/* Public/Shared view for leaderboard */}
                    <Route path="/player/leaderboard/:id" element={<Leaderboard />} />

                    {/* Creator Routes */}
                    <Route element={<ProtectedRoute allowedRoles={['creator', 'admin']} />}>
                        <Route path="/creator/dashboard" element={<CreatorDashboard />} />
                        <Route path="/creator/events/create" element={<CreateEvent />} />
                        <Route path="/creator/events/:id/rules" element={<RuleBuilder />} />
                        <Route path="/creator/events/:id/results" element={<UploadFlow />} />
                    </Route>

                    {/* Admin Routes */}
                    <Route element={<ProtectedRoute allowedRoles={['admin']} />}>
                        <Route path="/admin/dashboard" element={<AdminDashboard />} />
                    </Route>

                    {/* Player Routes */}
                    <Route element={<ProtectedRoute allowedRoles={['player']} />}>
                        <Route path="/player/dashboard" element={<PlayerDashboard />} />
                    </Route>
                </Routes>
            </main>
            <Footer />
        </div>
    );
};

export default App;
