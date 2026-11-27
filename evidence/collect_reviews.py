"""Collect a Google Play review sample and flag candidates for D1 evidence."""

import argparse
import csv
import re
import socket
import sys
import unicodedata
from datetime import datetime, timedelta, timezone
from pathlib import Path


APPS = {"shopeefood": "com.deliverynow", "grab": "com.grabtaxi.passenger"}
LABELS = {
    "thieu_mon": (
        r"\b(?:thieu|sot|quen) (?:mat )?(?:mon|phan|suat|do an|thuc an|nuoc|topping)\b"
        r"|\b(?:giao|gui|nhan|don hang) (?:bi )?(?:thieu|khong du)\b"
        r"|\b(?:khong giao du|missing (?:food|items?|dishes?)|items? (?:is |are )?missing)\b"
    ),
    "giao_sai": (
        r"\b(?:giao|gui|nhan) (?:bi )?(?:sai|nham|lon) (?:mon|don|do|thuc an|phan|nuoc)\b"
        r"|\b(?:sai|nham|lon) (?:mon|don hang|do an)\b|\bwrong (?:order|item|food|dish)\b"
    ),
    "ho_tro_cham": (
        r"\b(?:cskh|cham soc khach hang|ho tro|khieu nai|phan hoi|hoan tien|support|refund)\b.{0,110}"
        r"\b(?:cham|lau|mai|khong (?:the |ai |co )?(?:tra loi|phan hoi|xu ly|lien he)|no response|slow)\b"
        r"|\b(?:cho|doi)\b.{0,70}\b(?:ho tro|phan hoi|xu ly|hoan tien)\b"
        r"|\b(?:khong thay|khong ai|khong co) (?:ho tro|phan hoi|tra loi)\b"
    ),
}
FIELDS = (
    "ma", "ngay_review", "sao", "ngay_lay", "uu_tien",
    "nhan_goi_y", "nhan_da_kiem", "noi_dung", "nguon",
)


def suggest_labels(content):
    plain = unicodedata.normalize("NFD", content.casefold().replace("đ", "d"))
    plain = "".join(char for char in plain if not unicodedata.combining(char))
    plain = re.sub(r"\s+", " ", plain)
    return [label for label, pattern in LABELS.items() if re.search(pattern, plain)]


def fetch_sample(app_id, sample_size):
    try:
        from google_play_scraper import Sort, reviews
    except ModuleNotFoundError as exc:
        raise RuntimeError("Cài thư viện bằng python -m pip install -r requirements.txt.") from exc

    # The scraper uses urllib internally and does not expose a timeout option.
    socket.setdefaulttimeout(20)
    sample = []
    seen = set()
    token = None
    for _ in range(25):
        batch, token = reviews(
            app_id, lang="vi", country="vn", sort=Sort.NEWEST, count=100,
            continuation_token=token,
        )
        if not batch:
            break

        for review in batch:
            review_id = review["reviewId"]
            content = (review.get("content") or "").strip()
            if review_id in seen or not content or review["score"] not in (1, 2, 3):
                continue
            seen.add(review_id)
            sample.append((review["at"], review["score"], content))
            if len(sample) == sample_size:
                return sample

    if not sample:
        raise RuntimeError("Google Play không trả review có chữ 1–3 sao. Thử lại hoặc chọn app kia.")
    return sample


def write_sample(path, sample, app_id, limit):
    source = f"https://play.google.com/store/apps/details?id={app_id}"
    collected_at = datetime.now(timezone(timedelta(hours=7))).isoformat(timespec="seconds")
    rows = []
    shortlisted = 0
    for index, (reviewed_at, stars, content) in enumerate(sample, start=1):
        labels = suggest_labels(content)
        priority = bool(labels) and shortlisted < limit
        shortlisted += priority
        # Keep review text inert when the CSV is opened in a spreadsheet.
        if content.startswith(("=", "+", "-", "@")):
            content = "'" + content
        rows.append({
            "ma": f"R{index:03}",
            "ngay_review": reviewed_at.date().isoformat() if reviewed_at else "",
            "sao": stars,
            "ngay_lay": collected_at,
            "uu_tien": int(priority),
            "nhan_goi_y": ";".join(labels),
            "nhan_da_kiem": "",
            "noi_dung": content,
            "nguon": source,
        })

    rows.sort(key=lambda row: row["uu_tien"], reverse=True)
    with path.open("x", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    return shortlisted


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app", choices=APPS, default="shopeefood")
    parser.add_argument("--sample", type=int, default=800, help="Số review 1–3 sao có chữ cần quét")
    parser.add_argument("--limit", type=int, default=30, help="Số review tối đa được đưa lên đầu")
    parser.add_argument("--output", type=Path, help="Đường dẫn CSV mới, nên bắt đầu bằng raw-")
    args = parser.parse_args()
    if not 1 <= args.limit <= args.sample <= 1200:
        parser.error("Cần 1 <= --limit <= --sample <= 1200.")

    path = args.output or Path(__file__).with_name(f"raw-reviews-{args.app}-{args.sample}.csv")
    try:
        if path.exists():
            raise FileExistsError(f"{path} đã tồn tại. Dùng --output để chọn tên file mới.")
        app_id = APPS[args.app]
        sample = fetch_sample(app_id, args.sample)
        shortlisted = write_sample(path, sample, app_id, args.limit)
    except (OSError, RuntimeError) as exc:
        print(f"Lỗi: {exc}", file=sys.stderr)
        return 1

    print(f"Đã lưu {len(sample)}/{args.sample} review 1–3 sao vào {path}.")
    print(f"Tìm thấy {shortlisted}/{args.limit} ứng viên ưu tiên. Kiểm nội dung và điền nhan_da_kiem.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
