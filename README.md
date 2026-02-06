# Eduweaver

Multi-agent system for scientific content creation powered by Microsoft Agent Framework.

## Overview

Eduweaver transforms scientific content creation through intelligent multi-agent orchestration, reducing production time by 70% while maintaining academic rigor and scalability.

## Features

- **Research Intelligence**: Automated source discovery and synthesis
- **Content Generation**: Initial draft creation with academic structure
- **Quality Enhancement**: Style optimization and academic tone refinement
- **Verification & Compliance**: Fact-checking and citation validation

## Quick Start

### Prerequisites

- Python 3.12+
- Azure OpenAI access
- uv package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/luiscm17/eduweaver.git
cd eduweaver

# Install dependencies
uv sync

# Set up environment variables
cp .env.example .env
# Edit .env with your Azure OpenAI credentials
```

### Configuration

Add your Azure OpenAI credentials to `.env`:

```bash
AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME="gpt-4o-mini"
AZURE_AI_PROJECT_ENDPOINT="https://your-project.services.ai.azure.com/api/projects/your-project-id"
AZURE_AI_MODEL_DEPLOYMENT_NAME="gpt-4o-mini"
```

### Usage

```bash
# Run the interactive CLI
uv run src/main.py
```

## Architecture

Built with Microsoft Agent Framework using a Group Chat orchestration pattern:

- **BaseAgent**: Abstract class for all agents with Azure integration
- **ResearchIntelligence**: Source discovery and synthesis
- **Modular Design**: Easy to extend with additional agents
- **Azure Integration**: Seamless connection to Azure OpenAI and AI Foundry

## Project Structure

```yml
src/
├── agents/              # Agent implementations
│   ├── base_agent.py
│   └── research_intelligence.py
├── config/              # Configuration management
│   └── settings.py
└── main.py             # Entry point
```

## MVP Goals

- Generate scientific articles (1,500-3,000 words) in <45 minutes
- Achieve >70% quality score in readability and coherence
- Maintain >85% source accuracy
- Support multiple content types: articles, course modules, research summaries
