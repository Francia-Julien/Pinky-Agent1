"""Configuration management for agents and the coordinator"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class AgentConfig(BaseSettings):
    """Configuration for individual agents"""

    name: str = Field(..., description="Name of the agent")
    model: str = Field(default="claude-3-opus-20240229", description="LLM model to use")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=4096, gt=0)
    system_prompt: str = Field(default="", description="System prompt for the agent")
    enable_memory: bool = Field(default=True)
    enable_reasoning: bool = Field(default=True)
    reasoning_depth: int = Field(default=3, gt=0)

    class Config:
        env_prefix = "AGENT_"
        case_sensitive = False


class CoordinatorConfig(BaseSettings):
    """Configuration for the agent coordinator"""

    anthropic_api_key: str = Field(..., description="API key for Anthropic")
    max_agents: int = Field(default=10, gt=0)
    enable_agent_learning: bool = Field(default=True)
    enable_reasoning: bool = Field(default=True)
    reasoning_depth: int = Field(default=3, gt=0)
    memory_type: str = Field(default="conversation")
    memory_max_size: int = Field(default=50, gt=0)
    memory_persist_path: Optional[str] = Field(default=None)
    log_level: str = Field(default="INFO")

    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def agent_config(self) -> AgentConfig:
        """Get default agent configuration"""
        return AgentConfig(
            name="DefaultAgent",
            model="claude-3-opus-20240229",
            temperature=0.7,
            max_tokens=4096,
        )
