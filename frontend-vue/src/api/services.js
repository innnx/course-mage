import axios from 'axios';

const api = axios.create({
  baseURL: '',
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器：自动添加 token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// 响应拦截器：统一处理错误
api.interceptors.response.use(
  (response) => {
    const res = response.data;
    if (res.code === 200) {
      return res.data; // 返回 data 部分
    }
    return Promise.reject(new Error(res.message || '请求失败'));
  },
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('userInfo');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (data) => api.post('/api/user/login', data),
  register: (data) => api.post('/api/user/register', data),
};

// Course API
export const courseAPI = {
  getList: (params) => {
    const queryParams = { ...params };
    if (queryParams.current !== undefined) {
      queryParams.pageNum = queryParams.current;
      delete queryParams.current;
    }
    if (queryParams.size !== undefined) {
      queryParams.pageSize = queryParams.size;
      delete queryParams.size;
    }
    return api.get('/api/course/page', { params: queryParams });
  },
  getById: (id) => api.get(`/api/course/${id}`),
  create: (data) => api.post('/api/course', data),
  update: (id, data) => api.put('/api/course', { id, ...data }),
  delete: (id) => api.delete(`/api/course/${id}`),
  updateStatus: (id, status) => api.put(`/api/course/${id}/status`, null, { params: { status } }),
};

// Category API
export const categoryAPI = {
  getList: () => api.get('/api/category/list'),
  create: (data) => api.post('/api/category', data),
  update: (data) => api.put('/api/category', data),
  delete: (id) => api.delete(`/api/category/${id}`),
};

// Order API
export const orderAPI = {
  create: (data) => api.post('/api/order', data),
  pay: (orderNo) => api.put(`/api/order/${orderNo}/pay`),
  cancel: (orderNo) => api.put(`/api/order/${orderNo}/cancel`),
  getMyOrders: (params) => {
    const queryParams = { ...params };
    if (queryParams.current !== undefined) {
      queryParams.pageNum = queryParams.current;
      delete queryParams.current;
    }
    if (queryParams.size !== undefined) {
      queryParams.pageSize = queryParams.size;
      delete queryParams.size;
    }
    return api.get('/api/order/my', { params: queryParams });
  },
  getList: (params) => {
    const queryParams = { ...params };
    if (queryParams.current !== undefined) {
      queryParams.pageNum = queryParams.current;
      delete queryParams.current;
    }
    if (queryParams.size !== undefined) {
      queryParams.pageSize = queryParams.size;
      delete queryParams.size;
    }
    return api.get('/api/order/all', { params: queryParams });
  },
  getDetail: (orderNo) => api.get(`/api/order/${orderNo}`),
  checkPurchase: (courseId) => api.get(`/api/order/check/${courseId}`),
};

export default api;
