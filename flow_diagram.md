# System Flow Diagram

```mermaid
graph TD
    UI[UI (Port 5000)] -->|Sends patient_id| Router[Router (Port 7000)]
    Router -->|Queries Database| Database[(Database)]
    Router -->|Determines Modality| Model[Model (Agent, Port 8000)]
    Model -->|Processes Data| Router
    Router -->|Sends Response| UI
```