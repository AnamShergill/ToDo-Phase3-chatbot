'use client';

import { useAuth } from '@/context/auth-context';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import Header from '@/components/header';

export default function ChatSettingsPage() {
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
      <main className="py-6">
        <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="card bg-surface border-neon">
            <div className="px-4 py-5 sm:px-6 border-b border-neon">
              <h3 className="text-lg leading-6 font-medium text-primary">Chat Settings</h3>
              <p className="mt-1 text-sm text-muted">Configure your chat assistant preferences</p>
            </div>
            <div className="px-4 py-5 sm:p-6">
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="text-base font-medium text-primary">Enable Chat Assistant</h4>
                    <p className="text-sm text-muted">Allow the chatbot to help manage your tasks</p>
                  </div>
                  <button
                    type="button"
                    className="bg-highlight-primary relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-highlight-primary"
                    role="switch"
                    aria-checked="true"
                  >
                    <span
                      aria-hidden="true"
                      className="translate-x-5 pointer-events-none inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200"
                    />
                  </button>
                </div>

                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="text-base font-medium text-primary">Auto-respond to new tasks</h4>
                    <p className="text-sm text-muted">Get chat notifications when tasks are created</p>
                  </div>
                  <button
                    type="button"
                    className="bg-muted relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-highlight-primary"
                    role="switch"
                    aria-checked="false"
                  >
                    <span
                      aria-hidden="true"
                      className="translate-x-0 pointer-events-none inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200"
                    />
                  </button>
                </div>

                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="text-base font-medium text-primary">Daily task summaries</h4>
                    <p className="text-sm text-muted">Receive daily summaries of your tasks via chat</p>
                  </div>
                  <button
                    type="button"
                    className="bg-muted relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-highlight-primary"
                    role="switch"
                    aria-checked="false"
                  >
                    <span
                      aria-hidden="true"
                      className="translate-x-0 pointer-events-none inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200"
                    />
                  </button>
                </div>

                <div className="pt-4">
                  <h4 className="text-base font-medium text-primary">Chat Preferences</h4>
                  <div className="mt-4 space-y-4">
                    <div>
                      <label htmlFor="timezone" className="block text-sm font-medium text-muted">
                        Timezone
                      </label>
                      <select
                        id="timezone"
                        name="timezone"
                        className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-neon focus:outline-none focus:ring-highlight-primary focus:border-highlight-primary sm:text-sm rounded-md input-field"
                      >
                        <option>(GMT-12:00) International Date Line West</option>
                        <option>(GMT-11:00) Midway Island, Samoa</option>
                        <option>(GMT-10:00) Hawaii</option>
                        <option>(GMT-09:00) Alaska</option>
                        <option>(GMT-08:00) Pacific Time (US & Canada)</option>
                        <option>(GMT-07:00) Mountain Time (US & Canada)</option>
                        <option>(GMT-06:00) Central Time (US & Canada)</option>
                        <option>(GMT-05:00) Eastern Time (US & Canada)</option>
                        <option>(GMT-04:00) Atlantic Time (Canada)</option>
                      </select>
                    </div>

                    <div>
                      <label htmlFor="language" className="block text-sm font-medium text-muted">
                        Language
                      </label>
                      <select
                        id="language"
                        name="language"
                        className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-neon focus:outline-none focus:ring-highlight-primary focus:border-highlight-primary sm:text-sm rounded-md input-field"
                      >
                        <option>English</option>
                        <option>Spanish</option>
                        <option>French</option>
                        <option>German</option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}