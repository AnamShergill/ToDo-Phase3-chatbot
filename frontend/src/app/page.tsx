'use client';

import { useAuth } from '../context/auth-context';
import Link from 'next/link';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function HomePage() {
  const { loading, isAuthenticated } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && isAuthenticated()) {
      router.push('/welcome');
    }
  }, [loading, isAuthenticated, router]);

  return (
    <div className="min-h-screen bg-app flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h1 className="text-center text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-highlight-primary to-highlight-secondary mb-8 neon-glow">
          Welcome To TodoBoom 💥
        </h1>
        <h2 className="mt-6 text-center text-2xl font-bold tracking-tight text-primary">
          Explode your productivity. One task at a time.
        </h2>
        <p className="mt-2 text-center text-sm text-muted">
          A hackathon-ready todo app that amplifies your productivity
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="card py-8 px-4 sm:rounded-xl sm:px-10 border-neon">
          <div className="space-y-6">
            <div>
              <Link
                href="/register"
                className="w-full flex justify-center py-3 px-4 rounded-xl text-sm font-medium text-white bg-highlight-primary hover:bg-opacity-90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-highlight-primary transition-all duration-200 transform hover:-translate-y-0.5 shadow-neon-purple"
              >
                Get Started - Explode Productivity!
              </Link>
            </div>

            <div className="relative mt-6">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-neon" />
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-2 bg-surface text-muted">Or</span>
              </div>
            </div>

            <div>
              <Link
                href="/login"
                className="w-full flex justify-center py-3 px-4 border border-neon rounded-xl text-sm font-medium text-muted bg-surface hover:bg-opacity-10 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-highlight-primary transition-all duration-200 shadow-neon-cyan"
              >
                Sign in to your account
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}