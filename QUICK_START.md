"""Quick reference guide for Pinky Agent"""

# QUICK REFERENCE - Pinky Agent Multi-Agent System

## 1. INSTALLATION & SETUP
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env and add: ANTHROPIC_API_KEY=your_key_here
```

## 2. BASIC USAGE - Single Agent
```python
import asyncio
from src.agents import ResearchAgent
from dotenv import load_dotenv
import os

load_dotenv()

async def main():
    agent = ResearchAgent(os.getenv("ANTHROPIC_API_KEY"))
    result = await agent.process("Tell me about AI trends")
    print(result)

asyncio.run(main())
```

## 3. MULTI-AGENT COORDINATION
```python
from src.core.coordinator import AgentCoordinator
from src.core.config import CoordinatorConfig
from src.agents import ResearchAgent, AnalysisAgent

async def main():
    config = CoordinatorConfig(
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
    )
    coordinator = AgentCoordinator(config)
    
    # Register agents
    coordinator.register_agent(ResearchAgent(api_key))
    coordinator.register_agent(AnalysisAgent(api_key))
    
    # Execute coordinated task
    result = await coordinator.coordinate_task(
        task="Research and analyze AI trends",
        primary_agent="ResearchAgent",
        supporting_agents=["AnalysisAgent"],
    )
    print(result)
```

## 4. CREATE CUSTOM AGENT
```python
from src.core.base_agent import BaseAgent
from src.core.config import AgentConfig

class MySpecialAgent(BaseAgent):
    def __init__(self, api_key: str):
        config = AgentConfig(
            name="SpecialAgent",
            system_prompt="You are specialized in...",
            enable_memory=True,
            enable_reasoning=True,
        )
        super().__init__(config, api_key)
    
    async def process(self, input_text, context=None):
        # Use memory from similar tasks
        memory_context = self.get_memory_context(input_text)
        
        prompt = f"Context: {memory_context}\nTask: {input_text}"
        response = await self.llm.ainvoke(prompt)
        
        # Learn from this execution
        self.learn_from_execution(input_text, response.content, success=True)
        
        return response.content
```

## 5. ADD TOOLS TO AGENT
```python
from src.tools import get_default_tools

agent = ResearchAgent(api_key)

# Add default tools
tools = get_default_tools()
agent.add_tools(tools)

# Add custom tool
from langchain_core.tools import tool

@tool
def my_tool(input: str) -> str:
    """Does something special"""
    return f"Result: {input}"

agent.add_tool(my_tool)
```

## 6. USE REASONING
```python
# Agent with reasoning
config = AgentConfig(
    name="ThinkingAgent",
    enable_reasoning=True,
    reasoning_depth=5,  # More depth = more reasoning
)

agent = BaseAgent(config, api_key)

# Use reasoning for complex problems
reasoning_result = await agent.reason_about(
    "How would you solve X complex problem?"
)
```

## 7. MANAGE MEMORY
```python
# Store memory
agent.store_memory("Important insight about topic X")

# Retrieve relevant memories
memories = agent.get_memory_context("topic X", k=5)

# View agent status
status = agent.get_status()
print(f"Agent has {status['memory_size']} memories")
```

## 8. AGENT STATUS & MONITORING
```python
# Get individual agent status
status = agent.get_status()
# Returns: name, model, tools_count, memory_size, etc.

# Get coordinator status
coord_status = coordinator.get_status()
# Returns: total_agents, total_tasks, agent_status for each...

# List all agents
agents_info = coordinator.list_agents()
```

## 9. CONFIGURATION OPTIONS

### AgentConfig
- `name`: Agent name (required)
- `model`: LLM model (default: claude-3-opus-20240229)
- `temperature`: Creativity 0.0-2.0 (default: 0.7)
- `max_tokens`: Max output tokens (default: 4096)
- `system_prompt`: System instructions (default: "")
- `enable_memory`: Use memory system (default: True)
- `enable_reasoning`: Use reasoning engine (default: True)
- `reasoning_depth`: Reasoning steps 1-10 (default: 3)

### CoordinatorConfig
- `anthropic_api_key`: API key (required)
- `max_agents`: Max agents in system (default: 10)
- `enable_agent_learning`: Learn from executions (default: True)
- `enable_reasoning`: Reasoning available (default: True)
- `memory_type`: 'conversation'|'file'|'vector' (default: 'conversation')
- `memory_max_size`: Memory items limit (default: 50)

## 10. TESTING
```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_agents.py::TestMemoryManager -v

# Run with coverage
pytest tests/ --cov=src
```

## 11. ASYNC BEST PRACTICES
```python
# Always use async/await
async def process_task():
    result = await agent.process(task)
    return result

# Run with asyncio
asyncio.run(process_task())

# Or in another async context
results = await asyncio.gather(
    agent1.process(task1),
    agent2.process(task2),
    agent3.process(task3),
)
```

## 12. ERROR HANDLING
```python
try:
    result = await agent.process(task)
except ValueError as e:
    print(f"Invalid input: {e}")
except Exception as e:
    print(f"Error processing task: {e}")
    # Check agent status
    print(agent.get_status())
```

## KEY CLASSES

### AgentCoordinator
- `register_agent(agent)` - Add agent
- `deregister_agent(name)` - Remove agent
- `get_agent(name)` - Get agent by name
- `coordinate_task(task, primary_agent, supporting_agents)` - Run coordinated task
- `get_status()` - System status
- `list_agents()` - List all agents

### BaseAgent
- `process(input, context)` - Execute task
- `add_tool(tool)` / `add_tools(tools)` - Add capabilities
- `reason_about(problem)` - Use reasoning
- `store_memory(content)` - Save to memory
- `get_memory_context(query, k)` - Retrieve memories
- `learn_from_execution(input, output, success)` - Learn
- `get_status()` - Agent status

### MemoryManager
- `store(content)` - Save memory
- `retrieve(query, k)` - Get memories
- `clear()` - Clear all
- `__len__()` - Memory count

### ReasoningEngine
- `reason(problem, llm)` - Think through problem
- `compare_solutions(problem, solutions, llm)` - Compare approaches

## TROUBLESHOOTING

**ImportError in src.X**
→ Ensure all files in src/ have __init__.py

**ANTHROPIC_API_KEY not found**
→ Create .env file and add your key

**asyncio.InvalidStateError**
→ Use `await` for agent.process() calls

**Memory size growing**
→ Increase max_size in MemoryManager or enable memory clearing

**Slow responses**
→ Reduce reasoning_depth or max_tokens

## NEXT STEPS

1. Run `python main.py` to see example
2. Create your first custom agent (see #4)
3. Add tools to agents (see #5)
4. Integrate multiple agents (see #3)
5. Deploy to production!

---
For more details, see docs/README.md
