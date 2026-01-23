'use client';

import { useAuth } from '@/context/auth-context';
import { useTask } from '@/context/task-context';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import Link from 'next/link';
import Header from '@/components/header';
import TaskList from '@/components/task-list';
import TaskFilterBar from '@/components/task-filter-bar';

export default function DashboardPage() {
  const { loading, isAuthenticated } = useAuth();
  const { tasks, loading: tasksLoading } = useTask();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !isAuthenticated()) {
      router.push('/login');
    }
  }, [loading, isAuthenticated, router]);

  // Calculate stats
  const totalTasks = tasks.length;
  const completedTasks = tasks.filter(task => task.completed).length;
  const pendingTasks = totalTasks - completedTasks;

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
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Dashboard Header Section */}
          <div className="mb-8">
            <div className="flex justify-between items-start mb-6">
              <div>
                <h1 className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-highlight-primary to-highlight-secondary">TodoBoom Dashboard</h1>
                <p className="text-sm text-muted mt-2">Manage your tasks efficiently and boost your productivity</p>
              </div>
            </div>

            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <div className="bg-surface p-6 rounded-2xl border border-neon shadow-lg">
                <div className="flex items-center">
                  <div className="p-3 rounded-xl bg-highlight-primary/10">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-highlight-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                    </svg>
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-muted">Total Tasks</p>
                    <p className="text-2xl font-bold text-primary">{totalTasks}</p>
                  </div>
                </div>
              </div>

              <div className="bg-surface p-6 rounded-2xl border border-neon shadow-lg">
                <div className="flex items-center">
                  <div className="p-3 rounded-xl bg-success/10">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-success" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-muted">Completed</p>
                    <p className="text-2xl font-bold text-primary">{completedTasks}</p>
                  </div>
                </div>
              </div>

              <div className="bg-surface p-6 rounded-2xl border border-neon shadow-lg">
                <div className="flex items-center">
                  <div className="p-3 rounded-xl bg-warning/10">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-warning" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-muted">Pending</p>
                    <p className="text-2xl font-bold text-primary">{pendingTasks}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Task Management Section */}
          <div className="bg-surface rounded-2xl border border-neon shadow-xl p-6">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
              <h2 className="text-xl font-bold text-primary mb-4 sm:mb-0">Your Tasks</h2>
              <TaskFilterBar />
            </div>

            <TaskList />
          </div>
        </div>
      </main>
    </div>
  );
}