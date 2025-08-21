# tests/test_summaries_tool.py
from backend.tools.summaries_tool import get_summary_by_title, refresh_title_cache

def setup_module():
    # Make sure cached titles are rebuilt after ingestion
    refresh_title_cache()

def test_exact_title():
    title = "The Catcher in the Rye"   # choose a book you know exists in your collection
    summary, suggestions = get_summary_by_title(title)
    print("\n--- Exact Title Test ---")
    print(f"Query: {title}")
    print(f"Summary: {summary}")
    print(f"Suggestions: {suggestions}")
    assert summary is not None
    assert suggestions == []

def test_suggestions():
    title = "the something in the eye "  # deliberately not exact to trigger suggestions
    summary, suggestions = get_summary_by_title(title)
    print("\n--- Suggestions Test ---")
    print(f"Query: {title}")
    print(f"Summary: {summary}")
    print(f"Suggestions: {suggestions}")
    assert summary is None
    assert len(suggestions) > 0
