# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **CrewAI股票分析系统** - a fully functional multi-agent stock analysis system built with CrewAI framework. The project features comprehensive documentation and modular architecture supporting multiple AI model providers.

## Current State

**Implementation Status:**
- ✅ Complete source code structure in `src/` directory
- ✅ Multi-model support (OpenAI + DeepSeek integration)
- ✅ Comprehensive documentation system in `docs/`
- ✅ Configuration files and environment setup
- ✅ Demo scripts and usage examples

**Key Files:**
- `demo_deepseek.py` - DeepSeek model integration demonstration
- `src/` - Complete source code implementation
- `docs/` - Comprehensive user and developer documentation
- `.env.example` - Extended environment configuration with multi-model support
- `requirements.txt` - Project dependencies
- `CLAUDE.md` - This guidance file

## Technology Stack

- **Framework**: CrewAI - Python-based multi-agent AI framework
- **Language**: Python 3.9+
- **AI Models**:
  - OpenAI API (GPT-4, GPT-3.5-turbo)
  - DeepSeek API (deepseek-chat, deepseek-coder)
- **Data Sources**: AKShare for Chinese market data, Yahoo Finance for global markets
- **Tools Package**: crewai[tools] with SerperDevTool, ScrapeWebsiteTool, etc.
- **Documentation**: Comprehensive Chinese language documentation

## Architecture Patterns

The system implements CrewAI's core concepts:

1. **Agents**: Specialized AI roles with specific goals and backstories
   - 市场研究分析师 (Market Research Analyst)
   - 财务分析师 (Financial Analyst)
   - 技术分析师 (Technical Analyst)
   - 风险评估师 (Risk Assessment Specialist)
   - 投资顾问 (Investment Advisor)

2. **Tasks**: Well-defined work units with clear expected outputs
3. **Crews**: Teams of agents working collaboratively
4. **Model Integration**: Dynamic model switching between providers

## Key Features

1. **Multi-Model Support**:
   - Switch between OpenAI and DeepSeek models via environment configuration
   - Cost optimization through model selection
   - Enhanced Chinese language support with DeepSeek

2. **Comprehensive Analysis**:
   - Market research and data collection
   - Financial statement analysis
   - Technical indicator calculation
   - Risk assessment and management
   - Investment recommendation generation

3. **Documentation System**:
   - Quick start guides
   - User manuals
   - Developer documentation
   - API references

## Development Guidelines

- **Agent Design**: Single responsibility, clear goals, rich backstories
- **Task Decomposition**: Atomic tasks with clear dependencies
- **Tool Selection**: Role-appropriate tool assignment
- **Error Handling**: Retry mechanisms and monitoring
- **Performance**: Optimize agent count and use parallel processing
- **Model Selection**: Choose appropriate model based on task complexity and cost requirements
- **Documentation**: Maintain comprehensive Chinese documentation for Chinese users

## Usage Examples

### Quick Start
```bash
# Run with OpenAI models
python demo_deepseek.py

# Switch to DeepSeek models
# Set MODEL_PROVIDER=deepseek in .env
python demo_deepseek.py
```

### Model Configuration
```env
# OpenAI Configuration
MODEL_PROVIDER=openai
OPENAI_API_KEY=your-key
OPENAI_CHAT_MODEL=gpt-4o-mini

# DeepSeek Configuration
MODEL_PROVIDER=deepseek
DEEPSEEK_API_KEY=your-key
DEEPSEEK_CHAT_MODEL=deepseek-chat
```

## Recent Updates

**Latest Features (impl-integrate-model branch):**
- ✅ DeepSeek model integration with demo script
- ✅ Multi-provider model configuration system
- ✅ Complete documentation restructure
- ✅ Enhanced .env configuration options
- ✅ Improved .gitignore for development workflows