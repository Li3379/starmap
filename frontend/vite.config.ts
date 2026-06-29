import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    host: '0.0.0.0',  // 容器内需要监听 0.0.0.0 才能从宿主访问
    port: 5173,
    allowedHosts: ['localhost', '127.0.0.1', 'frontend', 'starmap-frontend', 'host.docker.internal'],
    proxy: {
      // 前端通过代理访问后端，避免 CORS（生产由 Nginx 反代）
      '/api': {
        target: process.env.VITE_API_BASE_URL || 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
  test: {
    environment: 'jsdom',
    globals: true,
  },
})
