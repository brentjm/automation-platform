# Lab Automation Framework (LAF)

Creating a lab automation framework to illustrate the
ideas of event-driven automation using webhooks and
data ETL pipelines using Apache Airflow.

## Compliance Ideas

In a regulated (FDA) environment, using the database as the source of truth and triggering tasks from database changes (e.g., via `pg_notify`) can offer significant advantages over relying solely on HTTP endpoints to make changes:

**Advantages:**

1. **Auditability:**  
   All changes are recorded in the database, providing a clear, tamper-evident audit trail—critical for FDA compliance.

2. **Consistency:**  
   The database state is always the authoritative record. Tasks are triggered only after a successful, committed change, reducing the risk of race conditions or missed events.

3. **Reliability:**  
   If an HTTP request fails or is duplicated, the database can enforce constraints and idempotency. Triggers and notifications ensure downstream processes only act on committed, valid data.

4. **Traceability:**  
   You can trace every action back to a database event, which is easier to validate and review during audits.

5. **Decoupling:**  
   Business logic can be separated from the API layer, reducing the risk of accidental or unauthorized changes via HTTP.

**Caveats:**

- You must ensure that all changes go through controlled, validated database transactions.
- Triggers and notification logic must be carefully designed and tested.
- You still need secure, validated APIs for user input, but the database remains the ultimate authority.

**Summary:**  
For FDA-regulated environments, using the database as the source of truth—with tasks and workflows triggered by database changes—improves auditability, consistency, and compliance compared to relying solely on HTTP endpoints for business logic.
