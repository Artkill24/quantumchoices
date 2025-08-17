// QuantumChoices Admin API
const express = require('express');
const fs = require('fs').promises;
const { exec } = require('child_process');
const app = express();

app.use(express.json());

// Get analytics data
app.get('/api/analytics', async (req, res) => {
    try {
        const data = await fs.readFile('assets/data/analytics_data.json', 'utf8');
        res.json(JSON.parse(data));
    } catch (error) {
        res.status(500).json({ error: 'Failed to load analytics' });
    }
});

// Run AI analysis
app.post('/api/run-analysis', (req, res) => {
    exec('python scripts/quantum_analyzer.py', (error, stdout, stderr) => {
        if (error) {
            return res.status(500).json({ error: 'Analysis failed' });
        }
        res.json({ message: 'Analysis completed', output: stdout });
    });
});

// Send newsletter
app.post('/api/send-newsletter', (req, res) => {
    exec('python scripts/email_automation.py newsletter', (error, stdout, stderr) => {
        if (error) {
            return res.status(500).json({ error: 'Failed to send newsletter' });
        }
        res.json({ message: 'Newsletter sent successfully' });
    });
});

// Export data
app.get('/api/export', async (req, res) => {
    try {
        const quantumData = await fs.readFile('assets/data/quantum_data.json', 'utf8');
        const analyticsData = await fs.readFile('assets/data/analytics_data.json', 'utf8');
        
        const exportData = {
            quantum: JSON.parse(quantumData),
            analytics: JSON.parse(analyticsData),
            exported_at: new Date().toISOString()
        };
        
        res.setHeader('Content-Disposition', 'attachment; filename=quantum-export.json');
        res.json(exportData);
    } catch (error) {
        res.status(500).json({ error: 'Export failed' });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`QuantumChoices API server running on port ${PORT}`);
});
