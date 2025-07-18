# Subject: Job Opportunity: Solution Architect (Remote/WFH with Travel)

## Job description

    Job Title: Solution Architect

    Location: Remote/WFH and travel to Rahway, NJ (Expenses reimbursed by the client)

    Duration: 6 months+

     

    Description:

    Design and implement solutions using Scitara, BIOVIA (CisPro/OneLab), and Appian to solve business challenges.
    Collaborate with stakeholders to gather requirements and translate them into architectural designs.
    Lead system integration efforts to ensure seamless data flow between applications.
    Provide support and optimization for existing solutions, addressing issues and implementing enhancements.
    Stay updated on industry trends and recommend innovative solutions for improved performance.
     

    Qualifications:

    Bachelor’s degree in Computer Science, Information Technology, or a related field; Master’s preferred.
    At least 5 years of experience as a Solutions Architect, focusing on Scitara, BIOVIA, and Appian.
    Experience in regulated environments, particularly in life sciences or pharmaceuticals.
    Strong understanding of system integration and data management practices.

## Overview of Requirements

Scitara, BIOVIA, and Appian are widely used in the pharmaceutical industry to
streamline laboratory operations, ensure regulatory compliance, and enable
digital transformation:

- **Scitara**: Provides a digital connectivity platform that integrates
laboratory instruments, software, and data sources. It enables seamless data
exchange, workflow automation, and compliance with industry regulations,
supporting efficient laboratory operations and data integrity.

- **BIOVIA**: Offers scientific informatics solutions such as CisPro and
OneLab, which manage laboratory information, automate workflows, and ensure
traceability of samples and processes. BIOVIA helps pharmaceutical companies
maintain compliance, improve productivity, and accelerate research and
development.

- **Appian**: Delivers a low-code automation platform for building business
process applications. In pharmaceuticals, Appian is used to automate quality
management, regulatory submissions, and other critical workflows, enhancing
operational efficiency and supporting compliance initiatives.

## Details of each technology

### Scitara

Scitara is a digital connectivity platform designed specifically for laboratory
environments. It connects disparate laboratory instruments, software, and data
sources, enabling seamless and secure data exchange. In the pharmaceutical
industry, Scitara automates workflows, ensures data integrity, and supports
regulatory compliance by providing traceable and auditable data movement. This
integration accelerates laboratory processes, reduces manual errors, and
improves overall operational efficiency.

Scitara is a web-based digital connectivity platform designed specifically for
laboratory environments. It features a user-friendly interface with a moderate
learning curve, making it accessible to both IT professionals and laboratory
staff. Scitara enables integration of disparate laboratory instruments,
software, and data sources using standard protocols such as REST APIs, OPC, and
file-based connectors. The platform supports low-code configuration for
building and automating workflows, allowing users to design data flows and
integrations with minimal programming effort. Scitara ensures seamless and
secure data exchange, automates workflows, maintains data integrity, and
supports regulatory compliance by providing traceable and auditable data
movement. This integration accelerates laboratory processes, reduces manual
errors, and improves overall operational efficiency. 

#### Company site information

[Scitara Platform](https://scitara.com/platform/)

Microservice-based structure DLX uses a modular architecture to enable easy
scaling of individual components and high performance under varying user loads
and data volumes.

Deployed on kubernetes DLX’s application management platform enables stability
and rapid response to dynamic workloads.

Standard, secure communication protocols We use well-established best practices
for seamless integration without compromising data privacy or customization
settings.

Optimized processing and storage DLX combines the best of Kafka and MongoDB to
provide efficient real-time data processing and storage.


[Scitara Connectors](https://scitara.com/platform/connectors/)

Streaming Connectors

Enable real-time data streaming from bioreactors based on
industry standards like OPC DA and OPC UA, ensuring up-to-the-minute insights.

Instrument Connectors

Connect diverse instruments critical to bioprocessing,
including plate readers, cell counters, centrifuges, and more.

Application Connectors

Streamline connections with popular applications like
cytiva UNICORN™, Waters™ Empower, Thermo Scientific™ Chromeleon™, Shimadzu
LabSolutions™, Agilent OpenLab™, and Mettler-Toledo LabX™.

ELN & LIMS Connectors

Seamlessly connect widely used ELNs like Benchling, IDBS
Polar, and Revvity Signals, along with LIMS solutions such as LabVantage and
LabWare.

Data Lake Connectors 

Seamlessly connect to data lakes like Snowflake’s Data
Cloud™ and Amazon RedShift™ to optimize data storage and analysis.

Scitara connects to RS232 instruments using a combination of hardware and software components. A specialized IoT device, often a small box, interfaces with the instrument through the RS232 port and then connects to the Scitara DLX platform via the internet (either wired or WiFi). This allows the instrument to be treated as a connected resource within the Scitara ecosystem. 
Here's a more detailed breakdown:

1. Hardware Interface:

Scitara utilizes a small IoT device, typically around 2"x3"x1", that acts as a
bridge between the RS232 port of the instrument and the Scitara network. This
device handles the physical connection and potentially some initial data
processing. 

2. Software Configuration: . The IoT device is provisioned through the Scitara
   DLX platform, which involves configuring the device within the platform's
interface. This configuration step establishes the connection and defines how
the instrument's data will be handled. 

3. Connection to Scitara DLX: .

Once provisioned, the instrument is treated like any other connected lab
resource within the Scitara DLX platform. This means it can be integrated into
workflows, data management systems, and other aspects of the lab's digital
infrastructure. 

4. Data Mobility and Automation: .

Scitara DLX orchestrations can then be used to automate tasks, trigger
workflows, and move data between the instrument and other lab systems like
Electronic Lab Notebooks (ELNs) or data lakes. 

Solving the Puzzle: Scitara Connectors and the Science of ... In essence,
Scitara provides a pathway to integrate even older instruments with their
modern digital lab platform by leveraging IoT technology and specialized
connectors

Scitara uses Apache Kafka as a core component of its DLX (Digital Lab Exchange)
platform to facilitate real-time, scalable data streaming and integration
within laboratories . 

Here's how Scitara leverages Kafka:

Real-time Data Streaming: Scitara DLX enables the streaming of laboratory
data in real time, making it instantly available for analysis and supporting
faster decision-making. This is crucial in industries like pharmaceuticals and
life sciences where timely insights are vital for research and development.
Enhanced Connectivity and Integration: By leveraging Kafka's capabilities,
Scitara DLX provides seamless connectivity between various lab instruments,
software, and systems, including legacy and modern devices. This creates a
unified framework for data exchange, eliminating the need for complex
point-to-point integrations that often hinder data flow in traditional lab
setups. Data Lakes and Analytics: Scitara integrates Kafka with data
repositories like Snowflake, Databricks, and Redshift. This allows lab data to
be combined with other enterprise data sources, enabling comprehensive analyses
and the uncovering of hidden patterns and insights. Support for FAIR Data:
Scitara DLX helps ensure that scientific data adheres to FAIR principles
(Findable, Accessible, Interoperable, and Reusable), making it readily
available for advanced analytics and AI applications. Scalability and
Performance: Kafka's architecture allows Scitara DLX to handle the growing
volume and velocity of data generated in modern laboratories, ensuring that the
platform remains scalable and performant even as data loads increase. 

In essence, Scitara harnesses Kafka to build a robust, event-driven
architecture that revolutionizes laboratory data management by enabling
real-time data flow, enhancing connectivity, supporting advanced analytics, and
streamlining laboratory workflows. 

### BIOVIA

BIOVIA provides a suite of scientific informatics solutions, including CisPro
and OneLab, tailored for laboratory management in the pharmaceutical sector.
BIOVIA CisPro manages chemical inventory and regulatory compliance, while
OneLab automates laboratory workflows and ensures sample traceability. These
tools help pharmaceutical companies maintain accurate records, streamline
research and development, and meet stringent regulatory requirements. BIOVIA’s
solutions enhance productivity, support collaboration, and facilitate
data-driven decision-making.

#### Video tutorials
[Pipeline Piplot Tutorials](https://www.3ds.com/products/biovia/training/pipeline-pilot?_gl=1*1en1jsn*_up*MQ..*_ga*MTM3MDY2NzUxNS4xNzUyNjY3MzE3*_ga_TPGKGE8GTG*czE3NTI2NjczMTckbzEkZzAkdDE3NTI2NjczMTckajYwJGwwJGgw*_ga_DYJDKXYEZ4*czE3NTI2NjczMTckbzEkZzAkdDE3NTI2NjczMTckajYwJGwwJGgw*_ga_39DKQ0LYW1*czE3NTI2NjczMTckbzEkZzEkdDE3NTI2NjczMTckajYwJGwwJGgw)


### Appian

Appian is a low-code automation platform that enables rapid development of business process applications. In the pharmaceutical industry, Appian is used to automate complex workflows such as quality management, regulatory submissions, and clinical trial processes. The platform’s flexibility allows organizations to adapt quickly to changing regulations and business needs. Appian improves operational efficiency, ensures compliance, and provides real-time visibility into critical business processes, supporting continuous improvement and innovation.

#### Created an Appian Community Edition Account

#### Youtube Videos

[Appian Overview](https://www.youtube.com/watch?v=8b1k2g3a4eY)

- Role based permissions
- Data Fabric: A unified data platform that connects and integrates data from
    various sources, enabling real-time insights and analytics (syncs data). Uses
     JDBC Tomcat Server to connect to databases.
- Forms to create schemas and data types
- UI to define CRUD operations
- UI / UX to create user interfaces


[Appian Environments](https://www.youtube.com/watch?v=P_F0ozMljes)

APPian environments are isolated instances of the Appian platform that can be
used for development, testing, and production purposes. Each environment has its
own set of applications, data, and configurations, allowing organizations to
manage their Appian applications in a controlled manner.

Appian environments can be created and managed through the Appian
Administration Console, which provides tools for configuring environment
settings, managing users, and monitoring application performance. Environments
can be deployed to different regions or cloud providers, enabling organizations
to choose the best infrastructure for their needs.

Create service accounts and API keys for secure connections between Appian
environments and external systems.

[DocSense and Prompt Engineering](https://www.youtube.com/watch?v=n_9gj4A8R0Y)

- Can be used to parse documents with a detailed prompt (using JSON)

[AIDocument Center](https://www.youtube.com/watch?v=wuIHN_3uOss)

- Form fields to guide AI assistant in extracting relevant information
- Would be better to use structured documents - create the document from
    database fields

#### Video to build full Appian Application [Appian App](https://www.youtube.com/watch?v=LvhRbnFvXy8)

- A unified data platform that connects and integrates data from various
    sources, enabling real-time insights and analytics.
- Has a data sync (like Dremeo)
- Applied data governance and security policies to ensure data integrity and
    compliance.
- Has a notification system to alert users of data changes or issues.
- When creating UI to display data, has interface that generates the underlying 
    React Props

#### Kafka Integration
In Appian, Kafka is primarily used as a high-throughput, low-latency messaging
system for internal communication and for building real-time streaming data
pipelines. It acts as a distributed message broker, facilitating the reliable
exchange of data between different components of the Appian platform. 

Here's a more detailed breakdown:
1. Internal Messaging Service:

    Appian utilizes Kafka as the foundation for its Internal Messaging Service,
    which relays data between various Appian components. 

This service leverages Kafka's publish-subscribe messaging pattern to enable
asynchronous communication. Kafka's transaction log functionality is also used
by Appian's engines and data service, ensuring data consistency and
reliability. 

2. Real-time Streaming Data Pipelines:

    Appian is developing a native integration with Kafka to enable users to
    build real-time streaming data pipelines. This integration allows users to
    automatically trigger Appian processes upon the arrival of new messages
    from Kafka topics. Future enhancements will include synchronizing record
    types and supporting other use cases related to real-time data processing. 

3. Other Use Cases:

    Kafka Tools, an Appian plugin, allows users to publish to and consume from Kafka topics. 

Users can leverage Kafka as a message queue for asynchronous communication
between Appian and other systems. Appian can act as a producer or consumer of
Kafka messages, enabling various integration scenarios. 

In essence, Kafka plays a crucial role in Appian's architecture by providing a
robust and scalable foundation for internal messaging, real-time data
processing, and integrations with other systems. 

[beta program](https://field-marketing.appianportals.com/event?survey=kafka-integration-beta-program%2FFN07)

#### Questions & Observations

- Who is the user base for building the Appian application?
- What is the skill level of Appian developers?

- Appian Uses ReactJS for UI development (Needs SSO integration)
[Appian ReactJS](https://sangeerththanbalachandran.hashnode.dev/build-a-website-with-appian-and-react)
- Appian uses Java as the backend language.
- Appian can integrate custom websites using iframes (Could be browser issues)
- Does not support WebSockets for real-time updates

- Limited CI/CD capabilities in Appian
- No Unit Testing framework

## Generate Workflow

### Solution 1: Appian-Centric Orchestration with Scitara Integration

- **UI & Workflow Initiation:**  
  Use Appian to build a user-friendly web interface for workflow initiation. Appian’s low-code platform enables rapid UI development, user authentication, and audit logging (who/when).
- **Tracking:**  
  Appian natively tracks user actions and timestamps. Store workflow initiation metadata in Appian’s Data Fabric or an external database.
- **Instrument Control & Data Gathering:**  
  Integrate Appian with Scitara via REST APIs or connectors. Appian triggers Scitara workflows to start instruments and collect data.
- **Data Aggregation & Storage:**  
  Scitara aggregates instrument data and pushes it to BIOVIA OneLab for further processing/storage. Appian can poll or subscribe to updates.
- **UI Updates & Notifications:**  
  Appian UI updates in real-time (via polling or refresh). Appian triggers subsequent workflows or sends notifications (email, in-app) based on data or workflow status.

---

### Solution 2: Scitara-Led Integration with Appian UI

- **UI & Workflow Initiation:**  
  Appian provides the UI for workflow initiation and user tracking.
- **Workflow Orchestration:**  
  Appian calls Scitara’s APIs to initiate a workflow. Scitara manages instrument orchestration, data collection, and aggregation.
- **Data Storage:**  
  Scitara pushes aggregated data to BIOVIA OneLab or a dedicated data lake.
- **Feedback Loop:**  
  Scitara notifies Appian (via webhook or API callback) when data is ready or workflow completes.
- **UI Updates & Next Steps:**  
  Appian updates the UI, displays results, and allows users to trigger follow-up workflows or receive notifications.

---

### Solution 3: BIOVIA OneLab as Data Hub, Appian as Orchestrator

- **UI & Workflow Initiation:**  
  Appian UI initiates workflows and records user/timestamp.
- **Workflow Orchestration:**  
  Appian triggers Scitara to start instruments and collect data.
- **Data Aggregation:**  
  Scitara sends raw data to BIOVIA OneLab, which aggregates, filters, and stores it.
- **Data Retrieval & UI Update:**  
  Appian queries BIOVIA OneLab for processed data and updates the UI.
- **Subsequent Actions:**  
  Appian triggers additional workflows or notifications based on data from OneLab.

**All solutions ensure:**
- User actions are tracked (who/when).
- Data integrity and compliance via audit trails.
- Modular integration using APIs and connectors.
- Extensibility for future workflow automation.

### Key Differences Between Solutions

- **Solution 1: Appian-Centric Orchestration**
  - Appian is the primary orchestrator and user interface.
  - All workflow initiation, tracking, and user interaction are managed in Appian.
  - Scitara acts as a backend integration layer for instrument control and data collection.
  - BIOVIA OneLab is used mainly for data storage and further processing.
  - Best when you want a unified UI and centralized workflow logic in Appian.

- **Solution 2: Scitara-Led Integration**
  - Appian provides the UI, but Scitara manages the orchestration and workflow logic.
  - Scitara is responsible for starting instruments, aggregating data, and notifying Appian when workflows complete.
  - BIOVIA OneLab is used for data storage, but Scitara controls when and how data is pushed.
  - Best when instrument/data orchestration is complex and best handled by Scitara’s native capabilities.

- **Solution 3: BIOVIA OneLab as Data Hub**
  - Appian initiates workflows and tracks users, but BIOVIA OneLab is the central data aggregation and processing hub.
  - Scitara is used for instrument control and raw data collection, but all aggregation/filtering happens in OneLab.
  - Appian retrieves processed data from OneLab and updates the UI or triggers further actions.
  - Best when data processing, filtering, and compliance are critical and best managed in OneLab.

Each solution shifts the center of orchestration and data management to a different platform, depending on organizational priorities, integration complexity, and compliance needs.

## Possible interview questions
