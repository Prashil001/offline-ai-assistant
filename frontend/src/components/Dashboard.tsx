import React, { useEffect, useState } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import { Activity, Cpu, Clock, CheckCircle } from 'lucide-react';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

export function Dashboard() {
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);

  useEffect(() => {
    fetchResults();
  }, []);

  const fetchResults = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/v1/benchmarks/results');
      const data = await res.json();
      setResults(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const runBenchmark = async () => {
    setRunning(true);
    try {
      await fetch('http://localhost:8000/api/v1/benchmarks/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ models: ['qwen3:4b', 'gemma3:4b', 'llama3.2:3b'] }),
      });
      await fetchResults();
    } catch (e) {
      console.error(e);
    } finally {
      setRunning(false);
    }
  };

  if (loading) return <div className="p-8 text-center">Loading dashboard...</div>;

  const latestRun = results.length > 0 ? results[0].data.results : null;
  const models = latestRun ? Object.keys(latestRun) : [];

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: { position: 'top' as const, labels: { color: '#e5e7eb' } },
    },
    scales: {
      y: { ticks: { color: '#9ca3af' }, grid: { color: '#374151' } },
      x: { ticks: { color: '#9ca3af' }, grid: { color: '#374151' } },
    },
  };

  return (
    <div className="flex-1 overflow-y-auto p-6 bg-gray-900 text-gray-100">
      <div className="max-w-6xl mx-auto space-y-8">
        <div className="flex justify-between items-center">
          <h2 className="text-2xl font-bold">Model Benchmarks</h2>
          <button
            onClick={runBenchmark}
            disabled={running}
            className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-md font-medium disabled:opacity-50"
          >
            {running ? 'Running...' : 'Run Benchmark Suite'}
          </button>
        </div>

        {!latestRun ? (
          <div className="text-gray-400">No benchmark results found. Run the suite to generate data.</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            
            {/* Latency Chart */}
            <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow-sm">
              <div className="flex items-center gap-2 mb-4">
                <Clock className="text-yellow-500 w-5 h-5" />
                <h3 className="font-semibold text-lg">Avg Latency (seconds)</h3>
              </div>
              <Bar 
                options={chartOptions} 
                data={{
                  labels: models,
                  datasets: [{
                    label: 'Latency',
                    data: models.map(m => latestRun[m].avg_latency_s),
                    backgroundColor: 'rgba(234, 179, 8, 0.6)',
                    borderColor: 'rgb(234, 179, 8)',
                    borderWidth: 1,
                  }]
                }} 
              />
            </div>

            {/* RAM Chart */}
            <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow-sm">
              <div className="flex items-center gap-2 mb-4">
                <Activity className="text-blue-500 w-5 h-5" />
                <h3 className="font-semibold text-lg">Avg RAM Usage (MB)</h3>
              </div>
              <Bar 
                options={chartOptions} 
                data={{
                  labels: models,
                  datasets: [{
                    label: 'RAM (MB)',
                    data: models.map(m => latestRun[m].avg_mem_mb),
                    backgroundColor: 'rgba(59, 130, 246, 0.6)',
                    borderColor: 'rgb(59, 130, 246)',
                    borderWidth: 1,
                  }]
                }} 
              />
            </div>

            {/* CPU Chart */}
            <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow-sm">
              <div className="flex items-center gap-2 mb-4">
                <Cpu className="text-purple-500 w-5 h-5" />
                <h3 className="font-semibold text-lg">Avg CPU Time (seconds)</h3>
              </div>
              <Bar 
                options={chartOptions} 
                data={{
                  labels: models,
                  datasets: [{
                    label: 'CPU Time',
                    data: models.map(m => latestRun[m].avg_cpu_s),
                    backgroundColor: 'rgba(168, 85, 247, 0.6)',
                    borderColor: 'rgb(168, 85, 247)',
                    borderWidth: 1,
                  }]
                }} 
              />
            </div>

            {/* Accuracy Chart */}
            <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow-sm">
              <div className="flex items-center gap-2 mb-4">
                <CheckCircle className="text-emerald-500 w-5 h-5" />
                <h3 className="font-semibold text-lg">Accuracy Rate</h3>
              </div>
              <Bar 
                options={{
                  ...chartOptions,
                  scales: { ...chartOptions.scales, y: { ...chartOptions.scales.y, max: 1.0 } }
                }} 
                data={{
                  labels: models,
                  datasets: [{
                    label: 'Accuracy',
                    data: models.map(m => latestRun[m].accuracy_rate),
                    backgroundColor: 'rgba(16, 185, 129, 0.6)',
                    borderColor: 'rgb(16, 185, 129)',
                    borderWidth: 1,
                  }]
                }} 
              />
            </div>

          </div>
        )}
      </div>
    </div>
  );
}
