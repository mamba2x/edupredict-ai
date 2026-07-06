import { reactive } from 'vue'
import { statsService } from './services/statsService'
import { recordService } from './services/recordService'

const API = 'http://localhost:8000'

export const store = reactive({
  stats: {
    total_students: 0,
    excellent_count: 0,
    average_count: 0,
    at_risk_count: 0,
    avg_cgpa: 0,
    avg_ca: 0,
    avg_study_hours: 0,
    recent_predictions: [],
    weekly_volume: { "Excellent": [0,0,0,0,0,0,0], "Average": [0,0,0,0,0,0,0], "At-Risk": [0,0,0,0,0,0,0] },
    cgpa_vs_outcome: [],
    study_hours_vs_outcome: []
  },
  
  notifications: [],
  activityLogs: [],
  notificationIdCounter: 0,

  async fetchStats() {
    try {
      const res = await statsService.getStats()
      this.stats = res

      // Hydrate activity logs from recent DB records so the feed
      // is populated even after a page refresh.
      const recent = res.recent_predictions || []
      if (recent.length > 0 && this.activityLogs.length === 0) {
        this.activityLogs = recent.map((r, i) => {
          const status = r.predicted_status
          const type   = status === 'Excellent' ? 'success'
                       : status === 'At-Risk'   ? 'error'
                       : 'info'
          return {
            id: -(i + 1), // negative IDs to avoid clash with live notifications
            message: `Prediction recorded — ${status} · CGPA ${r.previous_cgpa != null ? Number(r.previous_cgpa).toFixed(2) : 'N/A'} · CA Avg ${r.course_ca_average != null ? Number(r.course_ca_average).toFixed(1) : 'N/A'}`,
            type,
            timestamp: new Date(r.timestamp + 'Z'), // SQLite stores UTC without 'Z'
          }
        })
      }
    } catch (e) {
      console.error('Failed to fetch stats for global store', e)
    }
  },

  async resetSystem() {
    try {
      await recordService.deleteRecords()
      await this.fetchStats()
      this.activityLogs = [] // Clear local logs
      this.addNotification('System reset completed successfully. All data cleared.', 'success')
      return true
    } catch (e) {
      this.addNotification('Failed to reset system. Please try again.', 'error')
      return false
    }
  },

  addNotification(message, type = 'info') {
    const id = this.notificationIdCounter++
    this.notifications.push({ id, message, type })
    
    // Also add to persistent activity logs for the Home feed (keep last 20)
    this.activityLogs.unshift({ id, message, type, timestamp: new Date() })
    if (this.activityLogs.length > 20) this.activityLogs.pop()
    
    // Auto-remove toast after 4 seconds
    setTimeout(() => {
      this.removeNotification(id)
    }, 4000)
  },

  removeNotification(id) {
    const index = this.notifications.findIndex(n => n.id === id)
    if (index !== -1) {
      this.notifications.splice(index, 1)
    }
  }
})
