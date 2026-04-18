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
- AGE-backed smurfing detection query
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
├── scripts/
│   └── reset_pipeline.sh    # One-command Docker + PostgreSQL + AGE reset
├── src/
│   ├── analysis/            # Benchmark and analysis scripts
│   ├── dashboard/           # Reserved for application UI
│   └── data_generation/     # Synthetic data generation scripts
└── tests/                   # Reserved for smoke tests
```

## Prerequisites

- Docker Desktop running locally
- `python3` available on the host machine
- Optional: `psql` on the host if you want to connect outside the container

This prototype does not require an Apache web server. The runtime stack is:

- Dockerized PostgreSQL + Apache AGE
- Host-side Python for synthetic data generation and benchmarking

## Clone and Enter the Repo

```bash
git clone https://github.com/KHUCHAN/DSCI-551-Data-Base-Course-Project.git
cd DSCI-551-Data-Base-Course-Project
```

All commands below assume you are running them from the repository root. The reset script resolves paths relative to its own location, so it does not depend on a machine-specific absolute path.

## Quick Start

From the repository root:

```bash
./scripts/reset_pipeline.sh
```

That script will:

1. Pull the `apache/age` image if needed
2. Start a Docker container named `apache-age`
3. Generate the synthetic CSV data
4. Create the relational schema
5. Load CSV data into PostgreSQL
6. Enable the AGE extension
7. Build the baseline and tuned graph projections
8. Print final row counts

If you want to recreate the database volume from scratch:

```bash
RESET_DB_VOLUME=1 ./scripts/reset_pipeline.sh
```

The default container settings used by the script are:

- Container name: `apache-age`
- Database: `hybrid_aml`
- User: `postgres`
- Port: `5455`

## Manual Setup

```bash
docker pull apache/age

docker run -d \
  --name apache-age \
  -p 5455:5432 \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=hybrid_aml \
  -v age_pg18data:/var/lib/postgresql \
  -v "$PWD":/workspace \
  apache/age

python3 src/data_generation/generate_synthetic_data.py

docker exec -i -w /workspace apache-age \
  psql -v ON_ERROR_STOP=1 -U postgres -d hybrid_aml \
  < database/migrations/001_schema.sql

docker exec -i -w /workspace apache-age \
  psql -v ON_ERROR_STOP=1 -U postgres -d hybrid_aml \
  < database/seeds/load_from_csv.sql

docker exec -i -w /workspace apache-age \
  psql -v ON_ERROR_STOP=1 -U postgres -d hybrid_aml \
  < database/setup_age.sql

docker exec -i -w /workspace apache-age \
  psql -v ON_ERROR_STOP=1 -U postgres -d hybrid_aml \
  < database/seeds/load_age_graph.sql

docker exec -i -w /workspace apache-age \
  psql -v ON_ERROR_STOP=1 -U postgres -d hybrid_aml \
  < database/seeds/load_age_graph_tuned.sql
```

## Demo Queries

Run the core AML queries directly against the Dockerized database:

```bash
docker exec -i -w /workspace apache-age \
  psql -U postgres -d hybrid_aml \
  < database/queries/smurfing_detection.sql

docker exec -i -w /workspace apache-age \
  psql -U postgres -d hybrid_aml \
  < database/queries/smurfing_detection_age.sql

docker exec -i -w /workspace apache-age \
  psql -U postgres -d hybrid_aml \
  < database/queries/circular_trading_recursive.sql

docker exec -i -w /workspace apache-age \
  psql -U postgres -d hybrid_aml \
  < database/queries/circular_trading_cypher.sql

docker exec -i -w /workspace apache-age \
  psql -U postgres -d hybrid_aml \
  < database/queries/circular_trading_cypher_tuned.sql
```

## Benchmarks

To rerun the cycle-detection benchmark and refresh the saved `EXPLAIN ANALYZE` artifacts:

```bash
python3 src/analysis/benchmark_cycle_queries.py
```

The benchmark script expects the Docker container name to remain `apache-age`. The latest saved summaries and explain plans live under [docs/reports](docs/reports).

## Deliverables in This Repository

- Phase 1 proposal: [docs/proposal/Phase 1_ Project Proposal.pdf](docs/proposal/Phase%201_%20Project%20Proposal.pdf)
- Phase 2 report: [docs/reports/Phase2_MidtermReport_ChanyoungKim_YogitaMutyala.pdf](docs/reports/Phase2_MidtermReport_ChanyoungKim_YogitaMutyala.pdf)
- Detection rule pseudocode: [docs/reports/detection_rules_pseudocode.md](docs/reports/detection_rules_pseudocode.md)
- Circular trading scenario note: [docs/reports/circular_trading_scenario.md](docs/reports/circular_trading_scenario.md)
- Smurfing scenario note: [docs/reports/smurfing_scenario.md](docs/reports/smurfing_scenario.md)
- Cycle benchmark summary: [docs/reports/cycle_benchmark_summary.md](docs/reports/cycle_benchmark_summary.md)

## License

DSCI 551 Course Project
