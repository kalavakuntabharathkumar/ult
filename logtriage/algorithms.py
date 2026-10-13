from collections import Counter
from dataclasses import dataclass, field
import heapq

@dataclass
class Node:
    children: dict = field(default_factory=dict)
    count: int = 0

class PrefixTrie:
    def __init__(self):
        self.root = Node()

    def add(self, phrase, count=1):
        node = self.root
        for token in phrase.split():
            node = node.children.setdefault(token, Node())
            node.count += count

    def prefix_count(self, prefix):
        node = self.root
        for token in prefix.split():
            if token not in node.children:
                return 0
            node = node.children[token]
        return node.count

def top_k(counter, k=10):
    if k <= 0:
        return []
    return heapq.nlargest(k, counter.items(), key=lambda item: (item[1], item[0]))

def group_prefixes(counter, depth=2):
    groups = Counter()
    for pattern, count in counter.items():
        groups[" ".join(pattern.split()[:max(1, depth)]) or "<empty>"] += count
    return dict(groups)
