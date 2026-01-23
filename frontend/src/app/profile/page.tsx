'use client';

import { useAuth } from '@/context/auth-context';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import Header from '@/components/header';

export default function ProfilePage() {
  const { user, loading, isAuthenticated } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !isAuthenticated()) {
      router.push('/login');
    }
  }, [loading, isAuthenticated, router]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-app">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-highlight-primary"></div>
      </div>
    );
  }

  if (!isAuthenticated()) {
    return null; // Redirect happens in useEffect
  }

  return (
    <div className="min-h-screen bg-app">
      <Header />
      <main className="py-6">
        <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="card bg-surface border-neon">
            <div className="px-4 py-5 sm:px-6 border-b border-neon">
              <h3 className="text-lg leading-6 font-medium text-primary">Profile Information</h3>
              <p className="mt-1 text-sm text-muted">Manage your account information</p>
            </div>
            <div className="px-4 py-5 sm:p-6">
              {user && (
                <div className="grid grid-cols-1 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-muted">Name</label>
                    <div className="mt-1 text-primary">{user.name}</div>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-muted">Email</label>
                    <div className="mt-1 text-primary">{user.email}</div>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-muted">Account ID</label>
                    <div className="mt-1 text-primary">#{user.id}</div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}