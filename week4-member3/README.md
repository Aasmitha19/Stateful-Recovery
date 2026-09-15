# Week 4 Member 3 — Streaming DAG Monitoring Dashboard

## Overview

This project implements the Week 4 Member 3 "Refine & Polish" component
for the Stateful Recovery streaming pipeline.

The dashboard connects Prometheus metrics to a React Flow visualization
of the streaming DAG. It provides a visual overview of the pipeline and
helps identify the node with the highest processing lag.

## Architecture

The monitoring flow is:

Python Worker
    |
    v
Prometheus Metrics
    |
    v
Vite Proxy (/metrics)
    |
    v
React Dashboard
    |
    v
React Flow Streaming DAG

The main pipeline nodes displayed by the dashboard are:

1. Event Source
2. Stream Processor
3. Prometheus Metrics
4. Dashboard

## Dashboard Features

The Week 4 Member 3 dashboard provides:

- React Flow DAG visualization
- Prometheus metric integration
- Events processed metric
- Processing lag metric
- Number of tracked nodes
- Bottleneck detection
- Bottleneck node highlighting
- Node-level metric information
- Metrics loading state
- Metrics offline/error state
- Last successful metrics update time
- React Flow controls
- React Flow minimap
- Automatic metric refresh every 5 seconds

## Prometheus Metrics

The dashboard reads the following Prometheus metrics:

### events_processed_total

This metric represents the total number of events processed by the
Member 1 metrics worker.

### processing_lag

This metric represents the current processing lag reported by the
Member 1 metrics worker.

The dashboard retrieves these metrics through:

    /metrics

The Vite development server proxies this request to:

    http://localhost:8000/metrics

## Bottleneck Detection

The dashboard compares the processing lag associated with the tracked
nodes.

The node with the highest positive processing lag is considered the
current bottleneck.

When a bottleneck is detected:

- The bottleneck node is highlighted.
- The node displays a bottleneck status.
- The dashboard identifies the bottleneck in the summary metrics.

When no positive lag is detected, the dashboard reports:

    None detected

## Running the Dashboard

### Step 1 — Install dependencies

From the `week4-member3` directory:

    npm install

### Step 2 — Start the Prometheus metrics worker

From the repository root, run:

    python metrics_worker.py

The worker exposes Prometheus metrics on port 8000.

The metrics endpoint is:

    http://localhost:8000/metrics

### Step 3 — Start the React dashboard

From the `week4-member3` directory:

    npm run dev

Vite will display the local dashboard URL.

Open that URL in a browser.

## Production Build

To verify that the dashboard can be built for production:

    npm run build

A successful build ends with:

    ✓ built

## Git Branch

The Week 4 Member 3 work is developed on:

    week4-member3

The work is kept separate from the existing Week 3 Member 3 files.

## Current Metrics Limitation

The current Member 1 Prometheus implementation exposes global metrics:

    events_processed_total
    processing_lag

The metrics are not currently labelled with individual DAG node
identifiers.

Therefore, the dashboard demonstrates the node-level monitoring and
bottleneck visualization architecture, but true independent live
Prometheus measurements for every DAG node require node-specific
metrics or Prometheus labels.

The dashboard does not invent node-specific Prometheus values.
Instead, the currently available metrics are mapped to the relevant
monitoring stages while the limitation is clearly documented.

## Week 4 Member 3 Deliverable

The completed Member 3 component connects the Prometheus monitoring
layer with a React Flow streaming DAG dashboard.

It provides a visual monitoring interface that allows users to:

- Observe streaming pipeline metrics
- Monitor processing lag
- See the streaming DAG
- Understand the role of each monitoring stage
- Identify a detected bottleneck
- See when Prometheus metrics are unavailable

This completes the Week 4 Member 3 dashboard integration and polish
component.