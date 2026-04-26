import client from './client'

export const auth = {
  register: (data) => client.post('/api/auth/register/', data),
  login: (data) => client.post('/api/auth/login/', data),
  refresh: (data) => client.post('/api/auth/token/refresh/', data),
}

export const categories = {
  list: () => client.get('/api/categories/'),
}

export const expenses = {
  list: (params) => client.get('/api/expenses/', { params }),
  get: (id) => client.get(`/api/expenses/${id}/`),
  create: (data) => client.post('/api/expenses/', data),
  update: (id, data) => client.put(`/api/expenses/${id}/`, data),
  delete: (id) => client.delete(`/api/expenses/${id}/`),
}

export const analytics = {
  summary: (params) => client.get('/api/analytics/summary/', { params }),
  byCategory: (params) => client.get('/api/analytics/by-category/', { params }),
  monthlyComparison: (params) => client.get('/api/analytics/monthly-comparison/', { params }),
}

export const statements = {
  upload: (formData) => client.post('/api/statements/upload/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }),
}

export const agent = {
  chat: (data) => client.post('/api/ai/chat/', data),
}
