import React, { useEffect, useState } from 'react';
import { axiosPrivate } from '../api/axios';
import { useAuth } from '../context/AuthContext';

export const Dashboard: React.FC = () => {
    const { user } = useAuth();
    const [profileData, setProfileData] = useState<any>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        let isMounted = true;
        const controller = new AbortController();

        const getProfile = async () => {
            try {
                const response = await axiosPrivate.get('/auth/me/', {
                    signal: controller.signal
                });
                if (isMounted) {
                    setProfileData(response.data);
                    setLoading(false);
                }
            } catch (err: any) {
                if (err.name !== 'CanceledError') {
                    if (isMounted) {
                        setError('Failed to fetch profile data.');
                        setLoading(false);
                    }
                }
            }
        };

        getProfile();

        return () => {
            isMounted = false;
            controller.abort();
        };
    }, []);

    return(
        <div className="p-6">
            <h1 className="text-3xl font-bold mb-4">Barangay Dashboard</h1>
            
            <div className="bg-surface shadow rounded-lg p-6 mb-6">
                <h2 className="text-xl font-semibold mb-2">Welcome back, {user?.full_name || user?.username}!</h2>
                <p className="text-slate-600 mb-4">Role: <span className="font-medium text-primary">{user?.role}</span></p>
                
                {loading && <p className="text-slate-500 animate-pulse">Fetching full profile data...</p>}
                
                {error && <p className="text-red-500">{error}</p>}
                
                {profileData && (
                    <div className="mt-4 border-t pt-4">
                        <h3 className="text-lg font-medium mb-2">Detailed Profile Information</h3>
                        <pre className="bg-slate-100 p-4 rounded text-sm overflow-x-auto text-slate-800">
                            {JSON.stringify(profileData, null, 2)}
                        </pre>
                    </div>
                )}
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Placeholders for future metric cards */}
                <div className="bg-surface shadow rounded-lg p-6 border-t-4 border-blue-500">
                    <h3 className="text-slate-500 text-sm font-medium uppercase">Pending Documents</h3>
                    <p className="text-3xl font-bold mt-2">--</p>
                </div>
                <div className="bg-surface shadow rounded-lg p-6 border-t-4 border-yellow-500">
                    <h3 className="text-slate-500 text-sm font-medium uppercase">Active Issues</h3>
                    <p className="text-3xl font-bold mt-2">--</p>
                </div>
                <div className="bg-surface shadow rounded-lg p-6 border-t-4 border-green-500">
                    <h3 className="text-slate-500 text-sm font-medium uppercase">System Status</h3>
                    <p className="text-3xl font-bold mt-2 text-green-600">Online</p>
                </div>
            </div>
        </div>
    );
};