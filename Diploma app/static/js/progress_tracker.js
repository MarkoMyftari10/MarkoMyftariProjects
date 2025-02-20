class ProgressTracker {
    constructor(patientId) {
        this.patientId = patientId;
        this.metrics = {
            pain: [],
            mobility: [],
            strength: [],
            adherence: []
        };
        this.initializeCharts();
    }

    async loadPatientData() {
        try {
            const response = await fetch(`/patient_progress/${this.patientId}`);
            const data = await response.json();
            this.updateMetrics(data);
        } catch (error) {
            console.error('Error loading patient data:', error);
        }
    }

    updateMetrics(data) {
        Object.keys(this.metrics).forEach(metric => {
            if (data[metric]) {
                this.metrics[metric] = data[metric];
                this.updateChart(metric);
            }
        });
    }

    initializeCharts() {
        const chartConfigs = {
            pain: {
                type: 'line',
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 10
                        }
                    }
                }
            },
            mobility: {
                type: 'radar',
                options: {
                    scales: {
                        r: {
                            beginAtZero: true,
                            max: 100
                        }
                    }
                }
            }
            // More chart configurations...
        };

        Object.keys(chartConfigs).forEach(metric => {
            const ctx = document.getElementById(`${metric}Chart`);
            if (ctx) {
                this.createChart(ctx, chartConfigs[metric]);
            }
        });
    }

    createChart(ctx, config) {
        // Chart creation implementation
    }

    updateChart(metric) {
        // Chart update implementation
    }
} 