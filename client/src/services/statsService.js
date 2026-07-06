import api from './api';

export const statsService = {
  async getStats() {
    const response = await api.get('/stats');
    return response.data;
  }
};
