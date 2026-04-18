# Hybrid-AML: Graph-on-Relational Fraud Detection

**Course:** DSCI 551 Course Project, Spring '26  
**Team Members:** Chanyoung Kim, Yogita Mutyala

## Project Overview

This project studies whether PostgreSQL with Apache AGE can support AML-style graph analysis without leaving a relational system. The current prototype uses one PostgreSQL instance as the system of record, then projects account-to-account transaction flows into an AGE graph for graph-oriented pattern detection.

## Research Question

Can PostgreSQL with Apache AGE efficiently support graph traversal workloads compared with native relational approaches, and what storage and execution tradeoffs appear in this hybrid model?

## Implemented Midterm Scope

- Docker-based PostgreSQL + Apache AGE environment
- Relational schema for `customers`, `accounts`, and `transactions`
- Synthetic transaction generator with:
  - normal payroll, rent, utility, grocery, and peer-to-peer activity
  - nine smurfing funnel scenarios
  - nine circular trading scenarios
- SQL smurfing detection query
- Recursive SQL circular trading detection query
- Cypher circular trading query on AGE
- Tuned Cypher variant on a transfer-only graph projection

## Repository Structure

```text
.
├── assets/                  # Static assets for documentation
├── data/
│   ├── raw/                 # Reserved for original external datasets
│   └── synthetic/           # Generated CSVs used in the prototype
├── database/
│   ├── migrations/          # Schema creation scripts
│   ├── queries/             # SQL and Cypher detection queries
│   ├── seeds/               # CSV loading and graph projection scripts
│   └── setup_age.sql        # AGE extension setup
├── docs/
│   ├── guidelines/          # Course guidelines
│   ├── proposal/            # Phase 1 proposal
│   └── reports/             # Midterm report and supporting notes
├── src/
│   ├── analysis/            # Benchmark and analysis scripts
│   ├── dashboard/           # Reserved for application UI
│   └── data_generation/     # Synthetic data generation scripts
└── tests/                   # Reserved for smoke tests
```

## Setup

### 1. Generate synthetic data

```bash
cd repo_sync
python3 src/data_generation/generate_synthetic_data.py
```

### 2. Create the schema

```bash
psql -U postgres -d hybrid_aml -f database/migrations/001_schema.sql
```

### 3. Load CSV data

```bash
psql -U postgres -d hybrid_aml -f database/seeds/load_from_csv.sql
```

### 4. Enable AGE

```bash
psql -U postgres -d hybrid_aml -f database/setup_age.sql
```

### 5. Build graph projections

Baseline graph:

```bash
psql -U postgres -d hybrid_aml -f database/seeds/load_age_graph.sql
```

Tuned graph:

```bash
psql -U postgres -d hybrid_aml -f database/seeds/load_age_graph_tuned.sql
```

## Query Benchmarks

The circular trading benchmark was run on March 9, 2026 against the Dockerized `hybrid_aml` database using 20 repeated `EXPLAIN ANALYZE` executions.

- Recursive SQL
  - median execution: `0.187 ms`
  - trimmed execution mean: `0.196 ms`
- Cypher on AGE
  - median execution: `0.740 ms`
  - trimmed execution mean: `0.758 ms`
- Tuned Cypher on AGE
  - median execution: `0.494 ms`
  - trimmed execution mean: `0.495 ms`

## Current Interpretation

The current bounded cycle-detection workload is still faster in recursive SQL than in AGE/Cypher. The tuned graph projection reduces Cypher execution time, but the relational baseline remains more efficient on this small dataset. This is not a general statement about all graph databases; it is a result for the current AML prototype, current projection design, and current workload shape.

## Deliverables in This Repository

- Phase 1 proposal: [docs/proposal/Phase 1_ Project Proposal.pdf](docs/proposal/Phase%201_%20Project%20Proposal.pdf)
- Phase 2 report: [docs/reports/Phase 2_ Midterm Report.pdf](docs/reports/Phase%202_%20Midterm%20Report.pdf)
- Editable report copy: [docs/reports/Phase 2_ Midterm Report.docx](docs/reports/Phase%202_%20Midterm%20Report.docx)

## License

DSCI 551 Course Project
