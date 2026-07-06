import api from './api';

export const insightService = {
  async getInsights() {
    const response = await api.get('/insights');
    return response.data;
  }
};
