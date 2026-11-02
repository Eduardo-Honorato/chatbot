"""Documentation search module."""

import os
from typing import List, Dict


class DocumentationIndex:
    """Simple search index for documentation files."""

    def __init__(self, docs_path: str = "docs/"):
        self.docs_path = docs_path
        self.index: Dict[str, str] = {}
        self._build_index()

    def _build_index(self):
        """Build search index from local docs."""
        if os.path.exists(self.docs_path):
            for f in os.listdir(self.docs_path):
                fp = os.path.join(self.docs_path, f)
                if os.path.isfile(fp):
                    try:
                        with open(fp, 'r', encoding='utf-8', errors='replace') as cf:
                            self.index[f] = cf.read()[:500]
                    except Exception:
                        pass

    def search(self, query: str) -> List[Dict[str, str]]:
        """Search for query in indexed docs."""
        if not query:
            return []
        query_lower = query.lower()
        results = []
        for filename, content in self.index.items():
            if query_lower in content.lower():
                results.append({"file": filename, "excerpt": content[:200]})
        return results