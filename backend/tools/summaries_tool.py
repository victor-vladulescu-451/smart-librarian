# backend/tools/summaries_tool.py
from __future__ import annotations
from functools import lru_cache
from typing import List, Optional, Tuple
import chromadb
from backend.settings import settings

try:
    from rapidfuzz import fuzz, process  # optional, faster
    _HAVE_RAPIDFUZZ = True
except Exception:
    _HAVE_RAPIDFUZZ = False
    from difflib import SequenceMatcher

@lru_cache(maxsize=1)
def _get_collection():
    client = chromadb.PersistentClient(path=settings.CHROMA_DIR)
    return client.get_collection(settings.CHROMA_COLLECTION)

@lru_cache(maxsize=1)
def _get_all_titles() -> List[str]:
    col = _get_collection()
    total = col.count()
    titles: List[str] = []
    step = max(1, settings.TITLES_PAGE_SIZE)

    try:
        for offset in range(0, total, step):
            batch = col.get(include=["metadatas"], limit=min(step, total - offset), offset=offset)
            for m in batch.get("metadatas") or []:
                t = (m or {}).get("title")
                if isinstance(t, str):
                    titles.append(t)
    except TypeError:
        # Fallback: one-shot fetch if offset unsupported
        batch = col.get(include=["metadatas"], limit=total)
        for m in batch.get("metadatas") or []:
            t = (m or {}).get("title")
            if isinstance(t, str):
                titles.append(t)

    return titles


def refresh_title_cache() -> None:
    """Call this after re-ingesting to rebuild the in-memory title list."""
    _get_all_titles.cache_clear()

def _suggest_titles(query: str, top_k: int = 3) -> List[str]:
    titles = _get_all_titles()
    if not titles:
        return []
    if _HAVE_RAPIDFUZZ:
        matches = process.extract(query, titles, scorer=fuzz.WRatio, limit=top_k)
        return [t for (t, _score, _idx) in matches]
    # fallback
    q = query.lower().strip()
    scored = [(SequenceMatcher(None, q, t.lower()).ratio(), t) for t in titles]
    scored.sort(reverse=True, key=lambda x: x[0])
    return [t for _, t in scored[:top_k]]

def get_summary_by_title(title: str) -> Tuple[Optional[str], List[str]]:
    """
    Returns (summary|None, suggestions). Exact match by metadata; else top-3 suggestions.
    """
    if not title or not title.strip():
        return None, []

    col = _get_collection()

    # Preferred: case-insensitive exact match if you store a normalized key at ingest (see below).
    # hit = col.get(where={settings.TITLE_NORM_KEY: title.lower().strip()}, include=["documents"], limit=1)

    # Current: case-sensitive exact match on 'title'
    hit = col.get(where={"title": title}, include=["documents"], limit=1)
    docs = hit.get("documents") or []
    if docs:
        return docs[0], []

    return None, _suggest_titles(title, top_k=3)
