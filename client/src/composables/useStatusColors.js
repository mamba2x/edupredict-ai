import { computed } from 'vue';
import { STATUS_COLORS, STATUS_ICONS } from '../constants';

export function useStatusColors(statusRef) {
  const predictionColor = computed(() => {
    const status = statusRef.value;
    if (!status) return {};
    return STATUS_COLORS[status] || STATUS_COLORS['At-Risk'];
  });

  const predictionIcon = computed(() => {
    const status = statusRef.value;
    if (!status) return '❓';
    return STATUS_ICONS[status] || '⚠️';
  });

  const riskLevel = computed(() => {
    const status = statusRef.value;
    if (status === 'Excellent') return 'low';
    if (status === 'Average') return 'medium';
    return 'high';
  });

  const getStatusColor = (status) => {
    return STATUS_COLORS[status] || STATUS_COLORS['At-Risk'];
  };
  
  const getRiskColor = (risk) => {
    return risk === 'low' ? '#10B981' : risk === 'high' ? '#EF4444' : '#F59E0B';
  };

  return {
    predictionColor,
    predictionIcon,
    riskLevel,
    getStatusColor,
    getRiskColor
  };
}
