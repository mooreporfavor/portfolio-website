---
title: "Architecting a Modern Data Platform for the Peace Corps"
client: "Peace Corps Executive Leadership & Operations"
year: 2025
track: "Data Engineering & AI"
tags: ["Data Architecture", "ETL/ELT", "Business Intelligence", "AI Strategy", "Streamlit", "Full-Stack Data Science"]
isFeatured: true
---

### Problem

The <a href="https://www.peacecorps.gov/" target="_blank">Peace Corps'</a> ability to make data-driven decisions was severely hampered by a fragmented and brittle data infrastructure. Critical information on the volunteer lifecycle—from web engagement to application processing and in-service outcomes—was locked in disparate systems with no unified source of truth. The existing analytics tools were slow, unreliable, and required immense manual effort to maintain, leading to a lack of trust in the data and an inability to answer strategic questions.

The challenge was to architect and build an entire, end-to-end data platform from the ground up, delivering a fast, trusted, and AI-ready analytics service despite operating with a drastically reduced human capital footprint.

### Methodology

As the sole data platform architect and senior engineer, my role was to design, code, and lead the deployment of a complete <a href="https://www.databricks.com/glossary/medallion-architecture" target="_blank">Medallion Architecture</a> data pipeline and the flagship analytics application, "Mission Control." I strategically leveraged AI coding assistance to accelerate development and deliver a complex system with a team of one.

*   **Data Architecture & Full-Stack ETL Development:** I designed and single-handedly built a three-tiered data pipeline (Bronze, Silver, Gold) to transform raw, siloed data into trusted, high-performance analytical assets. This involved:
    *   **Bronze Layer (Ingestion):** Developing connectors to extract raw data from diverse sources, including <a href="https://analytics.google.com/" target="_blank">Google Analytics</a>, a transactional applicant tracking system (DOVE), and a legacy volunteer service database (Odyssey).
    *   **Silver Layer (Integration & Cleansing):** Engineering complex business logic to cleanse, de-duplicate, and conform the data into a unified, cross-functional view of the complete volunteer journey. This created the foundational, 360-degree view that was previously missing.
    *   **Gold Layer (Aggregation & Performance):** Architecting a suite of purpose-built, pre-aggregated data marts. This included a high-speed "Dashboard Mart" for operational metrics and a specialized "Time-Series Mart" for cohort analysis, designed to serve analytics with sub-second latency.

*   **Platform & Application Development:** I built the "Mission Control" analytics application in <a href="https://streamlit.io/" target="_blank">Streamlit</a>, establishing it as the agency's definitive source for operational intelligence. Key to its success and scalability was a **configuration-driven design**, where the application's layout and metric definitions are controlled by external configuration files. This decouples the UI from the data logic, enabling rapid, code-free updates.

*   **Strategy & AI Enablement:** I authored the platform's architectural vision, establishing a set of engineering principles and a component-based development pattern. This blueprint not only governs the current application but also strategically positions the Peace Corps for the future. The clean, granular Gold Layer data is intentionally structured to serve as a high-quality "<a href="https://www.featureform.com/post/what-is-a-feature-store" target="_blank">feature store</a>," creating a direct on-ramp for the agency to develop and deploy machine learning models and adopt a broader AI toolkit for predictive analytics.

### Outcome

This project delivered a complete, modern data platform that fundamentally transformed the Peace Corps' ability to use data for strategic decision-making.

*   **Strategic Impact:** The platform is now the **single source of truth** for the entire volunteer lifecycle, eliminating data silos and fostering universal trust in the metrics. By architecting the Gold Layer for machine learning, I delivered not just a reporting tool, but a foundational, **AI-ready infrastructure** that unlocks future capabilities like predictive forecasting and applicant risk modeling.

*   **Operational Impact:**
    *   **Performance:** End-user query and dashboard load times were reduced from minutes to **under one second**, enabling real-time operational monitoring.
    *   **Efficiency:** The automated, end-to-end pipeline replaced dozens of hours per week of manual data wrangling and report building.
    *   **Agility:** The configuration-driven design allows the analytics team to add or modify dashboard KPIs in minutes, providing unprecedented responsiveness to leadership's evolving questions.

*   **Knowledge Impact:** This initiative successfully demonstrated how a single architect, leveraging a modern Medallion Architecture and AI-assisted development tools, can deliver an enterprise-grade data platform at a fraction of the time and cost of traditional methods. It established a new, scalable blueprint for all future data product development at the agency.
