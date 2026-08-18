"""Reasoning engine for agents"""

import logging
from typing import Optional
from langchain_core.language_models import BaseLanguageModel

logger = logging.getLogger(__name__)


class ReasoningEngine:
    """Engine for complex reasoning tasks"""

    def __init__(self, depth: int = 3):
        """
        Initialize reasoning engine

        Args:
            depth: Depth of reasoning steps
        """
        self.depth = depth

    async def reason(self, problem: str, llm: BaseLanguageModel) -> str:
        """
        Reason through a problem using chain-of-thought

        Args:
            problem: Problem to reason about
            llm: Language model to use

        Returns:
            Reasoning result
        """
        reasoning_prompt = f"""You are an expert reasoner. Work through this problem step by step.

Problem: {problem}

Provide {self.depth} levels of reasoning:
1. First, identify the key components
2. Then, analyze relationships
3. Finally, synthesize a solution

Be thorough and explicit in your reasoning."""

        result = await llm.ainvoke(reasoning_prompt)
        return result.content if hasattr(result, "content") else str(result)

    async def compare_solutions(
        self, problem: str, solutions: list, llm: BaseLanguageModel
    ) -> str:
        """
        Compare multiple solutions and select the best

        Args:
            problem: Original problem
            solutions: List of proposed solutions
            llm: Language model to use

        Returns:
            Analysis of solutions
        """
        solutions_text = "\n".join(f"{i+1}. {sol}" for i, sol in enumerate(solutions))

        comparison_prompt = f"""Compare these solutions to the problem:

Problem: {problem}

Solutions:
{solutions_text}

Analyze each solution's strengths and weaknesses, then recommend the best one."""

        result = await llm.ainvoke(comparison_prompt)
        return result.content if hasattr(result, "content") else str(result)
