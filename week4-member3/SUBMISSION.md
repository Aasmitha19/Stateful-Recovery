# Week 4 Member 3 — Final Submission

## Completed Work

The Week 4 Member 3 dashboard provides a React Flow visualization of
the Stateful Recovery streaming pipeline and connects the dashboard
to Prometheus metrics exposed by the Python monitoring worker.

## Implemented Features

- React Flow streaming DAG
- Prometheus `/metrics` integration
- Events processed monitoring
- Processing lag monitoring
- Tracked node information
- Bottleneck detection logic
- Bottleneck node highlighting
- Node-level metric visualization
- Loading state
- Metrics offline/error state
- Last successful metrics update
- Automatic metrics refresh
- React Flow controls
- React Flow minimap

## Data Flow

Python Metrics Worker
        |
        v
Prometheus Metrics
        |
        v
Vite `/metrics` Proxy
        |
        v
React Dashboard
        |
        v
React Flow DAG

## Verification

The production dashboard build was verified using:

    npm run build

The build completed successfully.

The Prometheus endpoint used by the dashboard is:

    http://localhost:8000/metrics

## Running the Project

Start the metrics worker from the repository root:

    python metrics_worker.py

Then start the dashboard from this directory:

    npm run dev

The Vite development server displays the local dashboard URL.

## Bottleneck Monitoring

The dashboard evaluates processing lag and identifies the node with
the highest positive lag as the detected bottleneck.

A detected bottleneck is visually highlighted in the React Flow DAG.

When no positive lag is detected, the dashboard displays:

    None detected

## Current Limitation

The current Prometheus worker exposes global metrics rather than
independent metrics labelled for every DAG node.

Therefore, the dashboard demonstrates the node-level monitoring and
bottleneck visualization architecture using the currently available
metrics.

True independent live measurements for every DAG node would require
node-specific Prometheus metrics or labels.

## Final Status

Week 4 Member 3 dashboard integration, monitoring visualization,
bottleneck presentation, and project documentation are complete.