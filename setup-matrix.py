#!/usr/bin/env python

import json
import os
import sys

DRIVER_VERSIONS = os.environ.get("DRIVER_VERSIONS")
if DRIVER_VERSIONS is None:
    print("DRIVER_VERSIONS environment variable is not set")
    sys.exit(1)

versions = DRIVER_VERSIONS.split(" ")
batch_size = 30
matrix = []

for start_idx in range(0, len(versions), batch_size):
    batch_versions = versions[start_idx : start_idx + batch_size]
    matrix.append(
        {
            "id": start_idx // batch_size,
            "versions": " ".join(batch_versions),
        }
    )

print(matrix)

if "GITHUB_OUTPUT" in os.environ:
    matrix_json = json.dumps(matrix)
    with open(os.environ["GITHUB_OUTPUT"], "a") as f:
        f.write(f"matrix={matrix_json}\n")
