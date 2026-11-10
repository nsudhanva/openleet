"""The names LeetCode's Python 3 environment gives every solution, plus its node classes.

User code runs with this module's globals (copied), so `List`, `deque`, `heappush`, `inf`,
`SortedList`, `ListNode`, `TreeNode` and friends work without imports, as on LeetCode.
"""

import bisect
import collections
import functools
import heapq
import itertools
import math
import operator
import random
import re
import string
import sys
from bisect import *  # noqa: F403
from collections import *  # noqa: F403
from functools import *  # noqa: F403
from heapq import *  # noqa: F403
from itertools import *  # noqa: F403
from math import *  # noqa: F403
from operator import *  # noqa: F403
from string import *  # noqa: F403
from typing import *  # noqa: F403

import sortedcontainers
from sortedcontainers import SortedDict, SortedList, SortedSet

__all__ = [
    "ListNode",
    "Node",
    "SortedDict",
    "SortedList",
    "SortedSet",
    "TreeNode",
    "bisect",
    "collections",
    "functools",
    "heapq",
    "itertools",
    "math",
    "operator",
    "random",
    "re",
    "sortedcontainers",
    "string",
    "sys",
]


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __repr__(self):
        return f"ListNode({self.val})"


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return f"TreeNode({self.val})"


class Node:
    """LeetCode reuses the name `Node` for several shapes; this one accepts all their fields."""

    def __init__(
        self,
        val=0,
        left=None,
        right=None,
        next=None,
        random=None,
        children=None,
        neighbors=None,
        prev=None,
        child=None,
    ):
        self.val = val
        self.left = left
        self.right = right
        self.next = next
        self.random = random
        self.children = children if children is not None else []
        self.neighbors = neighbors if neighbors is not None else []
        self.prev = prev
        self.child = child

    def __repr__(self):
        return f"Node({self.val})"


def namespace() -> dict:
    """A fresh copy of the globals a solution sees."""
    hidden = {"namespace", "__all__", "__doc__", "__file__", "__loader__", "__spec__", "__cached__"}
    names = {k: v for k, v in globals().items() if k not in hidden}
    names["__name__"] = "solution"
    return names
