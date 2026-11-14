import unittest

from lib import normalize, open_sources, pipeline, health


class OpenSourceRegistryTests(unittest.TestCase):
    def test_sources_are_registered_and_capable(self):
        expected = {"arxiv_atom", "semantic_scholar", "crossref", "huggingface", "github_api", "openreview"}
        self.assertTrue(expected.issubset(set(pipeline.MOCK_AVAILABLE_SOURCES)))
        self.assertTrue(expected.issubset(set(pipeline.available_sources({}))))

    def test_open_source_items_use_shared_normalization(self):
        raw = [{"title": "Agent evaluation", "url": "https://example.org/paper", "snippet": "A paper", "date": "2026-11-10"}]
        for source in ("arxiv_atom", "semantic_scholar", "crossref", "huggingface", "github_api", "openreview"):
            items = normalize.normalize_source_items(source, raw, "2026-10-15", "2026-11-14")
            self.assertEqual(len(items), 1)
            self.assertEqual(items[0].source, source)

    def test_parse_does_not_trust_non_items(self):
        self.assertEqual(open_sources.parse({"results": [None, {"title": "ok"}]}, "crossref")[0]["title"], "ok")

    def test_health_score_marks_degraded_sources(self):
        class Outcome:
            def __init__(self, state): self.state = state
        result = health.source_health_score({"tavily": Outcome(health.OK), "reddit": Outcome(health.RATE_LIMITED)}, {"tavily": 2, "reddit": 0})
        self.assertEqual(result["score"], 50)
        self.assertEqual(result["degraded"], ["reddit"])


if __name__ == "__main__":
    unittest.main()
