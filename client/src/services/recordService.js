import api from './api';

export const recordService = {
  async getRecords() {
    const response = await api.get('/records');
    return response.data;
  },

  async deleteRecords() {
    const response = await api.delete('/records');
    return response.data;
  }
};
