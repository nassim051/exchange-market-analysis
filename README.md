# Exchange Market Analysis – Modular Time Series Analysis Framework

This personal project is a modular framework designed for analyzing temporal fluctuations across multiple real-time exchange platforms. It supports large-scale pattern detection, volatility segmentation, and volume-based signal extraction in multi-source environments.

## Objective

The goal is to study fluctuations and temporal waveforms in financial time series (price and volume) by building an architecture that supports:

- High-frequency data acquisition from heterogeneous exchange APIs
- Volatility and wave detection based on configurable amplitude and moving average parameters
- Volume anomaly detection across all listed assets on a platform
- Multi-processing and multi-threaded execution for efficient analysis

A backtesting component (in development, see `src/interface/Trade/Backtester/backtest_runner.py`) is being integrated to simulate and evaluate strategy performance on historical data.

## Technical Focus

- Modularity and extensibility of analysis components
- Multi-threaded execution and parallelism
- Knowledge encapsulation per exchange (Binance, LBank, Gate.io, etc.)
- CLI-based human-in-the-loop parameterization (amplitude, time frame, MA period…)

## Architecture

project/
│
├── main.py # CLI interface to launch analysis workflows
├── src/
│ ├── exchange/ # Individual logic for each exchange
│ ├── interface/Trade/Backtester/
│ │ └── backtest_runner.py # Backtesting module (WIP)
│ ├── Telegram/ # Notification component
│ └── db/ # Database interface for results storage

## Current Features

- Volume anomaly detection (per pair or globally)
- Waveform analysis (volatility-based)
- Real-time analysis via WebSocket (in selected modules)
- Extensible exchange support
- Data persistence and Telegram alerting

## In Progress

- Integration of historical backtesting for strategy prototyping
- Interface abstraction to simplify external strategy injection
- Unified reporting module (e.g., graphs, metrics)

## Technologies Used

- Python 3
- `ccxt`, `sqlite`, `pandas`, `numpy`
- Multiprocessing, threading
- Modular custom CLI system

## Note

This project was initiated for personal learning and architectural experimentation purposes in the context of real-time data analysis. It is not intended for financial speculation.
