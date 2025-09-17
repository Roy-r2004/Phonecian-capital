#!/usr/bin/env python3
"""
DCF Model Prompt Testing Agent
Advanced validation system for DCF (Discounted Cash Flow) model prompts
"""

import json
import requests
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import re

@dataclass
class DCFTestResult:
    """Data class to store DCF test results"""
    test_id: str
    timestamp: datetime
    prompt_used: str
    response: str
    validation_scores: Dict[str, float]
    missing_requirements: List[str]
    quality_score: float
    recommendations: List[str]
    financial_metrics: Dict[str, Any]

class DCFPromptValidator:
    """Advanced validator for DCF prompt responses"""
    
    def __init__(self):
        # Required sections for DCF analysis
        self.required_sections = [
            "Model Construction",
            "DCF Summary Table", 
            "WACC Calculation",
            "Three-Statement Model",
            "Scenario Analysis",
            "Sensitivity Analysis",
            "Historical Benchmarking",
            "Key Value Drivers",
            "Final Deliverables"
        ]
        
        # Required financial elements
        self.required_elements = {
            "revenue_projection": r"revenue|sales|top line",
            "free_cash_flow": r"free cash flow|FCF",
            "discounted_cash_flow": r"discounted|DCF|present value",
            "terminal_value": r"terminal value|perpetuity",
            "wacc_calculation": r"WACC|weighted average cost of capital",
            "cost_of_equity": r"cost of equity|CAPM|beta",
            "cost_of_debt": r"cost of debt|interest rate",
            "growth_rates": r"growth rate|CAGR|compound annual",
            "margin_evolution": r"margin|profitability|operating leverage",
            "working_capital": r"working capital|AR|AP|inventory",
            "capex": r"CapEx|capital expenditure|PP&E",
            "depreciation": r"depreciation|amortization",
            "tax_rate": r"tax rate|tax expense",
            "scenario_analysis": r"bull case|base case|bear case|scenario",
            "sensitivity_analysis": r"sensitivity|±\d+%|variation",
            "historical_benchmarking": r"historical|benchmark|precedent",
            "value_drivers": r"value driver|key driver|valuation swing",
            "excel_requirement": r"excel|worksheet|formula|linked"
        }
        
        # Financial metrics patterns
        self.financial_metrics = {
            "revenue_numbers": r"\$[\d,]+(?:\.\d+)?[BMK]?",
            "growth_percentages": r"\d+(?:\.\d+)?%",
            "wacc_percentage": r"WACC.*?(\d+(?:\.\d+)?%)",
            "terminal_growth": r"terminal.*?growth.*?(\d+(?:\.\d+)?%)",
            "discount_rates": r"discount.*?rate.*?(\d+(?:\.\d+)?%)",
            "valuation_numbers": r"equity value.*?\$[\d,]+(?:\.\d+)?[BMK]?",
            "per_share_value": r"per share.*?\$[\d,]+(?:\.\d+)?"
        }
    
    def validate_response(self, response: str) -> Dict[str, Any]:
        """Comprehensive validation of DCF response"""
        validation_results = {
            "sections_found": [],
            "elements_found": {},
            "financial_metrics": {},
            "missing_requirements": [],
            "quality_indicators": {},
            "overall_score": 0.0
        }
        
        response_lower = response.lower()
        
        # Check for required sections
        for section in self.required_sections:
            if section.lower() in response_lower:
                validation_results["sections_found"].append(section)
            else:
                validation_results["missing_requirements"].append(f"Missing section: {section}")
        
        # Check for required elements
        for element, pattern in self.required_elements.items():
            matches = re.findall(pattern, response, re.IGNORECASE)
            validation_results["elements_found"][element] = len(matches)
            if len(matches) == 0:
                validation_results["missing_requirements"].append(f"Missing element: {element}")
        
        # Extract financial metrics
        for metric, pattern in self.financial_metrics.items():
            matches = re.findall(pattern, response, re.IGNORECASE)
            validation_results["financial_metrics"][metric] = matches
        
        # Calculate quality indicators
        validation_results["quality_indicators"] = {
            "section_coverage": len(validation_results["sections_found"]) / len(self.required_sections),
            "element_coverage": len([e for e in validation_results["elements_found"].values() if e > 0]) / len(self.required_elements),
            "response_length": len(response),
            "has_financial_calculations": bool(re.search(r"\d+[\+\-\*\/]\d+|\$[\d,]+", response)),
            "has_tables": bool(re.search(r"table|worksheet|excel", response, re.IGNORECASE)),
            "has_scenarios": bool(re.search(r"bull|base|bear|scenario", response, re.IGNORECASE)),
            "has_sensitivity": bool(re.search(r"sensitivity|±\d+%", response, re.IGNORECASE)),
            "has_historical_analysis": bool(re.search(r"historical|benchmark|precedent", response, re.IGNORECASE)),
            "financial_metrics_count": sum(len(matches) for matches in validation_results["financial_metrics"].values())
        }
        
        # Calculate overall score with weighted components
        indicators = validation_results["quality_indicators"]
        validation_results["overall_score"] = (
            indicators["section_coverage"] * 0.25 +
            indicators["element_coverage"] * 0.25 +
            (1 if indicators["has_financial_calculations"] else 0) * 0.15 +
            (1 if indicators["has_tables"] else 0) * 0.10 +
            (1 if indicators["has_scenarios"] else 0) * 0.10 +
            (1 if indicators["has_sensitivity"] else 0) * 0.10 +
            min(indicators["financial_metrics_count"] / 10, 1) * 0.05  # Bonus for financial metrics
        )
        
        return validation_results

class DCFAgent:
    """Main agent for testing DCF prompts with AI models"""
    
    def __init__(self, api_key: str = None, base_url: str = "https://openrouter.ai/api/v1", model: str = "qwen/qwen2.5-vl-32b-instruct:free"):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.validator = DCFPromptValidator()
        self.test_results = []
        
    def load_dcf_prompt(self) -> str:
        """Load the DCF model prompt from file"""
        try:
            with open(r"C:\Phonecian Capital\Exercice 1\PROMPT2_DCF_Roy Rizkallah_September 17.doc", 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error loading DCF prompt: {e}")
            return ""
    
    def send_to_ai(self, prompt: str, company_context: str = "", max_retries: int = 3) -> str:
        """Send prompt to AI model and get response"""
        for attempt in range(max_retries):
            try:
                print(f"Attempt {attempt + 1}/{max_retries}...")
                
                # Prepare the full prompt with company context
                full_prompt = f"""
You are a senior financial analyst conducting a comprehensive 10-year DCF (Discounted Cash Flow) valuation analysis.

Company Context: {company_context}

Please provide a detailed DCF analysis following this framework:

{prompt}

Provide a comprehensive, professional DCF valuation suitable for institutional investors and investment committees.
"""
                
                # API call
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}" if self.api_key else "",
                    "HTTP-Referer": "https://github.com/your-repo/dcf-agent",
                    "X-Title": "DCF Analysis Agent"
                }
                
                payload = {
                    "model": self.model,
                    "messages": [
                        {"role": "user", "content": full_prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 3000  # DCF analysis needs more tokens
                }
                
                print("Sending request to AI model...")
                response = requests.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=45
                )
                
                print(f"Response status: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    content = result["choices"][0]["message"]["content"]
                    print(f"Success! Response length: {len(content)} characters")
                    return content
                else:
                    error_detail = response.text
                    try:
                        error_json = response.json()
                        if "error" in error_json:
                            error_detail = error_json["error"].get("message", error_detail)
                    except:
                        pass
                    print(f"API Error: {response.status_code} - {error_detail}")
                    
                    if attempt < max_retries - 1:
                        print(f"Retrying in 2 seconds...")
                        time.sleep(2)
                        continue
                    else:
                        return f"Error: {response.status_code} - {error_detail}"
                    
            except requests.exceptions.Timeout:
                print(f"Timeout on attempt {attempt + 1}")
                if attempt < max_retries - 1:
                    print("Retrying...")
                    time.sleep(2)
                    continue
                else:
                    return "Error: Request timeout - API is taking too long to respond"
                    
            except requests.exceptions.ConnectionError:
                print(f"Connection error on attempt {attempt + 1}")
                if attempt < max_retries - 1:
                    print("Retrying...")
                    time.sleep(2)
                    continue
                else:
                    return "Error: Connection failed - Check your internet connection"
                    
            except Exception as e:
                print(f"Unexpected error: {str(e)}")
                if attempt < max_retries - 1:
                    print("Retrying...")
                    time.sleep(2)
                    continue
                else:
                    return f"Error: {str(e)}"
        
        return "Error: All retry attempts failed"
    
    def test_prompt(self, company_context: str = "A SaaS company with recurring revenue model") -> DCFTestResult:
        """Test the DCF prompt with AI model"""
        print("Loading DCF prompt...")
        prompt = self.load_dcf_prompt()
        
        if not prompt:
            raise ValueError("Could not load DCF prompt")
        
        print("Sending prompt to AI model...")
        response = self.send_to_ai(prompt, company_context)
        
        print("Validating response...")
        validation = self.validator.validate_response(response)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(validation)
        
        # Create test result
        test_result = DCFTestResult(
            test_id=f"dcf_test_{int(time.time())}",
            timestamp=datetime.now(),
            prompt_used=prompt[:200] + "..." if len(prompt) > 200 else prompt,
            response=response,
            validation_scores=validation["quality_indicators"],
            missing_requirements=validation["missing_requirements"],
            quality_score=validation["overall_score"],
            recommendations=recommendations,
            financial_metrics=validation["financial_metrics"]
        )
        
        self.test_results.append(test_result)
        return test_result
    
    def _generate_recommendations(self, validation: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on validation results"""
        recommendations = []
        
        if validation["quality_indicators"]["section_coverage"] < 0.8:
            recommendations.append("Consider adding more explicit section headers to guide the AI model")
        
        if validation["quality_indicators"]["element_coverage"] < 0.7:
            recommendations.append("Add more specific examples of required DCF elements in the prompt")
        
        if not validation["quality_indicators"]["has_financial_calculations"]:
            recommendations.append("Prompt should explicitly request numerical DCF calculations and formulas")
        
        if not validation["quality_indicators"]["has_tables"]:
            recommendations.append("Consider requesting structured DCF tables and Excel-like outputs")
        
        if not validation["quality_indicators"]["has_scenarios"]:
            recommendations.append("Add explicit requirements for bull/base/bear scenario analysis")
        
        if not validation["quality_indicators"]["has_sensitivity"]:
            recommendations.append("Request sensitivity analysis with specific percentage variations")
        
        if validation["quality_indicators"]["financial_metrics_count"] < 5:
            recommendations.append("Prompt should request more specific financial metrics and numbers")
        
        if len(validation["missing_requirements"]) > 5:
            recommendations.append("DCF prompt may be too complex - consider breaking into focused sections")
        
        return recommendations
    
    def run_comprehensive_test(self, companies: List[str] = None) -> List[DCFTestResult]:
        """Run DCF tests with multiple company contexts"""
        if companies is None:
            companies = [
                "A SaaS company with recurring revenue model and high customer retention",
                "A manufacturing company with cyclical revenue and capital-intensive operations",
                "A fintech startup with high growth potential but regulatory risks",
                "A healthcare company with long product development cycles",
                "An e-commerce platform with seasonal variations and logistics complexity"
            ]
        
        results = []
        for company in companies:
            print(f"\nTesting DCF with company: {company}")
            try:
                result = self.test_prompt(company)
                results.append(result)
                print(f"DCF Quality Score: {result.quality_score:.2f}")
            except Exception as e:
                print(f"Error testing {company}: {e}")
        
        return results
    
    def generate_report(self, results: List[DCFTestResult] = None) -> str:
        """Generate a comprehensive DCF test report"""
        if results is None:
            results = self.test_results
        
        if not results:
            return "No DCF test results available"
        
        report = f"""
# DCF Model Prompt Testing Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary
- Total DCF Tests: {len(results)}
- Average Quality Score: {sum(r.quality_score for r in results) / len(results):.2f}
- Tests with High Quality (≥80%): {len([r for r in results if r.quality_score >= 0.8])}
- Tests with Financial Calculations: {len([r for r in results if r.validation_scores.get('has_financial_calculations', False)])}

## Detailed Results
"""
        
        for i, result in enumerate(results, 1):
            report += f"""
### DCF Test {i} - {result.test_id}
- Quality Score: {result.quality_score:.2f}
- Response Length: {len(result.response)} characters
- Missing Requirements: {len(result.missing_requirements)}

#### Validation Scores:
"""
            for metric, score in result.validation_scores.items():
                report += f"- {metric}: {score:.2f}\n"
            
            if result.financial_metrics:
                report += "\n#### Financial Metrics Found:\n"
                for metric, values in result.financial_metrics.items():
                    if values:
                        report += f"- {metric}: {len(values)} instances\n"
            
            if result.missing_requirements:
                report += "\n#### Missing Requirements:\n"
                for req in result.missing_requirements:
                    report += f"- {req}\n"
            
            if result.recommendations:
                report += "\n#### Recommendations:\n"
                for rec in result.recommendations:
                    report += f"- {rec}\n"
            
            report += "\n---\n"
        
        return report
    
    def save_results(self, filename: str = None):
        """Save DCF test results to JSON file"""
        if filename is None:
            filename = f"dcf_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        data = []
        for result in self.test_results:
            data.append({
                "test_id": result.test_id,
                "timestamp": result.timestamp.isoformat(),
                "quality_score": result.quality_score,
                "validation_scores": result.validation_scores,
                "missing_requirements": result.missing_requirements,
                "recommendations": result.recommendations,
                "financial_metrics": result.financial_metrics,
                "response_length": len(result.response)
            })
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"DCF results saved to {filename}")

def main():
    """Main function to run the DCF prompt testing agent"""
    print("DCF Model Prompt Testing Agent")
    print("=" * 50)
    
    # Initialize agent
    agent = DCFAgent()
    
    # Test with a single company
    print("\nRunning DCF test...")
    result = agent.test_prompt("A SaaS company with recurring revenue model")
    
    print(f"\nDCF Test Results:")
    print(f"Quality Score: {result.quality_score:.2f}")
    print(f"Missing Requirements: {len(result.missing_requirements)}")
    print(f"Recommendations: {len(result.recommendations)}")
    print(f"Financial Metrics: {sum(len(m) for m in result.financial_metrics.values())}")
    
    # Generate and display report
    report = agent.generate_report()
    print("\n" + report)
    
    # Save results
    agent.save_results()

if __name__ == "__main__":
    main()
