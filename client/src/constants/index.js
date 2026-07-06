export const CLASS_ORDER = ['Excellent', 'Average', 'At-Risk']

export const STATUS_COLORS = {
  Excellent: { text: '#10B981', bg: 'rgba(16,185,129,0.08)', border: 'rgba(16,185,129,0.5)' },
  Average:   { text: '#F59E0B', bg: 'rgba(245,158,11,0.08)', border: 'rgba(245,158,11,0.5)' },
  'At-Risk': { text: '#EF4444', bg: 'rgba(239,68,68,0.08)', border: 'rgba(239,68,68,0.5)' }
}

export const STATUS_ICONS = {
  Excellent: '🌟',
  Average: '📘',
  'At-Risk': '⚠️'
}

export const NOTIFICATION_TYPES = {
  success: { bg: 'rgba(16,185,129,0.15)', border: 'rgba(16,185,129,0.4)', text: '#10B981', icon: '✅' },
  error:   { bg: 'rgba(239,68,68,0.15)',  border: 'rgba(239,68,68,0.4)',  text: '#EF4444', icon: '⚠️' },
  warning: { bg: 'rgba(245,158,11,0.15)', border: 'rgba(245,158,11,0.4)', text: '#F59E0B', icon: '🔔' },
  info:    { bg: 'rgba(99,102,241,0.15)', border: 'rgba(99,102,241,0.4)', text: '#A5B4FC', icon: 'ℹ️' }
}
