from pathlib import Path

import pytest


def pytest_collection_modifyitems(items):
    """Mark Markdown-sensitive test modules as advisory prose contracts.

    Classification is intentionally conservative and module-level: if a test
    module references a Markdown file, every test collected from that module is
    treated as prose/document-contract coverage rather than core code coverage.
    """

    source_cache: dict[Path, str] = {}
    for item in items:
        path = Path(str(item.path))
        if path.suffix != ".py":
            continue
        source = source_cache.get(path)
        if source is None:
            source = path.read_text(encoding="utf-8")
            source_cache[path] = source
        if ".md" in source:
            item.add_marker(pytest.mark.prose_contract)
