import unittest

from openleet.videos import CREATORS, Video, explains, most_viewed, names, numbers, pick

NEETCODE_ID = CREATORS[0][1][0]
GREG_ID = CREATORS[1][1][0]


def video(title: str, channel_id: str = "UCother", views: int = 1, seconds: int = 600) -> Video:
    return Video(f"id-{title}-{channel_id}", title, "Someone", channel_id, views, seconds)


class VideosTest(unittest.TestCase):
    def test_numbers(self) -> None:
        assert numbers("Two Sum - Leetcode 1 - HashMap - Python") == {1}
        assert numbers("N Queens I + N Queens II - LeetCode 51 + Leetcode 52") == {51, 52}
        assert numbers("Leetcode | 1. Two Sum | Easy | Java Solution") == {1}
        assert numbers("Word Search II | DFS + TRIE | Leetcode #212") == {212}
        assert numbers("Two Sum explained") == set()

    def test_names_needs_the_whole_title(self) -> None:
        assert names("Two Sum - Leetcode 1 - HashMap", "Two Sum")
        assert names("LeetCode 1. Two Sum (Algorithm Explained)", "Two Sum")
        assert not names("Two Sum II - Input Array Is Sorted", "Two Sum")
        assert not names(
            "Best Time to Buy and Sell Stock with Cooldown - Leetcode 309",
            "Best Time to Buy and Sell Stock",
        )
        assert names(
            "Two Sum II - Input Array Is Sorted - Leetcode 167",
            "Two Sum II - Input Array Is Sorted",
        )

    def test_trusted_channels_match_by_number_or_title(self) -> None:
        assert explains(video("Candy - Leetcode 135 - Python"), 135, "Candy", trusted=True)
        assert explains(video("Jump Game - Greedy"), 55, "Jump Game", trusted=True)
        assert not explains(video("Jump Game II - Leetcode 45"), 55, "Jump Game", trusted=True)

    def test_others_need_number_and_words_or_title_and_leetcode(self) -> None:
        assert explains(video("Two Sum (LeetCode #1) | 3 Solutions"), 1, "Two Sum", trusted=False)
        assert not explains(video("LeetCode 75 study plan"), 75, "Sort Colors", trusted=False)
        assert explains(video("Sort Colors | Leetcode explained"), 75, "Sort Colors", trusted=False)
        assert not explains(video("Sort Colors for kids"), 75, "Sort Colors", trusted=False)

    def test_only_creator_shorts_match_and_longer_videos_come_first(self) -> None:
        short = video("Candy - Leetcode 135", seconds=58, views=1_000)
        assert explains(short, 135, "Candy", trusted=True)
        assert not explains(short, 135, "Candy", trusted=False)
        longer = video("Candy - Leetcode 135 - Python", views=10)
        assert most_viewed([short, longer]) == longer

    def test_pick_orders_creators_and_takes_the_most_viewed(self) -> None:
        problem = {"id": 1, "slug": "two-sum", "title": "Two Sum"}
        found = [
            video("Two Sum - Leetcode 1", "UCa", views=10),
            video("Two Sum | LeetCode 1", "UCb", views=500),
            video("Two Sum - Leetcode 1 - Python", GREG_ID, views=50),
            video("Two Sum II - Leetcode 167", "UCc", views=10_000),
        ]
        neetcode_video = video("Two Sum - Leetcode 1 - HashMap", NEETCODE_ID, views=9)
        channels = {c: [] for _, ids in CREATORS for c in ids}
        chosen = list(
            pick(
                problem,
                found,
                channels,
                {"two-sum": neetcode_video.id},
                {neetcode_video.id: neetcode_video},
            )
        )
        assert [v["creator"] for v in chosen] == ["NeetCode", "Greg Hogg", "Someone"]
        assert chosen[0]["id"] == neetcode_video.id
        assert chosen[2]["title"] == "Two Sum | LeetCode 1"
