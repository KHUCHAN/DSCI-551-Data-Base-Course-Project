# Representative AML Scenario: Smurfing Funnel

## Scenario Summary

This prototype uses one concrete money-laundering pattern: a smurfing funnel built around one aggregation account.

- **Placement:** six feeder accounts make cash deposits that stay just below the USD 10,000 reporting threshold.
- **Aggregation:** the deposits land in a single business account during the same morning.
- **Layering:** the business account quickly sends one large outbound wire to a shell account.

## Synthetic Actors

- **Aggregation account:** `ACC-AML-HUB-001`
- **Shell destination:** `ACC-SHELL-001`
- **Feeder accounts:** `ACC-FEED-001` through `ACC-FEED-006`

## Suspicious Timeline

On `2026-02-18`, the aggregation account receives six cash deposits:

- 09:05 - USD 8,940
- 09:32 - USD 9,180
- 10:04 - USD 9,420
- 10:41 - USD 9,760
- 11:18 - USD 9,860
- 11:54 - USD 9,640

Total inbound amount: **USD 56,800**

At `13:10` on the same day, the account sends an outbound wire of **USD 54,900** to `ACC-SHELL-001`.

## Why This Looks Like Smurfing

- Each inbound cash transfer stays below the common reporting threshold.
- The deposits are concentrated in a short time window.
- The beneficiary account acts as a funnel rather than an operating account.
- Most of the money leaves shortly after the deposits arrive.

## How This Maps to the Dataset

The suspicious transactions are tagged with:

- `is_fraud_label = 'smurfing'`
- `scenario_tag = 'smurfing_funnel_001'`

Normal salary, rent, merchant, and peer-to-peer activity is mixed into the same dataset so the suspicious pattern is not isolated.
