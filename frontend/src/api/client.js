import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

const client = axios.create({
    baseURL: API_BASE_URL,
});

// Request Interceptor: Attach Token
client.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Response Interceptor: Handle 401
client.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && error.response.status === 401) {
            // Do not reload page on failed login attempts so error messages can be shown
            if (error.config && error.config.url && error.config.url.includes('/auth/login')) {
                return Promise.reject(error);
            }
            localStorage.removeItem('access_token');
            // Only redirect if not already on /login
            if (!window.location.pathname.includes('/login')) {
                window.location.href = '/login';
            }
        }
        return Promise.reject(error);
    }
);

export const api = {
    // Auth
    login: async (email, password) => {
        const { data } = await client.post('/auth/login', { email, password });
        if (data.access_token) {
            localStorage.setItem('access_token', data.access_token);
        }
        return data;
    },
    getMe: async () => {
        const { data } = await client.get('/auth/me');
        return data;
    },
    register: async (userData) => {
        const { data } = await client.post('/auth/register', userData);
        return data;
    },
    logout: () => {
        localStorage.removeItem('access_token');
        window.location.href = '/login';
    },

    // Events
    getEvents: async (filters = {}) => {
        const { data } = await client.get('/events', { params: filters });
        return data;
    },
    getEvent: async (id) => {
        const { data } = await client.get(`/events/${id}`);
        return data;
    },
    createEvent: async (eventData) => {
        const { data } = await client.post('/events', eventData);
        return data;
    },
    updateEvent: async (id, eventData) => {
        const { data } = await client.put(`/events/${id}`, eventData);
        return data;
    },
    deleteEvent: async (id) => {
        const { data } = await client.delete(`/events/${id}`);
        return data;
    },

    // Rules
    getRules: async (eventId) => {
        const { data } = await client.get(`/events/${eventId}/rules`);
        return data;
    },
    createRule: async (eventId, ruleData) => {
        const { data } = await client.post(`/events/${eventId}/rules`, ruleData);
        return data;
    },

    // Uploads
    uploadResults: async (eventId, file) => {
        const formData = new FormData();
        formData.append('file', file);
        const { data } = await client.post(`/events/${eventId}/results/upload`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
        });
        return data;
    },
    validateUpload: async (uploadId) => {
        const { data } = await client.post(`/uploads/${uploadId}/validate`);
        return data;
    },
    processUpload: async (uploadId) => {
        const { data } = await client.post(`/uploads/${uploadId}/process`);
        return data;
    },
    getValidationReport: async (uploadId) => {
        const { data } = await client.get(`/uploads/${uploadId}/validation`);
        return data;
    },

    // Leaderboard
    getLeaderboard: async (eventId, params = {}) => {
        const { data } = await client.get(`/events/${eventId}/leaderboard`, { params });
        return data;
    },

    // Participants
    getMyParticipations: async () => {
        const { data } = await client.get('/participants/me');
        return data;
    },
    joinEvent: async (eventId, externalPlayerId = null) => {
        const { data } = await client.post(`/events/${eventId}/join`, {
            external_player_id: externalPlayerId,
        });
        return data;
    },
    getParticipants: async (eventId) => {
        const { data } = await client.get(`/events/${eventId}/participants`);
        return data;
    },
};
