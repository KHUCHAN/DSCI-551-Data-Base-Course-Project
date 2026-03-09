from __future__ import annotations

import csv
import random
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path


SEED = 551
PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "data" / "synthetic"


@dataclass(frozen=True)
class Customer:
    customer_id: str
    full_name: str
    customer_type: str
    risk_tier: str
    created_at: str


@dataclass(frozen=True)
class Account:
    account_id: str
    customer_id: str
    account_type: str
    open_date: str
    status: str
    home_country: str


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def created_at(days_ago: int) -> str:
    base = datetime(2026, 1, 1, 9, 0, 0)
    return (base - timedelta(days=days_ago)).strftime("%Y-%m-%d %H:%M:%S")


def build_customers() -> tuple[list[Customer], list[Account], dict[str, str], list[str], list[str]]:
    customers: list[Customer] = []
    accounts: list[Account] = []
    customer_to_primary_account: dict[str, str] = {}

    regular_people = [
        "Alex Carter",
        "Bailey Chen",
        "Cameron Diaz",
        "Dana Park",
        "Evan Scott",
        "Farah Khan",
        "Grace Kim",
        "Henry Lopez",
        "Irene Patel",
        "Jason Yu",
        "Kylie Smith",
        "Leo Johnson",
        "Mina Choi",
        "Noah White",
        "Olivia Martin",
        "Priya Gupta",
        "Quinn Taylor",
        "Rina Suzuki",
        "Samuel Brown",
        "Tina Nguyen",
    ]
    business_entities = [
        ("CUST-BIZ-001", "Northstar Payroll LLC", "business", "low", "ACC-BIZ-001", "business", "US"),
        ("CUST-BIZ-002", "Harbor View Properties", "business", "low", "ACC-BIZ-002", "business", "US"),
        ("CUST-BIZ-003", "Fresh Basket Market", "business", "low", "ACC-BIZ-003", "business", "US"),
        ("CUST-BIZ-004", "City Utilities Service", "business", "low", "ACC-BIZ-004", "business", "US"),
        ("CUST-BIZ-005", "Blueline Brokerage", "business", "medium", "ACC-BIZ-005", "business", "US"),
    ]

    for index, full_name in enumerate(regular_people, start=1):
        customer_id = f"CUST-IND-{index:03d}"
        risk_tier = "low" if index % 5 else "medium"
        customer = Customer(
            customer_id=customer_id,
            full_name=full_name,
            customer_type="individual",
            risk_tier=risk_tier,
            created_at=created_at(300 + index * 6),
        )
        primary_account_id = f"ACC-CHK-{index:03d}"
        primary_account = Account(
            account_id=primary_account_id,
            customer_id=customer_id,
            account_type="checking",
            open_date=str(date(2024, 1, 10) + timedelta(days=index * 4)),
            status="active",
            home_country="US",
        )
        customers.append(customer)
        accounts.append(primary_account)
        customer_to_primary_account[customer_id] = primary_account_id

        if index % 4 == 0:
            savings_account = Account(
                account_id=f"ACC-SAV-{index:03d}",
                customer_id=customer_id,
                account_type="savings",
                open_date=str(date(2024, 5, 1) + timedelta(days=index * 3)),
                status="active",
                home_country="US",
            )
            accounts.append(savings_account)

    for customer_id, full_name, customer_type, risk_tier, account_id, account_type, home_country in business_entities:
        customers.append(
            Customer(
                customer_id=customer_id,
                full_name=full_name,
                customer_type=customer_type,
                risk_tier=risk_tier,
                created_at=created_at(540),
            )
        )
        accounts.append(
            Account(
                account_id=account_id,
                customer_id=customer_id,
                account_type=account_type,
                open_date=str(date(2023, 7, 1)),
                status="active",
                home_country=home_country,
            )
        )
        customer_to_primary_account[customer_id] = account_id

    suspicious_customers = [
        ("CUST-AML-001", "Golden Crest Imports", "business", "high", "ACC-AML-HUB-001", "business", "US"),
        ("CUST-AML-002", "Marlin Export Consulting", "business", "high", "ACC-SHELL-001", "business", "KY"),
        ("CUST-CYCLE-001", "Orchid Metals Trading", "business", "high", "ACC-CYCLE-001", "business", "SG"),
        ("CUST-CYCLE-002", "Blue Mesa Commodities", "business", "high", "ACC-CYCLE-002", "business", "AE"),
        ("CUST-CYCLE-003", "North Gate Holdings", "business", "high", "ACC-CYCLE-003", "business", "HK"),
    ]
    feeder_customers: list[str] = []
    feeder_accounts: list[str] = []
    for index in range(1, 7):
        customer_id = f"CUST-FEED-{index:03d}"
        account_id = f"ACC-FEED-{index:03d}"
        suspicious_customers.append(
            (customer_id, f"Feeder Client {index}", "individual", "medium", account_id, "checking", "US")
        )
        feeder_customers.append(customer_id)
        feeder_accounts.append(account_id)

    for customer_id, full_name, customer_type, risk_tier, account_id, account_type, home_country in suspicious_customers:
        customers.append(
            Customer(
                customer_id=customer_id,
                full_name=full_name,
                customer_type=customer_type,
                risk_tier=risk_tier,
                created_at=created_at(120),
            )
        )
        accounts.append(
            Account(
                account_id=account_id,
                customer_id=customer_id,
                account_type=account_type,
                open_date=str(date(2025, 8, 1)),
                status="active",
                home_country=home_country,
            )
        )
        customer_to_primary_account[customer_id] = account_id

    return customers, accounts, customer_to_primary_account, feeder_accounts, regular_people


def build_transactions(accounts: list[Account], customer_to_primary_account: dict[str, str], feeder_accounts: list[str]) -> list[dict[str, str]]:
    rng = random.Random(SEED)
    account_ids = [account.account_id for account in accounts]
    customer_accounts = [
        account_id
        for account_id in account_ids
        if account_id.startswith("ACC-CHK-") and account_id not in feeder_accounts
    ]

    employer = customer_to_primary_account["CUST-BIZ-001"]
    landlord = customer_to_primary_account["CUST-BIZ-002"]
    grocery = customer_to_primary_account["CUST-BIZ-003"]
    utility = customer_to_primary_account["CUST-BIZ-004"]
    brokerage = customer_to_primary_account["CUST-BIZ-005"]
    suspicious_hub = customer_to_primary_account["CUST-AML-001"]
    shell = customer_to_primary_account["CUST-AML-002"]
    cycle_a = customer_to_primary_account["CUST-CYCLE-001"]
    cycle_b = customer_to_primary_account["CUST-CYCLE-002"]
    cycle_c = customer_to_primary_account["CUST-CYCLE-003"]

    transactions: list[dict[str, str]] = []
    tx_counter = 1

    def add_tx(
        from_account_id: str | None,
        to_account_id: str | None,
        amount: float,
        tx_time: datetime,
        channel: str,
        merchant_category: str | None,
        tx_type: str,
        is_fraud_label: str = "normal",
        scenario_tag: str | None = None,
    ) -> None:
        nonlocal tx_counter
        transactions.append(
            {
                "tx_id": f"TX-{tx_counter:05d}",
                "from_account_id": from_account_id or "",
                "to_account_id": to_account_id or "",
                "amount": f"{amount:.2f}",
                "tx_time": tx_time.strftime("%Y-%m-%d %H:%M:%S"),
                "channel": channel,
                "merchant_category": merchant_category or "",
                "tx_type": tx_type,
                "is_fraud_label": is_fraud_label,
                "scenario_tag": scenario_tag or "",
            }
        )
        tx_counter += 1

    base_day = datetime(2026, 2, 1, 8, 0, 0)

    for account_id in customer_accounts:
        payroll_day = base_day + timedelta(days=rng.randint(0, 2), hours=rng.randint(0, 5))
        payroll_amount = rng.uniform(1800, 3400)
        add_tx(employer, account_id, payroll_amount, payroll_day, "ach", "payroll", "transfer")

        rent_day = payroll_day + timedelta(days=rng.randint(2, 4), hours=rng.randint(1, 8))
        rent_amount = rng.uniform(950, 2200)
        add_tx(account_id, landlord, rent_amount, rent_day, "ach", "housing", "transfer")

        utility_day = payroll_day + timedelta(days=rng.randint(3, 8), hours=rng.randint(1, 6))
        utility_amount = rng.uniform(80, 240)
        add_tx(account_id, utility, utility_amount, utility_day, "ach", "utilities", "withdrawal")

        for _ in range(rng.randint(3, 6)):
            grocery_day = base_day + timedelta(
                days=rng.randint(0, 20),
                hours=rng.randint(8, 21),
                minutes=rng.randint(0, 59),
            )
            grocery_amount = rng.uniform(22, 190)
            add_tx(account_id, grocery, grocery_amount, grocery_day, "card", "groceries", "withdrawal")

        if rng.random() < 0.45:
            invest_day = base_day + timedelta(
                days=rng.randint(5, 20),
                hours=rng.randint(8, 18),
                minutes=rng.randint(0, 59),
            )
            invest_amount = rng.uniform(250, 1800)
            add_tx(account_id, brokerage, invest_amount, invest_day, "ach", "investment", "transfer")

        if rng.random() < 0.35:
            cash_day = base_day + timedelta(
                days=rng.randint(0, 18),
                hours=rng.randint(8, 19),
                minutes=rng.randint(0, 59),
            )
            cash_amount = rng.uniform(150, 2800)
            add_tx(account_id, account_id, cash_amount, cash_day, "cash", "branch_deposit", "deposit")

    for _ in range(35):
        sender, receiver = rng.sample(customer_accounts, 2)
        p2p_time = base_day + timedelta(
            days=rng.randint(0, 20),
            hours=rng.randint(8, 22),
            minutes=rng.randint(0, 59),
        )
        p2p_amount = rng.uniform(20, 420)
        add_tx(sender, receiver, p2p_amount, p2p_time, "internal", "p2p_transfer", "transfer")

    scenario_tag = "smurfing_funnel_001"
    suspicious_day = datetime(2026, 2, 18, 9, 5, 0)
    suspicious_deposits = [8940.00, 9180.00, 9420.00, 9760.00, 9860.00, 9640.00]
    for index, amount in enumerate(suspicious_deposits):
        add_tx(
            feeder_accounts[index],
            suspicious_hub,
            amount,
            suspicious_day + timedelta(minutes=[0, 27, 59, 96, 133, 169][index]),
            "cash",
            "branch_deposit",
            "deposit",
            "smurfing",
            scenario_tag,
        )

    add_tx(
        suspicious_hub,
        shell,
        54900.00,
        datetime(2026, 2, 18, 13, 10, 0),
        "wire",
        "consulting_services",
        "transfer",
        "smurfing",
        scenario_tag,
    )

    add_tx(
        suspicious_hub,
        customer_to_primary_account["CUST-BIZ-005"],
        1400.00,
        datetime(2026, 2, 20, 10, 15, 0),
        "ach",
        "brokerage",
        "transfer",
    )

    cycle_tag = "circular_trading_001"
    cycle_day = datetime(2026, 2, 22, 10, 15, 0)
    cycle_legs = [
        (cycle_a, cycle_b, 15150.00, cycle_day),
        (cycle_b, cycle_c, 14960.00, cycle_day + timedelta(minutes=48)),
        (cycle_c, cycle_a, 15040.00, cycle_day + timedelta(minutes=121)),
    ]
    for from_account_id, to_account_id, amount, tx_time in cycle_legs:
        add_tx(
            from_account_id,
            to_account_id,
            amount,
            tx_time,
            "wire",
            "brokerage_settlement",
            "transfer",
            "cycle",
            cycle_tag,
        )

    transactions.sort(key=lambda row: row["tx_time"])
    return transactions


def main() -> None:
    customers, accounts, customer_to_primary_account, feeder_accounts, _ = build_customers()
    transactions = build_transactions(accounts, customer_to_primary_account, feeder_accounts)

    customer_rows = [customer.__dict__ for customer in customers]
    account_rows = [account.__dict__ for account in accounts]

    write_csv(
        OUTPUT_DIR / "customers.csv",
        ["customer_id", "full_name", "customer_type", "risk_tier", "created_at"],
        customer_rows,
    )
    write_csv(
        OUTPUT_DIR / "accounts.csv",
        ["account_id", "customer_id", "account_type", "open_date", "status", "home_country"],
        account_rows,
    )
    write_csv(
        OUTPUT_DIR / "transactions.csv",
        [
            "tx_id",
            "from_account_id",
            "to_account_id",
            "amount",
            "tx_time",
            "channel",
            "merchant_category",
            "tx_type",
            "is_fraud_label",
            "scenario_tag",
        ],
        transactions,
    )

    smurfing_total = sum(
        float(row["amount"])
        for row in transactions
        if row["scenario_tag"] == "smurfing_funnel_001" and row["tx_type"] == "deposit"
    )
    cycle_total = sum(
        float(row["amount"])
        for row in transactions
        if row["scenario_tag"] == "circular_trading_001"
    )
    print(f"Wrote {len(customer_rows)} customers to {OUTPUT_DIR / 'customers.csv'}")
    print(f"Wrote {len(account_rows)} accounts to {OUTPUT_DIR / 'accounts.csv'}")
    print(f"Wrote {len(transactions)} transactions to {OUTPUT_DIR / 'transactions.csv'}")
    print(f"Smurfing inbound total for ACC-AML-HUB-001: ${smurfing_total:,.2f}")
    print(f"Circular trading notional total across loop edges: ${cycle_total:,.2f}")


if __name__ == "__main__":
    main()
