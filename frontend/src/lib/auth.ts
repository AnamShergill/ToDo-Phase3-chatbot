// Fallback auth functions that work with our backend API for JWT handling
export const jwtAuth = {
  signIn: async (email: string, password: string) => {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      throw new Error('Invalid credentials');
    }

    const data = await response.json();
    // Store token in localStorage
    localStorage.setItem('authToken', data.data.token);
    localStorage.setItem('user', JSON.stringify(data.data.user));

    return data.data;
  },

  signUp: async (email: string, password: string, name: string) => {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password, name }),
    });

    if (!response.ok) {
      throw new Error('Registration failed');
    }

    const data = await response.json();
    // Store token in localStorage
    localStorage.setItem('authToken', data.data.token);
    localStorage.setItem('user', JSON.stringify(data.data.user));

    return data.data;
  },

  signOut: async () => {
    // Remove token from localStorage
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
  },

  getSession: () => {
    const token = localStorage.getItem('authToken');
    const user = localStorage.getItem('user');

    if (token && user) {
      return {
        token,
        user: JSON.parse(user),
      };
    }

    return null;
  },
};