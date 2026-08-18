"""Documentation for the Pinky Agent System"""

# Pinky Agent - Multi-Agent System Coordinator

A production-ready, extensible multi-agent system built with LangChain and Claude AI. Pinky Agent enables coordination of multiple specialized AI agents for complex tasks.

## Features

- **Multi-Agent Coordination**: Orchestrate multiple specialized agents for complex workflows
- **Intelligent Memory**: Persistent memory system with retrieval for agents and coordinator
- **Reasoning Engine**: Built-in chain-of-thought reasoning capabilities
- **Tool Integration**: Easy tool/function definition and agent binding
- **Learning Adaptation**: Agents learn from past executions and improve over time
- **Async/Await**: Full async support for concurrent agent operations
- **Type Safety**: Built with Pydantic for configuration and type validation
- **Production Ready**: Comprehensive error handling, logging, and testing

## Architecture

```
┌─────────────────────────────────────────────┐
│         Agent Coordinator                    │
│  - Orchestrates multiple agents              │
│  - Manages interactions                      │
│  - Coordinates complex tasks                 │
└──────────────┬──────────────────────────────┘
               │
    ┌──────────┼──────────┐
    │          │          │
┌───▼──┐  ┌───▼──┐  ┌───▼──┐
│Agent1│  │Agent2│  │Agent3│
└─┬────┘  └─┬────┘  └─┬────┘
  │         │        │
  ├─Memory  ├─Memory ├─Memory
  ├─Tools   ├─Tools  ├─Tools
  └─Brain   └─Brain  └─Brain
```

## Installation

1. Clone the repository:
```bash
git clone <repo-url>
cd Pinky-Agent1
```

2. Create a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

## Quick Start

### Basic Usage

```python
import asyncio
from src.core.config import CoordinatorConfig
from src.core.coordinator import AgentCoordinator
from src.agents import ResearchAgent, AnalysisAgent

async def main():
    # Initialize coordinator
    config = CoordinatorConfig(
        anthropic_api_key="your-api-key",
        enable_reasoning=True,
    )
    coordinator = AgentCoordinator(config)
    
    # Create and register agents
    research_agent = ResearchAgent("your-api-key")
    coordinator.register_agent(research_agent)
    
    # Execute a task
    result = await research_agent.process("What is AI?")
    print(result)

asyncio.run(main())
```

### Creating Custom Agents

```python
from src.core.base_agent import BaseAgent
from src.core.config import AgentConfig

class MyCustomAgent(BaseAgent):
    def __init__(self, api_key: str):
        config = AgentConfig(
            name="MyCustomAgent",
            system_prompt="You are a helpful assistant.",
            enable_reasoning=True,
            enable_memory=True,
        )
        super().__init__(config, api_key)
    
    async def process(self, input_text: str, context=None):
        # Your custom logic here
        response = await self.llm.ainvoke(input_text)
        return response.content
```

### Adding Tools to Agents

```python
from langchain_core.tools import tool

@tool
def my_custom_tool(input: str) -> str:
    """Description of my tool"""
    return f"Processing: {input}"

# Add tool to agent
agent.add_tool(my_custom_tool)
```

## Configuration

### Environment Variables

See `.env.example` for all available options:

- `ANTHROPIC_API_KEY`: Your Anthropic API key (required)
- `AGENT_MODEL`: LLM model to use (default: claude-3-opus-20240229)
- `AGENT_TEMPERATURE`: Model temperature for creativity (default: 0.7)
- `MAX_AGENTS`: Maximum agents in coordinator (default: 10)
- `MEMORY_TYPE`: Memory backend (default: conversation)
- `LOG_LEVEL`: Logging level (default: INFO)

### Programmatic Configuration

```python
from src.core.config import CoordinatorConfig, AgentConfig

# Coordinator configuration
coord_config = CoordinatorConfig(
    anthropic_api_key="key",
    max_agents=10,
    enable_reasoning=True,
    enable_agent_learning=True,
)

# Agent configuration
agent_config = AgentConfig(
    name="MyAgent",
    model="claude-3-opus-20240229",
    temperature=0.7,
    max_tokens=4096,
    enable_reasoning=True,
    enable_memory=True,
    reasoning_depth=3,
)
```

## Core Components

### AgentCoordinator

Manages multiple agents and coordinates their interactions:

```python
# Register an agent
coordinator.register_agent(my_agent)

# Coordinate a task across agents
result = await coordinator.coordinate_task(
    task="Analyze this data",
    primary_agent="AnalysisAgent",
    supporting_agents=["ResearchAgent"],
)

# Get system status
status = coordinator.get_status()
```

### BaseAgent

Base class for all agents:

```python
# Execute a task
result = await agent.process("Your prompt here")

# Use reasoning
reasoning = await agent.reason_about("Complex problem")

# Manage memory
agent.store_memory("Important fact")
memories = agent.get_memory_context("search query")

# Learn from execution
agent.learn_from_execution(input, output, success=True)
```

### MemoryManager

Persistent memory with retrieval:

```python
# Store content
memory.store("Important information")

# Retrieve relevant memories
results = memory.retrieve("search query", k=5)

# Manage memory size
memory.clear()
```

### ReasoningEngine

Chain-of-thought reasoning:

```python
# Basic reasoning
result = await engine.reason(problem, llm)

# Compare solutions
best = await engine.compare_solutions(problem, solutions, llm)
```

## Pre-built Agents

### ResearchAgent
Specialized in information gathering and research tasks.

```python
research = ResearchAgent(api_key)
result = await research.process("Research AI trends")
```

### AnalysisAgent
Specialized in data analysis and generating insights.

```python
analysis = AnalysisAgent(api_key)
result = await analysis.process("Analyze this dataset", context={"use_reasoning": True})
```

### PlanningAgent
Specialized in breaking down complex tasks into action plans.

```python
planning = PlanningAgent(api_key)
result = await planning.process("Create an action plan for...")
```

## Testing

Run tests with pytest:

```bash
pip install pytest pytest-asyncio
pytest tests/ -v
```

## Project Structure

```
Pinky-Agent1/
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── base_agent.py      # Base agent class
│   │   ├── coordinator.py     # Agent coordinator
│   │   └── config.py          # Configuration classes
│   ├── agents/
│   │   └── __init__.py        # Pre-built agents
│   ├── tools/
│   │   ├── __init__.py
│   │   └── tools.py           # Tool definitions
│   ├── memory/
│   │   ├── __init__.py
│   │   └── manager.py         # Memory management
│   └── reasoning/
│       ├── __init__.py
│       └── engine.py          # Reasoning engine
├── tests/
│   └── test_agents.py         # Unit tests
├── main.py                    # Example usage
├── requirements.txt           # Dependencies
├── setup.py                   # Package setup
├── pyproject.toml            # Project configuration
└── README.md                 # This file
```

## Best Practices

1. **Always use async/await**: All agent processing is async
2. **Set up environment early**: Load `.env` before creating agents
3. **Configure agents appropriately**: Match agent configuration to task complexity
4. **Use memory effectively**: Store and retrieve relevant context
5. **Handle errors gracefully**: Wrap agent calls in try-except
6. **Log comprehensively**: Use Python logging for debugging
7. **Test thoroughly**: Include unit tests for custom agents

## Performance Tips

- Use `reasoning_depth=3` for fast tasks, `5+` for complex reasoning
- Set `memory_max_size` based on available resources
- Use `enable_memory=False` for stateless operations
- Batch multiple tasks when possible
- Reuse agent instances instead of recreating them

## Troubleshooting

### ANTHROPIC_API_KEY not found
- Ensure `.env` file exists and contains your API key
- Check `.env` file is in project root directory
- Use `load_dotenv()` before creating agents

### Memory errors
- Reduce `memory_max_size` in configuration
- Use `enable_memory=False` for memory-sensitive tasks
- Periodically clear old memories with `memory.clear()`

### Async/await errors
- Ensure you're using `async def` for functions calling agents
- Use `asyncio.run()` to execute async main functions
- Don't forget to `await` async calls

## Contributing

Contributions are welcome! Please:
1. Create a new branch for your feature
2. Write tests for new functionality
3. Ensure all tests pass
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or suggestions, please open an issue on GitHub.
