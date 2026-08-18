from setuptools import setup, find_packages

setup(
    name="pinky-agent",
    version="0.1.0",
    description="A production-ready multi-agent system coordinator using LangChain",
    author="Francia Julien",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "langchain>=0.3.0,<0.4",
        "langchain-anthropic>=0.3.0,<0.4",
        "langchain-community>=0.3.0,<0.4",
        "anthropic>=0.28.0,<1.0",
        "pydantic>=2.7.4,<3.0",
        "pydantic-settings>=2.7.0,<3.0",
        "python-dotenv>=1.0.0",
        "aiohttp>=3.9.2",
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.4",
            "pytest-asyncio>=0.23.3",
            "pytest-cov>=4.1.0",
            "black>=24.1.1",
            "ruff>=0.2.2",
            "mypy>=1.8.0",
        ],
    },
)
