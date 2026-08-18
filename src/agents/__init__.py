"""Example agents using the framework"""

from typing import Any, Optional, Dict
import logging

from src.core.base_agent import BaseAgent
from src.core.config import AgentConfig

logger = logging.getLogger(__name__)


class ResearchAgent(BaseAgent):
    """Agent specialized in research and information gathering"""

    def __init__(self, api_key: str, **kwargs):
        config = AgentConfig(
            name="ResearchAgent",
            system_prompt="You are a research expert. Help gather and analyze information.",
            enable_reasoning=True,
            enable_memory=True,
            **kwargs,
        )
        super().__init__(config, api_key)

    async def process(
        self, input_text: str, context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Process research request"""
        # Get relevant memories
        memory_context = self.get_memory_context(input_text)

        # Build prompt
        prompt = f"""Research Request: {input_text}

Relevant Past Research:
{memory_context}

Please provide a comprehensive research response."""

        # Generate response
        try:
            response = await self.llm.ainvoke(prompt)
            output = response.content if hasattr(response, "content") else str(response)

            # Learn from execution
            self.learn_from_execution(input_text, output, success=True)
            return output

        except Exception as e:
            logger.error(f"Error in ResearchAgent: {e}")
            self.learn_from_execution(input_text, str(e), success=False)
            return f"Error: {str(e)}"


class AnalysisAgent(BaseAgent):
    """Agent specialized in data analysis and insights"""

    def __init__(self, api_key: str, **kwargs):
        config = AgentConfig(
            name="AnalysisAgent",
            system_prompt="You are a data analysis expert. Provide deep insights.",
            enable_reasoning=True,
            enable_memory=True,
            reasoning_depth=4,
            **kwargs,
        )
        super().__init__(config, api_key)

    async def process(
        self, input_text: str, context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Process analysis request"""
        # Use reasoning for complex analysis
        if context and context.get("use_reasoning"):
            reasoning_result = await self.reason_about(input_text)
            prompt = f"""Based on this reasoning:
{reasoning_result}

Please provide your analysis."""
        else:
            prompt = f"Please analyze: {input_text}"

        try:
            response = await self.llm.ainvoke(prompt)
            output = response.content if hasattr(response, "content") else str(response)

            self.learn_from_execution(input_text, output, success=True)
            return output

        except Exception as e:
            logger.error(f"Error in AnalysisAgent: {e}")
            self.learn_from_execution(input_text, str(e), success=False)
            return f"Error: {str(e)}"


class PlannningAgent(BaseAgent):
    """Agent specialized in planning and coordination"""

    def __init__(self, api_key: str, **kwargs):
        config = AgentConfig(
            name="PlanningAgent",
            system_prompt="You are a planning expert. Break down tasks into actionable steps.",
            enable_reasoning=True,
            enable_memory=True,
            reasoning_depth=5,
            **kwargs,
        )
        super().__init__(config, api_key)

    async def process(
        self, input_text: str, context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Process planning request"""
        prompt = f"""Create a detailed plan for: {input_text}

Include:
1. Objective analysis
2. Key steps
3. Required resources
4. Success metrics
5. Risk mitigation"""

        try:
            response = await self.llm.ainvoke(prompt)
            output = response.content if hasattr(response, "content") else str(response)

            self.learn_from_execution(input_text, output, success=True)
            return output

        except Exception as e:
            logger.error(f"Error in PlanningAgent: {e}")
            self.learn_from_execution(input_text, str(e), success=False)
            return f"Error: {str(e)}"
