export function useChartDefaults() {
  const commonOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          color: '#94A3B8',
          padding: 20,
          font: { family: "'Inter', sans-serif", size: 11, weight: '600' },
          usePointStyle: true,
          boxWidth: 8
        }
      },
      tooltip: {
        backgroundColor: 'rgba(15,23,42,0.95)',
        titleColor: '#F8FAFC',
        bodyColor: '#CBD5E1',
        borderColor: 'rgba(99,102,241,0.2)',
        borderWidth: 1,
        padding: 12,
        cornerRadius: 8,
        displayColors: true,
        boxPadding: 4
      }
    }
  };

  const axisOptions = {
    scales: {
      x: {
        grid: { color: 'rgba(255,255,255,0.03)', drawBorder: false },
        ticks: { color: '#64748B', font: { size: 10 } }
      },
      y: {
        grid: { color: 'rgba(255,255,255,0.03)', drawBorder: false },
        ticks: { color: '#64748B', font: { size: 10 } },
        beginAtZero: true
      }
    }
  };

  return {
    commonOptions,
    axisOptions,
    getBarOptions: () => ({ ...commonOptions, ...axisOptions }),
    getLineOptions: () => ({ ...commonOptions, ...axisOptions }),
    getDoughnutOptions: () => ({ ...commonOptions, cutout: '75%' })
  };
}
