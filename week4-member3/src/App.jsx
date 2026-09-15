import { useEffect, useState } from 'react'
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
} from '@xyflow/react'
import '@xyflow/react/dist/style.css'
import './App.css'

const initialNodes = [
  {
    id: 'source',
    position: { x: 50, y: 150 },
    data: {
      label: (
        <div>
          <strong>Event Source</strong>
          <div>Streaming input</div>
        </div>
      ),
      type: 'source',
    },
  },
  {
    id: 'processor',
    position: { x: 300, y: 150 },
    data: {
      label: (
        <div>
          <strong>Stream Processor</strong>
          <div>Processing events</div>
        </div>
      ),
      type: 'processor',
    },
  },
  {
    id: 'metrics',
    position: { x: 550, y: 150 },
    data: {
      label: (
        <div>
          <strong>Prometheus Metrics</strong>
          <div>Events & lag</div>
        </div>
      ),
      type: 'metrics',
    },
  },
  {
    id: 'dashboard',
    position: { x: 800, y: 150 },
    data: {
      label: (
        <div>
          <strong>Dashboard</strong>
          <div>Bottleneck detection</div>
        </div>
      ),
      type: 'dashboard',
    },
  },
]

const initialEdges = [
  {
    id: 'source-processor',
    source: 'source',
    target: 'processor',
    animated: true,
  },
  {
    id: 'processor-metrics',
    source: 'processor',
    target: 'metrics',
    animated: true,
  },
  {
    id: 'metrics-dashboard',
    source: 'metrics',
    target: 'dashboard',
    animated: true,
  },
]

const initialNodeMetrics = {
  source: {
    eventsProcessed: 0,
    processingLag: 0,
  },
  processor: {
    eventsProcessed: 0,
    processingLag: 0,
  },
  metrics: {
    eventsProcessed: 0,
    processingLag: 0,
  },
  dashboard: {
    eventsProcessed: 0,
    processingLag: 0,
  },
}

function parsePrometheusMetrics(text) {
  const metrics = {}

  text.split('\n').forEach((line) => {
    if (!line || line.startsWith('#')) {
      return
    }

    const match = line.match(
      /^([a-zA-Z_:][a-zA-Z0-9_:]*)\s+([-+]?(?:\d*\.?\d+)(?:[eE][-+]?\d+)?)$/
    )

    if (match) {
      metrics[match[1]] = Number(match[2])
    }
  })

  return metrics
}

function formatMetricValue(value) {
  if (value === null || value === undefined) {
    return '--'
  }

  return Number(value).toLocaleString()
}
function detectBottleneck(metrics) {
  let bottleneckNode = null
  let highestLag = -1

  Object.entries(metrics).forEach(([nodeId, nodeMetric]) => {
    if (nodeMetric.processingLag > highestLag) {
      highestLag = nodeMetric.processingLag
      bottleneckNode = nodeId
    }
  })

  return {
    nodeId: bottleneckNode,
    processingLag: highestLag,
  }
}
function App() {
  const [nodes] = useState(initialNodes)
  const [edges] = useState(initialEdges)
  const [nodeMetrics, setNodeMetrics] = useState(initialNodeMetrics)
  const [bottleneckNode, setBottleneckNode] = useState(null)
  const [eventsProcessed, setEventsProcessed] = useState(null)
  const [processingLag, setProcessingLag] = useState(null)
  const [metricsError, setMetricsError] = useState(false)

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const response = await fetch('/metrics', {
          cache: 'no-store',
        })

        if (!response.ok) {
          throw new Error('Failed to fetch metrics')
        }

        const text = await response.text()
        const metrics = parsePrometheusMetrics(text)

        const processed = metrics.events_processed_total ?? null
        const lag = metrics.processing_lag ?? null

        setEventsProcessed(processed)
        setProcessingLag(lag)

        setNodeMetrics((currentMetrics) => ({
          ...currentMetrics,
          processor: {
            ...currentMetrics.processor,
            eventsProcessed: processed ?? currentMetrics.processor.eventsProcessed,
            processingLag: lag ?? currentMetrics.processor.processingLag,
          },
          metrics: {
            ...currentMetrics.metrics,
            eventsProcessed: processed ?? currentMetrics.metrics.eventsProcessed,
            processingLag: lag ?? currentMetrics.metrics.processingLag,
          },
        }))
const updatedNodeMetrics = {
  ...nodeMetrics,
  processor: {
    ...nodeMetrics.processor,
    eventsProcessed: processed ?? nodeMetrics.processor.eventsProcessed,
    processingLag: lag ?? nodeMetrics.processor.processingLag,
  },
  metrics: {
    ...nodeMetrics.metrics,
    eventsProcessed: processed ?? nodeMetrics.metrics.eventsProcessed,
    processingLag: lag ?? nodeMetrics.metrics.processingLag,
  },
}

const detectedBottleneck = detectBottleneck(updatedNodeMetrics)

setBottleneckNode(detectedBottleneck.nodeId)
        setMetricsError(false)
      } catch (error) {
        console.error('Metrics fetch failed:', error)
        setMetricsError(true)
      }
    }

    fetchMetrics()

    const interval = setInterval(fetchMetrics, 5000)

    return () => clearInterval(interval)
  }, [])

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div>
          <h1>Streaming DAG Monitor</h1>
          <p>
            Prometheus-powered monitoring for the Stateful Recovery pipeline
          </p>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          {metricsError ? 'Metrics Offline' : 'Monitoring'}
        </div>
      </header>

      <section className="metrics-summary">
        <div className="metric-card">
          <span>Events Processed</span>
          <strong>
            {formatMetricValue(eventsProcessed)}
          </strong>
        </div>

        <div className="metric-card">
          <span>Processing Lag</span>
          <strong>
            {processingLag !== null ? `${processingLag} seconds` : '--'}
          </strong>
        </div>

        <div className="metric-card">
          <span>Tracked Nodes</span>
          <strong>{Object.keys(nodeMetrics).length}</strong>
        </div>
      </section>

      <section className="dag-container">
     <ReactFlow
  nodes={nodes.map((node) => ({
    ...node,
    style: {
      border: node.id === bottleneckNode ? '3px solid red' : undefined,
      background: node.id === bottleneckNode ? '#fff1f2' : undefined,
    },
  }))}
  edges={edges}
  fitView
>
          <Background />
          <Controls />
          <MiniMap />
        </ReactFlow>
      </section>
    </div>
  )
}

export default App