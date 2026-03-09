# Circular Trading Benchmark Summary

Benchmark date: March 9, 2026  
Database: PostgreSQL 18.1 with Apache AGE 1.7.0  
Runs per query: 20 warm-cache `EXPLAIN ANALYZE` executions

## Query Variants

- Recursive SQL over the relational `transactions` table
- Cypher on the baseline `aml_graph`
- Cypher on the tuned `aml_graph_tuned`

## Execution Results

| Query | Median Execution (ms) | Trimmed Mean Execution (ms) |
| --- | ---: | ---: |
| Recursive SQL | 0.187 | 0.196 |
| Cypher on AGE | 0.740 | 0.758 |
| Tuned Cypher on AGE | 0.494 | 0.495 |

## Interpretation

The tuned Cypher graph reduces execution time relative to the baseline graph by narrowing the graph to transfer edges only and by comparing internal graph identifiers and numeric timestamps. Even after tuning, the bounded 3-hop cycle detection workload remains faster in recursive SQL on the current small synthetic dataset.
