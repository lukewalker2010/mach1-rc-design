"""Offline CSV ingestion only. Preserve every row; create a new no-clobber archive."""
import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

if __package__:
    from .bench_schema import FIELDS, canonical_hash, read_csv, validate_events
else:
    from bench_schema import FIELDS, canonical_hash, read_csv, validate_events

_hash_record = canonical_hash


def ingest(rows, *, expected_source_id=None, max_gap_s=None):
    rows = [dict(row) for row in rows]
    checks = validate_events(rows, expected_source_id=expected_source_id, max_gap_s=max_gap_s)
    records, rejected = [], []
    # Use a common set of columns before hashing, including extra input metadata.
    fields = set(FIELDS) | {"raw_record_json", "ingest_valid", "ingest_errors"}
    for row in rows:
        fields.update(row)
    fields.discard("record_hash")
    for row, check in zip(rows, checks):
        record = {key: row.get(key, "") for key in sorted(fields)}
        record["raw_record_json"] = json.dumps(row, sort_keys=True, separators=(",", ":"))
        record["ingest_valid"] = "0" if check["errors"] else "1"
        record["ingest_errors"] = json.dumps(check["errors"], separators=(",", ":"))
        record["record_hash"] = canonical_hash(record)
        records.append(record)
        if check["errors"]:
            rejected.append({"line": check["line"], "reasons": check["errors"]})
    return {"status": "EMPTY" if not rows else "FLAGGED" if rejected else "INGESTED",
            "records": records, "records_count": len(records),
            "valid_count": len(rows) - len(rejected), "rejected_count": len(rejected),
            "rejected": rejected, "scope": "Offline ingestion; no hardware acquisition or qualification."}


def write_output(records, output_path):
    fields = list(records[0]) if records else list(FIELDS) + ["record_hash"]
    with Path(output_path).open("x", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(records)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="CSV path or - for offline stdin")
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument("--source-id")
    parser.add_argument("--max-gap-s", type=float)
    args = parser.parse_args(argv)
    try:
        raw = sys.stdin.buffer.read() if args.input == "-" else Path(args.input).read_bytes()
        rows = read_csv(raw)
        report = ingest(rows, expected_source_id=args.source_id, max_gap_s=args.max_gap_s)
        write_output(report["records"], args.output)
        summary = {k: v for k, v in report.items() if k != "records"}
        summary.update(input_sha256=hashlib.sha256(raw).hexdigest(), output=str(args.output))
        print(json.dumps(summary, indent=2, allow_nan=False))
        return 0 if report["status"] == "INGESTED" else 1
    except (OSError, ValueError, UnicodeError, csv.Error, OverflowError) as exc:
        parser.exit(2, f"error: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
