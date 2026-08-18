
import asyncio
import logging
import sys
from dotenv import load_dotenv
import os

from src.core.config import CoordinatorConfig, AgentConfig
from src.core.coordinator import AgentCoordinator
from src.agents import ResearchAgent, AnalysisAgent, PlannningAgent
from src.tools import get_default_tools

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


async def main():
    """Main function demonstrating the multi-agent system"""

    # Load configuration from environment
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        logger.error("ANTHROPIC_API_KEY not found in .env file")
        sys.exit(1)

    # Initialize coordinator
    coordinator_config = CoordinatorConfig(
        anthropic_api_key=api_key,
        max_agents=10,
        enable_agent_learning=True,
        enable_reasoning=True,
    )

    coordinator = AgentCoordinator(coordinator_config)
    logger.info("Initialized AgentCoordinator")

    # Create example agents
    try:
        research_agent = ResearchAgent(api_key)
        analysis_agent = AnalysisAgent(api_key)
        planning_agent = PlannningAgent(api_key)

        # Add default tools to agents
        default_tools = get_default_tools()
        research_agent.add_tools(default_tools)
        analysis_agent.add_tools(default_tools)
        planning_agent.add_tools(default_tools)

        # Register agents with coordinator
        coordinator.register_agent(research_agent)
        coordinator.register_agent(analysis_agent)
        coordinator.register_agent(planning_agent)

        logger.info(f"Registered {len(coordinator.agents)} agents")

        # Example 1: Single agent task
        logger.info("\n--- Example 1: Single Agent Task ---")
        task = "What are the latest trends in artificial intelligence?"
        result = await research_agent.process(task)
        logger.info(f"Research Agent Result:\n{result[:500]}...")

        # Example 2: Coordinated task with multiple agents
        logger.info("\n--- Example 2: Coordinated Multi-Agent Task ---")
        coord_task = "Analyze the impact of AI on software development"
        coord_result = await coordinator.coordinate_task(
            task=coord_task,
            primary_agent="ResearchAgent",
            supporting_agents=["AnalysisAgent"],
            context={"use_reasoning": True},
        )
        logger.info(f"Coordinator Result: {coord_result}")

        # Example 3: Planning task
        logger.info("\n--- Example 3: Planning Task ---")
        planning_task = "Create a roadmap for building an AI agent system"
        plan = await planning_agent.process(planning_task)
        logger.info(f"Planning Result:\n{plan[:500]}...")

        # Print system status
        logger.info("\n--- System Status ---")
        status = coordinator.get_status()
        logger.info(f"Coordinator Status: {status}")

    except Exception as e:
        logger.error(f"Error in main: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
