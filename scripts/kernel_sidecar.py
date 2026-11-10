#!/usr/bin/env python3
"""kernel_sidecar.py — write the JSON sidecar of a framework holographic kernel's 00-kernel.yaml, for a rhizome body
governed by it (scripts/rhizome_kernel.py). The sidecar records the YAML's SHA-256, and the builder refuses a sidecar
that no longer matches the kernel it names.    python3 scripts/kernel_sidecar.py <kernel dir> <sidecar.json>"""
import hashlib, json, pathlib, sys
import yaml
kd, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
b = (kd / "00-kernel.yaml").read_bytes()
out.write_text(json.dumps({"source": str(kd / "00-kernel.yaml"), "sha256": hashlib.sha256(b).hexdigest(),
                           "kernel": yaml.safe_load(b.decode("utf-8"))}, ensure_ascii=False, indent=1, sort_keys=True, default=str) + "\n", encoding="utf-8")
print("sidecar", out, hashlib.sha256(b).hexdigest()[:12])
