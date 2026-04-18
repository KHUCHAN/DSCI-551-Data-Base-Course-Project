# AML Detection Rule Pseudocode

This note summarizes the two core AML detection rules used in this prototype and maps each rule to the implemented query files.

## Rule 1: Smurfing Funnel Detection

### Detection Logic

- Group cash deposits by beneficiary account and day.
- Mark the account as suspicious when:
  - each inbound deposit is below USD 10,000,
  - there are at least 5 such deposits,
  - the same-day total is at least USD 45,000.
- Then check whether the beneficiary account sends a large outbound transfer:
  - within 24 hours after the last inbound deposit,
  - with amount at least 70% of the structured inbound total.

### Pseudocode

```text
FOR each beneficiary_account_id, deposit_day:
    deposits = all transactions
        WHERE tx_type = "deposit"
          AND channel = "cash"
          AND to_account_id = beneficiary_account_id
          AND DATE(tx_time) = deposit_day
          AND amount < 10000

    IF COUNT(deposits) >= 5
       AND SUM(deposits.amount) >= 45000:
        first_deposit_at = MIN(deposits.tx_time)
        last_deposit_at = MAX(deposits.tx_time)
        structured_total = SUM(deposits.amount)

        outbound_transfers = all transactions
            WHERE tx_type = "transfer"
              AND from_account_id = beneficiary_account_id
              AND tx_time BETWEEN last_deposit_at
                              AND last_deposit_at + 24 hours
              AND amount >= structured_total * 0.70

        FOR each outbound transfer in outbound_transfers:
            EMIT suspicious smurfing funnel case
```

### Implemented Queries

- Relational SQL: `database/queries/smurfing_detection.sql`
- AGE-backed graph extraction + SQL aggregation: `database/queries/smurfing_detection_age.sql`
- Representative graph subgraph lookup: `database/queries/age_smurfing_subgraph.sql`

## Rule 2: Circular Trading Detection

### Detection Logic

- Consider only account-to-account transfer transactions.
- Find 3-account cycles `A -> B -> C -> A`.
- Require all three accounts to be distinct.
- Require the transfers to occur in chronological order.
- Require the full cycle to complete within 6 hours from the first transfer.
- Do not apply an additional amount threshold in the current implementation.

### Pseudocode

```text
FOR each transfer t1: A -> B:
    FOR each transfer t2: B -> C:
        IF C = A:
            CONTINUE
        IF t2.tx_time < t1.tx_time:
            CONTINUE

        FOR each transfer t3: C -> A:
            IF A, B, C are not all distinct:
                CONTINUE
            IF t3.tx_time < t2.tx_time:
                CONTINUE
            IF t3.tx_time > t1.tx_time + 6 hours:
                CONTINUE

            canonical_origin = minimum(A, B, C) under the query's dedup rule
            IF A is the canonical_origin:
                EMIT suspicious circular trading cycle
```

### Implemented Queries

- Relational recursive SQL: `database/queries/circular_trading_recursive.sql`
- AGE Cypher on baseline graph: `database/queries/circular_trading_cypher.sql`
- AGE Cypher on tuned transfer-only graph: `database/queries/circular_trading_cypher_tuned.sql`

## Notes

- The smurfing rule is aggregation-heavy, so the relational SQL version is the primary baseline.
- The circular trading rule is traversal-heavy, so it is the main SQL versus AGE comparison workload.
- The current circular trading rule uses account topology and timing; the synthetic transfer amounts are descriptive scenario details rather than enforced thresholds.
- In the current synthetic dataset, each rule produces 9 detected cases.
