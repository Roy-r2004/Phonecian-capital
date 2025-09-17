# Phoenician Capital - AI-Powered Financial Analysis Platform

A comprehensive web application for testing and validating AI-powered financial analysis prompts, specifically designed for **Total Addressable Market (TAM)** estimation and **Discounted Cash Flow (DCF)** modeling using advanced language models.

## 🚀 Features

### TAM (Total Addressable Market) Analysis
- **Multi-Model Support**: Test prompts with Qwen2.5 VL 32B and Gemini 1.5 Pro
- **Comprehensive Validation**: Automated scoring of response quality and completeness
- **Market Metrics Extraction**: Automatic parsing of market size, confidence intervals, and methodology
- **Real-time Testing**: Interactive web interface for prompt testing
- **Batch Analysis**: Support for testing multiple company contexts

### DCF (Discounted Cash Flow) Analysis
- **Advanced Financial Modeling**: Complete DCF model construction and validation
- **WACC Calculation**: Weighted Average Cost of Capital analysis
- **Scenario Analysis**: Multiple scenario modeling with sensitivity analysis
- **Financial Metrics**: Comprehensive extraction of key financial indicators
- **Historical Benchmarking**: Industry comparison and validation

### Web Interface
- **Modern UI**: Clean, responsive design with real-time results
- **Model Selection**: Switch between different AI models seamlessly
- **Export Functionality**: Download results in JSON format
- **Health Monitoring**: Built-in health checks and status monitoring

## 📋 Prerequisites

- Python 3.8 or higher
- OpenRouter API key (for Qwen model access)
- Google AI API key (for Gemini model access)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Roy-r2004/Phonecian-capital.git
   cd Phonecian-capital
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API keys**
   
   Edit `config.py` and update the API keys:
   ```python
   # OpenRouter API Key (for Qwen)
   QWEN_CONFIG = {
       "api_key": "your-openrouter-api-key-here",
       # ... other config
   }
   
   # Google AI API Key (for Gemini)
   GEMINI_CONFIG = {
       "api_key": "your-google-ai-api-key-here",
       # ... other config
   }
   ```

## 🚀 Quick Start

1. **Start the application**
   ```bash
   python app.py
   ```

2. **Access the web interface**
   - Open your browser and navigate to `http://127.0.0.1:8000`
   - TAM Analysis: `http://127.0.0.1:8000/`
   - DCF Analysis: `http://127.0.0.1:8000/dcf`

3. **Test a prompt**
   - Select your preferred AI model (Qwen or Gemini)
   - Enter a company context or use the predefined examples
   - Click "Test Prompt" to analyze the response
   - View detailed results including quality scores and recommendations

## 📁 Project Structure

```
Phonecian-capital/
├── app.py                 # Main FastAPI application
├── config.py             # Configuration and API keys
├── requirements.txt      # Python dependencies
├── tam_qwen_agent.py     # TAM analysis agent
├── dcf_agent.py          # DCF analysis agent
├── run_tam_tests.py      # Batch testing script
├── setup_openrouter.py   # OpenRouter setup utilities
├── templates/
│   ├── index.html        # TAM analysis web interface
│   ├── dcf.html          # DCF analysis web interface
│   └── thumbnail_company_logo.png
├── Exercice 1/           # Documentation and prompts
└── venv/                 # Virtual environment
```

## 🔧 Configuration

### Available Models

The application supports multiple AI models:

- **Qwen2.5 VL 32B Instruct** (Free via OpenRouter)
- **Gemini 1.5 Pro** (Google AI)

### Test Companies

Predefined company contexts for testing:
- SaaS project management software
- Fintech digital banking
- AI computer vision solutions
- Healthcare SaaS platforms
- E-commerce marketplaces
- Cybersecurity solutions
- Logistics tech
- Edtech platforms

### Validation Thresholds

Configurable quality thresholds in `config.py`:
- Minimum quality score: 0.7
- Minimum section coverage: 0.8
- Minimum element coverage: 0.7
- Minimum response length: 1000 characters
- Maximum missing requirements: 3

## 📊 API Endpoints

### TAM Analysis
- `POST /test-single` - Test TAM prompt with single company context
- `GET /results/{test_id}` - Get detailed test results
- `GET /export-results` - Export all TAM test results

### DCF Analysis
- `POST /test-dcf` - Test DCF prompt with company context
- `GET /export-dcf-results` - Export all DCF test results

### System
- `GET /health` - Health check endpoint
- `GET /` - TAM analysis interface
- `GET /dcf` - DCF analysis interface

## 🧪 Testing

### Run Batch Tests
```bash
python run_tam_tests.py
```

This will:
- Test all predefined company contexts
- Generate comprehensive quality reports
- Save results to JSON files
- Provide detailed analysis and recommendations

### Manual Testing
Use the web interface to test custom company contexts and compare different AI models.

## 📈 Understanding Results

### Quality Scores
- **Overall Quality**: 0-1 scale based on comprehensive validation
- **Section Coverage**: Percentage of required sections present
- **Element Coverage**: Percentage of required elements found
- **Response Length**: Character count of the response

### Validation Metrics
- **Missing Requirements**: List of missing critical elements
- **Recommendations**: Specific suggestions for improvement
- **Market Metrics**: Extracted financial and market data
- **Confidence Intervals**: Uncertainty ranges in estimates



**Phoenician Capital** - Empowering financial analysis with AI-driven insights.
