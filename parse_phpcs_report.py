#!/usr/bin/env python3

import json
import sys

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument(
    "-s", "--sniffs", nargs="+", help="Only show information about a specific sniff or set of sniffs"
)

parser.add_argument(
    "-f",
    "--file",
    help=(
        "The path to a json formatted phpcs report. "
        "Otherwise, JSON report can be piped in"
    ),
)

parser.add_argument(
    "--fixable",
    action="store_true",
    help=(
        "Only collate automatically fixable sniffs."
    ),
)

parser.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    default=False,
    help="Show all occurrences of the sniff",
)


args = parser.parse_args()

if args.file:
    # Read JSON input from file
    with open(args.file, "r") as f:
        input_data = f.read()
elif not sys.stdin.isatty():
    # Read JSON input from stdin
    input_data = sys.stdin.read()
else:
    print(
        (
            "phpcs report must be either piped in or a file"
            "must be specified with the -f, --file option"
        )
    )
    sys.exit(1)

data = json.loads(input_data)
sniffs = {}

# Group warnings by sniff
for file, report in data.get("files", {}).items():
    for message in report["messages"]:
        sniff_name = message["source"]
        warnings = sniffs.get(sniff_name, [])

        m = (
            f"[{message['type']}:{message['severity']}] {message['message']}",
            f"{file}, line: {message['line']}",
        )

        if args.fixable:
            if message['fixable']:
                warnings.append(m)
        else:
            warnings.append(m)

        sniffs[sniff_name] = warnings

# If a specific sniff is requested, throw away everything else.
if args.sniffs:
    sniffs = {k: v for k, v in sniffs.items() if k in args.sniffs}

for sniff_name, occurrences in sniffs.items():
    print(f"{len(occurrences):<5} {sniff_name}")
    if args.verbose:
        for occurrence in occurrences:
            print("  ", occurrence[0], "...", occurrence[1])
