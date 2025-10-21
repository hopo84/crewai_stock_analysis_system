# API参考

CrewAI股票分析系统提供了丰富的API接口，支持程序化调用和集成到其他应用中。

## 目录

- [核心API接口](./核心API接口.md) - 主要的分析接口
- [数据接口](./数据接口.md) - 数据获取和处理接口
- [工具接口](./工具接口.md) - 各种分析工具的接口
- [配置接口](./配置接口.md) - 系统配置和管理接口
- [WebSocket接口](./WebSocket接口.md) - 实时通信接口

## API概览

### 接口设计原则

#### 🎯 RESTful设计
- 使用标准HTTP方法（GET, POST, PUT, DELETE）
- 资源导向的URL设计
- 统一的响应格式
- 合理的HTTP状态码

#### 📊 数据格式
- 请求/响应均使用JSON格式
- 时间格式统一使用ISO 8601标准
- 错误信息结构化返回
- 支持数据压缩

#### 🔒 安全机制
- API密钥认证
- 请求频率限制
- 数据加密传输
- 敏感信息脱敏

## 快速开始

### 1. 认证配置

```python
import requests

# API基础配置
BASE_URL = "http://localhost:8000/api/v1"
API_KEY = "your-api-key"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
```

### 2. 基础调用示例

```python
# 单股票分析
def analyze_stock(company: str, ticker: str):
    url = f"{BASE_URL}/analysis/single"
    data = {
        "company": company,
        "ticker": ticker,
        "mode": "standard"
    }

    response = requests.post(url, json=data, headers=headers)
    return response.json()

# 调用示例
result = analyze_stock("苹果公司", "AAPL")
print(result)
```

### 3. 批量分析示例

```python
# 批量股票分析
def batch_analyze(stocks: list):
    url = f"{BASE_URL}/analysis/batch"
    data = {
        "stocks": stocks,
        "mode": "quick",
        "concurrent": True
    }

    response = requests.post(url, json=data, headers=headers)
    return response.json()

# 调用示例
stocks = [
    {"company": "苹果公司", "ticker": "AAPL"},
    {"company": "微软", "ticker": "MSFT"},
    {"company": "谷歌", "ticker": "GOOGL"}
]
result = batch_analyze(stocks)
```

## 核心API端点

### 分析服务 `/analysis/`

#### 单股票分析
```http
POST /api/v1/analysis/single
```

**请求参数**：
```json
{
  "company": "公司名称",
  "ticker": "股票代码",
  "mode": "quick|standard|detailed",
  "options": {
    "use_cache": true,
    "include_charts": false,
    "focus_areas": ["financial", "technical", "risk"]
  }
}
```

**响应示例**：
```json
{
  "status": "success",
  "task_id": "task_123456",
  "data": {
    "company": "苹果公司",
    "ticker": "AAPL",
    "analysis_time": "2024-10-20T15:30:00Z",
    "recommendation": {
      "action": "买入",
      "confidence": 0.85,
      "target_price": 180.00,
      "current_price": 175.43
    },
    "summary": {
      "market_score": 8.5,
      "financial_score": 9.2,
      "technical_score": 7.8,
      "risk_score": 6.5
    },
    "reports": {
      "market_research": "...",
      "financial_analysis": "...",
      "technical_analysis": "...",
      "risk_assessment": "...",
      "final_recommendation": "..."
    }
  }
}
```

#### 批量分析
```http
POST /api/v1/analysis/batch
```

**请求参数**：
```json
{
  "stocks": [
    {"company": "公司1", "ticker": "CODE1"},
    {"company": "公司2", "ticker": "CODE2"}
  ],
  "mode": "quick|standard|detailed",
  "concurrent": true,
  "max_concurrent": 3
}
```

#### 分析状态查询
```http
GET /api/v1/analysis/{task_id}/status
```

**响应示例**：
```json
{
  "task_id": "task_123456",
  "status": "running|completed|failed",
  "progress": {
    "current_step": "financial_analysis",
    "completed_steps": ["market_research"],
    "total_steps": 5,
    "percentage": 40
  },
  "estimated_remaining": 180
}
```

### 数据服务 `/data/`

#### 股票基础信息
```http
GET /api/v1/data/stock/{ticker}/info
```

**响应示例**：
```json
{
  "ticker": "AAPL",
  "company_name": "Apple Inc.",
  "sector": "Technology",
  "industry": "Consumer Electronics",
  "market_cap": 2800000000000,
  "current_price": 175.43,
  "currency": "USD",
  "exchange": "NASDAQ"
}
```

#### 股票价格数据
```http
GET /api/v1/data/stock/{ticker}/price?period=1y&interval=1d
```

**查询参数**：
- `period`: 时间周期 (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
- `interval`: 数据间隔 (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)

**响应示例**：
```json
{
  "ticker": "AAPL",
  "period": "1y",
  "interval": "1d",
  "data": [
    {
      "date": "2024-01-01",
      "open": 170.25,
      "high": 172.80,
      "low": 168.90,
      "close": 171.50,
      "volume": 85420000,
      "adj_close": 171.50
    }
  ],
  "metadata": {
    "data_points": 252,
    "start_date": "2023-10-20",
    "end_date": "2024-10-20"
  }
}
```

#### 财务数据
```http
GET /api/v1/data/stock/{ticker}/financials?type=income&period=annual
```

### 工具服务 `/tools/`

#### 技术指标计算
```http
POST /api/v1/tools/indicators/calculate
```

**请求参数**：
```json
{
  "ticker": "AAPL",
  "indicators": [
    {
      "name": "SMA",
      "params": {"period": 20}
    },
    {
      "name": "RSI",
      "params": {"period": 14}
    },
    {
      "name": "MACD",
      "params": {"fast": 12, "slow": 26, "signal": 9}
    }
  ],
  "period": "1y"
}
```

#### 估值模型
```http
POST /api/v1/tools/valuation/dcf
```

**请求参数**：
```json
{
  "ticker": "AAPL",
  "assumptions": {
    "growth_rate": 0.08,
    "discount_rate": 0.10,
    "terminal_growth": 0.025,
    "projection_years": 5
  }
}
```

## WebSocket实时接口

### 连接建立

```javascript
// JavaScript WebSocket客户端示例
const ws = new WebSocket('ws://localhost:8000/ws/analysis');

ws.onopen = function(event) {
    console.log('WebSocket连接已建立');

    // 发送分析请求
    ws.send(JSON.stringify({
        action: 'start_analysis',
        data: {
            company: '苹果公司',
            ticker: 'AAPL',
            mode: 'standard'
        }
    }));
};

ws.onmessage = function(event) {
    const message = JSON.parse(event.data);

    switch(message.type) {
        case 'progress':
            console.log(`分析进度: ${message.data.percentage}%`);
            break;
        case 'step_completed':
            console.log(`步骤完成: ${message.data.step}`);
            break;
        case 'analysis_completed':
            console.log('分析完成:', message.data.result);
            break;
        case 'error':
            console.error('分析错误:', message.data.error);
            break;
    }
};
```

### 消息格式

#### 进度更新
```json
{
  "type": "progress",
  "timestamp": "2024-10-20T15:30:00Z",
  "data": {
    "task_id": "task_123456",
    "percentage": 65,
    "current_step": "risk_assessment",
    "message": "正在进行风险评估..."
  }
}
```

#### 步骤完成
```json
{
  "type": "step_completed",
  "timestamp": "2024-10-20T15:32:00Z",
  "data": {
    "task_id": "task_123456",
    "step": "financial_analysis",
    "result": {
      "summary": "财务状况良好",
      "key_metrics": {
        "roe": 0.28,
        "debt_ratio": 0.32
      }
    }
  }
}
```

## SDK和客户端库

### Python SDK

```python
from crewai_stock_analysis import StockAnalysisClient

# 初始化客户端
client = StockAnalysisClient(
    api_key="your-api-key",
    base_url="http://localhost:8000"
)

# 同步分析
result = client.analyze_stock("苹果公司", "AAPL")

# 异步分析
async def async_analysis():
    result = await client.analyze_stock_async("苹果公司", "AAPL")
    return result

# 批量分析
stocks = [("苹果", "AAPL"), ("微软", "MSFT")]
results = client.batch_analyze(stocks)

# 实时分析（WebSocket）
def progress_callback(progress):
    print(f"进度: {progress['percentage']}%")

client.analyze_stock_realtime(
    "苹果公司", "AAPL",
    progress_callback=progress_callback
)
```

### JavaScript SDK

```javascript
import { StockAnalysisClient } from 'crewai-stock-analysis-js';

// 初始化客户端
const client = new StockAnalysisClient({
    apiKey: 'your-api-key',
    baseUrl: 'http://localhost:8000'
});

// Promise方式
client.analyzeStock('苹果公司', 'AAPL')
    .then(result => console.log(result))
    .catch(error => console.error(error));

// async/await方式
async function analyzeStock() {
    try {
        const result = await client.analyzeStock('苹果公司', 'AAPL');
        console.log(result);
    } catch (error) {
        console.error(error);
    }
}

// 实时分析
const analysisStream = client.analyzeStockRealtime('苹果公司', 'AAPL');

analysisStream.on('progress', (data) => {
    console.log(`进度: ${data.percentage}%`);
});

analysisStream.on('completed', (result) => {
    console.log('分析完成:', result);
});
```

## 错误处理

### 错误响应格式

```json
{
  "status": "error",
  "error": {
    "code": "INVALID_TICKER",
    "message": "股票代码无效",
    "details": {
      "ticker": "INVALID",
      "suggestion": "请检查股票代码格式"
    },
    "request_id": "req_123456",
    "timestamp": "2024-10-20T15:30:00Z"
  }
}
```

### 常见错误码

| 错误码 | HTTP状态 | 描述 |
|--------|----------|------|
| `INVALID_API_KEY` | 401 | API密钥无效 |
| `RATE_LIMIT_EXCEEDED` | 429 | 请求频率超限 |
| `INVALID_TICKER` | 400 | 股票代码无效 |
| `DATA_NOT_AVAILABLE` | 404 | 数据不可用 |
| `ANALYSIS_FAILED` | 500 | 分析过程失败 |
| `QUOTA_EXCEEDED` | 402 | 配额不足 |

### 重试机制

```python
import time
import random

def api_call_with_retry(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e

            # 指数退避
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            time.sleep(wait_time)

# 使用示例
result = api_call_with_retry(
    lambda: client.analyze_stock("苹果公司", "AAPL")
)
```

## 频率限制

### 限制策略

| 用户类型 | 每分钟请求 | 每小时请求 | 每日请求 |
|----------|------------|------------|----------|
| 免费用户 | 10 | 100 | 1000 |
| 标准用户 | 60 | 1000 | 10000 |
| 企业用户 | 300 | 5000 | 50000 |

### 响应头信息

```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 55
X-RateLimit-Reset: 1634567890
```

### 处理频率限制

```python
def handle_rate_limit(response):
    if response.status_code == 429:
        reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
        wait_time = reset_time - int(time.time())

        if wait_time > 0:
            print(f"频率限制，等待 {wait_time} 秒")
            time.sleep(wait_time)
            return True

    return False
```

通过这些API接口，您可以轻松地将CrewAI股票分析系统集成到您的应用中，实现程序化的股票分析功能。