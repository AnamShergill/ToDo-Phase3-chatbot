'use client';

import React from 'react';
import Link from 'next/link';
import { useAuth } from '@/context/auth-context';

const Header: React.FC = () => {
  const { user, logout } = useAuth();

  return (
    <header className="bg-surface border-b border-neon shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/dashboard" className="flex-shrink-0 flex items-center">
              <span className="text-xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-highlight-primary to-highlight-secondary">TodoBoom 💥</span>
            </Link>
            <nav className="ml-6 flex space-x-8">
              <Link
                href="/dashboard"
                className="inline-flex items-center px-1 pt-1 border-b-2 border-transparent text-sm font-medium text-muted hover:text-primary hover:border-highlight-primary transition-colors duration-200"
              >
                Dashboard
              </Link>
              <Link
                href="/chat"
                className="inline-flex items-center px-1 pt-1 border-b-2 border-transparent text-sm font-medium text-muted hover:text-primary hover:border-highlight-primary transition-colors duration-200"
              >
                AI Chat
              </Link>
              <Link
                href="/profile"
                className="inline-flex items-center px-1 pt-1 border-b-2 border-transparent text-sm font-medium text-muted hover:text-primary hover:border-highlight-primary transition-colors duration-200"
              >
                Profile
              </Link>
            </nav>
          </div>
          <div className="flex items-center">
            {user ? (
              <div className="flex items-center space-x-4">
                <div className="text-sm text-muted">
                  Welcome, <span className="font-medium text-primary">{user.name}</span>
                </div>
                <button
                  onClick={logout}
                  className="ml-4 inline-flex items-center px-4 py-2 rounded-xl text-sm font-medium text-white bg-danger hover:bg-opacity-90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-danger/50 transition-all duration-200 shadow-neon-red"
                >
                  Logout
                </button>
              </div>
            ) : (
              <div className="flex space-x-4">
                <Link
                  href="/login"
                  className="inline-flex items-center px-4 py-2 border border-neon rounded-xl text-sm font-medium text-muted bg-surface hover:bg-opacity-10 transition-all duration-200 shadow-neon-cyan"
                >
                  Sign In
                </Link>
                <Link
                  href="/register"
                  className="inline-flex items-center px-4 py-2 rounded-xl text-sm font-medium text-white bg-highlight-primary hover:bg-opacity-90 transition-all duration-200 transform hover:-translate-y-0.5 shadow-neon-purple"
                >
                  Sign Up
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;