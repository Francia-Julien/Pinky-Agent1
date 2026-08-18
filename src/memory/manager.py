"""Memory management for agents"""

import logging
from typing import List, Optional
from datetime import datetime
import json
import os

logger = logging.getLogger(__name__)


class MemoryManager:
    """Manages agent memory with storage and retrieval capabilities"""

    def __init__(
        self,
        agent_name: str,
        enabled: bool = True,
        max_size: int = 50,
        persist_path: Optional[str] = None,
    ):
        """
        Initialize memory manager

        Args:
            agent_name: Name of the agent
            enabled: Whether memory is enabled
            max_size: Maximum number of memories to keep
            persist_path: Path to persist memory to disk
        """
        self.agent_name = agent_name
        self.enabled = enabled
        self.max_size = max_size
        self.persist_path = persist_path
        self.memories: List[dict] = []

        if persist_path and os.path.exists(persist_path):
            self._load_from_disk()

    def store(self, content: str) -> None:
        """
        Store content in memory

        Args:
            content: Content to store
        """
        if not self.enabled:
            return

        memory_item = {
            "timestamp": datetime.now().isoformat(),
            "content": content,
        }
        self.memories.append(memory_item)

        # Maintain max size
        if len(self.memories) > self.max_size:
            self.memories.pop(0)

        # Persist to disk if configured
        if self.persist_path:
            self._save_to_disk()

        logger.debug(f"Stored memory for {self.agent_name}: {content[:50]}...")

    def retrieve(self, query: str, k: int = 5) -> List[str]:
        """
        Retrieve relevant memories for a query

        Args:
            query: Query string
            k: Number of memories to retrieve

        Returns:
            List of relevant memory contents
        """
        if not self.enabled or not self.memories:
            return []

        # Simple keyword matching (can be enhanced with embeddings)
        query_lower = query.lower()
        relevant = []

        for memory in reversed(self.memories):  # Most recent first
            if any(
                word in memory["content"].lower()
                for word in query_lower.split()
                if len(word) > 2
            ):
                relevant.append(memory["content"])

            if len(relevant) >= k:
                break

        return relevant

    def clear(self) -> None:
        """Clear all memories"""
        self.memories.clear()
        if self.persist_path and os.path.exists(self.persist_path):
            os.remove(self.persist_path)
        logger.info(f"Cleared all memories for {self.agent_name}")

    def __len__(self) -> int:
        """Return number of stored memories"""
        return len(self.memories)

    def _save_to_disk(self) -> None:
        """Save memories to disk"""
        if not self.persist_path:
            return

        os.makedirs(os.path.dirname(self.persist_path), exist_ok=True)
        with open(self.persist_path, "w") as f:
            json.dump(self.memories, f)

    def _load_from_disk(self) -> None:
        """Load memories from disk"""
        if not self.persist_path or not os.path.exists(self.persist_path):
            return

        try:
            with open(self.persist_path, "r") as f:
                self.memories = json.load(f)
            logger.info(f"Loaded {len(self.memories)} memories from disk")
        except Exception as e:
            logger.error(f"Error loading memories from disk: {e}")
