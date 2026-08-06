import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { axiosPublic } from '../api/axios';

export const Login: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleLogin = async (e: React.ChangeEvent) => {
    e.preventDefault();
    
    try {
      const response = await axiosPublic.post('/auth/login/', { 
        username: email, // The backend expects 'username', but we're passing the email field value
        password: password 
      });
      
      const { access } = response.data;
      // Store the access token for future API requests
      localStorage.setItem('access_token', access);
      
      // Decode the JWT payload without a library
      const payload = JSON.parse(atob(access.split('.')[1]));
      
      login({ 
        id: payload.user_id,
        username: payload.username,
        full_name: payload.full_name,
        role: payload.role
      });
      
      navigate('/dashboard');
    } catch (error) {
      console.error("Login failed:", error);
      alert("Failed to login. Please check your credentials.");
    }
  };

  return (
    <div className="min-h-screen bg-background flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 className="mt-6 text-center text-3xl font-extrabold text-slate-900">
          Gridy Admin Portal
        </h2>
        <p className="mt-2 text-center text-sm text-slate-600">
          Secure Barangay Management System
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-surface py-8 px-4 shadow-md sm:rounded-lg sm:px-10 border border-border">
          <form className="space-y-6" onSubmit={handleLogin}>
            <div>
              <label className="block text-sm font-medium text-slate-700">
                Email address
              </label>
              <div className="mt-1">
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="appearance-none block w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm placeholder-slate-400 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                  placeholder="admin@barangay.gov.ph"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700">
                Password
              </label>
              <div className="mt-1">
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="appearance-none block w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm placeholder-slate-400 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                  placeholder="••••••••"
                />
              </div>
            </div>

            <div>
              <button
                type="submit"
                className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary hover:bg-primary-hover focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-colors"
              >
                Sign in
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};