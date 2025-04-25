#!/usr/bin/env python

import json
import math
import os

DRIVER_VERSIONS = os.environ.get("DRIVER_VERSIONS")
if DRIVER_VERSIONS is None:
    print("DRIVER_VERSIONS environment variable is not set")
    exit(1)

versions = DRIVER_VERSIONS.split(" ")
num_batches = math.ceil(len(versions) // 50)
batch_size = 50

matrix = []
for i in range(num_batches):
    start_idx = i * batch_size
    end_idx = min(start_idx + batch_size, len(versions))
    batch_versions = versions[start_idx:end_idx]

    matrix.append(
        {
            "id": i,
            "versions": " ".join(batch_versions),
        }
    )

print(matrix)

if "GITHUB_OUTPUT" in os.environ:
    matrix_json = json.dumps(matrix)
    with open(os.environ["GITHUB_OUTPUT"], "a") as f:
        f.write(f"matrix={matrix_json}\n")
