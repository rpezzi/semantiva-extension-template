import os
import re

FORBIDDEN_TERMS = [
    "ima" "ging",
    "radi" "ology",
    "di" "com",
    "sc" "an",
    "mod" "ality",
    "pix" "el",
]

FORBIDDEN = re.compile(r"\b(" + "|".join(FORBIDDEN_TERMS) + r")\b", re.IGNORECASE)


def test_no_domain_terms_present():
    roots = ["template_extension", "tests", "pyproject.toml", "README.md"]
    offenders = []
    for root in roots:
        if not os.path.exists(root):
            continue
        if os.path.isdir(root):
            for dirpath, _, files in os.walk(root):
                if "__pycache__" in dirpath:
                    continue
                for f in files:
                    path = os.path.join(dirpath, f)
                    if os.path.abspath(path) == os.path.abspath(__file__):
                        continue
                    if f.endswith(
                        (
                            ".png",
                            ".jpg",
                            ".jpeg",
                            ".pdf",
                            ".bin",
                            ".npy",
                            ".npz",
                            ".gz",
                            ".xz",
                            ".zip",
                            ".ico",
                            ".icns",
                            ".svg",
                            ".pyc",
                        )
                    ):
                        continue
                    with open(path, "rb") as fh:
                        try:
                            text = fh.read().decode("utf-8", errors="ignore")
                        except Exception:
                            continue
                    if FORBIDDEN.search(text):
                        offenders.append(path)
        else:
            with open(root, "rb") as fh:
                text = fh.read().decode("utf-8", errors="ignore")
            if FORBIDDEN.search(text):
                offenders.append(root)

    assert not offenders, f"Forbidden domain terms found in: {offenders}"
