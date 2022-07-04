# Architecture

## Architecture Components

### Domain
The domain contains **models**, **events**, and **commands**.

**Domain modeling** is the process of abstracting reality
into models (entities), events, and commands that are triggered by those events. It is assumed that the domain can model
any real-world entity, thus being **complete**.

In an **event-driven system**, events define the information that can be received (*input messages*) and triggered
(*output messages*) by the system.

As in reality, events trigger **actions** or so-called *commands*. An event can trigger *one or a finite number* of
commands.

The triggered commands in turn define the **state changes** to the domain model of the system. Thus, a command execution
is required to change any model state.

### Message Bus
The **message bus** processes the incoming internal and external events and commands by routing them to relating
handlers. **Handler mappings** define the relationship between the **domain entity** (command or event) and the
implemented **handler (function)**.

The arguments (dependencies, e.g. UOW, adapters, etc.) of a *handler function* are injected using **signature
reflection**.

### Unit of Work (UOW)
A **unit of work (UOW)** is a stateful abstraction around data integrity. Each unit of work defines an atomic update to
the domain model.

The different states (e.g. commit, rollback) enforce data integrity and avoid inconsistency, especially in case of
errors.

### Adapters
**Adapters** define interfaces to communicate with external resources (e.g. third-party service,
databases, message broker, (email) notifications/messaging, file system, etc.).

#### Repository
A **repository** is an abstraction around persistent storage (e.g. database system). Each aggregate has its own
repository.

#### Message Broker
A **message broker** is an intermediary *message-oriented middleware* that enables asynchronous communication between 
clients. The clients can be **producers/publishers** or **consumers/subscribers** of messages.

The broker is responsible to receive, validate, process (ordering, filtering, queueing), and deliver the messages
(events).

As the broker acts as a decoupled, isolated middleware, producers and consumers do not necessarily need to know about
each other's existence. A broker summons a **star network topology**, reducing the overall **network complexity**,
supporting **scalability**, and **performance**. In the meantime, a broker introduces a highly system-critical component
that needs to ensure high resilience in the dimensions of **security**, **performance**, **scalability**, etc.

## Architecture Diagrams

### Overview
<img src='architecture.drawio.svg' alt='architecture' />

### (Package) Organization
<img src='architecture-organization.drawio.svg' alt='architecture-organization' />