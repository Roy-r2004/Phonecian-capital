#!/usr/bin/env python3
"""
Simple command-line interface for running TAM prompt tests with Qwen
"""

import argparse
import sys
from tam_qwen_agent import QwenTAMAgent
from config import QWEN_CONFIG, TEST_COMPANIES, VALIDATION_THRESHOLDS

def main():
    parser = argparse.ArgumentParser(description="Test TAM estimation prompt with Qwen2.5 VL 32B (Free)")
    parser.add_argument("--company", type=str, help="Specific company context to test")
    parser.add_argument("--all-companies", action="store_true", 
                       help="Test with all predefined company contexts")
    parser.add_argument("--output", type=str, help="Output file for results")
    parser.add_argument("--verbose", action="store_true", help="Show detailed output")
    
    args = parser.parse_args()
    
    # Initialize agent with Qwen2.5 VL 32B configuration
    agent = QwenTAMAgent(
        api_key=QWEN_CONFIG["api_key"],
        base_url=QWEN_CONFIG["base_url"],
        model=QWEN_CONFIG["model"]
    )
    
    print("Using Qwen2.5 VL 32B Instruct (Free Model)")
    print(f"Base URL: {QWEN_CONFIG['base_url']}")
    print(f"Model: {QWEN_CONFIG['model']}")
    print("-" * 50)
    
    try:
        if args.company:
            # Test with specific company
            print(f"Testing with company: {args.company}")
            result = agent.test_prompt(args.company)
            print_results(result, args.verbose)
            
        elif args.all_companies:
            # Test with all companies
            print("Running comprehensive test with all companies...")
            results = agent.run_comprehensive_test(TEST_COMPANIES)
            
            # Summary
            avg_score = sum(r.quality_score for r in results) / len(results)
            print(f"\nSummary:")
            print(f"Total tests: {len(results)}")
            print(f"Average quality score: {avg_score:.2f}")
            print(f"Tests above threshold: {len([r for r in results if r.quality_score >= VALIDATION_THRESHOLDS['min_quality_score']])}")
            
            if args.verbose:
                for i, result in enumerate(results, 1):
                    print(f"\nTest {i}:")
                    print_results(result, False)
            
        else:
            # Default test
            print("Running default test...")
            result = agent.test_prompt()
            print_results(result, args.verbose)
        
        # Save results
        if args.output:
            agent.save_results(args.output)
        else:
            agent.save_results()
        
        # Generate report
        report = agent.generate_report()
        report_file = args.output.replace('.json', '.md') if args.output else None
        if report_file:
            with open(report_file, 'w') as f:
                f.write(report)
            print(f"Report saved to {report_file}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def print_results(result, verbose=False):
    """Print test results in a formatted way"""
    print(f"\nTest Results:")
    print(f"Quality Score: {result.quality_score:.2f}")
    print(f"Response Length: {len(result.response)} characters")
    print(f"Missing Requirements: {len(result.missing_requirements)}")
    
    if verbose:
        print(f"\nValidation Scores:")
        for metric, score in result.validation_scores.items():
            print(f"  {metric}: {score:.2f}")
        
        if result.missing_requirements:
            print(f"\nMissing Requirements:")
            for req in result.missing_requirements:
                print(f"  - {req}")
        
        if result.recommendations:
            print(f"\nRecommendations:")
            for rec in result.recommendations:
                print(f"  - {rec}")
        
        print(f"\nResponse Preview (first 500 chars):")
        print(result.response[:500] + "..." if len(result.response) > 500 else result.response)

if __name__ == "__main__":
    main()
