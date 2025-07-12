import React from 'react';

interface Result {
  id: number;
  data: Record<string, any>;
}

interface Task {
  id: number;
  name: string;
  instrument: string;
  status: string;
  results?: Result[];
}

interface Workflow {
  id: number;
  name: string;
  tasks: Task[];
}

interface WorkflowListProps {
  workflows: Workflow[];
}

const getStatusColor = (status: string) => {
  switch (status) {
    case 'completed': return 'lightgreen';
    case 'running': return 'lightblue';
    case 'failed': return 'lightcoral';
    default: return 'lightgrey';
  }
};

const ResultsTable: React.FC<{ task: Task }> = ({ task }) => {
  if (!task.results || task.results.length === 0) return null;
  const keys = Object.keys(task.results[0].data);
  return (
    <table>
      <thead>
        <tr>
          {keys.map(key => <th key={key}>{key}</th>)}
        </tr>
      </thead>
      <tbody>
        {task.results.map(result => (
          <tr key={result.id}>
            {keys.map(key => <td key={key}>{String(result.data[key])}</td>)}
          </tr>
        ))}
      </tbody>
    </table>
  );
};

const WorkflowList: React.FC<WorkflowListProps> = ({ workflows }) => (
  <div className="workflows">
    <h2>Workflows</h2>
    {workflows.map(workflow => (
      <div key={workflow.id} className="workflow-card">
        <h3>{workflow.name}</h3>
        {workflow.tasks.map(task => (
          <div key={task.id} className="task-item" style={{ backgroundColor: getStatusColor(task.status) }}>
            <p><strong>Task:</strong> {task.name} ({task.instrument})</p>
            <p><strong>Status:</strong> {task.status}</p>
            {task.status === 'completed' && <ResultsTable task={task} />}
          </div>
        ))}
      </div>
    ))}
  </div>
);

export default WorkflowList;
