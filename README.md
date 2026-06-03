# Crypto ETL Pipeline System

A real-time automated data engineering pipeline that collects cryptocurrency prices, processes and analyzes market movements, stores historical data, and triggers intelligent alerts via Discord.

This project demonstrates a production-style ETL architecture with scheduling, validation, persistence, and observability, built entirely in Python.

---

# Features
• Automated ETL pipeline (Extract → Transform → Load)
• Real-time cryptocurrency data ingestion (CoinGecko API)
• Data validation layer to ensure API integrity
• Market intelligence engine (trend, volatility, momentum analysis)
• Persistent storage using SQLite
• Smart alert system with cooldown protection
• Discord webhook notifications
• Scheduled execution every 5 minutes
• Retry logic with exponential backoff
• Structured logging system

---

# System Architecture
    Collector → Validator → Transformer → Trends Engine → Database → Alert System
                                 ↓
                     Scheduler (runs every 5 min)
    The system is designed as a modular ETL pipeline where each component is independent, testable, and replaceable.

---

# Tech Stack
• Python 3.x
• SQLite (local persistence)
• APScheduler (task scheduling)
• Requests (API communication)
• Discord Webhooks (notifications)
• Standard Library (threading, logging, datetime)

---

# 📁 Project Structure
crypto-pipeline/
│
├── app/
│   ├── collector.py
│   ├── validator.py
│   ├── transformer.py
│   ├── pipeline.py
│   ├── trends.py
│   ├── database.py
│   ├── scheduler.py
│   ├── monitor.py
│   ├── pipeline_launcher.py
│   └── config.py
│
├── data/
│   └── crypto.db
│
├── logs/
│   └── pipeline.log
│
├── launch.py
├── requirements.txt
└── README.md

---

# How It Works
## 1.  Data Collection
Fetches Bitcoin and Ethereum prices from CoinGecko API with retry and rate-limit handling.

## 2. Validation Layer
Ensures API responses are structurally valid before processing.

## 3. Transformation Layer
Normalizes raw API data into structured, database-ready records.

## 4. Processing & Intelligence
• Calculates price change percentage
• Detects market trend (UPTREND / DOWNTREND / SIDEWAYS)
• Computes volatility and momentum indicators

## 5. Persistence Layer
Stores historical price data and maintains alert state for cooldown control.

## 6. Scheduler
Runs pipeline every 5 minutes with concurrency protection to prevent overlapping executions.

## 7. Alert System
Triggers Discord notifications when:
• Price change ≥ 2%
• Cooldown period has passed

---

# Alert Logic
⚠️ALERT⚠️
BITCOIN moved +2.45%
Trend: UPTREND
Price: $66,000 → $67,600

---

# Market Intelligence Layer
The system computes:
• Trend detection (UPTREND / DOWNTREND / SIDEWAYS)
• Volatility (standard deviation of returns)
• Momentum (net directional movement)

---

# 🛠 Setup & Installation

```bash
 git clone https://github.com/your-username/crypto-pipeline.git
 cd crypto-pipeline
 pip install -r requirements.txt
 python launch.py
```

---

# Environment Setup
 Create a .env file:

 DISCORD_WEBHOOK_URL=your_webhook_url_here

# Use Cases
• Real-time crypto monitoring system
• ETL pipeline architecture template
• Backend automation project for portfolio
• Junior Python / Data Engineering showcase project

---

# Key Learnings
• ETL pipeline architecture design
• API reliability engineering (retry + rate limiting)
• Scheduler-based automation systems
• Data validation strategies
• Logging and observability design
• Lightweight financial data analytics

---

# Future Improvements
• Docker containerization
• PostgreSQL migration
• Web dashboard (FastAPI / Flask)
• Streaming architecture (Kafka)
• Cloud deployment (AWS / GCP)

---

# Author
Built as portfolio project for Junior Python Automation / Data Engineering roles

---

# Why this project matters
This project simulates a real-world automated data pipeline system, similar in structure to systems used in:
• fintech monitoring tools
• trading data pipelines
• real-time analytics services