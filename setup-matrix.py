#!/usr/bin/env python

import json
import os
import sys

DRIVER_VERSIONS = os.environ.get("DRIVER_VERSIONS")
if DRIVER_VERSIONS is None:
    print("DRIVER_VERSIONS environment variable is not set")
    sys.exit(1)

versions = DRIVER_VERSIONS.split(" ")
batch_size = 15
matrix = []

# Generate batches of driver versions for x86_64 / i386
for start_idx in range(0, len(versions), batch_size):
    batch_versions = versions[start_idx : start_idx + batch_size]
    matrix.append(
        {
            "arch": "x86_64",
            "id": start_idx // batch_size,
            "versions": " ".join(batch_versions),
        }
    )

# Filter out driver versions that don't have an aarch64 build.
aarch64_versions = [v for v in versions if os.path.isfile(f'./data/nvidia-{v}-aarch64.data')]

# Generate batches of driver versions for aarch64
for start_idx in range(0, len(aarch64_versions), batch_size):
    batch_versions = aarch64_versions[start_idx : start_idx + batch_size]
    matrix.append(
        {
            "arch": "aarch64",
            "id": start_idx // batch_size,
            "versions": " ".join(batch_versions),
        }
    )

print(matrix)

if "GITHUB_OUTPUT" in os.environ:
    matrix_json = json.dumps(matrix)
    with open(os.environ["GITHUB_OUTPUT"], "a") as f:
        f.write(f"matrix={matrix_json}\n")
