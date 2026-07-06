import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: 30000,
});

// Response interceptor to format errors nicely
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    let message = 'An unexpected error occurred. Is the backend running?';

    if (error.response?.data) {
      let data = error.response.data;

      // If response is a Blob, parse it to extract the JSON error payload
      if (data instanceof Blob) {
        try {
          const text = await data.text();
          data = JSON.parse(text);
        } catch (e) {
          // Ignore parse errors
        }
      }

      if (data && typeof data === 'object') {
        if (data.detail) {
          if (typeof data.detail === 'object') {
            if (Array.isArray(data.detail)) {
              message = data.detail.map(d => `${d.loc?.join('.') || 'field'}: ${d.msg}`).join(', ');
            } else if (data.detail.message) {
              message = `${data.detail.message}: ${data.detail.errors?.join(', ') || ''}`;
            } else {
              message = JSON.stringify(data.detail);
            }
          } else {
            message = data.detail;
          }
        } else if (data.message) {
          message = data.message;
        }
      }
    }

    return Promise.reject(new Error(message));
  }
);

export default api;
