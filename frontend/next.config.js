/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    NEXT_PUBLIC_API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL || 'https://todo-phase3-chatbot-2.onrender.com',
  },
};

module.exports = nextConfig;
