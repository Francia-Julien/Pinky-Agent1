"""Tests for the agent system"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from src.core.config import AgentConfig, CoordinatorConfig
from src.core.base_agent import BaseAgent
from src.core.coordinator import AgentCoordinator
from src.memory.manager import MemoryManager


class TestMemoryManager:
    """Test memory manager"""

    def test_memory_store_and_retrieve(self):
        """Test storing and retrieving memories"""
        memory = MemoryManager("test_agent", enabled=True, max_size=10)
        
        memory.store("Test memory 1")
        memory.store("Test memory 2")
        
        assert len(memory) == 2

    def test_memory_retrieve_query(self):
        """Test memory retrieval with query"""
        memory = MemoryManager("test_agent", enabled=True)
        
        memory.store("The quick brown fox jumps")
        memory.store("The lazy dog sleeps")
        
        results = memory.retrieve("fox", k=5)
        assert len(results) > 0
        assert "fox" in results[0].lower()

    def test_memory_disabled(self):
        """Test memory when disabled"""
        memory = MemoryManager("test_agent", enabled=False)
        
        memory.store("This should not be stored")
        assert len(memory) == 0

    def test_memory_max_size(self):
        """Test memory respects max size"""
        memory = MemoryManager("test_agent", max_size=3)
        
        for i in range(5):
            memory.store(f"Memory {i}")
        
        assert len(memory) <= 3


class TestAgentConfig:
    """Test agent configuration"""

    def test_agent_config_creation(self):
        """Test creating agent config"""
        config = AgentConfig(
            name="TestAgent",
            temperature=0.5,
            max_tokens=2000,
        )
        
        assert config.name == "TestAgent"
        assert config.temperature == 0.5
        assert config.max_tokens == 2000

    def test_agent_config_validation(self):
        """Test agent config validation"""
        with pytest.raises(ValueError):
            AgentConfig(
                name="TestAgent",
                temperature=3.0,  # Invalid: must be <= 2.0
            )


class TestCoordinator:
    """Test agent coordinator"""

    @pytest.fixture
    def coordinator(self):
        """Create coordinator instance"""
        config = CoordinatorConfig(
            anthropic_api_key="test_key",
            max_agents=5,
        )
        return AgentCoordinator(config)

    def test_coordinator_initialization(self, coordinator):
        """Test coordinator initialization"""
        assert len(coordinator.agents) == 0
        assert coordinator.config.max_agents == 5

    def test_register_agent(self, coordinator):
        """Test registering an agent"""
        # Create mock agent
        mock_agent = Mock(spec=BaseAgent)
        mock_agent.config = AgentConfig(name="TestAgent")
        
        coordinator.register_agent(mock_agent)
        
        assert "TestAgent" in coordinator.agents
        assert coordinator.agents["TestAgent"] == mock_agent

    def test_register_duplicate_agent(self, coordinator):
        """Test error on duplicate agent registration"""
        mock_agent = Mock(spec=BaseAgent)
        mock_agent.config = AgentConfig(name="TestAgent")
        
        coordinator.register_agent(mock_agent)
        
        with pytest.raises(ValueError):
            coordinator.register_agent(mock_agent)

    def test_max_agents_limit(self, coordinator):
        """Test max agents limit"""
        for i in range(5):
            mock_agent = Mock(spec=BaseAgent)
            mock_agent.config = AgentConfig(name=f"Agent{i}")
            coordinator.register_agent(mock_agent)
        
        # Try to add one more - should fail
        mock_agent = Mock(spec=BaseAgent)
        mock_agent.config = AgentConfig(name="ExtraAgent")
        
        with pytest.raises(ValueError):
            coordinator.register_agent(mock_agent)

    def test_deregister_agent(self, coordinator):
        """Test deregistering an agent"""
        mock_agent = Mock(spec=BaseAgent)
        mock_agent.config = AgentConfig(name="TestAgent")
        
        coordinator.register_agent(mock_agent)
        assert len(coordinator.agents) == 1
        
        coordinator.deregister_agent("TestAgent")
        assert len(coordinator.agents) == 0

    def test_get_coordinator_status(self, coordinator):
        """Test getting coordinator status"""
        mock_agent = Mock(spec=BaseAgent)
        mock_agent.config = AgentConfig(name="TestAgent")
        mock_agent.get_status = Mock(return_value={"name": "TestAgent"})
        
        coordinator.register_agent(mock_agent)
        
        status = coordinator.get_status()
        
        assert status["total_agents"] == 1
        assert "TestAgent" in status["agent_names"]


class TestBaseAgentMemory:
    """Test base agent memory functionality"""

    @pytest.mark.asyncio
    async def test_agent_memory_storage(self):
        """Test agent can store and retrieve memories"""
        config = AgentConfig(name="TestAgent", enable_memory=True)
        
        # Mock the LLM
        mock_llm = AsyncMock()
        
        agent = BaseAgent(config, "test_key")
        agent.llm = mock_llm
        
        agent.store_memory("Test memory content")
        
        memories = agent.memory.retrieve("Test", k=1)
        assert len(memories) > 0

    @pytest.mark.asyncio
    async def test_agent_learning(self):
        """Test agent learning from executions"""
        config = AgentConfig(name="TestAgent")
        agent = BaseAgent(config, "test_key")
        
        agent.learn_from_execution("input", "output", success=True)
        
        assert len(agent.execution_history) == 1
        assert agent.execution_history[0]["success"] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
