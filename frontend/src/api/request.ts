/**
 * axios 实例封装。
 * base URL 走 Vite 代理（见 vite.config.ts），生产由 Nginx 反代。
 */
import axios from 'axios'

const request = axios.create({
  baseURL: '/api/v1',
  timeout: 30000,
})

request.interceptors.response.use(
  (resp) => resp.data,
  (error) => {
    console.error('[API]', error?.response?.status, error?.message)
    return Promise.reject(error)
  },
)

export default request
