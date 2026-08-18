"""Base agent class that all agents inherit from"""

import logging
from typing import Any, Optional, Dict, List
from abc import ABC
from datetime import datetime

from langchain_anthropic import ChatAnthropic
from langchain_core.tools import Tool

from src.core.config import AgentConfig
from src.memory.manager import MemoryManager
from src.reasoning.engine import ReasoningEngine

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Base class for all agents in the system"""

    def __init__(
        self,
        config: AgentConfig,
        api_key: str,
        tools: Optional[List[Tool]] = None,
    ):
        """
        Initialize the base agent

        Args:
            config: Agent configuration
            api_key: Anthropic API key
            tools: List of tools the agent can use
        """
        self.config = config
        self.api_key = api_key
        self.tools = tools or []
        self.memory = MemoryManager(config.name, enabled=config.enable_memory)
        self.reasoning_engine = ReasoningEngine(depth=config.reasoning_depth)

        # Initialize LLM
        self.llm = ChatAnthropic(
            api_key=api_key,
            model=config.model,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
        )

        # Agent state tracking
        self.execution_history: List[Dict[str, Any]] = []
        self.created_at = datetime.now()

        logger.info(f"Initialized agent: {config.name}")

    def add_tool(self, tool: Tool) -> None:
        """Add a tool to the agent"""
        self.tools.append(tool)
        logger.debug(f"Added tool '{tool.name}' to agent '{self.config.name}'")

    def add_tools(self, tools: List[Tool]) -> None:
        """Add multiple tools to the agent"""
        self.tools.extend(tools)
        logger.debug(f"Added {len(tools)} tools to agent '{self.config.name}'")

    async def process(self, input_text: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Default agent processing flow.

        Subclasses can override this method with specialized logic.
        """
        prompt = input_text
        if self.config.system_prompt:
            prompt = f"{self.config.system_prompt}\n\n{input_text}"

        try:
            response = await self.llm.ainvoke(prompt)
            output = response.content if hasattr(response, "content") else str(response)
            self.learn_from_execution(input_text, output, success=True)
            return output
        except Exception as e:
            logger.error(f"Error in BaseAgent.process: {e}")
            self.learn_from_execution(input_text, str(e), success=False)
            return f"Error: {str(e)}"

    async def reason_about(self, problem: str) -> str:
        """
        Use the reasoning engine to work through a problem

        Args:
            problem: Problem to reason about

        Returns:
            Reasoning result
        """
        if not self.config.enable_reasoning:
            return "Reasoning is disabled for this agent"

        return await self.reasoning_engine.reason(problem, self.llm)

    def get_memory_context(self, query: str, k: int = 5) -> str:
        """
        Retrieve relevant memories for a query

        Args:
            query: Query to search for
            k: Number of memories to retrieve

        Returns:
            Memory context as string
        """
        memories = self.memory.retrieve(query, k=k)
        if not memories:
            return "No relevant memories found."
        return "\n".join(memories)

    def store_memory(self, content: str) -> None:
        """
        Store content in agent memory

        Args:
            content: Content to store
        """
        self.memory.store(content)

    def learn_from_execution(self, input_text: str, output: str, success: bool) -> None:
        """
        Learn from an execution result

        Args:
            input_text: Original input
            output: Execution output
            success: Whether execution was successful
        """
        execution_record = {
            "timestamp": datetime.now().isoformat(),
            "input": input_text,
            "output": output,
            "success": success,
        }
        self.execution_history.append(execution_record)

        # Store successful executions in memory
        if success:
            memory_content = f"Successful execution: Input '{input_text}' -> Output '{output}'"
            self.store_memory(memory_content)

    def get_status(self) -> Dict[str, Any]:
        """Get agent status and statistics"""
        successful_executions = sum(
            1 for e in self.execution_history if e.get("success", False)
        )

        return {
            "name": self.config.name,
            "model": self.config.model,
            "tools_count": len(self.tools),
            "created_at": self.created_at.isoformat(),
            "total_executions": len(self.execution_history),
            "successful_executions": successful_executions,
            "memory_size": len(self.memory),
            "enable_reasoning": self.config.enable_reasoning,
            "enable_memory": self.config.enable_memory,
        }
