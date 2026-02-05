'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import api from '@/lib/api.ts';
import { jwtAuth } from '@/lib/auth.ts';

interface User {
  id: number;
  email: string;
  name: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, name: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: () => boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const router = useRouter();

  // Initialize auth state from localStorage on mount
  useEffect(() => {
    const storedToken = localStorage.getItem('authToken');
    const storedUser = localStorage.getItem('user');

    if (storedToken && storedUser) {
      setToken(storedToken);
      setUser(JSON.parse(storedUser));
    }

    setLoading(false);
  }, []);

  const login = async (email: string, password: string) => {
    try {
      // Use the JWT auth function to maintain compatibility with our backend
      const result = await jwtAuth.signIn(email, password);

      setToken(result.token);
      setUser(result.user);

      router.push('/welcome');
    } catch (error: any) {
      if (error.message.includes('credentials')) {
        throw new Error(error.message || 'Login failed');
      } else {
        throw new Error('Network error. Please try again.');
      }
    }
  };

  const register = async (email: string, password: string, name: string) => {
    try {
      // Use the JWT auth function to maintain compatibility with our backend
      const result = await jwtAuth.signUp(email, password, name);

      setToken(result.token);
      setUser(result.user);

      router.push('/welcome');
    } catch (error: any) {
      throw new Error(error.message || 'Registration failed');
    }
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    jwtAuth.signOut();

    router.push('/login');
  };

  const isAuthenticated = () => {
    return !!token;
  };

  const value = {
    user,
    token,
    loading,
    login,
    register,
    logout,
    isAuthenticated,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};