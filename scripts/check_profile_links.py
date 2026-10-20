from pathlib import Path
from urllib.parse import urlsplit, unquote
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

def local_target(source: Path, ref: str, root: Path):
    ref = ref.strip().strip("<>")
    if not ref or ref.startswith("#") or ref.startswith("//"):
        return None
    parsed = urlsplit(ref)
    if parsed.scheme or parsed.netloc or not parsed.path or parsed.path.startswith("/"):
        return None
    return (source.parent / unquote(parsed.path)).resolve()

def check_file(source: Path, root: Path = ROOT):
    body = source.read_text(encoding="utf-8")
    refs = re.findall(r"!{0,1}\[[^\]]*\]\(([^)]+)\)", body)
    refs += re.findall(r'(?:src|href)="([^"]+)"', body)
    errors = []
    for ref in refs:
        dest = local_target(source, ref, root)
        if dest is not None and (not dest.is_relative_to(root.resolve()) or not dest.exists()):
            errors.append(str(source.relative_to(root)) + ": invalid local link " + ref)
    return errors

def scan(root: Path = ROOT):
    sources = [root / "README.md"] + list((root / "writing").glob("*.md")) + list((root / "docs").glob("*.md"))
    return [error for file in sources if file.is_file() for error in check_file(file, root)]

if __name__ == "__main__":
    errors = scan()
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        sys.exit(1)
    print("Local profile documentation links resolve")
