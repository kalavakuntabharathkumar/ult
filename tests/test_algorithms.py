from collections import Counter
from logtriage.algorithms import PrefixTrie, top_k, group_prefixes

def test_top_k_and_prefixes():
    c = Counter({"database timeout": 7, "database refused": 4, "payment failed": 3})
    assert top_k(c, 2) == [("database timeout", 7), ("database refused", 4)]
    assert group_prefixes(c, 1)["database"] == 11

def test_trie_prefix_count():
    t = PrefixTrie()
    t.add("database connection timeout", 3)
    t.add("database connection refused", 2)
    assert t.prefix_count("database connection") == 5
