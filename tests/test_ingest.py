import unittest

from openleet.ingest import front_matter


class IngestTests(unittest.TestCase):
    def test_front_matter_stops_tags_at_the_next_top_level_key_and_unquotes_values(self):
        markdown = """---
difficulty: "Medium"
tags:
  - "Array"
  - 'Graph''s Algorithm'
other: value
  - Not a tag
---
"""

        self.assertEqual(front_matter(markdown), ("Medium", ["Array", "Graph's Algorithm"]))
