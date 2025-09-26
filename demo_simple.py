"""
Simple demonstration script showing LNA Bot functionality.
"""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"  
sys.path.insert(0, str(src_path))

from lna_bot import LNABot

def main():
    """Demonstrate LNA Bot functionality."""
    
    print("\nLNA Bot - AI-Powered Training Recommendations")
    print("=" * 50)
    
    try:
        # Initialize bot
        print("Initializing LNA Bot...")
        bot = LNABot()
        
        # Show configuration info
        print("\nConfiguration Information:")
        config_info = bot.get_business_rules_info()
        
        print(f"External Threshold: ≤ {config_info['external_threshold']} trainees")
        print(f"In-house Threshold: > {config_info['in_house_threshold']} trainees") 
        print(f"Total Skills Mapped: {config_info['total_skills_mapped']}")
        print(f"Niche Competencies: {config_info['niche_competencies_count']}")
        print(f"Common Competencies: {config_info['common_competencies_count']}")
        
        # Analyze a sample file
        csv_file = Path("Testing/TestData/lna_report_2024_q1.csv")
        print(f"\nAnalyzing sample file: {csv_file}")
        
        results, summary = bot.analyze_csv_file(csv_file)
        
        # Show summary
        print(f"\nAnalysis Summary:")
        total = summary.total_entries
        type_dist = summary.training_type_distribution
        
        in_house = type_dist.get('In-house', 0)
        sdp = type_dist.get('SDP', 0)
        external = type_dist.get('External', 0)
        
        print(f"In-house: {in_house} ({(in_house/total*100):.1f}%)")
        print(f"SDP: {sdp} ({(sdp/total*100):.1f}%)")
        print(f"External: {external} ({(external/total*100):.1f}%)")
        print(f"Total: {total} (100.0%)")
        
        # Show sample recommendations
        print(f"\nSample Recommendations (first 5):")
        print("-" * 80)
        print(f"{'ID':<8} {'Competency':<25} {'Trainees':<10} {'Training Type':<15} {'Priority':<10}")
        print("-" * 80)
        
        for result in results[:5]:
            competency_name = result.record.targeted_competencies
            training_type = result.recommendation.training_type
            priority = result.record.priority
            
            training_type_str = training_type.value if hasattr(training_type, 'value') else str(training_type)
            priority_str = priority.value if hasattr(priority, 'value') else str(priority)
            
            print(f"{result.record.id:<8} {competency_name[:25]:<25} {result.record.estimated_trainees:<10} {training_type_str:<15} {priority_str:<10}")
        
        # Show example reasoning
        if results:
            first_result = results[0]
            print(f"\nExample Recommendation - {first_result.record.id}:")
            print("-" * 40)
            print(f"Competency: {first_result.record.targeted_competencies}")
            print(f"Trainees: {first_result.record.estimated_trainees}")
            training_type_val = first_result.recommendation.training_type.value if hasattr(first_result.recommendation.training_type, 'value') else str(first_result.recommendation.training_type)
            print(f"Recommendation: {training_type_val}")
            print(f"Reasoning: {first_result.recommendation.reasoning}")
        
        # Show single record analysis example
        print(f"\nInteractive Example:")
        print("-" * 30)
        recommendation = bot.get_training_recommendation(
            estimated_trainees=25,
            competency="Patient Safety"
        )
        
        print(f"Input:")
        print(f"• Competency: Patient Safety")
        print(f"• Estimated Trainees: 25")
        print(f"")
        print(f"Recommendation: {recommendation['training_type'].value}")
        print(f"Classification: {recommendation['competency_classification'].value}")
        print(f"Reasoning: {recommendation['reasoning']}")
        print(f"Associated Skills: {len(recommendation['associated_skills'])} skills mapped")
        
        print(f"\n✓ Demonstration complete!")
        print(f"Processed {len(results)} records from {csv_file}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    main()