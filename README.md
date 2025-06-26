# SmartGarageMonitor
# 🚗 Smart Parking Monitoring System with Python, Prometheus, and Grafana

This project simulates a smart garage monitoring system using Python, Prometheus, and Grafana. It exposes custom metrics that reflect the state of a parking lot in real-time, and provides alerting when the garage reaches full capacity.

## 🔧 Project Overview

The system simulates a garage with a total capacity of **50 parking spots**. Cars randomly enter and leave the garage. For each vehicle entry, the system randomly assigns:

- **Car Color** (`red`, `blue`, `black`, etc.)
- **Car Type** (`sedan`, `suv`, `truck`, etc.)
- **Parking Spot** (e.g., `spot_1`, `spot_2`, ..., `spot_50`)

These details are then exposed as Prometheus metrics with detailed labels.

## 📈 Prometheus Metrics

The following metrics are defined and served via an HTTP endpoint on port `8000`:

- `garage_total_cars_entered{color, type, spot}`  
  → Counter metric showing all vehicles that have ever entered the garage.

- `garage_current_cars{color, type, spot}`  
  → Gauge metric indicating cars currently in the garage.

- `garage_available_spots`  
  → Gauge metric showing how many spots are still available.

## 🔁 System Behavior

- Every few seconds, a new car may enter the garage (70% chance).
- Cars that have stayed for more than **3 minutes** (simulation of 30 days) are removed.
- Metrics are continuously updated and served via Prometheus client.

## 📊 Visualization and Alerting

- **Prometheus** is configured to scrape metrics from `localhost:8000`.
- **Grafana** is used to visualize car activity, availability, and trends over time.
- An **email alert** is configured in Grafana to notify when the garage reaches full capacity.

## 🛠 Tech Stack

- **Python**: Metric generation and data simulation.
- **prometheus_client**: Used to expose metrics via HTTP.
- **Prometheus**: Scrapes and stores the time series data.
- **Grafana**: Visualizes the metrics and handles alerting.

## 📌 Future Enhancements

- Integrate persistent storage or database support.
- Replace random generation with real-time sensor or camera input.
- Add support for multiple garage zones or locations.
