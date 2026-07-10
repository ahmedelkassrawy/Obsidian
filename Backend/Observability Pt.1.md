## Why Observability?

- Many developers (backend, sysadmins, DevOps) are expected to monitor features but don’t know how.
- You build a feature (e.g., file export) – how many succeeded/failed? Can you track it with numbers?
- Often companies have dashboards (e.g., Grafana) but people don’t understand them or how to build effective ones.
- Goal: empower developers to build their own dashboards, gain confidence in their features, and provide meaningful metrics to the company.

---

## The Running Analogy (Health Check)

A person wants to improve cardiovascular health in 3 months.  
They research and decide: **Zone 2 training** (steady-state cardio, constant pace for 60 min, 4 days/week).

They buy an Apple Watch Ultra to measure pace (7.5 km/h).  
After 3 weeks:
- Watch shows pace is perfect → all green.
- But they feel exhausted, sleep quality is poor.

**Key lesson:**  
> If the user is not happy, no metric matters.

### What went wrong?
- They focused only on one metric (pace) – too narrow.
- Ignored other factors: sleep quality, hydration, nutrition, technique, phone distractions.

### The fix – add more signals:
- Sleep quality (1–10 scale)
- Daily water intake (liters)
- Self-assessed technique (breathing, posture)

After adjusting (hydration, no phone, better pillow), health improved within two weeks.

**Takeaway for systems:**
- Invest in understanding your system’s internals (e.g., reference counting in Python, WAL files in Postgres).
- Design meaningful metrics: **primary** (directly show the problem) and **secondary** (help narrow down).
- Don’t just rely on default dashboards – build what you actually need.

---

## Foundational Concepts

### The Four Golden Signals (Google SRE)
1. **Traffic** – How many requests per second?
2. **Latency** – Time to serve each request (p95, p99).
3. **Errors** – Rate of failed requests (e.g., HTTP 500s).
4. **Saturation** – How “full” is the system? (e.g., database connections, CPU, memory).

### Three Pillars of Observability
- **Logs** – Discrete events with timestamp and message.
- **Metrics** – Numerical measurements over time (counters, gauges, histograms).
- **Traces** – End-to-end request path across services (spans, trace IDs).

### Correlation
- Ability to jump from a log to a trace, from a trace to metrics, etc.
- Essential for root cause analysis.
- Achieved via **context propagation** (trace ID, span ID passed between services).

---

## Practical Example: Dice Game

**Game rules:**  
Roll a die 4 times. If any roll = 1 → lose (HTTP 400). Else → win (HTTP 200).

**Simulated load:**  
5 workers × 50 req/sec × 120 seconds = 30,000 requests.

### Dashboard Analysis
- **Success rate:** ~48% – matches probability (5/6)^4 = 48.2%.
- **Availability:** 100% – no 500 errors.
- **Latency:** p95 = 4.75 ms, p99 = 4.95 ms.
- **Traffic:** 250 req/sec total, split 125 success / 125 failure.

**Custom metric:** Frequency of each die face – all ~17% (fair die).  
If one face appears more often → random function might be biased.

### Traces in Action
- Each request is a **trace** containing 4 **spans** (one per roll).
- Spans have attributes: roll number, result, error flag.
- Trace view shows where failure occurred (e.g., roll #3 got a 1).

**Context propagation:**  
Trace ID and span ID passed from client → backend → database → back.  
Allows linking logs and traces.

### Logs ↔ Traces Correlation
- Click on a failing trace → view all logs belonging to that trace.
- From a log → find its trace and see the full journey.

---

## Instrumentation Types

### Automatic Instrumentation
- Provided by libraries/frameworks out of the box (e.g., Django logs requests/responses, Apple Watch measures heart rate).
- Good starting point, but often insufficient.

### Manual Instrumentation
- You add custom logs, metrics, and spans for the parts you care about.
- Example: adding a log when a die roll fails, or a counter for each HTTP status code.

### Profiling
- Used for resource-heavy code (memory leaks, CPU hotspots).
- Tools: flame graphs, memory profilers.

---

## Metrics Types (Prometheus/VictoriaMetrics style)

| Type       | Behavior                    | Example                          |
|------------|-----------------------------|----------------------------------|
| Counter    | Only increases              | Total requests, total errors     |
| Gauge      | Goes up and down            | Current memory usage, active requests |
| Histogram  | Samples into buckets        | Request latency buckets (≤100ms, ≤200ms, etc.) |

**Example – active requests gauge:**  
Increment on request received, decrement on response sent. Shows real-time concurrency.

---

## Logging Levels

- **DEBUG** – Detailed diagnostics (parameters, state).
- **INFO** – Normal events (request received, job completed).
- **WARN** – Unexpected but non-fatal (e.g., retry needed).
- **ERROR** – Operation failed but service continues.
- **CRITICAL** – Service cannot function.

Adjust log level at runtime to debug without redeploy.

---

## OpenTelemetry (OTel)

- **Unified standard** for logs, metrics, and traces.
- Spans are created via SDK (e.g., `trace.Span`, `span.Start()`).
- **Context propagation** automatically injects trace headers across HTTP/gRPC.
- Components:
  - **OTel SDK** – Instrument your code.
  - **OTel Collector** – Receives telemetry, processes, exports.
  - **OTel Protocol (OTLP)** – Wire protocol.

### Why OpenTelemetry?
- Language‑agnostic (Java, Go, Python, Node, etc.).
- Avoids vendor lock‑in.
- Replaces mixing different agents (Jaeger, Prometheus, Elastic).

---

## Common Tools (Observability Stack)

| Purpose       | Tools                                                                                                                                     |
|---------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| Log storage   | Loki, Elasticsearch, VictoriaLogs, Quickwit                                                                                               |
| Metrics       | Prometheus, VictoriaMetrics, Mimir, Thanos                                                                                                |
| Traces        | Tempo, Jaeger, VictoriaTraces                                                                                                             |
| Visualization | Grafana (unified dashboards)                                                                                                              |

**Why separate stores?**  
Each data type has different access patterns. Logs need text search, metrics need high‑frequency time‑series, traces need high‑cardinality indexing. Using one store for everything (e.g., Elasticsearch) leads to high cost and maintenance.

**Loki’s approach:**  
Index only **labels** (service name, pod, etc.), not log content. Makes log storage cheap and fast for filtering.

---

## Best Practices & Tips

1. **Start small** – Instrument your most critical feature first. Don’t boil the ocean.
2. **Instrument during development** – Not after the incident. Add observability as you write code.
3. **Use correlation** – Trace IDs in logs, metric labels linking to traces.
4. **Design good dashboards** – Avoid “wall of graphs”. Focus on primary metrics first, then secondary.
5. **Understand cardinality** – Don’t put user IDs or high‑cardinality values as labels in metrics (blows up storage). Use traces for that.
6. **Alert on symptoms, not causes** – Alert when user experience degrades (high latency, errors), then use traces to find cause.

---

## What’s Next in the Series (Upcoming Episodes)

- Deep dive into **logs** (handlers, filters, structured logging).
- Deep dive into **metrics** (PromQL, aggregation, recording rules).
- Deep dive into **traces** (sampling, tail‑based sampling, span events).
- **OpenTelemetry** collector configuration and deployment.
- **Grafana** dashboards from scratch.
- **Profiling** in production (Pyroscope, Parca).
- Real‑world use cases:
  - Postgres replication lag monitoring.
  - Shadow deployment observability.
  - Client‑side (web/mobile) metrics.
  - Cost/performance comparison of different backends.

---

## Key Quotes

> “If the user is not happy, no metric matters.”  
> “The best time to instrument is **while** you build the feature.”  
> “Observability is a **unique experience** for every system – you have to understand your own architecture.”