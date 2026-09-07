import React, { createContext, useContext, useState, useEffect } from 'react';
import { api } from '../api/client';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    const checkAuth = async () => {
        try {
            if (localStorage.getItem('access_token')) {
                const userData = await api.getMe();
                setUser(userData);
                return userData;
            }
        } catch (error) {
            console.error('Auth check failed', error);
            setUser(null);
        } finally {
            setLoading(false);
        }
        return null;
    };

    useEffect(() => {
        checkAuth();
    }, []);

    const login = async (email, password) => {
        await api.login(email, password);
        return await checkAuth();
    };

    const register = async (userData) => {
        await api.register(userData);
    };

    const logout = () => {
        api.logout();
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, loading, login, register, logout, checkAuth }}>
            {!loading && children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
