# QuantHunt: Y2Q Network Kinematics Dataset

This repository contains the empirical dataset, simulation logs, and Python analysis scripts used in the research paper: **"Quantifying the MTU Fragmentation Penalty of Post-Quantum TLS Handshakes in Legacy Financial Networks: An Empirical Kinematics Analysis"** by Saksham Shreyans and Akul Attre (RGIPT).

## Overview
As the financial sector transitions to NIST's Post-Quantum Cryptography standards (ML-KEM and ML-DSA), the size of TLS 1.3 handshakes balloons to over 16.8 KB. This dataset measures the Time-To-First-Byte (TTFB) degradation caused by TCP MTU fragmentation and the $iw=10$ congestion window ceiling across 307 real-world financial domains.

## Repository Contents

### 1. Raw Dataset (`.csv` files)
The data consists of 923 successful empirical connections simulated across three network weather profiles:
* `fleet-simulation-scenario-a-fiber.csv`: 0.1% packet loss (Fiber/Broadband Backbone)
* `fleet-simulation-scenario-b-4g.csv`: 1.2% packet loss (Standard 4G Mobile RAN)
* `fleet-simulation-scenario-c-rural.csv`: 3.5% packet loss (Rural Edge Network)

**Data Dictionary (Column Definitions):**
* `domain`: The financial/e-commerce endpoint profiled.
* `baseline_rtt_ms`: The classical classical TLS 1.3 Round Trip Time.
* `pqc_ttfb_ms`: The simulated Time-To-First-Byte for a hybrid ML-DSA/ML-KEM payload.
* `extra_flights`: The number of forced TCP slow-start flights (Consistently 2 due to $iw=10$).
* `degradation_pct`: The percentage increase in latency versus the baseline.

### 2. Analysis & Visualization (`.py` and `.png`)
* `generate_graphs.py`: The Python script (using Pandas and Seaborn) used to calculate averages, percentiles, and generate the visualizations used in the paper.
* Included are the four high-resolution outputs: Grouped Bar Chart, IQR Box Plot, RTT Scatter Plot, and the QoS Cumulative Distribution Function (CDF).

## Reproducibility
To reproduce the graphs from the raw CSV data, simply run:
`python generate_graphs.py`
*(Requires pandas, matplotlib, and seaborn)*
