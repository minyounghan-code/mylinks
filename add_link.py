"""멀티링크 페이지에 상품 링크 블럭을 추가한다 (최신이 맨 위).

사용:
    python add_link.py --title "허리 넥밴드 선풍기" --url "https://link.coupang.com/a/xxxx" --note "아빠 여름 선물"

--push 를 붙이면 git commit + push까지 수행 (GitHub Pages 자동 반영).
"""
import argparse
import datetime
import json
import subprocess
import sys
from pathlib import Path

LINKS = Path(__file__).parent / "links.json"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--title", required=True)
    p.add_argument("--url", required=True)
    p.add_argument("--note", default="")
    p.add_argument("--push", action="store_true", help="git commit + push")
    args = p.parse_args()

    data = json.loads(LINKS.read_text(encoding="utf-8"))

    if any(l["url"] == args.url for l in data["links"]):
        print(f"이미 등록된 링크: {args.url}")
        sys.exit(0)

    data["links"].insert(0, {
        "title": args.title,
        "url": args.url,
        "note": args.note,
        "date": datetime.date.today().isoformat(),
    })
    LINKS.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"추가됨: {args.title} (총 {len(data['links'])}개)")

    if args.push:
        repo = Path(__file__).parent
        subprocess.run(["git", "add", "links.json"], cwd=repo, check=True)
        subprocess.run(["git", "commit", "-m", f"link: {args.title}"], cwd=repo, check=True)
        subprocess.run(["git", "push"], cwd=repo, check=True)
        print("push 완료 — GitHub Pages에 곧 반영됩니다.")


if __name__ == "__main__":
    main()
