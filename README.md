# Pinky Agent - Multi-Agent System Coordinator

A production-ready multi-agent AI system built with LangChain and Claude.

## Quick Start

1. **Clone and setup**:
```bash
git clone <repo>
cd Pinky-Agent1
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your ANTHROPIC_API_KEY
```

2. **Run example**:
```bash
python main.py
```

3. **Create custom agent**:
```python
from src.agents import BaseAgent
from src.core.config import AgentConfig

class MyAgent(BaseAgent):
    async def process(self, input_text, context=None):
        response = await self.llm.ainvoke(input_text)
        return response.content
```

## Features

✨ **Multi-Agent Coordination** - Orchestrate multiple specialized agents
💾 **Persistent Memory** - Agents remember and learn from experiences
🧠 **Reasoning Engine** - Chain-of-thought reasoning built-in
🛠️ **Tool Integration** - Easy to add tools and capabilities
📊 **Learning** - Agents improve from successful executions
🔄 **Async** - Full asynchronous support
✅ **Production Ready** - Comprehensive error handling and logging

## Architecture

```
AgentCoordinator
├── ResearchAgent (memory, tools, reasoning)
├── AnalysisAgent (memory, tools, reasoning)
└── PlanningAgent (memory, tools, reasoning)
```

## Documentation

See [docs/README.md](docs/README.md) for comprehensive documentation.

## Key Components

- **AgentCoordinator**: Manages multiple agents and coordinates tasks
- **BaseAgent**: Foundation for all agents with memory and reasoning
- **MemoryManager**: Persistent agent memory with retrieval
- **ReasoningEngine**: Complex problem-solving with chain-of-thought
- **Pre-built Agents**: ResearchAgent, AnalysisAgent, PlanningAgent

## Example: Coordinated Multi-Agent Task

```python
import asyncio
from src.core.coordinator import AgentCoordinator
from src.core.config import CoordinatorConfig
from src.agents import ResearchAgent, AnalysisAgent

async def main():
    config = CoordinatorConfig(anthropic_api_key="your-key")
    coordinator = AgentCoordinator(config)
    
    # Register agents
    coordinator.register_agent(ResearchAgent("your-key"))
    coordinator.register_agent(AnalysisAgent("your-key"))
    
    # Coordinate task
    result = await coordinator.coordinate_task(
        task="Analyze AI market trends",
        primary_agent="ResearchAgent",
        supporting_agents=["AnalysisAgent"],
    )
    print(result)

asyncio.run(main())
```

## Testing

```bash
pytest tests/ -v
```

## Project Structure

```
src/
├── core/          # Core components (agents, coordinator, config)
├── agents/        # Pre-built agent implementations
├── tools/         # Tool definitions and integration
├── memory/        # Memory management system
└── reasoning/     # Reasoning engine
```

## Requirements

- Python 3.10+
- LangChain 0.1.14+
- Anthropic 0.26.1+
- Pydantic 2.6.4+

## License

MIT - See LICENSE file

## Next Steps

1. Review [docs/README.md](docs/README.md) for detailed documentation
2. Run `python main.py` to see example usage
3. Create your first custom agent by extending `BaseAgent`
4. Run tests: `pytest tests/ -v`
5. Deploy to production!

---

**Built with ❤️ using LangChain & Anthropic Claude**

