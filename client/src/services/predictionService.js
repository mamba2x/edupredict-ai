import api from './api';

export const predictionService = {
  async predictSingle(data) {
    const response = await api.post('/predict', data);
    return response.data;
  },

  async predictBatch(file, replace = false) {
    const formData = new FormData();
    formData.append('file', file);
    if (replace) {
      formData.append('replace', 'true');
    }

    const response = await api.post('/predict/batch', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      responseType: 'blob'
    });
    
    return response.data; // This is a Blob
  }
};
