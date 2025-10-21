# 开发指南

欢迎参与CrewAI股票分析系统的开发！本指南将帮助您了解项目架构、开发环境配置、代码规范和贡献流程。

## 目录

- [项目结构](./项目结构.md) - 详细的项目目录和模块说明
- [开发环境配置](./开发环境配置.md) - 开发环境搭建和工具配置
- [代码规范](./代码规范.md) - 编码标准和最佳实践
- [测试指南](./测试指南.md) - 测试编写和执行指南
- [贡献指南](./贡献指南.md) - 如何为项目贡献代码

## 项目概览

### 技术栈

#### 核心框架
- **CrewAI 0.28+** - 多智能体协作框架
- **Python 3.9+** - 主要开发语言
- **OpenAI API** - 大语言模型服务

#### 数据处理
- **Pandas** - 数据分析和处理
- **NumPy** - 数值计算
- **AKShare** - 金融数据获取

#### Web和API
- **FastAPI** - 现代API框架
- **Flask** - 轻量级Web框架
- **Uvicorn** - ASGI服务器

#### 开发工具
- **Black** - 代码格式化
- **Flake8** - 代码检查
- **Pytest** - 测试框架
- **Pre-commit** - Git钩子管理

### 架构原则

#### 🎯 设计理念
1. **模块化设计** - 功能解耦，便于维护和扩展
2. **智能体协作** - 基于CrewAI的多Agent架构
3. **可配置性** - 通过配置文件灵活调整行为
4. **可扩展性** - 支持新增智能体和工具
5. **可测试性** - 完善的测试覆盖和mock机制

#### 🏗️ 核心组件
```
系统架构
├── 智能体层 (Agents)      # 各种专业分析师
├── 任务层 (Tasks)         # 具体分析任务
├── 工具层 (Tools)         # 数据获取和处理工具
├── 流程层 (Flows)         # 复杂业务流程控制
└── 接口层 (APIs)          # 外部接口和服务
```

## 快速开始开发

### 1. 环境准备

```bash
# 克隆项目
git clone [项目地址]
cd crewai_stock_analysis_system

# 创建开发环境
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或 .venv\Scripts\activate  # Windows

# 安装开发依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 2. 配置开发环境

```bash
# 复制环境配置
cp .env.example .env
# 编辑.env文件，添加必要的API密钥

# 安装pre-commit钩子
pre-commit install

# 验证环境
python main.py --check-env
pytest tests/ -v
```

### 3. 代码结构理解

```python
# 查看项目结构
tree src/ -I "__pycache__"

# 运行示例分析
python main.py --company "苹果公司" --ticker "AAPL" --quick

# 查看日志了解执行流程
tail -f log.txt
```

## 核心概念理解

### CrewAI基础概念

#### Agent（智能体）
```python
# 示例：创建一个市场分析师Agent
@agent
def market_researcher(self) -> Agent:
    return Agent(
        role="高级市场研究分析师",
        goal="收集并分析{company}的最新市场数据和行业趋势",
        backstory="""
        你是一位拥有10年经验的资深市场分析师，
        擅长从海量信息中提取关键趋势和数据。
        """,
        tools=[SerperDevTool(), ScrapeWebsiteTool()],
        verbose=True
    )
```

#### Task（任务）
```python
# 示例：创建市场研究任务
@task
def research_task(self) -> Task:
    return Task(
        description="""
        对{company}进行全面的市场研究，包括：
        1. 最近3个月的股价走势
        2. 行业竞争态势
        3. 市场新闻和重大事件
        """,
        expected_output="详细的市场研究报告",
        agent=self.market_researcher()
    )
```

#### Crew（团队）
```python
# 示例：组建分析团队
@crew
def crew(self) -> Crew:
    return Crew(
        agents=[
            self.market_researcher(),
            self.financial_analyst(),
            self.investment_advisor()
        ],
        tasks=[
            self.research_task(),
            self.analysis_task(),
            self.recommendation_task()
        ],
        process=Process.sequential,
        verbose=True
    )
```

## 开发工作流

### 1. 功能开发流程

```bash
# 1. 创建功能分支
git checkout -b feature/new-agent

# 2. 开发和测试
# 编写代码...
python -m pytest tests/test_new_agent.py -v

# 3. 代码检查
black src/
flake8 src/
pre-commit run --all-files

# 4. 提交代码
git add .
git commit -m "feat: add new market sentiment agent"

# 5. 推送和创建PR
git push origin feature/new-agent
# 创建Pull Request
```

### 2. 调试技巧

#### 启用调试模式
```bash
# 详细日志输出
python main.py --debug --company "公司名" --ticker "代码"

# 保存中间结果
python main.py --save-intermediate --company "公司名" --ticker "代码"
```

#### 单元测试调试
```python
# 在代码中添加断点
import pdb; pdb.set_trace()

# 或使用更现代的调试器
import ipdb; ipdb.set_trace()

# 运行特定测试
pytest tests/test_specific.py::test_function -v -s
```

#### 智能体行为调试
```python
# 在Agent配置中启用详细输出
Agent(
    role="分析师",
    verbose=True,  # 显示思考过程
    memory=True,   # 启用记忆功能
    max_iter=3,    # 限制迭代次数
)
```

## 常见开发任务

### 添加新的智能体

```python
# 1. 在agents.yaml中定义配置
new_sentiment_analyst:
  role: >
    市场情绪分析师
  goal: >
    分析{company}的市场情绪和投资者心理
  backstory: >
    你专门研究市场心理学和投资者行为，
    能够从社交媒体和新闻中洞察市场情绪。

# 2. 在crew类中实现Agent方法
@agent
def sentiment_analyst(self) -> Agent:
    return Agent(
        config=self.agents_config['new_sentiment_analyst'],
        tools=[SentimentAnalysisTool(), SocialMediaTool()],
        verbose=True
    )

# 3. 添加对应的Task
@task
def sentiment_analysis_task(self) -> Task:
    return Task(
        description="分析市场对{company}的情绪倾向",
        expected_output="情绪分析报告",
        agent=self.sentiment_analyst()
    )

# 4. 集成到Crew中
@crew
def crew(self) -> Crew:
    return Crew(
        agents=[
            # ... 其他agents
            self.sentiment_analyst(),
        ],
        tasks=[
            # ... 其他tasks
            self.sentiment_analysis_task(),
        ]
    )
```

### 开发新的工具

```python
# 创建自定义工具
from crewai_tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

class CustomAnalysisTool(BaseTool):
    name: str = "Custom Analysis Tool"
    description: str = "执行自定义的股票分析"

    class CustomAnalysisInput(BaseModel):
        """Custom analysis tool input schema."""
        ticker: str = Field(..., description="股票代码")
        analysis_type: str = Field(..., description="分析类型")

    args_schema: Type[BaseModel] = CustomAnalysisInput

    def _run(self, ticker: str, analysis_type: str) -> str:
        # 实现具体的分析逻辑
        result = self.perform_analysis(ticker, analysis_type)
        return f"分析结果: {result}"

    def perform_analysis(self, ticker: str, analysis_type: str) -> str:
        # 具体的分析实现
        pass
```

### 扩展数据源

```python
# 添加新的数据源
class NewDataSource:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_stock_data(self, ticker: str, period: str = "1y"):
        """获取股票数据"""
        # 实现数据获取逻辑
        pass

    def get_financial_data(self, ticker: str):
        """获取财务数据"""
        # 实现财务数据获取
        pass

# 在配置中注册新数据源
DATA_SOURCES = {
    'akshare': AKShareDataSource(),
    'yahoo': YahooFinanceDataSource(),
    'new_source': NewDataSource(api_key=os.getenv('NEW_API_KEY'))
}
```

## 性能优化

### 缓存策略

```python
# 使用缓存装饰器
from functools import lru_cache
from cachetools import TTLCache
import time

# 内存缓存
@lru_cache(maxsize=128)
def get_company_info(ticker: str):
    # 耗时的API调用
    pass

# 时效性缓存
cache = TTLCache(maxsize=100, ttl=3600)  # 1小时过期

def get_market_data(ticker: str):
    if ticker in cache:
        return cache[ticker]

    data = fetch_market_data(ticker)
    cache[ticker] = data
    return data
```

### 异步处理

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

async def analyze_multiple_stocks(tickers: list):
    """并发分析多只股票"""
    with ThreadPoolExecutor(max_workers=3) as executor:
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(executor, analyze_stock, ticker)
            for ticker in tickers
        ]
        results = await asyncio.gather(*tasks)
    return results
```

## 配置管理

### 环境配置

```python
# config/settings.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    # API配置
    openai_api_key: str
    openai_model: str = "gpt-3.5-turbo"

    # 数据源配置
    primary_data_source: str = "akshare"
    enable_cache: bool = True
    cache_ttl: int = 3600

    # 并发配置
    max_concurrent_tasks: int = 3
    task_timeout: int = 300

    class Config:
        env_file = ".env"

settings = Settings()
```

### 动态配置

```yaml
# config/analysis_profiles.yaml
quick_analysis:
  max_tokens: 1000
  temperature: 0.3
  agents:
    - market_researcher
    - financial_analyst

standard_analysis:
  max_tokens: 2000
  temperature: 0.5
  agents:
    - market_researcher
    - financial_analyst
    - technical_analyst
    - risk_assessor

detailed_analysis:
  max_tokens: 4000
  temperature: 0.7
  agents:
    - market_researcher
    - financial_analyst
    - technical_analyst
    - risk_assessor
    - sentiment_analyst
```

## 部署和发布

### Docker容器化

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py", "--api-mode"]
```

### API服务部署

```python
# api/server.py
from fastapi import FastAPI
from .routers import analysis, health

app = FastAPI(title="Stock Analysis API")

app.include_router(analysis.router, prefix="/api/v1")
app.include_router(health.router, prefix="/health")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 监控和日志

### 结构化日志

```python
import structlog

logger = structlog.get_logger()

def analyze_stock(ticker: str):
    logger.info("开始股票分析", ticker=ticker)

    try:
        result = perform_analysis(ticker)
        logger.info("分析完成",
                   ticker=ticker,
                   duration=result.duration,
                   recommendation=result.recommendation)
        return result
    except Exception as e:
        logger.error("分析失败",
                    ticker=ticker,
                    error=str(e))
        raise
```

### 性能监控

```python
import time
from functools import wraps

def monitor_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            logger.info(f"{func.__name__} 执行成功", duration=duration)
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"{func.__name__} 执行失败",
                        duration=duration, error=str(e))
            raise
    return wrapper
```

通过这个开发指南，您应该能够理解项目架构，配置开发环境，并开始为CrewAI股票分析系统贡献代码。