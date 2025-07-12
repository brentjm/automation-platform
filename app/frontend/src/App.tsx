import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import LabVisual from './LabVisual';
import WorkflowList from './WorkflowList';
import './App.css';

const API_URL = import.meta.env.VITE_API_URL || '';

interface Task {
  id: number;
  name: string;
  instrument: string;
  status: string;
  results?: any[];
}

interface Workflow {
  id: number;
  name: string;
  tasks: Task[];
}

function App() {
  const [workflows, setWorkflows] = useState<Workflow[]>([]);
  const [activeInstruments, setActiveInstruments] = useState<string[]>([]);

  const fetchWorkflows = useCallback(async () => {
    try {
      const response = await axios.get<Workflow[]>(`${API_URL}/api/workflows`);
      setWorkflows(response.data);

      const runningInstruments = response.data
        .flatMap(w => w.tasks)
        .filter(t => t.status === 'running')
        .map(t => t.instrument);
      setActiveInstruments([...new Set(runningInstruments)]);
    } catch (error) {
      console.error("Error fetching workflows:", error);
    }
  }, []);

  useEffect(() => {
    fetchWorkflows();
    const interval = setInterval(fetchWorkflows, 2000); // Poll every 2 seconds
    return () => clearInterval(interval);
  }, [fetchWorkflows]);

  const handleCreateWorkflow = async () => {
    const workflowData = {
      name: `My Workflow #${workflows.length + 1}`,
      tasks: [
        { name: "Sample Prep", instrument: "instrument-a" },
        { name: "Analysis", instrument: "instrument-b" }
      ]
    };
    try {
      await axios.post(`${API_URL}/api/workflows`, workflowData);
      fetchWorkflows();
    } catch (error) {
      console.error("Error creating workflow:", error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Laboratory Automation Framework</h1>
      </header>
      <main>
        <div className="main-layout">
          <div className="controls-and-workflows">
            <div className="controls">
              <h2>Controls</h2>
              <button onClick={handleCreateWorkflow}>Start New Workflow</button>
            </div>
            <WorkflowList workflows={workflows} />
          </div>
          <div className="visuals">
            <h2>Lab Status</h2>
            <LabVisual activeInstruments={activeInstruments} />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
