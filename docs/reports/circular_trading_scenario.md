# Representative AML Scenario: Circular Trading Loop

## Scenario Summary

This prototype includes representative circular trading patterns built around three business accounts that move funds in a closed loop within a short time window.

- **Pattern:** three accounts transfer funds in the sequence `A -> B -> C -> A`.
- **Timing:** all three transfers occur in chronological order and complete within 6 hours.
- **Purpose:** the loop structure is intended to resemble suspicious circular movement of funds between related entities.

## Synthetic Actors

- **Account A:** `ACC-CYCLE-001` (`Orchid Metals Trading`)
- **Account B:** `ACC-CYCLE-002` (`Blue Mesa Commodities`)
- **Account C:** `ACC-CYCLE-003` (`North Gate Holdings`)

## Representative Timeline

For the first representative scenario, `circular_trading_001`, the generator creates the following transfers on `2026-02-22`:

- 10:15 - `ACC-CYCLE-001 -> ACC-CYCLE-002` - USD 15,150
- 11:03 - `ACC-CYCLE-002 -> ACC-CYCLE-003` - USD 14,960
- 12:16 - `ACC-CYCLE-003 -> ACC-CYCLE-001` - USD 15,040

Total notional amount moved across the loop: **USD 45,150**

## Why This Looks Suspicious

- The same three accounts participate in a closed fund-flow loop.
- The transfers occur in a short and ordered sequence.
- The structure suggests money circulation rather than ordinary one-way settlement behavior.

## Important Rule Note

The current circular trading detection queries do **not** apply a separate amount threshold. The implemented rule is based on:

- transfer-only edges,
- three distinct accounts,
- chronological transfer order,
- full cycle completion within 6 hours.

The synthetic amounts above are included to make the scenario realistic and easier to explain in demos, but the current detection rule is primarily **topology + time-window based**, not amount-threshold based.

## How This Maps to the Dataset

The suspicious transactions are tagged with:

- `is_fraud_label = 'cycle'`
- `scenario_tag = 'circular_trading_001'`

Additional cohorts generate related variants through `circular_trading_009`.

## Related Queries

- Relational recursive SQL: `database/queries/circular_trading_recursive.sql`
- AGE baseline Cypher: `database/queries/circular_trading_cypher.sql`
- AGE tuned Cypher: `database/queries/circular_trading_cypher_tuned.sql`
