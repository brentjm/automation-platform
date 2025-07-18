# Automation Platform

The goal of this project is to create an automation platform that
can be used in home, laboratory, office and manufacturing environments. The platform should be easily set up and run and rely on local
services for data privacy.

## Overview

- Proxmox as base system
- VMs and containers for services
    - PostgreSQL for data storage
    - InfluxDB for time series data
    - Grafana for visualization
    - Node-RED for device data normalization
    - Node-RED for automation
    - Traefik for reverse proxy
    - Telegraf for data collection
    - n8n for system automation
    - Home Assistant for home automation
    - Protocols
        - MQTT for device communication
        - HTTP for web services
        - WebSocket for real-time communication
        - OPC UA for industrial automation
    - Docker for custom web applications
        - specific physics models

## Set up

Ansible playbooks for deployment. The Ansible playbook
should be broken into roles that can be used to set up
services for different use cases.


## Business model

- Open source software
- Free to use
- Paid support and consulting
- Paid custom development
- Paid training and workshops


## Create blog posts to compare to existing solutions


- demonstrate digital twins
- demonstrate a computer vision application
- basic ASAP application

## FAIR

The FAIR Data Principles are a set of guidelines designed to make research data
more findable, accessible, interoperable, and reusable (hence the acronym
FAIR). These principles aim to improve the sharing and reuse of research data,
ultimately accelerating scientific discovery. Here's a breakdown of each
principle: 

    Findable:

    Data should be easy to find, both for humans and machines. This involves using
    globally unique and persistent identifiers, rich metadata, and registering data
    in a searchable resource.

    Accessible:

    Data should be retrievable by their identifier using a standardized
    communication protocol, and metadata should remain accessible even when the
    data is no longer available.

    Interoperable:

    Data should be represented in a format that allows for integration with other
    data and analysis tools. This includes using formal, accessible, shared, and
    broadly applicable languages for knowledge representation, and vocabularies
    that follow the FAIR principles.

    Reusable:

    Data should be released with clear usage licenses and detailed provenance
    information. They should also meet domain-relevant community standards and be
    richly described with accurate and relevant attributes.

## Data Fabric

[IBM Data Fabric](https://www.ibm.com/cloud/data-fabric)
A data fabric is an architecture that provides a unified and consistent way to
manage, integrate, and access data across various sources and environments. It
aims to simplify data management by creating a seamless layer that connects
disparate data sources, whether they are on-premises, in the cloud, or in
hybrid environments.
A data fabric typically includes features such as:
- **Data Integration:** Seamlessly integrates data from various sources, including databases, data lakes, and applications.
- **Data Governance:** Ensures data quality, security, and compliance across the organization.
- **Data Access:** Provides a unified interface for accessing data, regardless of its location or format.
- **Data Orchestration:** Automates data workflows and processes, enabling efficient data movement and transformation.
- **Data Virtualization:** Allows users to access and query data without needing to physically move it, providing real-time access to data across the fabric.
A data fabric is particularly useful in complex environments where data
is distributed across multiple systems, as it simplifies data management
and enhances data accessibility for analytics and decision-making.

- Active Metadata: Metadata that is continuously updated and reflects the
current state of data assets, enabling real-time insights and governance.

- Apache NiFi: A data integration tool that supports data flow automation and management, often used in data fabric architectures.
- Dremio: A data virtualization platform that provides a unified interface for accessing and querying data across various sources.
[Dremio](https://www.dremio.com/blog/understanding-data-mesh-and-data-fabric-a-guide-for-data-leaders/)

## Data Mesh
A data mesh is a decentralized approach to data architecture that emphasizes
domain-oriented ownership and self-serve data infrastructure. It aims to
overcome the limitations of traditional centralized data architectures by
treating data as a product and empowering teams to manage their own data
domains. Key principles of a data mesh include:
- **Domain-Oriented Decentralization:** Each domain team is responsible for the lifecycle of their data products, including data quality, governance, and access.
- **Data as a Product:** Data is treated as a product with its own lifecycle, including design, development, and maintenance. Domain teams are responsible for delivering high-quality data products to consumers.
- **Self-Serve Data Infrastructure:** Teams have access to self-serve tools and platforms that enable them to manage their data products independently, without relying on a centralized data team.
- **Federated Computational Governance:** A governance model that balances autonomy and standardization, allowing teams to innovate while adhering to organizational standards and policies.
A data mesh is particularly beneficial in large, complex organizations where
data is distributed across multiple domains, as it promotes agility,
scalability, and innovation by enabling teams to take ownership of their data
products.

