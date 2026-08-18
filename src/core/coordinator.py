"""Agent coordinator that manages multiple agents"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

from src.core.base_agent import BaseAgent
from src.core.config import CoordinatorConfig
from src.memory.manager import MemoryManager

logger = logging.getLogger(__name__)


class AgentCoordinator:
    """Coordinates multiple agents and orchestrates their interactions"""

    def __init__(self, config: CoordinatorConfig):
        """
        Initialize the agent coordinator

        Args:
            config: Coordinator configuration
        """
        self.config = config
        self.agents: Dict[str, BaseAgent] = {}
        self.coordinator_memory = MemoryManager(
            "coordinator",
            max_size=config.memory_max_size,
            persist_path=config.memory_persist_path,
        )
        self.created_at = datetime.now()
        self.interaction_log: List[Dict[str, Any]] = []

        logger.info("Initialized AgentCoordinator")

    def register_agent(self, agent: BaseAgent) -> None:
        """
        Register an agent with the coordinator

        Args:
            agent: Agent to register

        Raises:
            ValueError: If max agents reached or agent name already exists
        """
        if len(self.agents) >= self.config.max_agents:
            raise ValueError(
                f"Maximum number of agents ({self.config.max_agents}) reached"
            )

        if agent.config.name in self.agents:
            raise ValueError(f"Agent with name '{agent.config.name}' already registered")

        self.agents[agent.config.name] = agent
        logger.info(f"Registered agent: {agent.config.name}")

    def deregister_agent(self, agent_name: str) -> None:
        """
        Deregister an agent from the coordinator

        Args:
            agent_name: Name of agent to deregister
        """
        if agent_name in self.agents:
            del self.agents[agent_name]
            logger.info(f"Deregistered agent: {agent_name}")

    def get_agent(self, agent_name: str) -> Optional[BaseAgent]:
        """Get an agent by name"""
        return self.agents.get(agent_name)

    async def coordinate_task(
        self,
        task: str,
        primary_agent: str,
        supporting_agents: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Coordinate a task across multiple agents

        Args:
            task: Task description
            primary_agent: Name of primary agent to execute task
            supporting_agents: Names of agents that can support
            context: Additional context

        Returns:
            Result dictionary with outputs from each agent
        """
        if primary_agent not in self.agents:
            raise ValueError(f"Primary agent '{primary_agent}' not found")

        results = {
            "task": task,
            "timestamp": datetime.now().isoformat(),
            "primary_agent": primary_agent,
            "primary_result": None,
            "supporting_results": {},
            "coordinator_insights": None,
        }

        try:
            # Execute with primary agent
            agent = self.agents[primary_agent]
            primary_result = await agent.process(task, context)
            results["primary_result"] = primary_result

            # Execute with supporting agents if specified
            if supporting_agents:
                for agent_name in supporting_agents:
                    if agent_name in self.agents:
                        try:
                            support_agent = self.agents[agent_name]
                            support_result = await support_agent.process(task, context)
                            results["supporting_results"][agent_name] = support_result
                        except Exception as e:
                            logger.error(f"Error with supporting agent '{agent_name}': {e}")
                            results["supporting_results"][agent_name] = f"Error: {str(e)}"

            # Generate coordinator insights
            if self.config.enable_reasoning:
                insights = await self._generate_insights(results)
                results["coordinator_insights"] = insights

            # Log interaction
            self.interaction_log.append(results)

            # Store in memory
            if self.config.enable_agent_learning:
                await self._learn_from_interaction(results)

        except Exception as e:
            logger.error(f"Error during task coordination: {e}")
            results["error"] = str(e)

        return results

    async def _generate_insights(self, results: Dict[str, Any]) -> str:
        """Generate coordinator insights from results"""
        # This could use the coordinator's own reasoning engine
        return f"Processed task with {len(results.get('supporting_results', {}))} supporting agents"

    async def _learn_from_interaction(self, results: Dict[str, Any]) -> None:
        """Learn from agent interactions"""
        learning_content = (
            f"Task: {results['task']}\n"
            f"Primary Agent: {results['primary_agent']}\n"
            f"Success: {results.get('error') is None}"
        )
        self.coordinator_memory.store(learning_content)

    def get_status(self) -> Dict[str, Any]:
        """Get coordinator status"""
        return {
            "created_at": self.created_at.isoformat(),
            "total_agents": len(self.agents),
            "agent_names": list(self.agents.keys()),
            "total_tasks": len(self.interaction_log),
            "coordinator_memory_size": len(self.coordinator_memory),
            "enable_learning": self.config.enable_agent_learning,
            "enable_reasoning": self.config.enable_reasoning,
            "agents_status": {
                name: agent.get_status() for name, agent in self.agents.items()
            },
        }

    def list_agents(self) -> List[Dict[str, Any]]:
        """List all registered agents with their info"""
        return [agent.get_status() for agent in self.agents.values()]
