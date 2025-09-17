"""
Configuration file for TAM Qwen Agent
"""

# OpenRouter API Configuration
OPENROUTER_CONFIG = {
    "base_url": "https://openrouter.ai/api/v1",
    "api_key": "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", 
    "timeout": 60,
    "max_tokens": 4000,
    "temperature": 0.7
}

# Qwen2.5 VL 32B Instruct (Free Model)
QWEN_MODEL = "qwen/qwen2.5-vl-32b-instruct:free"

# Qwen2.5 VL 32B Configuration (Free Model)
QWEN_CONFIG = {
    "base_url": "https://openrouter.ai/api/v1",
    "model": "qwen/qwen2.5-vl-32b-instruct:free",
    "api_key": "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",
    "timeout": 60,
    "max_tokens": 4000,
    "temperature": 0.7
}

# Gemini Configuration
GEMINI_CONFIG = {
    "base_url": "https://generativelanguage.googleapis.com/v1beta",
    "model": "gemini-1.5-pro",
    "api_key": "AIzaSyAi192yjl0QxTExI6c0_MNQF_Yac-VwlOk",
    "timeout": 60,
    "max_tokens": 4000,
    "temperature": 0.7
}

# Available Models
AVAILABLE_MODELS = {
    "qwen": QWEN_CONFIG,
    "gemini": GEMINI_CONFIG
}

# Test company contexts
TEST_COMPANIES = [
    "A SaaS company providing project management software to small and medium businesses",
    "A fintech startup offering digital banking services to millennials",
    "An AI company providing computer vision solutions to manufacturing companies",
    "A healthcare SaaS platform for small medical practices",
    "An e-commerce marketplace for sustainable products",
    "A cybersecurity company offering endpoint protection to enterprises",
    "A logistics tech company providing last-mile delivery solutions",
    "An edtech platform for online coding bootcamps"
]

# Validation thresholds
VALIDATION_THRESHOLDS = {
    "min_quality_score": 0.7,
    "min_section_coverage": 0.8,
    "min_element_coverage": 0.7,
    "min_response_length": 1000,
    "max_missing_requirements": 3
}
