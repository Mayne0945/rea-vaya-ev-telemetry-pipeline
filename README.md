# ⚡ Production-Ready EV Fleet Telemetry Pipeline

### 🚀 The Business Problem
Fleet operators lack real-time visibility into battery health and driver behavior, leading to preventable failures and inefficient routing. Traditional batch processing is too slow (15+ min latency) for critical alerts like thermal runaway or rapid discharge.

### 🛠 The Solution
A scalable, serverless IoT pipeline on AWS that ingests, processes, and visualizes high-frequency vehicle telemetry with **sub-minute latency**, utilizing a **Medallion Architecture** for cost-efficient analytics.

### 🏗 Architecture

```mermaid
graph LR
    subgraph "Edge (Vehicle)"
        V[EV Sensor Node] -->|MQTT| IOT[AWS IoT Core]
    end

    subgraph "Ingestion"
        IOT -->|Rule| FH[Kinesis Firehose]
        FH -->|Raw JSON| S3_B[("S3 Bronze")]
    end

    subgraph "Medallion Processing"
        S3_B -->|ETL Transformation| S3_S[("S3 Silver (Parquet)")]
        S3_S -->|Crawler| G[AWS Glue Data Catalog]
    end

    subgraph "Analytics & Viz"
        G -->|Schema| ATH[Amazon Athena]
        ATH -->|SQL Query| GRAF[Grafana Dashboard]
        GRAF -->|Alerts| USR[Fleet Manager]
    end

    style V fill:#f9f,stroke:#333,stroke-width:2px
    style IOT fill:#ff9900,stroke:#333,stroke-width:2px
    style FH fill:#ff9900,stroke:#333,stroke-width:2px
    style S3_B fill:#232f3e,stroke:#fff,stroke-width:2px,color:#fff
    style S3_S fill:#232f3e,stroke:#00ff00,stroke-width:2px,color:#fff
    style G fill:#232f3e,stroke:#fff,stroke-width:2px,color:#fff
    style ATH fill:#232f3e,stroke:#fff,stroke-width:2px,color:#fff
    style GRAF fill:#fff,stroke:#333,stroke-width:2px
```

🧠 ###Key Engineering Decisions
Why Kinesis Firehose? Chosen over Kinesis Data Streams to handle batching (60s buffer) automatically, reducing S3 PUT costs and avoiding the "small file problem."

Why Parquet (Silver Layer)? Converting raw JSON to Parquet reduced Athena query scan size by ~90%, significantly lowering query latency and cost.

Why Serverless? Eliminated idle compute costs by using AWS IoT Core and Athena instead of provisioning EC2 instances or Kafka clusters.

💰 ###Cost & Scalability Strategy
Partitioning: Data is partitioned by time (Year/Month/Day) to limit query scope.

Storage Tiers: Lifecycle policies configured to move Bronze data to Glacier after 30 days.

On-Demand: The entire infrastructure scales to zero when no vehicles are active.

📊 ###Performance Metrics
Ingestion Latency: < 200ms (Edge to Cloud).

End-to-End Latency: ~60 seconds (Sensor to Dashboard).

Throughput: Tested at 50+ records/second.

🎥 ###Demo
(Link your video here later)
[Watch the Demo](LINK_TO_VIDEO)

🧪 ###Simulation Setup
The sentinel_active_node.py script acts as a digital twin, generating realistic telemetry:

Engine RPM: Randomly fluctuates based on throttle position.

Battery Temp: gradually increases with load (simulating thermal stress).

Location: Lat/Long coordinates for route mapping.

💻 ###How to Run
Clone the repo:

Bash
git clone [https://github.com/Mayne0945/ev-telemetry-pipeline.git](https://github.com/Mayne0945/ev-telemetry-pipeline.git)
Install dependencies:

Bash
pip install -r requirements.txt
Run the producer:

Bash
python sentinel_active_node.py
Built with Python, AWS IoT Core, Kinesis Firehose, S3, Glue, Athena, and Grafana.