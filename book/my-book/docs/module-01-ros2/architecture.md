---
title: "ROS 2 Architecture and Core Concepts"
sidebar_position: 2
---

## Learning Objectives
- Comprehend the distributed architecture of ROS 2 and its underlying principles.
- Understand the role and functionality of the Data Distribution Service (DDS) as ROS 2's middleware.
- Analyze the node-based computational graph model and its benefits for robotic system design.
- Explore Quality of Service (QoS) policies and their application in ROS 2 communication.

## The Distributed Architecture of ROS 2

ROS 2 is designed with a highly distributed and decentralized architecture, a fundamental departure from ROS 1's master-slave model. In ROS 1, a central `roscore` (the ROS Master) was responsible for managing all nodes, providing name registration, and looking up connections between publishers and subscribers. While simple for single-robot setups, this central point of failure and lack of native support for multi-robot scenarios posed significant challenges for robust and scalable deployments.

ROS 2 eliminates the `roscore` entirely. Instead, it leverages a sophisticated data-centric middleware, primarily the Data Distribution Service (DDS), to enable direct peer-to-peer communication between components. This means that nodes can discover each other and establish communication channels directly, without needing a central broker. This decentralized approach brings several crucial advantages:

-   **Increased Robustness:** The absence of a single point of failure makes ROS 2 systems more resilient to individual component failures.
-   **Enhanced Scalability:** It simplifies the deployment and management of large-scale robotic systems, including multi-robot fleets, by removing bottlenecks associated with a central master.
-   **Improved Real-time Performance:** DDS is optimized for low-latency, high-throughput data exchange, which is critical for real-time control loops in robotics.
-   **Better Security:** DDS provides built-in mechanisms for authentication, authorization, and encryption, allowing for secure communication in sensitive applications.
-   **Platform Agnosticism:** DDS implementations are available across a wide range of operating systems and hardware, making ROS 2 highly portable.

### Data Distribution Service (DDS) Middleware Explanation

DDS is an international standard developed by the Object Management Group (OMG) for real-time, peer-to-peer data exchange in distributed systems. It is the backbone of ROS 2's communication layer, handling everything from node discovery to message passing. DDS is designed for applications that require high-performance, predictable, and reliable data delivery, making it a natural fit for robotics.

At its core, DDS operates on a publish-subscribe model, similar to ROS 1 topics, but with significant enhancements. Key concepts in DDS include:

-   **Domain:** A logical grouping of DDS applications that can communicate with each other. ROS 2 typically uses a single DDS domain per system, identified by a domain ID.
-   **Topic:** A named stream of data, similar to ROS 1 topics. Publishers write data to topics, and subscribers read data from topics.
-   **DataWriter (Publisher):** An entity that sends data on a specific topic.
-   **DataReader (Subscriber):** An entity that receives data from a specific topic.
-   **Discovery:** DDS automatically discovers DataWriters and DataReaders within the same domain, allowing them to establish communication channels directly. This eliminates the need for a central registry.
-   **Quality of Service (QoS) Policies:** This is a powerful feature of DDS, allowing developers to specify the behavior of data communication, such as reliability, durability, and latency. ROS 2 exposes these policies to fine-tune communication for specific needs.

ROS 2 abstracts away much of the complexity of DDS, providing user-friendly APIs (like `rclcpp` for C++ and `rclpy` for Python) that allow developers to interact with the underlying middleware without needing deep DDS knowledge. This abstraction maintains the benefits of DDS while keeping the ROS 2 programming experience intuitive.

### Node-based Architecture

The node-based architecture is a fundamental concept inherited from ROS 1 and refined in ROS 2. A **node** is an executable process that performs computation. Nodes are typically designed to be modular and single-purpose, encapsulating specific functionalities of a robotic system.

Examples of nodes include:

-   A camera driver node that publishes image data.
-   A LiDAR sensor node that publishes point cloud data.
-   A navigation node that subscribes to sensor data and publishes robot commands.
-   A motor controller node that subscribes to commands and publishes motor status.
-   A user interface node that displays robot status and sends high-level commands.

The benefits of a node-based architecture are substantial:

-   **Modularity:** Each component of the robot (e.g., sensor driver, control algorithm, path planner) can be developed, debugged, and run independently.
-   **Reusability:** Nodes can be reused across different robotic projects or even within different parts of the same project.
-   **Fault Isolation:** If one node crashes, it typically does not bring down the entire system, as other nodes continue to operate independently.
-   **Concurrency:** Multiple nodes can run concurrently on the same or different machines, allowing for parallel processing and distributed computation.
-   **Language Agnostic:** Nodes can be written in different programming languages (e.g., Python, C++) and still communicate seamlessly.

### The Computational Graph Model

The computational graph in ROS 2 describes the network of ROS 2 nodes and their connections through topics, services, and actions. It's a conceptual map of how data flows and how different computational units interact to achieve the robot's overall behavior. Unlike ROS 1, where the graph was managed by `roscore`, in ROS 2, this graph emerges dynamically through the DDS discovery process.

Key elements of the computational graph:

-   **Nodes:** The computational entities.
-   **Topics:** Asynchronous, many-to-many communication channels for streaming data.
-   **Services:** Synchronous, request-response communication for direct interactions.
-   **Actions:** Long-running, goal-oriented communication for complex tasks with feedback.

Visualizing the computational graph helps developers understand the system's architecture, debug communication issues, and optimize data flow. Tools like `rqt_graph` (a graphical introspection tool) are used to visualize this dynamic graph, showing which nodes are active and how they are connected.

### Quality of Service (QoS) Policies

QoS policies are a cornerstone of ROS 2's communication flexibility, inherited from DDS. They allow developers to specify the desired behavior of communication channels, ensuring that data is delivered in a way that meets the application's requirements. Each publisher and subscriber can define its own QoS profile, and DDS will attempt to match compatible policies between them.

Some of the most commonly used QoS policies in ROS 2 include:

-   **Reliability:**
    -   `BEST_EFFORT`: Messages are sent without guarantee of delivery. Useful for high-frequency sensor data where missing a few samples is acceptable (e.g., camera images, LiDAR scans).
    -   `RELIABLE`: Messages are guaranteed to be delivered, even if retransmissions are required. Essential for critical data like robot commands or configuration parameters.

-   **Durability:**
    -   `VOLATILE`: Only messages published while a subscriber is active are received. No history is kept.
    -   `TRANSIENT_LOCAL`: Publishers retain a history of messages for new subscribers. When a new subscriber connects, it receives the latest (or a specified amount of) messages that were published before it joined. Useful for publishing maps or robot states that new nodes need upon startup.

-   **History:**
    -   `KEEP_LAST`: Only a certain number of the most recent messages are stored.
    -   `KEEP_ALL`: All messages are stored up to the history depth limit.

-   **Deadline:** Specifies the maximum expected time between consecutive messages. If a publisher fails to send messages within this deadline, it signals a communication problem.

-   **Liveliness:** Ensures that communication entities (nodes) are active. If a node fails to assert its liveliness within a certain period, others are notified.

By carefully configuring QoS policies, developers can optimize network usage, ensure data integrity, and guarantee timely delivery for different types of robotic data. For instance, a robot's motor commands might use `RELIABLE` and a small `KEEP_LAST` history, while a high-frequency camera feed might use `BEST_EFFORT` and `VOLATILE` to minimize latency and resource usage.

These core concepts – distributed architecture, DDS, nodes, the computational graph, and QoS policies – form the foundation of ROS 2, enabling the creation of advanced, robust, and scalable robotic applications.

## Key Takeaways
- ROS 2 features a decentralized, distributed architecture, eliminating ROS 1's `roscore` for enhanced robustness and scalability.
- Data Distribution Service (DDS) is the core middleware, facilitating peer-to-peer, real-time data exchange via a publish-subscribe model.
- Nodes are modular, single-purpose executable processes, forming the building blocks of a ROS 2 system.
- The computational graph dynamically represents the network of nodes and their communication pathways.
- Quality of Service (QoS) policies (e.g., Reliability, Durability) allow fine-tuning communication behavior for specific data requirements.

---

## Self-Assessment

Test your understanding of this chapter:

### Question 1
What is the primary advantage of ROS 2's decentralized architecture compared to ROS 1's master-slave model?

A) Easier debugging due to centralized logging.
B) Increased robustness and scalability by eliminating a single point of failure.
C) Reduced memory footprint on individual nodes.
D) Simpler initial setup for new users.

### Question 2
Which standard does ROS 2 use as its core communication middleware?

A) MQTT
B) AMQP
C) DDS (Data Distribution Service)
D) ZeroMQ

### Question 3
In ROS 2, what is a 'node'?

A) A central server that manages all robot communications.
B) A physical component of the robot, such as a motor.
C) An executable process that performs a specific computation.
D) A data structure used for message storage.

### Question 4
Which Quality of Service (QoS) policy would be most appropriate for high-frequency sensor data where occasional data loss is acceptable, to prioritize low latency?

A) `RELIABLE`
B) `TRANSIENT_LOCAL`
C) `BEST_EFFORT`
D) `KEEP_ALL`

### Question 5
What is the main purpose of the computational graph in ROS 2?

A) To provide a visual representation of the robot's hardware components.
B) To manage software dependencies between different programming languages.
C) To describe the network of ROS 2 nodes and their interconnections through communication mechanisms.
D) To perform real-time simulations of robot behavior.

<details>
<summary>Click to reveal answers</summary>

**Answer Key:**
1. **B** - The decentralized architecture removes the `roscore` (single point of failure), making ROS 2 systems more robust and scalable for complex and multi-robot deployments.
2. **C** - ROS 2 leverages the Data Distribution Service (DDS), an OMG standard for real-time, peer-to-peer data exchange, as its core communication middleware.
3. **C** - A node in ROS 2 is an executable process designed to perform a specific computational task, promoting modularity and reusability.
4. **C** - `BEST_EFFORT` reliability prioritizes latency over guaranteed delivery, making it suitable for high-frequency sensor data where missing some samples is not critical.
5. **C** - The computational graph conceptually maps how ROS 2 nodes interact and exchange data via topics, services, and actions, providing an overview of the system's runtime architecture.

**Scoring Guide:**
- 5/5: Excellent! You've mastered ROS 2 architecture and core concepts.
- 4/5: Great work! Review the missed concept.
- 3/5: Good start. Re-read the sections you struggled with.
- 2/5 or below: Recommended to review this chapter again.

</details>

---

## Next Steps

Continue to [Nodes, Topics, Services, and Actions](./nodes-topics-services.md)

---