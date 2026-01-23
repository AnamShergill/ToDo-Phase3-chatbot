'use client';

import { useAuth } from '@/context/auth-context';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import Link from 'next/link';
import Header from '@/components/header';

export default function WelcomePage() {
  const { loading, isAuthenticated } = useAuth();
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
      <main className="py-12">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-highlight-primary to-highlight-secondary mb-6">
              Welcome to TodoBoom! 💥
            </h1>
            <p className="text-xl text-muted mb-8 max-w-2xl mx-auto">
              Congratulations on joining TodoBoom! Your productivity explosion starts now.
            </p>

            <div className="bg-surface rounded-2xl p-8 border border-neon shadow-xl mb-12">
              <h2 className="text-2xl font-bold text-primary mb-4">About TodoBoom</h2>
              <p className="text-muted mb-6">
                TodoBoom is your ultimate productivity companion designed to help you manage tasks efficiently
                and achieve your goals. Our platform offers a seamless experience to organize, track, and
                complete your tasks with ease.
              </p>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
                <div className="bg-app p-6 rounded-xl border border-neon">
                  <h3 className="font-bold text-highlight-primary mb-2">Organize</h3>
                  <p className="text-sm text-muted">Effortlessly categorize and prioritize your tasks</p>
                </div>
                <div className="bg-app p-6 rounded-xl border border-neon">
                  <h3 className="font-bold text-highlight-primary mb-2">Track</h3>
                  <p className="text-sm text-muted">Monitor your progress and stay on top of deadlines</p>
                </div>
                <div className="bg-app p-6 rounded-xl border border-neon">
                  <h3 className="font-bold text-highlight-primary mb-2">Achieve</h3>
                  <p className="text-sm text-muted">Complete tasks and celebrate your wins</p>
                </div>
              </div>
            </div>

            <div className="mb-8">
              <p className="text-lg text-muted mb-6">
                Ready to boost your productivity? Start managing your tasks effectively with TodoBoom.
              </p>

              <Link
                href="/dashboard"
                className="inline-flex items-center px-8 py-4 rounded-xl text-lg font-bold text-white bg-gradient-to-r from-highlight-primary to-highlight-secondary hover:from-highlight-primary/90 hover:to-highlight-secondary/90 focus:outline-none focus:ring-4 focus:ring-highlight-primary/30 transition-all duration-300 transform hover:-translate-y-1 shadow-2xl shadow-highlight-primary/30"
              >
                Go to Dashboard →
              </Link>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}