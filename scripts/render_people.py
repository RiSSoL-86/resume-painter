import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")

import django  # noqa: E402

django.setup()

from django.template.loader import render_to_string  # noqa: E402

from services.api.analyses.schemas import Dashboard  # noqa: E402

PEOPLE = ROOT / "people"


def render_one(path: Path) -> None:
    """Validate one payload and render it to a sibling ``.html`` file."""
    dashboard = Dashboard.model_validate(json.loads(path.read_text("utf-8")))
    html = render_to_string(
        "analyses/dashboard.html",
        {"d": dashboard, "pending": False},
    )
    out = path.with_suffix(".html")
    out.write_text(html, encoding="utf-8")
    print(f"{path.name} -> {out.name}")


def main() -> None:
    """Render the given payloads, or every ``dashboard_*.json`` by default."""
    args = sys.argv[1:]
    paths = (
        [Path(arg) for arg in args]
        if args
        else sorted(PEOPLE.glob("dashboard_*.json"))
    )
    if not paths:
        print("No dashboard payloads found in people/.")
        return
    for path in paths:
        render_one(path)


if __name__ == "__main__":
    main()
