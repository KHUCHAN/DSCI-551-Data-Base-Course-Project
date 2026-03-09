from __future__ import annotations

import re
import statistics
import subprocess
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONTAINER = "apache-age"
DB_NAME = "hybrid_aml"
RUNS = 20


def run_psql(sql: str) -> str:
    result = subprocess.run(
        [
            "docker",
            "exec",
            "-i",
            CONTAINER,
            "psql",
            "-v",
            "ON_ERROR_STOP=1",
            "-P",
            "pager=off",
            "-U",
            "postgres",
            "-d",
            DB_NAME,
        ],
        input=sql,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout


def load_query(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def parse_timings(explain_output: str) -> tuple[float, float]:
    planning_match = re.search(r"Planning Time: ([0-9.]+) ms", explain_output)
    execution_match = re.search(r"Execution Time: ([0-9.]+) ms", explain_output)
    if not planning_match or not execution_match:
        raise ValueError("Could not parse planning/execution time from EXPLAIN output")
    return float(planning_match.group(1)), float(execution_match.group(1))


def benchmark_sql_query(query_path: Path) -> tuple[list[float], list[float], str]:
    query = load_query(query_path)
    planning_times: list[float] = []
    execution_times: list[float] = []
    last_output = ""

    warmup_sql = f"EXPLAIN (ANALYZE, BUFFERS)\n{query}"
    run_psql(warmup_sql)

    for _ in range(RUNS):
        output = run_psql(warmup_sql)
        planning, execution = parse_timings(output)
        planning_times.append(planning)
        execution_times.append(execution)
        last_output = output

    return planning_times, execution_times, last_output


def benchmark_cypher_query(query_path: Path) -> tuple[list[float], list[float], str]:
    query = load_query(query_path)
    select_start = query.index("SELECT *")
    cypher_select = query[select_start:]
    explain_sql = "\n".join(
        [
            "LOAD 'age';",
            'SET search_path = ag_catalog, "$user", public;',
            f"EXPLAIN (ANALYZE, BUFFERS)\n{cypher_select}",
        ]
    )

    planning_times: list[float] = []
    execution_times: list[float] = []
    last_output = ""

    run_psql(explain_sql)

    for _ in range(RUNS):
        output = run_psql(explain_sql)
        planning, execution = parse_timings(output)
        planning_times.append(planning)
        execution_times.append(execution)
        last_output = output

    return planning_times, execution_times, last_output


def summarize(label: str, planning_times: list[float], execution_times: list[float]) -> None:
    trimmed = sorted(execution_times)[2:-2] if len(execution_times) > 4 else execution_times
    print(label)
    print(f"  planning_ms: {', '.join(f'{value:.3f}' for value in planning_times)}")
    print(f"  execution_ms: {', '.join(f'{value:.3f}' for value in execution_times)}")
    print(f"  avg_planning_ms: {statistics.mean(planning_times):.3f}")
    print(f"  median_planning_ms: {statistics.median(planning_times):.3f}")
    print(f"  avg_execution_ms: {statistics.mean(execution_times):.3f}")
    print(f"  median_execution_ms: {statistics.median(execution_times):.3f}")
    print(f"  trimmed_execution_ms: {statistics.mean(trimmed):.3f}")


def main() -> None:
    sql_path = PROJECT_ROOT / "database" / "queries" / "circular_trading_recursive.sql"
    cypher_path = PROJECT_ROOT / "database" / "queries" / "circular_trading_cypher.sql"
    tuned_cypher_path = PROJECT_ROOT / "database" / "queries" / "circular_trading_cypher_tuned.sql"

    sql_planning, sql_execution, sql_plan = benchmark_sql_query(sql_path)
    cypher_planning, cypher_execution, cypher_plan = benchmark_cypher_query(cypher_path)
    tuned_planning, tuned_execution, tuned_plan = benchmark_cypher_query(tuned_cypher_path)

    summarize("Recursive SQL", sql_planning, sql_execution)
    summarize("Cypher on AGE", cypher_planning, cypher_execution)
    summarize("Cypher on AGE (tuned)", tuned_planning, tuned_execution)

    sql_plan_path = PROJECT_ROOT / "docs" / "reports" / "cycle_recursive_explain.txt"
    cypher_plan_path = PROJECT_ROOT / "docs" / "reports" / "cycle_cypher_explain.txt"
    tuned_plan_path = PROJECT_ROOT / "docs" / "reports" / "cycle_cypher_tuned_explain.txt"
    sql_plan_path.parent.mkdir(parents=True, exist_ok=True)
    sql_plan_path.write_text(sql_plan, encoding="utf-8")
    cypher_plan_path.write_text(cypher_plan, encoding="utf-8")
    tuned_plan_path.write_text(tuned_plan, encoding="utf-8")
    print(f"Saved latest recursive SQL plan to {sql_plan_path}")
    print(f"Saved latest Cypher plan to {cypher_plan_path}")
    print(f"Saved latest tuned Cypher plan to {tuned_plan_path}")


if __name__ == "__main__":
    main()
