# Architecture Diagram

```mermaid
flowchart LR
  request[User request] --> fastapi[FastAPI API and static UI]
  fastapi --> planner[Copilot planner]
  planner --> mockllm[Mock LLM provider]
  mockllm --> plan[Structured tool plan]
  plan --> router[Tool router]
  router --> graph[Mock Microsoft Graph client]
  router --> license[License advisor]
  router --> groups[Group advisor]
  router --> saas[Mock SaaS payload generator]
  router --> tickets[Ticket analyzer]
  router --> writer[Report writer]
  writer --> markdown[Markdown report]
  writer --> json[JSON report]
```
