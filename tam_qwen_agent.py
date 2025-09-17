#!/usr/bin/env python3
"""
TAM Estimation Prompt Testing Agent with Qwen LLM Integration
This agent tests the TAM estimation prompt by sending it to Qwen and analyzing the responses.
"""

import json
import requests
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import re

@dataclass
class PromptTestResult:
    """Data class to store test results"""
    test_id: str
    timestamp: datetime
    prompt_used: str
    response: str
    validation_scores: Dict[str, float]
    missing_requirements: List[str]
    quality_score: float
    recommendations: List[str]
    market_metrics: Dict[str, Any]

class TAMPromptValidator:
    """Validates TAM prompt responses against requirements"""
    
    def __init__(self):
        self.required_sections = [
            "Opening Overview",
            "Bottom-Up Analysis", 
            "Top-Down Analysis",
            "Hybrid Analysis",
            "Market Capture Analysis",
            "Final Deliverables"
        ]
        
        self.required_elements = {
            "market_size": r"\$[\d,]+(?:\.\d+)?[BMK]?",
            "confidence_intervals": r"confidence|interval|range",
            "methodology": r"method|approach|analysis",
            "customer_segments": r"segment|customer|enterprise|SMB|consumer",
            "acv_ltv": r"ACV|LTV|average customer value|lifetime value",
            "penetration_rate": r"penetration|market share|capture",
            "sources": r"source|reference|Gartner|IDC|McKinsey",
            "sensitivity": r"sensitivity|±\d+%|scenario",
            "revenue_projection": r"revenue|projection|3-year|5-year",
            "constraints_enablers": r"constraint|enabler|barrier|moat"
        }
    
    def validate_response(self, response: str) -> Dict[str, Any]:
        """Validate response against TAM prompt requirements"""
        validation_results = {
            "sections_found": [],
            "elements_found": {},
            "missing_requirements": [],
            "quality_indicators": {},
            "overall_score": 0.0
        }
        
        # Check for required sections
        response_lower = response.lower()
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
        
        # Extract market metrics
        market_metrics = {
            "market_size_numbers": re.findall(r"\$[\d,]+(?:\.\d+)?[BMK]?", response, re.IGNORECASE),
            "growth_percentages": re.findall(r"\d+(?:\.\d+)?%", response),
            "market_share": re.findall(r"market share.*?(\d+(?:\.\d+)?%)", response, re.IGNORECASE),
            "penetration_rates": re.findall(r"penetration.*?(\d+(?:\.\d+)?%)", response, re.IGNORECASE),
            "customer_numbers": re.findall(r"[\d,]+(?:\.\d+)?\s*(?:customers|users|subscribers)", response, re.IGNORECASE),
            "revenue_projections": re.findall(r"revenue.*?\$[\d,]+(?:\.\d+)?[BMK]?", response, re.IGNORECASE),
            "market_cagr": re.findall(r"CAGR.*?(\d+(?:\.\d+)?%)", response, re.IGNORECASE),
            "geographic_coverage": re.findall(r"(?:global|regional|national|international)", response, re.IGNORECASE)
        }
        
        # Calculate quality indicators
        validation_results["quality_indicators"] = {
            "section_coverage": len(validation_results["sections_found"]) / len(self.required_sections),
            "element_coverage": len([e for e in validation_results["elements_found"].values() if e > 0]) / len(self.required_elements),
            "response_length": len(response),
            "has_calculations": bool(re.search(r"\d+[\+\-\*\/]\d+|\$[\d,]+", response)),
            "has_tables": bool(re.search(r"table|worksheet|excel", response, re.IGNORECASE)),
            "has_segmentation": bool(re.search(r"segment|customer|enterprise|SMB|consumer", response, re.IGNORECASE)),
            "market_metrics_count": sum(len(matches) for matches in market_metrics.values())
        }
        
        # Add market metrics to results
        validation_results["market_metrics"] = market_metrics
        
        # Calculate overall score
        validation_results["overall_score"] = (
            validation_results["quality_indicators"]["section_coverage"] * 0.4 +
            validation_results["quality_indicators"]["element_coverage"] * 0.4 +
            (1 if validation_results["quality_indicators"]["has_calculations"] else 0) * 0.1 +
            (1 if validation_results["quality_indicators"]["has_tables"] else 0) * 0.1
        )
        
        return validation_results

class QwenTAMAgent:
    """Main agent for testing TAM prompts with Qwen LLM"""
    
    def __init__(self, api_key: str = None, base_url: str = "https://openrouter.ai/api/v1", model: str = "qwen/qwen2.5-vl-32b-instruct:free"):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.validator = TAMPromptValidator()
        self.test_results = []
        
    def load_tam_prompt(self) -> str:
        """Load the TAM estimation prompt from file"""
        try:
            with open(r"C:\Phonecian Capital\Exercice 1\PROMPT1_TAM_Roy Rizkallah_September 17.doc", 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error loading TAM prompt: {e}")
            return ""
    
    def send_to_qwen(self, prompt: str, company_context: str = "") -> str:
        """Send prompt to Qwen LLM via OpenRouter and get response"""
        try:
            # Prepare the full prompt with company context
            full_prompt = f"""
You are a financial analyst conducting a Total Addressable Market (TAM) analysis. 

Company Context: {company_context}

Please provide a comprehensive TAM analysis following this framework:

{prompt}

Provide a detailed, professional analysis suitable for investment committee review.
"""
            
            # OpenRouter API call
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}" if self.api_key else "",
                "HTTP-Referer": "https://github.com/your-repo/tam-agent",  # Optional: for OpenRouter tracking
                "X-Title": "TAM Analysis Agent"  # Optional: for OpenRouter tracking
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "user", "content": full_prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 2000
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                error_detail = response.text
                try:
                    error_json = response.json()
                    if "error" in error_json:
                        error_detail = error_json["error"].get("message", error_detail)
                except:
                    pass
                return f"Error: {response.status_code} - {error_detail}"
                
        except Exception as e:
            return f"Error connecting to OpenRouter: {str(e)}"
    
    def test_prompt(self, company_context: str = "A SaaS company providing project management software to small and medium businesses") -> PromptTestResult:
        """Test the TAM prompt with Qwen"""
        try:
            print("Loading TAM prompt...")
            prompt = self.load_tam_prompt()
            
            if not prompt:
                raise ValueError("Could not load TAM prompt")
            
            print("Sending prompt to AI model...")
            if "gemini" in self.model.lower():
                response = self.send_to_gemini(prompt, company_context)
            else:
                response = self.send_to_qwen(prompt, company_context)
            
            print(f"Response received, length: {len(response)}")
            
            if response.startswith("Error:"):
                raise ValueError(f"API Error: {response}")
            
            print("Validating response...")
            validation = self.validator.validate_response(response)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(validation)
            
            # Create test result
            test_result = PromptTestResult(
                test_id=f"test_{int(time.time())}",
                timestamp=datetime.now(),
                prompt_used=prompt[:200] + "..." if len(prompt) > 200 else prompt,
                response=response,
                validation_scores=validation["quality_indicators"],
                missing_requirements=validation["missing_requirements"],
                quality_score=validation["overall_score"],
                recommendations=recommendations,
                market_metrics=validation["market_metrics"]
            )
            
            self.test_results.append(test_result)
            return test_result
            
        except Exception as e:
            print(f"Error in test_prompt: {str(e)}")
            raise
    
    def send_to_gemini(self, prompt: str, company_context: str = "", max_retries: int = 3) -> str:
        """Send prompt to Gemini LLM and get response"""
        for attempt in range(max_retries):
            try:
                print(f"Attempt {attempt + 1}/{max_retries}...")
                
                # Prepare the full prompt with company context
                full_prompt = f"""
You are a financial analyst conducting a Total Addressable Market (TAM) analysis. 

Company Context: {company_context}

Please provide a comprehensive TAM analysis following this framework:

{prompt}

Provide a detailed, professional analysis suitable for investment committee review.
"""
                
                # Gemini API call
                headers = {
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "contents": [{
                        "parts": [{
                            "text": full_prompt
                        }]
                    }],
                    "generationConfig": {
                        "temperature": 0.7,
                        "maxOutputTokens": 2000
                    }
                }
                
                print("Sending request to Gemini...")
                response = requests.post(
                    f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}",
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                
                print(f"Response status: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    if "candidates" in result and len(result["candidates"]) > 0:
                        content = result["candidates"][0]["content"]["parts"][0]["text"]
                        print(f"Success! Response length: {len(content)} characters")
                        return content
                    else:
                        print("No content in response")
                        return "Error: No content generated"
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
    
    def _generate_recommendations(self, validation: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on validation results"""
        recommendations = []
        
        if validation["quality_indicators"]["section_coverage"] < 0.8:
            recommendations.append("Consider adding more explicit section headers to guide the LLM")
        
        if validation["quality_indicators"]["element_coverage"] < 0.7:
            recommendations.append("Add more specific examples of required elements in the prompt")
        
        if not validation["quality_indicators"]["has_calculations"]:
            recommendations.append("Prompt should explicitly request numerical calculations and formulas")
        
        if not validation["quality_indicators"]["has_tables"]:
            recommendations.append("Consider requesting structured table outputs for better organization")
        
        if len(validation["missing_requirements"]) > 3:
            recommendations.append("Prompt may be too complex - consider breaking into smaller, focused sections")
        
        return recommendations
    
    def run_comprehensive_test(self, companies: List[str] = None) -> List[PromptTestResult]:
        """Run tests with multiple company contexts"""
        if companies is None:
            companies = [
                "A fintech startup offering digital banking services to millennials",
                "An AI company providing computer vision solutions to manufacturing",
                "A healthcare SaaS platform for small medical practices",
                "An e-commerce marketplace for sustainable products"
            ]
        
        results = []
        for company in companies:
            print(f"\nTesting with company: {company}")
            try:
                result = self.test_prompt(company)
                results.append(result)
                print(f"Quality Score: {result.quality_score:.2f}")
            except Exception as e:
                print(f"Error testing {company}: {e}")
        
        return results
    
    def generate_report(self, results: List[PromptTestResult] = None) -> str:
        """Generate a comprehensive test report"""
        if results is None:
            results = self.test_results
        
        if not results:
            return "No test results available"
        
        report = f"""
# TAM Prompt Testing Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
- Total Tests: {len(results)}
- Average Quality Score: {sum(r.quality_score for r in results) / len(results):.2f}
- Tests with Issues: {len([r for r in results if r.quality_score < 0.7])}

## Detailed Results
"""
        
        for i, result in enumerate(results, 1):
            report += f"""
### Test {i} - {result.test_id}
- Quality Score: {result.quality_score:.2f}
- Response Length: {len(result.response)} characters
- Missing Requirements: {len(result.missing_requirements)}

#### Validation Scores:
"""
            for metric, score in result.validation_scores.items():
                report += f"- {metric}: {score:.2f}\n"
            
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
        """Save test results to JSON file"""
        if filename is None:
            filename = f"tam_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        data = []
        for result in self.test_results:
            data.append({
                "test_id": result.test_id,
                "timestamp": result.timestamp.isoformat(),
                "quality_score": result.quality_score,
                "validation_scores": result.validation_scores,
                "missing_requirements": result.missing_requirements,
                "recommendations": result.recommendations,
                "response_length": len(result.response)
            })
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Results saved to {filename}")

def main():
    """Main function to run the TAM prompt testing agent"""
    print("TAM Estimation Prompt Testing Agent with Qwen")
    print("=" * 50)
    
    # Initialize agent
    agent = QwenTAMAgent()
    
    # Test with a single company
    print("\nRunning single test...")
    result = agent.test_prompt("A cloud-based CRM company targeting mid-market businesses")
    
    print(f"\nTest Results:")
    print(f"Quality Score: {result.quality_score:.2f}")
    print(f"Missing Requirements: {len(result.missing_requirements)}")
    print(f"Recommendations: {len(result.recommendations)}")
    
    # Run comprehensive test
    print("\nRunning comprehensive test...")
    comprehensive_results = agent.run_comprehensive_test()
    
    # Generate and display report
    report = agent.generate_report(comprehensive_results)
    print("\n" + report)
    
    # Save results
    agent.save_results()
    
    # Save full report
    report_filename = f"tam_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(report_filename, 'w') as f:
        f.write(report)
    print(f"Full report saved to {report_filename}")

if __name__ == "__main__":
    main()
