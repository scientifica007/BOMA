#!/usr/bin/env python3
"""One-shot pre-START installer for the BOMA autonomy bootstrap payload."""
from __future__ import annotations
import base64
import io
import lzma
import os
import pathlib
import shutil
import tarfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
EXPECTED_REPO = "scientifica007/BOMA"
CHUNKS = ROOT / "bootstrap" / "chunks"


def main() -> int:
    repo = os.environ.get("GITHUB_REPOSITORY")
    if repo and repo != EXPECTED_REPO:
        raise SystemExit(f"Refusing bootstrap outside {EXPECTED_REPO}: {repo}")
    parts = sorted(CHUNKS.glob("*.txt"))
    if not parts:
        raise SystemExit("bootstrap payload chunks are missing")
    encoded = "".join(path.read_text(encoding="utf-8").strip() for path in parts)
    raw = lzma.decompress(base64.b64decode(encoded))
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:") as tf:
        for member in tf.getmembers():
            rel = pathlib.PurePosixPath(member.name)
            if not member.isfile() or rel.is_absolute() or ".." in rel.parts:
                raise SystemExit(f"unsafe payload member: {member.name}")
            target = ROOT.joinpath(*rel.parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            src = tf.extractfile(member)
            if src is None:
                raise SystemExit(f"missing payload bytes: {member.name}")
            target.write_bytes(src.read())
    shutil.rmtree(ROOT / "bootstrap", ignore_errors=True)
    (ROOT / ".github" / "workflows" / "boma-autonomy-bootstrap-install.yml").unlink(missing_ok=True)
    print("BOMA autonomy bootstrap payload installed; experiment remains NOT STARTED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
