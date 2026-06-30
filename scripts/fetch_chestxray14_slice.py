"""Fetch a small slice of real NIH ChestX-ray14 (Track-1 surrogate for the Vision Agent).

Downloads the official Kaggle NIH "sample" dataset (5,606 real images + labels) via `kagglehub`
and copies the first N images + a `Data_Entry_2017.csv` into `data/chestxray14/` in the schema
`ChestXray14Loader` (Card 1) reads. Open-licensed images; nothing is committed (data/ is gitignored).

Auth (first run only; the download is then cached): provide Kaggle creds via `~/.kaggle/kaggle.json`
or the `KAGGLE_USERNAME`/`KAGGLE_KEY` (or `KAGGLE_KEY` token) env vars. NEVER commit the token.

Run:  python scripts/fetch_chestxray14_slice.py    (env: NIH_SLICE_N, CHESTXRAY14_DIR)
"""

from __future__ import annotations

import csv
import os
import shutil
from pathlib import Path

import kagglehub

_COLUMNS = ["Image Index", "Finding Labels", "Patient ID", "Follow-up #"]


def main() -> None:
    n = int(os.environ.get("NIH_SLICE_N", "300"))
    out = Path(os.environ.get("CHESTXRAY14_DIR", "data/chestxray14"))
    (out / "images").mkdir(parents=True, exist_ok=True)

    base = Path(kagglehub.dataset_download("nih-chest-xrays/sample"))
    images_dir = next(p for p in base.rglob("images") if p.is_dir())
    labels_csv = next(base.rglob("sample_labels.csv"))

    rows: list[tuple[str, str, str, str]] = []
    with labels_csv.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if len(rows) >= n:
                break
            name = row["Image Index"]
            src = images_dir / name
            if not src.exists():
                continue
            shutil.copy(src, out / "images" / name)
            rows.append(
                (name, row["Finding Labels"], row["Patient ID"], row.get("Follow-up #", "0"))
            )

    with (out / "Data_Entry_2017.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(_COLUMNS)
        w.writerows(rows)
    print(f"wrote {len(rows)} images + Data_Entry_2017.csv to {out}")


if __name__ == "__main__":
    main()
