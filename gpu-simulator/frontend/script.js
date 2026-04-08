// NVIDIA Quantum Compute Studio - Premium Frontend
// Enterprise-grade parallel computing simulation interface

// Chart Image Capture Class
class ChartImageCapture {
    async captureChart(chartId) {
        try {
            const canvas = document.getElementById(chartId);
            if (!canvas) {
                throw new Error(`Chart canvas not found: ${chartId}`);
            }
            
            // Capture at 2x resolution for high quality
            return canvas.toDataURL('image/png', 1.0);
        } catch (error) {
            console.error(`Failed to capture chart ${chartId}:`, error);
            return null;
        }
    }
    
    async captureThreadVisualization() {
        try {
            const container = document.getElementById('thread-block-viz');
            if (!container) {
                throw new Error('Thread visualization container not found');
            }
            
            // Use html2canvas if available, otherwise create a simple placeholder
            if (typeof html2canvas !== 'undefined') {
                const canvas = await html2canvas(container);
                return canvas.toDataURL('image/png', 1.0);
            } else {
                // Fallback: return empty string
                return '';
            }
        } catch (error) {
            console.error('Failed to capture thread visualization:', error);
            return '';
        }
    }
    
    async captureAllCharts() {
        const charts = {
            time_chart: await this.captureChart('time-chart'),
            speedup_chart: await this.captureChart('speedup-chart'),
            efficiency_chart: await this.captureChart('efficiency-chart')
        };
        
        // Filter out null values
        return Object.fromEntries(
            Object.entries(charts).filter(([_, v]) => v !== null)
        );
    }
}

// Export Controller Class
class ExportController {
    constructor(studio) {
        this.studio = studio;
        this.chartCapture = new ChartImageCapture();
    }
    
    async prepareExportData() {
        // Gather all simulation data
        const exportData = {
            simulation_data: {
                dataset_size: this.studio.currentData?.size || 0,
                operation: this.studio.currentData?.operation || '',
                cpu_execution_time: this.studio.currentData?.cpuTime || 0,
                gpu_execution_time: this.studio.currentData?.gpuTime || 0,
                speedup_ratio: this.studio.currentData?.cpuTime && this.studio.currentData?.gpuTime 
                    ? this.studio.currentData.cpuTime / this.studio.currentData.gpuTime 
                    : 0,
                efficiency_percentage: 0,
                throughput: this.studio.currentData?.size && this.studio.currentData?.gpuTime
                    ? Math.round(this.studio.currentData.size / this.studio.currentData.gpuTime)
                    : 0,
                thread_block_info: this.studio.currentData?.threadBlockInfo || {},
                timestamp: new Date().toISOString()
            },
            performance_history: this.studio.performanceHistory,
            console_logs: this.getConsoleLogs(),
            timestamp: new Date().toISOString()
        };
        
        return exportData;
    }
    
    getConsoleLogs() {
        const consoleOutput = document.querySelector('.console-output');
        if (!consoleOutput) return [];
        
        const lines = consoleOutput.querySelectorAll('.console-line');
        return Array.from(lines).map(line => line.textContent);
    }
    
    async exportPDF() {
        try {
            this.studio.showNotification('Preparing PDF export...', 'info');
            
            // Capture chart images
            const chartImages = await this.chartCapture.captureAllCharts();
            const threadVizImage = await this.chartCapture.captureThreadVisualization();
            
            // Prepare export data
            const exportData = await this.prepareExportData();
            
            // Build request payload
            const payload = {
                simulation_data: exportData.simulation_data,
                chart_images: chartImages,
                thread_viz_image: threadVizImage,
                console_logs: exportData.console_logs,
                include_branding: true,
                report_title: "GPU Quantum Compute Simulation Report"
            };
            
            // Show loading indicator
            this.studio.showLoadingOverlay('Generating PDF report...');
            
            // Send request to backend
            const response = await fetch('/api/export-pdf', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            
            if (!response.ok) {
                throw new Error(`PDF generation failed: ${response.statusText}`);
            }
            
            // Download PDF
            const blob = await response.blob();
            const timestamp = new Date().toISOString().split('T')[0];
            const filename = `quantum-compute-report-${timestamp}.pdf`;
            this.downloadFile(blob, filename);
            
            this.studio.showNotification('PDF exported successfully!', 'success');
            
        } catch (error) {
            console.error('PDF export failed:', error);
            this.studio.showNotification(`PDF export failed: ${error.message}`, 'error');
        }
    }
    
    async exportJSON() {
        try {
            const exportData = await this.prepareExportData();
            
            const dataStr = JSON.stringify(exportData, null, 2);
            const dataBlob = new Blob([dataStr], { type: 'application/json' });
            
            const timestamp = new Date().toISOString().split('T')[0];
            const filename = `quantum-compute-results-${timestamp}.json`;
            
            this.downloadFile(dataBlob, filename);
            this.studio.showNotification('Results exported as JSON!', 'success');
            
        } catch (error) {
            console.error('JSON export failed:', error);
            this.studio.showNotification(`Export failed: ${error.message}`, 'error');
        }
    }
    
    downloadFile(blob, filename) {
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        link.click();
        URL.revokeObjectURL(url);
    }
}

// Configuration Manager Class
class ConfigurationManager {
    constructor(studio) {
        this.studio = studio;
        this.storageKey = 'quantum_compute_presets';
    }
    
    savePreset(name, description = '') {
        try {
            const config = this.getCurrentConfig();
            const presets = this.listPresets();
            
            const preset = {
                name: name,
                description: description,
                datasetSize: config.datasetSize,
                operation: config.operation,
                numProcesses: config.numProcesses,
                createdAt: new Date().toISOString()
            };
            
            presets[name] = preset;
            localStorage.setItem(this.storageKey, JSON.stringify(presets));
            
            return true;
        } catch (error) {
            console.error('Failed to save preset:', error);
            return false;
        }
    }
    
    loadPreset(name) {
        try {
            const presets = this.listPresets();
            const preset = presets[name];
            
            if (!preset) {
                throw new Error(`Preset not found: ${name}`);
            }
            
            // Validate preset
            if (!this.validatePreset(preset)) {
                throw new Error('Invalid preset data');
            }
            
            return preset;
        } catch (error) {
            console.error('Failed to load preset:', error);
            return null;
        }
    }
    
    listPresets() {
        try {
            const data = localStorage.getItem(this.storageKey);
            return data ? JSON.parse(data) : {};
        } catch (error) {
            console.error('Failed to list presets:', error);
            return {};
        }
    }
    
    deletePreset(name) {
        try {
            const presets = this.listPresets();
            delete presets[name];
            localStorage.setItem(this.storageKey, JSON.stringify(presets));
            return true;
        } catch (error) {
            console.error('Failed to delete preset:', error);
            return false;
        }
    }
    
    resetToDefault() {
        return {
            datasetSize: 50000,
            operation: 'vector_add',
            numProcesses: 8
        };
    }
    
    getCurrentConfig() {
        return {
            datasetSize: parseInt(document.getElementById('dataset-size')?.value || 50000),
            operation: document.getElementById('operation')?.value || 'vector_add',
            numProcesses: 8
        };
    }
    
    applyConfig(config) {
        const datasetSizeEl = document.getElementById('dataset-size');
        const operationEl = document.getElementById('operation');
        
        if (datasetSizeEl) datasetSizeEl.value = config.datasetSize;
        if (operationEl) operationEl.value = config.operation;
        
        // Update UI
        this.studio.updateMemoryEstimate(config.datasetSize);
        this.studio.updateComplexityBadge(config.operation);
    }
    
    validatePreset(preset) {
        const validSizes = [10000, 50000, 100000, 500000];
        const validOps = ['vector_add', 'vector_multiply', 'dot_product', 'matrix_multiply'];
        
        return preset.datasetSize && validSizes.includes(preset.datasetSize) &&
               preset.operation && validOps.includes(preset.operation);
    }
}

class QuantumComputeStudio {
    constructor() {
        this.currentData = null;
        this.performanceHistory = [];
        this.timeChart = null;
        this.speedupChart = null;
        this.efficiencyChart = null;
        this.isProcessing = false;
        this.exportController = new ExportController(this);
        this.configManager = new ConfigurationManager(this);
        
        this.initializeParticles();
        this.initializeEventListeners();
        this.initializeCharts();
        this.startLiveMetrics();
        this.addEnterpriseFeatures();
    }

    initializeParticles() {
        // Create a simple animated background since particles.js might not load
        const particlesContainer = document.getElementById('particles-js');
        if (particlesContainer) {
            // Add some floating elements for visual effect
            for (let i = 0; i < 20; i++) {
                const particle = document.createElement('div');
                particle.style.cssText = `
                    position: absolute;
                    width: ${Math.random() * 4 + 2}px;
                    height: ${Math.random() * 4 + 2}px;
                    background: rgba(118, 185, 0, ${Math.random() * 0.5 + 0.2});
                    border-radius: 50%;
                    left: ${Math.random() * 100}%;
                    top: ${Math.random() * 100}%;
                    animation: float ${Math.random() * 10 + 5}s infinite linear;
                `;
                particlesContainer.appendChild(particle);
            }
        }
        
        // Add CSS animation for floating particles
        const style = document.createElement('style');
        style.textContent = `
            @keyframes float {
                0% { transform: translateY(0px) rotate(0deg); opacity: 0; }
                10% { opacity: 1; }
                90% { opacity: 1; }
                100% { transform: translateY(-100vh) rotate(360deg); opacity: 0; }
            }
        `;
        document.head.appendChild(style);
    }

    initializeEventListeners() {
        // Main execution buttons
        document.getElementById('generate-data').addEventListener('click', () => this.generateData());
        document.getElementById('run-cpu').addEventListener('click', () => this.runCPUSimulation());
        document.getElementById('run-gpu').addEventListener('click', () => this.runGPUSimulation());
        
        // Dataset size change handler
        document.getElementById('dataset-size').addEventListener('change', (e) => this.updateMemoryEstimate(e.target.value));
        
        // Operation change handler
        document.getElementById('operation').addEventListener('change', (e) => this.updateComplexityBadge(e.target.value));
        
        // Quick actions
        document.querySelectorAll('.quick-action').forEach(btn => {
            btn.addEventListener('click', (e) => this.handleQuickAction(e.target.closest('.quick-action').dataset.action));
        });
        
        // Chart controls
        document.querySelectorAll('.chart-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.switchChart(e.target.dataset.chart));
        });
        
        // Tab controls
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.switchTab(e.target.dataset.tab));
        });
        
        // Console controls
        document.querySelectorAll('.console-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const action = e.target.closest('.console-btn').title;
                if (action.includes('Clear')) {
                    this.clearConsole();
                } else if (action.includes('Export')) {
                    this.exportConsoleLogs();
                }
            });
        });
        
        // Configuration controls
        document.querySelectorAll('.btn-icon').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const action = e.target.closest('.btn-icon').title;
                if (action.includes('Reset')) {
                    this.resetConfiguration();
                } else if (action.includes('Save')) {
                    this.showSavePresetDialog();
                }
            });
        });
        
        // Initialize default values
        this.updateMemoryEstimate(50000);
        this.updateComplexityBadge('vector_add');
    }

    initializeCharts() {
        // Initialize performance comparison chart with premium styling
        const timeCtx = document.getElementById('time-chart').getContext('2d');
        this.timeChart = new Chart(timeCtx, {
            type: 'bar',
            data: {
                labels: [],
                datasets: [{
                    label: 'CPU Execution Time',
                    data: [],
                    backgroundColor: 'rgba(255, 107, 107, 0.8)',
                    borderColor: 'rgba(255, 107, 107, 1)',
                    borderWidth: 2,
                    borderRadius: 8,
                    borderSkipped: false,
                }, {
                    label: 'GPU Execution Time',
                    data: [],
                    backgroundColor: 'rgba(118, 185, 0, 0.8)',
                    borderColor: 'rgba(118, 185, 0, 1)',
                    borderWidth: 2,
                    borderRadius: 8,
                    borderSkipped: false,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            color: '#ffffff',
                            font: { family: 'Inter', size: 12, weight: '500' },
                            usePointStyle: true,
                            pointStyle: 'circle'
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(26, 26, 26, 0.95)',
                        titleColor: '#ffffff',
                        bodyColor: '#b3b3b3',
                        borderColor: 'rgba(118, 185, 0, 0.3)',
                        borderWidth: 1,
                        cornerRadius: 8,
                        displayColors: true
                    }
                },
                scales: {
                    x: {
                        grid: { color: 'rgba(255, 255, 255, 0.1)' },
                        ticks: { color: '#b3b3b3', font: { family: 'Inter' } }
                    },
                    y: {
                        beginAtZero: true,
                        grid: { color: 'rgba(255, 255, 255, 0.1)' },
                        ticks: { 
                            color: '#b3b3b3', 
                            font: { family: 'Inter' },
                            callback: function(value) {
                                return value.toFixed(3) + 's';
                            }
                        },
                        title: {
                            display: true,
                            text: 'Execution Time (seconds)',
                            color: '#ffffff',
                            font: { family: 'Inter', size: 14, weight: '600' }
                        }
                    }
                },
                animation: {
                    duration: 1000,
                    easing: 'easeOutQuart'
                }
            }
        });

        // Initialize speedup chart
        const speedupCtx = document.getElementById('speedup-chart').getContext('2d');
        this.speedupChart = new Chart(speedupCtx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Speedup Ratio',
                    data: [],
                    backgroundColor: 'rgba(0, 212, 255, 0.1)',
                    borderColor: 'rgba(0, 212, 255, 1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: 'rgba(0, 212, 255, 1)',
                    pointBorderColor: '#ffffff',
                    pointBorderWidth: 2,
                    pointRadius: 6,
                    pointHoverRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            color: '#ffffff',
                            font: { family: 'Inter', size: 12, weight: '500' }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(26, 26, 26, 0.95)',
                        titleColor: '#ffffff',
                        bodyColor: '#b3b3b3',
                        borderColor: 'rgba(0, 212, 255, 0.3)',
                        borderWidth: 1,
                        cornerRadius: 8
                    }
                },
                scales: {
                    x: {
                        grid: { color: 'rgba(255, 255, 255, 0.1)' },
                        ticks: { color: '#b3b3b3', font: { family: 'Inter' } },
                        title: {
                            display: true,
                            text: 'Dataset Size',
                            color: '#ffffff',
                            font: { family: 'Inter', size: 14, weight: '600' }
                        }
                    },
                    y: {
                        beginAtZero: true,
                        grid: { color: 'rgba(255, 255, 255, 0.1)' },
                        ticks: { 
                            color: '#b3b3b3', 
                            font: { family: 'Inter' },
                            callback: function(value) {
                                return value.toFixed(1) + 'x';
                            }
                        },
                        title: {
                            display: true,
                            text: 'Speedup Ratio (CPU/GPU)',
                            color: '#ffffff',
                            font: { family: 'Inter', size: 14, weight: '600' }
                        }
                    }
                },
                animation: {
                    duration: 1000,
                    easing: 'easeOutQuart'
                }
            }
        });
        
        // Initialize efficiency chart
        const efficiencyCtx = document.getElementById('efficiency-chart')?.getContext('2d');
        if (efficiencyCtx) {
            this.efficiencyChart = new Chart(efficiencyCtx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Parallel Efficiency',
                        data: [],
                        backgroundColor: 'rgba(255, 215, 0, 0.1)',
                        borderColor: 'rgba(255, 215, 0, 1)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.4,
                        pointBackgroundColor: 'rgba(255, 215, 0, 1)',
                        pointBorderColor: '#ffffff',
                        pointBorderWidth: 2,
                        pointRadius: 6,
                        pointHoverRadius: 8
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'top',
                            labels: {
                                color: '#ffffff',
                                font: { family: 'Inter', size: 12, weight: '500' }
                            }
                        },
                        tooltip: {
                            backgroundColor: 'rgba(26, 26, 26, 0.95)',
                            titleColor: '#ffffff',
                            bodyColor: '#b3b3b3',
                            borderColor: 'rgba(255, 215, 0, 0.3)',
                            borderWidth: 1,
                            cornerRadius: 8
                        }
                    },
                    scales: {
                        x: {
                            grid: { color: 'rgba(255, 255, 255, 0.1)' },
                            ticks: { color: '#b3b3b3', font: { family: 'Inter' } },
                            title: {
                                display: true,
                                text: 'Dataset Size',
                                color: '#ffffff',
                                font: { family: 'Inter', size: 14, weight: '600' }
                            }
                        },
                        y: {
                            beginAtZero: true,
                            max: 100,
                            grid: { color: 'rgba(255, 255, 255, 0.1)' },
                            ticks: { 
                                color: '#b3b3b3', 
                                font: { family: 'Inter' },
                                callback: function(value) {
                                    return value.toFixed(0) + '%';
                                }
                            },
                            title: {
                                display: true,
                                text: 'Efficiency Percentage',
                                color: '#ffffff',
                                font: { family: 'Inter', size: 14, weight: '600' }
                            }
                        }
                    },
                    animation: {
                        duration: 1000,
                        easing: 'easeOutQuart'
                    }
                }
            });
        }
    }

    startLiveMetrics() {
        // Simulate live system metrics
        setInterval(() => {
            if (this.isProcessing) {
                this.updateLiveMetric('GPU Utilization', Math.random() * 100);
                this.updateLiveMetric('Memory Usage', Math.random() * 8);
                this.updateActiveCores(Math.floor(Math.random() * 8) + 1);
            } else {
                this.updateLiveMetric('GPU Utilization', 0);
                this.updateLiveMetric('Memory Usage', 0);
                this.updateActiveCores(0);
            }
        }, 1000);
    }

    updateLiveMetric(label, value) {
        const metrics = document.querySelectorAll('.metric');
        metrics.forEach(metric => {
            const metricLabel = metric.querySelector('.metric-label');
            if (metricLabel && metricLabel.textContent === label) {
                const fill = metric.querySelector('.metric-fill');
                const valueSpan = metric.querySelector('.metric-value');
                
                if (label === 'GPU Utilization') {
                    fill.style.width = `${value}%`;
                    valueSpan.textContent = `${Math.round(value)}%`;
                } else if (label === 'Memory Usage') {
                    const percentage = (value / 8) * 100;
                    fill.style.width = `${percentage}%`;
                    valueSpan.textContent = `${value.toFixed(1)} GB`;
                }
            }
        });
    }

    updateActiveCores(count) {
        const activeCoresElement = document.getElementById('active-cores');
        if (activeCoresElement) {
            activeCoresElement.textContent = `${count}/8`;
        }
    }

    updateMemoryEstimate(size) {
        const estimate = (size * 8) / (1024 * 1024); // bytes to MB
        const badge = document.getElementById('memory-estimate');
        if (badge) {
            if (estimate < 1) {
                badge.textContent = `~${Math.round(estimate * 1024)} KB`;
            } else {
                badge.textContent = `~${estimate.toFixed(1)} MB`;
            }
        }
    }

    updateComplexityBadge(operation) {
        const badge = document.getElementById('complexity-badge');
        if (badge) {
            const complexities = {
                'vector_add': 'Linear Complexity',
                'vector_multiply': 'Linear Complexity',
                'dot_product': 'Linear Complexity',
                'matrix_multiply': 'Cubic Complexity'
            };
            badge.textContent = complexities[operation] || 'Unknown';
        }
    }

    addEnterpriseFeatures() {
        // Add premium visual effects
        this.addGlowEffects();
        this.addHoverAnimations();
        this.addLoadingAnimations();
    }

    addGlowEffects() {
        // Add glow effects to important elements
        const glowElements = document.querySelectorAll('.btn-primary, .stat, .metric-card');
        glowElements.forEach(element => {
            element.addEventListener('mouseenter', () => {
                element.style.boxShadow = '0 0 30px rgba(118, 185, 0, 0.4)';
            });
            element.addEventListener('mouseleave', () => {
                element.style.boxShadow = '';
            });
        });
    }

    addHoverAnimations() {
        // Add smooth hover animations
        const cards = document.querySelectorAll('.control-card, .dashboard-card, .viz-card');
        cards.forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'translateY(-5px)';
                card.style.transition = 'all 0.3s ease';
            });
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'translateY(0)';
            });
        });
    }

    addLoadingAnimations() {
        // Enhanced loading states
        const buttons = document.querySelectorAll('.btn-primary, .btn-secondary, .btn-accent');
        buttons.forEach(button => {
            const originalText = button.innerHTML;
            button.dataset.originalText = originalText;
        });
    }

    showLoadingOverlay(text = 'Processing quantum calculations...') {
        const overlay = document.getElementById('loading-overlay');
        const loadingText = overlay.querySelector('.loading-text');
        const progressFill = overlay.querySelector('.progress-fill');
        const progressText = overlay.querySelector('.progress-text');
        
        loadingText.textContent = text;
        overlay.classList.add('active');
        
        // Animate progress bar
        let progress = 0;
        const progressInterval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress > 100) progress = 100;
            
            progressFill.style.width = `${progress}%`;
            progressText.textContent = `${Math.round(progress)}%`;
            
            if (progress >= 100) {
                clearInterval(progressInterval);
                setTimeout(() => {
                    overlay.classList.remove('active');
                }, 500);
            }
        }, 200);
    }

    async generateData() {
        const size = parseInt(document.getElementById('dataset-size').value);
        const operation = document.getElementById('operation').value;
        
        this.setButtonLoading('generate-data', true);
        this.showLoadingOverlay('Initializing quantum dataset...');
        this.isProcessing = true;
        
        this.addConsoleMessage('system', `Initializing ${size.toLocaleString()} element dataset for ${operation.replace('_', ' ')}...`);

        // CO4: Simulate I/O Input Operation
        if (window.coaDemo) {
            this.addConsoleMessage('info', '[CO4: I/O] Reading configuration from input devices...');
            await this.simulateDelay(200);
        }

        try {
            const response = await fetch('/api/generate-data', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    size: size,
                    operation_type: operation
                })
            });

            const result = await response.json();
            
            if (result.success) {
                this.currentData = { size, operation };
                this.addConsoleMessage('success', `Dataset initialized successfully! Memory usage: ${result.memory_usage_mb}MB`);
                this.addConsoleMessage('info', `Generation time: ${result.generation_time}s`);
                
                // CO4: Simulate I/O Write Operation
                this.addConsoleMessage('info', '[CO4: I/O] Writing dataset to memory...');
                await this.simulateDelay(150);
                this.addConsoleMessage('success', '[CO4: I/O] Dataset stored in memory successfully');
                
                // Update hero stats
                this.updateHeroStat('total-operations', Math.round(size / result.generation_time));
                
            } else {
                this.addConsoleMessage('error', `Initialization failed: ${result.message}`);
            }
        } catch (error) {
            this.addConsoleMessage('error', `Network error: ${error.message}`);
        } finally {
            this.setButtonLoading('generate-data', false);
            this.isProcessing = false;
        }
    }

    async runCPUSimulation() {
        if (!this.currentData) {
            this.showNotification('Please initialize dataset first!', 'warning');
            return;
        }

        this.setButtonLoading('run-cpu', true);
        this.isProcessing = true;
        this.addConsoleMessage('system', 'Starting CPU baseline simulation...');
        
        // CO1: Simulate instruction cycle for CPU operations
        this.addConsoleMessage('info', '[CO1: Instruction Cycle] Loading CPU instructions...');
        if (window.coaDemo) {
            await window.coaDemo.simulateCPUInstructions(this.currentData);
        }

        try {
            const response = await fetch('/api/run-cpu-simulation', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    operation: this.currentData.operation,
                    dataset_size: this.currentData.size
                })
            });

            const result = await response.json();
            
            if (result.success) {
                this.addConsoleMessage('success', `CPU simulation completed in ${result.execution_time.toFixed(3)}s`);
                this.addConsoleMessage('info', result.result_summary);
                
                this.currentData.cpuTime = result.execution_time;
                this.updatePerformanceMetrics();
                
                // Update analytics display
                this.updateMetricCard('Execution Time', `${result.execution_time.toFixed(3)}s`);
                
                // CO4: Output results
                this.addConsoleMessage('info', '[CO4: I/O] Displaying results to output device...');
                
            } else {
                this.addConsoleMessage('error', `CPU simulation failed: ${result.message}`);
            }
        } catch (error) {
            this.addConsoleMessage('error', `Network error: ${error.message}`);
        } finally {
            this.setButtonLoading('run-cpu', false);
            this.isProcessing = false;
        }
    }

    async runGPUSimulation() {
        if (!this.currentData) {
            this.showNotification('Please initialize dataset first!', 'warning');
            return;
        }

        this.setButtonLoading('run-gpu', true);
        this.isProcessing = true;
        this.addConsoleMessage('system', 'Starting GPU accelerated simulation...');
        
        // CO5: Visualize thread blocks automatically
        this.addConsoleMessage('info', '[CO5: GPU Architecture] Creating thread block grid...');
        if (window.coaDemo) {
            await window.coaDemo.autoVisualizeThreads(this.currentData.size);
        }
        
        // CO3: Simulate interrupt during GPU execution
        this.addConsoleMessage('info', '[CO3: Interrupt] Monitoring for interrupts during execution...');

        try {
            const response = await fetch('/api/run-gpu-simulation', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    operation: this.currentData.operation,
                    dataset_size: this.currentData.size
                })
            });

            const result = await response.json();
            
            if (result.success) {
                this.addConsoleMessage('success', `GPU simulation completed in ${result.execution_time.toFixed(3)}s`);
                this.addConsoleMessage('info', result.result_summary);
                
                this.currentData.gpuTime = result.execution_time;
                
                // Store thread block info
                if (result.thread_block_info) {
                    this.currentData.threadBlockInfo = result.thread_block_info;
                    this.updateThreadBlockVisualization(result.thread_block_info);
                    
                    // CO5: Show thread block details
                    this.addConsoleMessage('info', `[CO5: GPU] Executed across ${result.thread_block_info.num_blocks} thread blocks`);
                }
                
                // CO3: Simulate timer interrupt
                if (window.coaDemo && Math.random() > 0.5) {
                    await this.simulateDelay(300);
                    this.addConsoleMessage('warning', '[CO3: Interrupt] Timer interrupt triggered during execution!');
                    await window.coaDemo.autoHandleInterrupt();
                }
                
                this.updatePerformanceMetrics();
                
                // CO2: Performance evaluation happens automatically in updatePerformanceMetrics
                
            } else {
                this.addConsoleMessage('error', `GPU simulation failed: ${result.message}`);
            }
        } catch (error) {
            this.addConsoleMessage('error', `Network error: ${error.message}`);
        } finally {
            this.setButtonLoading('run-gpu', false);
            this.isProcessing = false;
        }
    }

    async simulateDelay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    updatePerformanceMetrics() {
        if (this.currentData.cpuTime && this.currentData.gpuTime) {
            const speedup = this.currentData.cpuTime / this.currentData.gpuTime;
            const efficiency = (speedup / 8) * 100; // Assuming 8 cores
            
            // CO2: Performance Evaluation - Highlight this is happening
            this.addConsoleMessage('info', '[CO2: Performance] Calculating speedup and efficiency...');
            
            // Update hero stats with animations
            this.animateCounter('speedup-ratio', speedup, 'x', 1);
            this.animateCounter('efficiency-score', efficiency, '%', 0);
            
            // Update metric cards
            this.updateMetricCard('Speedup Factor', `${speedup.toFixed(2)}x`);
            this.updateMetricCard('Throughput', `${Math.round(this.currentData.size / this.currentData.gpuTime)} ops/s`);
            
            // Add to performance history
            this.performanceHistory.push({
                size: this.currentData.size,
                operation: this.currentData.operation,
                cpuTime: this.currentData.cpuTime,
                gpuTime: this.currentData.gpuTime,
                speedup: speedup
            });
            
            this.updateCharts();
            
            // Show performance summary with CO2 label
            const improvement = ((this.currentData.cpuTime - this.currentData.gpuTime) / this.currentData.cpuTime * 100);
            this.addConsoleMessage('success', `[CO2: Performance] ${improvement.toFixed(1)}% faster with GPU acceleration`);
            this.addConsoleMessage('info', `[CO2: Performance] Speedup: ${speedup.toFixed(2)}x, Efficiency: ${efficiency.toFixed(1)}%`);
        }
    }

    updateCharts() {
        // Update time comparison chart
        const labels = this.performanceHistory.map(h => `${(h.size/1000).toFixed(0)}K`);
        const cpuTimes = this.performanceHistory.map(h => h.cpuTime);
        const gpuTimes = this.performanceHistory.map(h => h.gpuTime);
        
        this.timeChart.data.labels = labels;
        this.timeChart.data.datasets[0].data = cpuTimes;
        this.timeChart.data.datasets[1].data = gpuTimes;
        this.timeChart.update('active');
        
        // Update speedup chart
        const speedups = this.performanceHistory.map(h => h.speedup);
        this.speedupChart.data.labels = labels;
        this.speedupChart.data.datasets[0].data = speedups;
        this.speedupChart.update('active');
        
        // Update efficiency chart
        if (this.efficiencyChart) {
            const numProcesses = 8; // Default process count
            const efficiencies = this.performanceHistory.map(h => (h.speedup / numProcesses) * 100);
            this.efficiencyChart.data.labels = labels;
            this.efficiencyChart.data.datasets[0].data = efficiencies;
            this.efficiencyChart.update('active');
        }
    }

    updateThreadBlockVisualization(threadBlockInfo) {
        const container = document.getElementById('thread-block-viz');
        container.innerHTML = '';
        
        // Update thread count display
        const threadCount = document.getElementById('thread-count');
        if (threadCount) {
            threadCount.textContent = `${threadBlockInfo.num_blocks} Blocks`;
        }
        
        const colors = [
            '#76B900', '#00D4FF', '#FF6B6B', '#FFD93D', '#9ACD32',
            '#0099CC', '#EE5A52', '#FF9500', '#32CD32', '#1E90FF'
        ];
        
        // Create thread blocks with premium styling
        for (let i = 0; i < threadBlockInfo.num_blocks; i++) {
            const block = document.createElement('div');
            block.className = 'thread-block';
            block.style.background = `linear-gradient(135deg, ${colors[i % colors.length]}, ${colors[(i + 1) % colors.length]})`;
            block.textContent = `T${i + 1}`;
            block.title = `Thread Block ${i + 1}: ${threadBlockInfo.process_distribution[i] || threadBlockInfo.block_size} elements`;
            
            // Add animation delay
            block.style.animationDelay = `${i * 0.1}s`;
            block.classList.add('animate-fade-in');
            
            container.appendChild(block);
        }
    }

    // Utility methods
    addConsoleMessage(type, message) {
        const console = document.querySelector('.console-output');
        const line = document.createElement('div');
        line.className = 'console-line';
        
        const timestamp = new Date().toLocaleTimeString();
        const typeColors = {
            'system': '#76B900',
            'success': '#32CD32',
            'error': '#FF6B6B',
            'info': '#00D4FF',
            'warning': '#FFD93D'
        };
        
        line.innerHTML = `
            <span class="console-prompt" style="color: ${typeColors[type] || '#76B900'}">[${timestamp}]</span>
            <span class="console-text">${message}</span>
        `;
        
        console.appendChild(line);
        console.scrollTop = console.scrollHeight;
    }

    setButtonLoading(buttonId, isLoading) {
        const button = document.getElementById(buttonId);
        if (isLoading) {
            button.disabled = true;
            button.innerHTML = `<i class="fas fa-spinner fa-spin"></i> <span>Processing...</span>`;
            button.classList.add('animate-pulse');
        } else {
            button.disabled = false;
            button.innerHTML = button.dataset.originalText;
            button.classList.remove('animate-pulse');
        }
    }

    updateHeroStat(statId, value) {
        const element = document.getElementById(statId);
        if (element) {
            this.animateCounter(statId, value, '', 0);
        }
    }

    animateCounter(elementId, targetValue, suffix = '', decimals = 0) {
        const element = document.getElementById(elementId);
        if (!element) return;
        
        const startValue = parseFloat(element.textContent) || 0;
        const duration = 1000;
        const startTime = performance.now();
        
        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const currentValue = startValue + (targetValue - startValue) * this.easeOutQuart(progress);
            element.textContent = currentValue.toFixed(decimals) + suffix;
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };
        
        requestAnimationFrame(animate);
    }

    easeOutQuart(t) {
        return 1 - Math.pow(1 - t, 4);
    }

    updateMetricCard(title, value) {
        const cards = document.querySelectorAll('.metric-card');
        cards.forEach(card => {
            const cardTitle = card.querySelector('.metric-title');
            if (cardTitle && cardTitle.textContent === title) {
                const valueElement = card.querySelector('.metric-number');
                if (valueElement) {
                    valueElement.textContent = value;
                    card.classList.add('animate-glow');
                    setTimeout(() => card.classList.remove('animate-glow'), 2000);
                }
            }
        });
    }

    handleQuickAction(action) {
        switch (action) {
            case 'benchmark':
                this.runBenchmarkSuite();
                break;
            case 'optimize':
                this.autoOptimize();
                break;
            case 'export':
                this.showExportDialog();
                break;
        }
    }
    
    showExportDialog() {
        // Create export format selection dialog
        const dialog = document.createElement('div');
        dialog.className = 'export-dialog';
        dialog.innerHTML = `
            <div class="dialog-overlay"></div>
            <div class="dialog-content">
                <h3>Export Results</h3>
                <p>Choose export format:</p>
                <div class="export-options">
                    <button class="export-option-btn" data-format="json">
                        <i class="fas fa-file-code"></i>
                        <span>JSON Format</span>
                        <small>Raw data export</small>
                    </button>
                    <button class="export-option-btn" data-format="pdf">
                        <i class="fas fa-file-pdf"></i>
                        <span>PDF Report</span>
                        <small>Professional report</small>
                    </button>
                </div>
                <button class="dialog-close">Cancel</button>
            </div>
        `;
        
        // Add styles
        dialog.querySelector('.dialog-overlay').style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.7);
            z-index: 9998;
        `;
        
        dialog.querySelector('.dialog-content').style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: #1a1a1a;
            padding: 30px;
            border-radius: 12px;
            z-index: 9999;
            min-width: 400px;
            border: 1px solid #76B900;
        `;
        
        document.body.appendChild(dialog);
        
        // Handle format selection
        dialog.querySelectorAll('.export-option-btn').forEach(btn => {
            btn.addEventListener('click', async () => {
                const format = btn.dataset.format;
                document.body.removeChild(dialog);
                
                if (format === 'json') {
                    await this.exportController.exportJSON();
                } else if (format === 'pdf') {
                    await this.exportController.exportPDF();
                }
            });
        });
        
        // Handle close
        dialog.querySelector('.dialog-close').addEventListener('click', () => {
            document.body.removeChild(dialog);
        });
        
        dialog.querySelector('.dialog-overlay').addEventListener('click', () => {
            document.body.removeChild(dialog);
        });
    }

    async runBenchmarkSuite() {
        try {
            this.showNotification('Starting benchmark suite...', 'info');
            
            // Show progress modal
            const modal = this.createBenchmarkModal();
            document.body.appendChild(modal);
            
            // Start benchmark
            const response = await fetch('/api/run-benchmark', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    operations: ['vector_add', 'vector_multiply', 'dot_product', 'matrix_multiply'],
                    dataset_sizes: [10000, 50000, 100000, 500000]
                })
            });
            
            const results = await response.json();
            
            // Update performance history with benchmark results
            if (results.results) {
                results.results.forEach(result => {
                    this.performanceHistory.push({
                        size: result.dataset_size,
                        operation: result.operation,
                        cpuTime: result.cpu_time,
                        gpuTime: result.gpu_time,
                        speedup: result.speedup
                    });
                });
                
                this.updateCharts();
            }
            
            // Remove modal
            document.body.removeChild(modal);
            
            // Show summary
            this.showNotification(
                `Benchmark complete! Average speedup: ${results.average_speedup.toFixed(2)}x`,
                'success'
            );
            
        } catch (error) {
            this.showNotification(`Benchmark failed: ${error.message}`, 'error');
        }
    }
    
    createBenchmarkModal() {
        const modal = document.createElement('div');
        modal.className = 'benchmark-modal';
        modal.innerHTML = `
            <div class="modal-overlay"></div>
            <div class="modal-content">
                <h3>Running Benchmark Suite</h3>
                <div class="progress-container">
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: 0%"></div>
                    </div>
                    <div class="progress-text">0%</div>
                </div>
                <p class="benchmark-status">Initializing...</p>
            </div>
        `;
        
        modal.querySelector('.modal-overlay').style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.8);
            z-index: 9998;
        `;
        
        modal.querySelector('.modal-content').style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: #1a1a1a;
            padding: 30px;
            border-radius: 12px;
            z-index: 9999;
            min-width: 400px;
            border: 1px solid #76B900;
        `;
        
        return modal;
    }

    async autoOptimize() {
        try {
            this.showNotification('Analyzing system...', 'info');
            
            const response = await fetch('/api/auto-optimize');
            const suggestions = await response.json();
            
            if (!suggestions.success) {
                throw new Error('Failed to get optimization suggestions');
            }
            
            // Show suggestions modal
            this.showOptimizationModal(suggestions);
            
        } catch (error) {
            this.showNotification(`Auto-optimize failed: ${error.message}`, 'error');
        }
    }
    
    showOptimizationModal(suggestions) {
        const modal = document.createElement('div');
        modal.className = 'optimization-modal';
        modal.innerHTML = `
            <div class="modal-overlay"></div>
            <div class="modal-content">
                <h3>Optimization Suggestions</h3>
                <div class="suggestions">
                    <div class="suggestion-item">
                        <strong>Recommended Dataset Size:</strong>
                        <span>${suggestions.recommended_dataset_size.toLocaleString()} elements</span>
                        <small>${suggestions.rationale.dataset_size}</small>
                    </div>
                    <div class="suggestion-item">
                        <strong>Recommended Processes:</strong>
                        <span>${suggestions.recommended_processes} processes</span>
                        <small>${suggestions.rationale.processes}</small>
                    </div>
                    <div class="suggestion-item">
                        <strong>System Info:</strong>
                        <span>${suggestions.cpu_cores} CPU cores, ${suggestions.available_memory_gb}GB RAM</span>
                    </div>
                </div>
                <div class="modal-actions">
                    <button class="btn-primary apply-btn">Apply Suggestions</button>
                    <button class="btn-secondary dismiss-btn">Dismiss</button>
                </div>
            </div>
        `;
        
        modal.querySelector('.modal-overlay').style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.8);
            z-index: 9998;
        `;
        
        modal.querySelector('.modal-content').style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: #1a1a1a;
            padding: 30px;
            border-radius: 12px;
            z-index: 9999;
            min-width: 500px;
            border: 1px solid #76B900;
        `;
        
        document.body.appendChild(modal);
        
        // Handle apply
        modal.querySelector('.apply-btn').addEventListener('click', () => {
            this.configManager.applyConfig({
                datasetSize: suggestions.recommended_dataset_size,
                operation: this.configManager.getCurrentConfig().operation,
                numProcesses: suggestions.recommended_processes
            });
            document.body.removeChild(modal);
            this.showNotification('Optimization applied!', 'success');
        });
        
        // Handle dismiss
        modal.querySelector('.dismiss-btn').addEventListener('click', () => {
            document.body.removeChild(modal);
        });
        
        modal.querySelector('.modal-overlay').addEventListener('click', () => {
            document.body.removeChild(modal);
        });
    }

    switchChart(chartType) {
        const charts = ['time-chart', 'speedup-chart', 'efficiency-chart'];
        const buttons = document.querySelectorAll('.chart-btn');
        
        // Update button states
        buttons.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.chart === chartType);
        });
        
        // Show/hide charts
        charts.forEach(chartId => {
            const chart = document.getElementById(chartId);
            if (chart) {
                chart.style.display = chartId === `${chartType}-chart` ? 'block' : 'none';
            }
        });
    }
    
    clearConsole() {
        const consoleOutput = document.querySelector('.console-output');
        if (consoleOutput) {
            // Keep the initial message
            consoleOutput.innerHTML = `
                <div class="console-line">
                    <span class="console-prompt">nvidia@quantum:~$</span>
                    <span class="console-text">Console cleared. System ready.</span>
                </div>
            `;
            this.showNotification('Console cleared', 'success');
        }
    }
    
    exportConsoleLogs() {
        const logs = this.exportController.getConsoleLogs();
        
        if (logs.length === 0) {
            this.showNotification('No console logs to export', 'warning');
            return;
        }
        
        // Format logs with timestamps
        const timestamp = new Date().toISOString();
        const header = `GPU Quantum Compute Simulator - Console Logs\nExported: ${timestamp}\n${'='.repeat(60)}\n\n`;
        const logText = header + logs.join('\n');
        
        // Create and download file
        const blob = new Blob([logText], { type: 'text/plain' });
        const filename = `simulation-log-${new Date().toISOString().split('T')[0]}.txt`;
        this.exportController.downloadFile(blob, filename);
        
        this.showNotification('Console logs exported', 'success');
    }
    
    resetConfiguration() {
        const defaultConfig = this.configManager.resetToDefault();
        this.configManager.applyConfig(defaultConfig);
        this.showNotification('Configuration reset to defaults', 'success');
    }
    
    showSavePresetDialog() {
        const dialog = document.createElement('div');
        dialog.className = 'preset-dialog';
        dialog.innerHTML = `
            <div class="dialog-overlay"></div>
            <div class="dialog-content">
                <h3>Save Configuration Preset</h3>
                <div class="form-group">
                    <label>Preset Name:</label>
                    <input type="text" id="preset-name" placeholder="My Configuration" />
                </div>
                <div class="form-group">
                    <label>Description (optional):</label>
                    <input type="text" id="preset-description" placeholder="Description..." />
                </div>
                <div class="modal-actions">
                    <button class="btn-primary save-btn">Save</button>
                    <button class="btn-secondary cancel-btn">Cancel</button>
                </div>
            </div>
        `;
        
        dialog.querySelector('.dialog-overlay').style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.8);
            z-index: 9998;
        `;
        
        dialog.querySelector('.dialog-content').style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: #1a1a1a;
            padding: 30px;
            border-radius: 12px;
            z-index: 9999;
            min-width: 400px;
            border: 1px solid #76B900;
        `;
        
        document.body.appendChild(dialog);
        
        // Handle save
        dialog.querySelector('.save-btn').addEventListener('click', () => {
            const name = document.getElementById('preset-name').value.trim();
            const description = document.getElementById('preset-description').value.trim();
            
            if (!name) {
                this.showNotification('Please enter a preset name', 'warning');
                return;
            }
            
            const success = this.configManager.savePreset(name, description);
            document.body.removeChild(dialog);
            
            if (success) {
                this.showNotification(`Preset "${name}" saved successfully`, 'success');
            } else {
                this.showNotification('Failed to save preset', 'error');
            }
        });
        
        // Handle cancel
        dialog.querySelector('.cancel-btn').addEventListener('click', () => {
            document.body.removeChild(dialog);
        });
        
        dialog.querySelector('.dialog-overlay').addEventListener('click', () => {
            document.body.removeChild(dialog);
        });
    }

    switchTab(tabType) {
        const buttons = document.querySelectorAll('.tab-btn');
        buttons.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.tab === tabType);
        });
        
        // Tab switching logic here
    }

    showNotification(message, type = 'info') {
        // Create and show notification
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        // Style the notification
        Object.assign(notification.style, {
            position: 'fixed',
            top: '90px',
            right: '20px',
            padding: '16px 24px',
            borderRadius: '12px',
            color: '#ffffff',
            fontWeight: '600',
            zIndex: '10000',
            transform: 'translateX(400px)',
            transition: 'transform 0.3s ease',
            maxWidth: '400px'
        });
        
        const colors = {
            'success': 'linear-gradient(135deg, #32CD32, #228B22)',
            'error': 'linear-gradient(135deg, #FF6B6B, #EE5A52)',
            'warning': 'linear-gradient(135deg, #FFD93D, #FF9500)',
            'info': 'linear-gradient(135deg, #00D4FF, #0099CC)'
        };
        
        notification.style.background = colors[type] || colors.info;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        // Remove after delay
        setTimeout(() => {
            notification.style.transform = 'translateX(400px)';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 4000);
    }
}

// Initialize the application when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.studioInstance = new QuantumComputeStudio();
});


// ============================================
// COA DEMONSTRATION FUNCTIONALITY
// ============================================

class COADemonstrations {
    constructor(studio) {
        this.studio = studio;
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // CO1: Instruction Cycle
        document.getElementById('run-instruction-cycle')?.addEventListener('click', () => this.runInstructionCycle());
        document.getElementById('step-instruction')?.addEventListener('click', () => this.stepInstruction());

        // CO3: Interrupt Handling
        document.getElementById('trigger-interrupt')?.addEventListener('click', () => this.triggerInterrupt());

        // CO5: Thread Visualization
        document.getElementById('visualize-threads')?.addEventListener('click', () => this.visualizeThreads());
    }

    // ========== CO1: Instruction Cycle ==========
    async runInstructionCycle() {
        const btn = document.getElementById('run-instruction-cycle');
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i><span>Running...</span>';

        try {
            const response = await fetch('/api/instruction-cycle', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });

            const result = await response.json();

            if (result.success) {
                this.animateInstructionCycle(result.execution_log);
                this.updateCPUState(result.cpu_state);
                this.studio.showNotification('Instruction cycle completed!', 'success');
            } else {
                this.studio.showNotification('Instruction cycle failed', 'error');
            }
        } catch (error) {
            console.error('Instruction cycle error:', error);
            this.studio.showNotification('Network error', 'error');
        } finally {
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-play"></i><span>Run Instruction Cycle</span>';
        }
    }

    // Automatic CO1 simulation during CPU execution
    async simulateCPUInstructions(currentData) {
        try {
            // Map operation to instruction count
            const instructionMap = {
                'vector_add': 3,
                'vector_multiply': 3,
                'dot_product': 4,
                'matrix_multiply': 5
            };
            
            const numInstructions = instructionMap[currentData.operation] || 3;
            
            const response = await fetch(`/api/instruction-cycle?num_instructions=${numInstructions}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });

            const result = await response.json();

            if (result.success) {
                // Animate in background
                this.animateInstructionCycleQuiet(result.execution_log);
                this.updateCPUState(result.cpu_state);
            }
        } catch (error) {
            console.error('Auto instruction cycle error:', error);
        }
    }

    animateInstructionCycleQuiet(executionLog) {
        // Faster animation for automatic mode
        executionLog.forEach((step, index) => {
            setTimeout(() => {
                this.highlightStage(step.stage);
                this.updateStageContent(step);
                if (index % 3 === 2) { // Only log complete instructions
                    this.addInstructionLog(step);
                }
            }, index * 300);
        });
    }

    async stepInstruction() {
        try {
            const response = await fetch('/api/instruction-cycle/step', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });

            const result = await response.json();

            if (result.success) {
                this.animateInstructionCycle(result.steps);
                this.updateCPUState(result.cpu_state);
            } else {
                this.studio.showNotification(result.message, 'warning');
            }
        } catch (error) {
            console.error('Step instruction error:', error);
        }
    }

    animateInstructionCycle(executionLog) {
        const logContainer = document.getElementById('instruction-log');
        
        executionLog.forEach((step, index) => {
            setTimeout(() => {
                // Highlight active stage
                this.highlightStage(step.stage);
                
                // Update stage content
                this.updateStageContent(step);
                
                // Add to log
                this.addInstructionLog(step);
            }, index * 800);
        });
    }

    highlightStage(stageName) {
        // Remove active class from all stages
        document.querySelectorAll('.stage-box').forEach(box => box.classList.remove('active'));
        
        // Add active class to current stage
        const stageMap = {
            'FETCH': 'fetch-stage',
            'DECODE': 'decode-stage',
            'EXECUTE': 'execute-stage'
        };
        
        const stageId = stageMap[stageName];
        if (stageId) {
            document.getElementById(stageId)?.classList.add('active');
        }
    }

    updateStageContent(step) {
        const stageMap = {
            'FETCH': 'fetch-stage',
            'DECODE': 'decode-stage',
            'EXECUTE': 'execute-stage'
        };
        
        const stageId = stageMap[step.stage];
        if (stageId) {
            const stageBox = document.getElementById(stageId);
            const contentDiv = stageBox?.querySelector('.stage-content');
            if (contentDiv) {
                if (step.stage === 'FETCH') {
                    contentDiv.textContent = step.instruction || step.message;
                } else if (step.stage === 'DECODE') {
                    contentDiv.textContent = `${step.opcode} ${step.operand1}, ${step.operand2}`;
                } else if (step.stage === 'EXECUTE') {
                    contentDiv.textContent = step.details?.alu_operation || step.message;
                }
            }
        }
    }

    addInstructionLog(step) {
        const logContainer = document.getElementById('instruction-log');
        const entry = document.createElement('div');
        entry.className = 'log-entry';
        entry.innerHTML = `
            <span class="log-stage">[${step.stage}]</span>
            <span class="log-message">${step.message}</span>
        `;
        logContainer.appendChild(entry);
        logContainer.scrollTop = logContainer.scrollHeight;
    }

    updateCPUState(state) {
        document.getElementById('pc-value').textContent = state.program_counter;
        document.getElementById('acc-value').textContent = state.accumulator.toFixed(2);
    }

    // ========== CO3: Interrupt Handling ==========
    async triggerInterrupt() {
        const btn = document.getElementById('trigger-interrupt');
        const interruptType = document.getElementById('interrupt-type').value;
        
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i><span>Triggering...</span>';

        try {
            // First, trigger the interrupt
            const triggerResponse = await fetch('/api/trigger-interrupt', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    interrupt_type: interruptType,
                    data: { source: 'ui', timestamp: Date.now() }
                })
            });

            const triggerResult = await triggerResponse.json();

            if (triggerResult.success) {
                this.studio.showNotification(`Interrupt ${interruptType} triggered!`, 'warning');
                
                // Animate interrupt indicator
                this.animateInterruptIndicator();
                
                // Wait a moment, then handle the interrupt
                setTimeout(async () => {
                    await this.handleInterrupt();
                }, 500);
            }
        } catch (error) {
            console.error('Trigger interrupt error:', error);
            this.studio.showNotification('Failed to trigger interrupt', 'error');
        } finally {
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-exclamation-triangle"></i><span>Trigger Interrupt</span>';
        }
    }

    // Automatic interrupt handling during GPU execution
    async autoHandleInterrupt() {
        try {
            const response = await fetch('/api/handle-interrupt', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    current_state: {
                        pc: parseInt(document.getElementById('pc-value')?.textContent || 0),
                        accumulator: parseFloat(document.getElementById('acc-value')?.textContent || 0),
                        registers: {}
                    }
                })
            });

            const result = await response.json();

            if (result.success) {
                this.animateInterruptHandlingQuiet(result.handling_log);
            }
        } catch (error) {
            console.error('Auto interrupt handling error:', error);
        }
    }

    animateInterruptHandlingQuiet(handlingLog) {
        const logContainer = document.getElementById('interrupt-log');
        
        const stepMap = {
            'SAVE_CONTEXT': 'save-context-step',
            'DISABLE_INTERRUPTS': 'disable-int-step',
            'EXECUTE_ISR': 'execute-isr-step',
            'ISR_COMPLETE': 'execute-isr-step',
            'RESTORE_CONTEXT': 'restore-context-step',
            'ENABLE_INTERRUPTS': 'restore-context-step'
        };
        
        handlingLog.forEach((logEntry, index) => {
            setTimeout(() => {
                // Highlight flow step
                document.querySelectorAll('.flow-step').forEach(step => step.classList.remove('active'));
                const stepId = stepMap[logEntry.step];
                if (stepId) {
                    document.getElementById(stepId)?.classList.add('active');
                }
                
                // Add to log (only key steps)
                if (['SAVE_CONTEXT', 'EXECUTE_ISR', 'RESTORE_CONTEXT'].includes(logEntry.step)) {
                    const entry = document.createElement('div');
                    entry.className = 'log-entry';
                    entry.innerHTML = `
                        <span class="log-stage">[${logEntry.step}]</span>
                        <span class="log-message">${logEntry.message}</span>
                    `;
                    logContainer.appendChild(entry);
                    logContainer.scrollTop = logContainer.scrollHeight;
                }
            }, index * 400);
        });
        
        // Clear active states after animation
        setTimeout(() => {
            document.querySelectorAll('.flow-step').forEach(step => step.classList.remove('active'));
        }, handlingLog.length * 400 + 300);
    }

    async handleInterrupt() {
        try {
            const response = await fetch('/api/handle-interrupt', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    current_state: {
                        pc: parseInt(document.getElementById('pc-value')?.textContent || 0),
                        accumulator: parseFloat(document.getElementById('acc-value')?.textContent || 0),
                        registers: {}
                    }
                })
            });

            const result = await response.json();

            if (result.success) {
                this.animateInterruptHandling(result.handling_log);
                this.studio.showNotification('Interrupt handled successfully!', 'success');
            }
        } catch (error) {
            console.error('Handle interrupt error:', error);
        }
    }

    animateInterruptIndicator() {
        const indicator = document.getElementById('interrupt-indicator');
        const statusText = document.getElementById('interrupt-status-text');
        
        indicator.classList.add('disabled');
        statusText.textContent = 'Interrupts Disabled';
        
        setTimeout(() => {
            indicator.classList.remove('disabled');
            statusText.textContent = 'Interrupts Enabled';
        }, 3000);
    }

    animateInterruptHandling(handlingLog) {
        const logContainer = document.getElementById('interrupt-log');
        logContainer.innerHTML = '';
        
        const stepMap = {
            'SAVE_CONTEXT': 'save-context-step',
            'DISABLE_INTERRUPTS': 'disable-int-step',
            'EXECUTE_ISR': 'execute-isr-step',
            'ISR_COMPLETE': 'execute-isr-step',
            'RESTORE_CONTEXT': 'restore-context-step',
            'ENABLE_INTERRUPTS': 'restore-context-step'
        };
        
        handlingLog.forEach((logEntry, index) => {
            setTimeout(() => {
                // Highlight flow step
                document.querySelectorAll('.flow-step').forEach(step => step.classList.remove('active'));
                const stepId = stepMap[logEntry.step];
                if (stepId) {
                    document.getElementById(stepId)?.classList.add('active');
                }
                
                // Add to log
                const entry = document.createElement('div');
                entry.className = 'log-entry';
                entry.innerHTML = `
                    <span class="log-stage">[${logEntry.step}]</span>
                    <span class="log-message">${logEntry.message}</span>
                `;
                logContainer.appendChild(entry);
                logContainer.scrollTop = logContainer.scrollHeight;
            }, index * 600);
        });
        
        // Clear active states after animation
        setTimeout(() => {
            document.querySelectorAll('.flow-step').forEach(step => step.classList.remove('active'));
        }, handlingLog.length * 600 + 500);
    }

    // ========== CO5: Thread Visualization ==========
    async visualizeThreads() {
        const btn = document.getElementById('visualize-threads');
        const datasetSize = parseInt(document.getElementById('dataset-size')?.value || 50000);
        
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i><span>Visualizing...</span>';

        try {
            const response = await fetch(`/api/thread-visualization?dataset_size=${datasetSize}`);
            const result = await response.json();

            if (result.success) {
                this.renderThreadBlocks(result);
                this.updateThreadStats(result);
                this.studio.showNotification('Thread blocks visualized!', 'success');
            }
        } catch (error) {
            console.error('Thread visualization error:', error);
            this.studio.showNotification('Visualization failed', 'error');
        } finally {
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-eye"></i><span>Visualize Thread Blocks</span>';
        }
    }

    // Automatic thread visualization during GPU execution
    async autoVisualizeThreads(datasetSize) {
        try {
            const response = await fetch(`/api/thread-visualization?dataset_size=${datasetSize}`);
            const result = await response.json();

            if (result.success) {
                this.renderThreadBlocks(result, true); // true = auto mode
                this.updateThreadStats(result);
            }
        } catch (error) {
            console.error('Auto thread visualization error:', error);
        }
    }

    renderThreadBlocks(data, autoMode = false) {
        const gridContainer = document.getElementById('enhanced-thread-grid');
        gridContainer.innerHTML = '';
        
        // Limit blocks shown in auto mode for performance
        const blocksToShow = autoMode ? Math.min(data.blocks.length, 20) : data.blocks.length;
        
        for (let i = 0; i < blocksToShow; i++) {
            const block = data.blocks[i];
            const blockElement = document.createElement('div');
            blockElement.className = 'thread-block-item';
            blockElement.innerHTML = `
                <div class="block-id">Block ${block.block_id}</div>
                <div class="block-threads">${block.thread_count} threads</div>
            `;
            
            // Add animation delay
            blockElement.style.animationDelay = `${i * 0.05}s`;
            
            // Add hover tooltip
            blockElement.title = `Block ${block.block_id}: Elements ${block.start_index}-${block.end_index}`;
            
            // Simulate execution animation
            setTimeout(() => {
                blockElement.classList.add('executing');
                setTimeout(() => {
                    blockElement.classList.remove('executing');
                }, autoMode ? 500 : 1000);
            }, i * (autoMode ? 50 : 100));
            
            gridContainer.appendChild(blockElement);
        }
        
        // Show message if blocks were limited
        if (autoMode && data.blocks.length > blocksToShow) {
            const moreElement = document.createElement('div');
            moreElement.className = 'thread-block-item';
            moreElement.style.background = 'rgba(118, 185, 0, 0.3)';
            moreElement.innerHTML = `
                <div class="block-id">+${data.blocks.length - blocksToShow}</div>
                <div class="block-threads">more blocks</div>
            `;
            gridContainer.appendChild(moreElement);
        }
        
        // Update grid info
        document.getElementById('grid-info').textContent = 
            `${data.num_blocks} blocks × ${data.block_size} threads = ${data.num_blocks * data.block_size} total threads`;
    }

    updateThreadStats(data) {
        document.getElementById('grid-size').textContent = `${data.num_blocks} blocks`;
        document.getElementById('block-size-stat').textContent = `${data.block_size} threads`;
        document.getElementById('total-threads').textContent = `${data.num_blocks * data.block_size}`;
    }
}

// Initialize COA demonstrations when studio is ready
document.addEventListener('DOMContentLoaded', () => {
    // Wait for studio to be initialized
    setTimeout(() => {
        if (window.studioInstance) {
            window.coaDemo = new COADemonstrations(window.studioInstance);
        }
    }, 100);
});
