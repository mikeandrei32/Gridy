import React from 'react';
import { Outlet } from 'react-router-dom';

export const AdminLayout: React.FC = () => {
  return (
    <div className="flex h-screen bg-background text-slate-900 font-sans">
      {/* Sidebar (Fixed width) */}
      <aside className="w-64 bg-surface border-r border-border shadow-sm flex flex-col">
        <div className="h-16 flex items-center px-6 border-b border-border">
          <h1 className="text-xl font-bold text-primary">Gridy Admin</h1>
        </div>
        <nav className="flex-1 p-4">
          <ul className="space-y-2">
            <li>
              <a href="/dashboard" className="block px-4 py-2 rounded-md hover:bg-primary/10 hover:text-primary transition-colors">
                Dashboard
              </a>
            </li>
          </ul>
        </nav>
      </aside>

      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Header */}
        <header className="h-16 bg-surface border-b border-border shadow-sm flex items-center justify-between px-6">
          <div className="text-lg font-medium text-slate-700">Admin Portal</div>
          <div className="flex items-center gap-4">
            <span className="text-sm font-medium">System Admin</span>
            <div className="w-8 h-8 rounded-full bg-primary text-white flex items-center justify-center font-bold">
              A
            </div>
          </div>
        </header>

        <main className="flex-1 overflow-auto p-8">
          <Outlet /> 
        </main>
      </div>
    </div>
  );
};
