import json
from functools import lru_cache
from pathlib import Path

_BRAND_DIR = Path(__file__).parent
_COMPANIES_FILE = _BRAND_DIR / "companies.json"
_TECHNOLOGIES_FILE = _BRAND_DIR / "technologies.json"


def _normalize(value: str) -> str:
    """Lowercase and trim so labels/aliases match regardless of case."""
    return value.strip().lower()


def _build_index(path: Path) -> dict[str, str]:
    """Map slug, display name and every alias to the entry's icon URL."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    index: dict[str, str] = {}
    for slug, entry in raw.items():
        if slug.startswith("_"):
            continue
        icon = entry.get("icon_url")
        if not icon:
            continue
        keys = [slug, entry.get("name", ""), *entry.get("aliases", [])]
        for key in keys:
            if key:
                index[_normalize(key)] = icon
    return index


@lru_cache(maxsize=1)
def _company_index() -> dict[str, str]:
    return _build_index(_COMPANIES_FILE)


@lru_cache(maxsize=1)
def _technology_index() -> dict[str, str]:
    return _build_index(_TECHNOLOGIES_FILE)


@lru_cache(maxsize=1)
def _company_catalog() -> tuple[dict[str, object], ...]:
    """Renderable companies with slug, name, category, aliases and icon."""
    raw = json.loads(_COMPANIES_FILE.read_text(encoding="utf-8"))
    catalog: list[dict[str, object]] = []
    for slug, entry in raw.items():
        if slug.startswith("_"):
            continue
        icon = entry.get("icon_url")
        if not icon:
            continue
        catalog.append(
            {
                "slug": slug,
                "name": entry.get("name", slug),
                "category": entry.get("category"),
                "aliases": list(entry.get("aliases", [])),
                "icon_url": icon,
            }
        )
    return tuple(catalog)


def company_catalog() -> tuple[dict[str, object], ...]:
    """List of companies we can render a badge for (slug + labels + icon)."""
    return _company_catalog()


def company_icon(label: str | None) -> str | None:
    """Icon URL for a company label/alias, or None if unknown."""
    if not label:
        return None
    return _company_index().get(_normalize(label))


def technology_icon(label: str | None) -> str | None:
    """Icon URL for a technology label/alias, or None if unknown."""
    if not label:
        return None
    return _technology_index().get(_normalize(label))
