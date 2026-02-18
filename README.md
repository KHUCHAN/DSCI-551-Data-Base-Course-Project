<<<<<<< HEAD
# Hybrid-AML: Relational Fraud Detection System

**Course:** DSCI 551 Course Project, Spring '26  
**Team Members:** Chanyoung Kim, Yogita Mutyala

## Project Overview

This project investigates a "Graph-on-Relational" approach to financial fraud detection. Specifically, we aim to answer: *"Can PostgreSQL with Apache AGE efficiently support graph traversal workloads compared to native relational approaches, and what are the storage and execution tradeoffs of this hybrid model?"*

### Motivation
Financial fraud detection (e.g., Anti-Money Laundering) requires both strict ACID compliance for transactions (Relational DBMS strength) and deep traversal capabilities for detecting patterns like circular trading rings (Graph DBMS strength). Instead of maintaining two separate systems, we propose using **PostgreSQL** extended with **Apache AGE** to handle both workloads.

## Technology Stack

- **Database:** PostgreSQL with Apache AGE Extension
- **Backend/Application:** Python (Planned)
- **Data Generation:** Synthetic data script (Python)

## Project Structure

```plaintext
/
├── assets/                 # Images, diagrams for reports/README
├── data/
│   ├── raw/                # Original datasets
│   └── synthetic/          # Generated synthetic data for testing
├── database/
│   ├── migrations/         # SQL scripts for schema changes
│   ├── seeds/              # Initial data seeding scripts
│   └── setup_age.sql       # Apache AGE extension setup
├── docs/                   # Documentation
│   ├── guidelines/         # Course guidelines (551_project_guideline_sp26.pdf)
│   ├── proposal/           # Project proposal (Phase 1_ Project Proposal.pdf)
│   └── reports/            # Future reports
├── src/                    # Source code
│   ├── dashboard/          # Web application code
│   ├── data_generation/    # Scripts to generate synthetic data
│   └── analysis/           # Performance testing and analysis scripts
├── tests/                  # Automated tests
└── README.md               # Project documentation
```

## Setup Instructions

### Prerequisites
- PostgreSQL
- Apache AGE extension
- Python 3.8+

### Database Setup
*(Instructions to set up the database and install AGE extension will go here)*

### Running the Application
*(Instructions to generating data and running the dashboard will go here)*

## Expected Deliverables (Phase 1 - Proposal)

- [x] **Project Proposal**: Submitted 2/20
- [ ] **Midterm Report & Implementation Checkpoint**: Due 3/13
- [ ] **Final Demo**: 4/20 - 4/27
- [ ] **Final Report**: Due 5/8

## Research Focus Areas

1.  **Storage Architecture**: Graph to Relational Mapping (Vertices/Edges in Heap files vs JSONB).
2.  **Query Execution**: Cypher queries (AGE) vs Recursive SQL (CTEs).

## License
DSCI 551 Course Project
=======
# DSCI-551-Data-Base-Course-Project
Project for DSCI 551
>>>>>>> 0f95a9f35446f9cb4c6e59811ed6016a7010bc89
