---
description: Book chapter comparing REST, webhooks, GraphQL, SOAP, WebSockets and gRPC with adoption numbers and when each architecture fits.
domain: backend
type: book
status: digested
tags:
  - domain/backend
  - type/book
  - status/digested
  - topic/api-design
  - topic/grpc
  - topic/http-and-networking
aliases:
  - Ch2. Selecting Your API  Architecture
  - REST vs GraphQL vs gRPC
hubs:
  - "[[API Design]]"
  - "[[gRPC]]"
  - "[[HTTP & Networking]]"
---
- REST: 86% 
- Webhooks: 36% 
- GraphQL: 29% 
- Simple Object Access Protocol (SOAP): 26% 
- WebSockets: 25% 
- gRPC: 11%

REST (Representational State Transfer)
API providers make resources available at individual addresses (e.g., /customers, /products, etc.). Consumers make requests to these resources using standard HTTP verbs. Producers provide a response. This is the client/server model. The response is defined by the producer. The standard structure of the response is the same for each consumer. The REST response is typically in JSON or, sometimes, XML format, both of which are standard text-based data transfer formats. The interaction is stateless, which means that each message back and forth stands on its own. So, in a conversation of multiple requests and responses, each request has to provide information or context from previous responses. For example, a consumer might retrieve a list of players and then provide one player’s ID to request additional details.

Graph Query Language (GraphQL)
both a query language for APIs and a query runtime engine.

- Communication uses the client/server model (like RESTful APIs). 
- Communication is stateless (like RESTful APIs). 
- The response is usually in JSON (like RESTful APIs).
- Instead of only using HTTP verbs, the consumer uses the GraphQL query language.
- The consumer can specify the contents of the response, along with the query options. (In REST, the producer defines the response contents.)
- The producer makes the API available at a single address (e.g., /graphql), and the consumer passes queries to it via the HTTP POST verb.
- Versioning is not recommended, because the consumer defines the contents they are requesting

A big advantage of GraphQL over RESTful APIs is that fewer API calls are needed for the consumer to get the information they need. This requires less network traffic.

### gRPC
gRPC was developed for very fast, efficient communication between microservices.

gRPC is usually used for a different set of problems than REST, and it has many differences:
- Instead of sharing resources, gRPC provides remote procedure calls, which are more like traditional code functions
- Instead of being limited to stateless request-response patterns, gRPC can be used for continuous streaming.
- Instead of returning data in a text-based format like JSON, it uses protocol buffers, which is a format for serializing data that is smaller and faster than JSON or XML.

gRPC is not a likely candidate for the APIs that you will be creating in your portfolio project. However, it’s worth mentioning in this discussion of API architectural styles related to data science for one big reason: large language models (LLMs). These machine learning models are the engines behind generative AI services such as Gemini and ChatGPT. These are very big models that need all the performance they can get, and they are using gRPC in some cases to achieve this.