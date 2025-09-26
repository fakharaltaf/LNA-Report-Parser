#!/usr/bin/env python3
"""
Main entry point for LNA Bot testing.

This script provides a simple menu-driven interface to test all
LNA Bot functionality directly from the terminal.
"""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from lna_bot import LNABot
from lna_bot.models import LNARecord, PriorityLevel, CompetencyType, RequestType
from datetime import datetime
import json

def print_menu():
    """Print the main menu."""
    print("\n" + "=" * 60)
    print("LNA Bot - AI-Powered Training Recommendations")
    print("=" * 60)
    print("1. Analyze CSV file")
    print("2. Single record analysis")
    print("3. Test business rules")
    print("4. View configuration")
    print("5. Export analysis results")
    print("6. Run all tests")
    print("7. Exit")
    print("-" * 60)

def analyze_csv():
    """Analyze a CSV file."""
    print("\nAvailable CSV files:")
    csv_files = [
        "Testing/TestData/lna_report_2024_q1.csv",
        "Testing/TestData/lna_report_2024_q2.csv", 
        "Testing/TestData/lna_report_2024_q3.csv",
        "Testing/TestData/lna_report_2024_q4_2025_preview.csv"
    ]
    
    for i, file in enumerate(csv_files, 1):
        if Path(file).exists():
            print(f"{i}. {file}")
        else:
            print(f"{i}. {file} (NOT FOUND)")
    
    print("5. Enter custom path")
    
    try:
        choice = input("\nSelect file (1-5): ").strip()
        
        if choice == "5":
            csv_path = input("Enter CSV file path: ").strip()
        elif choice in ["1", "2", "3", "4"]:
            csv_path = csv_files[int(choice) - 1]
        else:
            print("Invalid choice!")
            return
        
        if not Path(csv_path).exists():
            print(f"File not found: {csv_path}")
            return
        
        print(f"\nAnalyzing {csv_path}...")
        bot = LNABot()
        results, summary = bot.analyze_csv_file(Path(csv_path))
        
        # Display summary
        print(f"\nAnalysis Summary:")
        print("-" * 40)
        total = summary.total_entries
        type_dist = summary.training_type_distribution
        
        in_house = type_dist.get('In-house', 0)
        sdp = type_dist.get('SDP', 0)
        external = type_dist.get('External', 0)
        
        print(f"Total Records: {total}")
        print(f"In-house: {in_house} ({(in_house/total*100):.1f}%)")
        print(f"SDP: {sdp} ({(sdp/total*100):.1f}%)")
        print(f"External: {external} ({(external/total*100):.1f}%)")
        
        # Show sample results
        print(f"\nSample Results (first 10):")
        print("-" * 80)
        print(f"{'ID':<8} {'Competency':<30} {'Trainees':<10} {'Type':<12} {'Priority':<8}")
        print("-" * 80)
        
        for result in results[:10]:
            competency = result.record.targeted_competencies[:29]
            training_type = result.recommendation.training_type.value
            priority = result.record.priority.value
            
            print(f"{result.record.id:<8} {competency:<30} {result.record.estimated_trainees:<10} {training_type:<12} {priority:<8}")
        
        if len(results) > 10:
            print(f"... and {len(results) - 10} more records")
        
        # Ask to export
        export = input(f"\nExport results to JSON? (y/n): ").strip().lower()
        if export == 'y':
            output_file = Path(f"analysis_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            bot.export_results_to_json(results, summary, output_file)
            print(f"Results exported to: {output_file}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

def single_record_analysis():
    """Analyze a single record."""
    print("\nSingle Record Analysis")
    print("-" * 30)
    
    try:
        # Get input
        competency = input("Enter competency name: ").strip()
        if not competency:
            print("Competency name is required!")
            return
        
        while True:
            try:
                trainees = int(input("Enter number of trainees: ").strip())
                if trainees <= 0:
                    print("Number of trainees must be positive!")
                    continue
                break
            except ValueError:
                print("Please enter a valid number!")
        
        print("Priority levels: 1=High, 2=Medium, 3=Low")
        while True:
            try:
                priority_choice = int(input("Select priority (1-3): ").strip())
                if priority_choice == 1:
                    priority = PriorityLevel.HIGH
                elif priority_choice == 2:
                    priority = PriorityLevel.MEDIUM
                elif priority_choice == 3:
                    priority = PriorityLevel.LOW
                else:
                    print("Please enter 1, 2, or 3!")
                    continue
                break
            except ValueError:
                print("Please enter a valid number!")
        
        # Create record
        record = LNARecord(
            id=f"MANUAL_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            submission=datetime.now(),
            priority=priority,
            competency_type=CompetencyType.TECHNICAL,
            job_families="Manual Entry",
            targeted_competencies=competency,
            request_type=RequestType.NEW_TRAINING,
            targeted_audience="Manual Entry",
            estimated_trainees=trainees,
            comment="Manual entry for testing",
            year=2024,
            division="Test",
            department="Test",
            section="Test"
        )
        
        # Analyze
        bot = LNABot()
        result = bot.analyze_single_record(record)
        
        # Display result
        print(f"\nAnalysis Result:")
        print("-" * 40)
        print(f"Record ID: {result.record.id}")
        print(f"Competency: {result.record.targeted_competencies}")
        print(f"Trainees: {result.record.estimated_trainees}")
        print(f"Priority: {result.record.priority.value}")
        print(f"Recommendation: {result.recommendation.training_type.value}")
        print(f"Classification: {result.recommendation.competency_classification.value}")
        print(f"Demand Score: {result.recommendation.demand_score:.2f}")
        print(f"\nReasoning:")
        print(f"{result.recommendation.reasoning}")
        
        if result.recommendation.associated_skills:
            print(f"\nAssociated Skills ({len(result.recommendation.associated_skills)}):")
            for skill in result.recommendation.associated_skills[:5]:
                print(f"• {skill}")
            if len(result.recommendation.associated_skills) > 5:
                print(f"... and {len(result.recommendation.associated_skills) - 5} more skills")
        
    except Exception as e:
        print(f"Error: {str(e)}")

def test_business_rules():
    """Test business rule scenarios."""
    print("\nBusiness Rules Test")
    print("-" * 25)
    
    try:
        bot = LNABot()
        
        test_cases = [
            (5, "Patient Safety", "External (≤10 trainees)"),
            (25, "Communication Skills", "SDP (11-50 trainees)"),
            (75, "Patient Safety", "In-house (>50 trainees)"),
            (15, "Advanced Clinical Research", "SDP (niche competency)"),
            (60, "Specialized Surgery Techniques", "In-house (niche but >50 trainees)")
        ]
        
        print(f"{'Trainees':<10} {'Competency':<25} {'Expected':<20} {'Actual':<15}")
        print("-" * 75)
        
        for trainees, competency, expected in test_cases:
            recommendation = bot.get_training_recommendation(
                estimated_trainees=trainees,
                competency=competency
            )
            
            actual = recommendation['training_type'].value
            status = "✓" if expected.startswith(actual) else "✗"
            
            print(f"{trainees:<10} {competency[:24]:<25} {expected:<20} {actual:<15} {status}")
        
        print(f"\nBusiness Rules Summary:")
        print(f"• ≤10 trainees → External Training")
        print(f"• 11-50 trainees → Special Development Program (SDP)")
        print(f"• >50 trainees → In-house Training")
        print(f"• Niche competencies → SDP (unless >50, then In-house)")
        
    except Exception as e:
        print(f"Error: {str(e)}")

def view_configuration():
    """View current configuration."""
    print("\nConfiguration Information")
    print("-" * 35)
    
    try:
        bot = LNABot()
        config_info = bot.get_business_rules_info()
        
        print(f"Business Rules:")
        print(f"• External Threshold: ≤ {config_info['external_threshold']} trainees")
        print(f"• In-house Threshold: > {config_info['in_house_threshold']} trainees")
        print(f"• Priority Weights: {config_info['priority_weights']}")
        
        print(f"\nCompetency Classification:")
        print(f"• Niche Competencies: {config_info['niche_competencies_count']}")
        print(f"• Common Competencies: {config_info['common_competencies_count']}")
        print(f"• Total Skills Mapped: {config_info['total_skills_mapped']}")
        
        # Validation
        issues = bot.validate_configuration()
        if issues:
            print(f"\nConfiguration Issues:")
            for issue in issues:
                print(f"⚠ {issue}")
        else:
            print(f"\n✓ Configuration is valid")
        
        # Show sample competencies
        print(f"\nSample Niche Competencies:")
        niche_samples = ["Advanced Clinical Research", "Specialized Surgery Techniques", "Nuclear Medicine"]
        for comp in niche_samples:
            skills = bot.get_competency_skills(comp)
            print(f"• {comp}: {len(skills)} skills mapped")
        
    except Exception as e:
        print(f"Error: {str(e)}")

def export_analysis():
    """Export analysis results for a selected file."""
    print("\nExport Analysis Results")
    print("-" * 30)
    
    try:
        # Select file to analyze
        csv_files = [
            "Testing/TestData/lna_report_2024_q1.csv",
            "Testing/TestData/lna_report_2024_q2.csv",
            "Testing/TestData/lna_report_2024_q3.csv", 
            "Testing/TestData/lna_report_2024_q4_2025_preview.csv"
        ]
        
        print("Select file to analyze and export:")
        for i, file in enumerate(csv_files, 1):
            if Path(file).exists():
                print(f"{i}. {file}")
        
        choice = input("Select file (1-4): ").strip()
        if choice not in ["1", "2", "3", "4"]:
            print("Invalid choice!")
            return
        
        csv_path = csv_files[int(choice) - 1]
        if not Path(csv_path).exists():
            print(f"File not found: {csv_path}")
            return
        
        # Analyze
        print(f"Analyzing {csv_path}...")
        bot = LNABot()
        results, summary = bot.analyze_csv_file(Path(csv_path))
        
        # Export options
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        json_file = Path(f"lna_analysis_{timestamp}.json")
        summary_file = Path(f"lna_summary_{timestamp}.txt")
        
        # Export JSON
        bot.export_results_to_json(results, summary, json_file)
        print(f"✓ JSON results exported to: {json_file}")
        
        # Export summary
        summary_text = bot.get_summary_report(summary)
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary_text)
        print(f"✓ Summary report exported to: {summary_file}")
        
        print(f"\nExport complete! Files created:")
        print(f"• {json_file} ({json_file.stat().st_size} bytes)")
        print(f"• {summary_file} ({summary_file.stat().st_size} bytes)")
        
    except Exception as e:
        print(f"Error: {str(e)}")

def run_all_tests():
    """Run comprehensive functionality tests."""
    print("\nRunning All Tests")
    print("-" * 20)
    
    tests = [
        ("Configuration", test_configuration),
        ("Individual Record", test_individual_record),
        ("CSV Analysis", test_csv_analysis),
        ("Business Rules", test_business_rules_validation),
        ("Export Functions", test_export_functions),
        ("Error Handling", test_error_handling)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nTesting {test_name}...")
        try:
            if test_func():
                print(f"✓ {test_name} test passed")
                passed += 1
            else:
                print(f"✗ {test_name} test failed")
        except Exception as e:
            print(f"✗ {test_name} test failed: {str(e)}")
    
    print(f"\n" + "=" * 40)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! LNA Bot is fully functional.")
    else:
        print(f"❌ {total - passed} tests failed.")

def test_configuration():
    """Test configuration loading."""
    bot = LNABot()
    issues = bot.validate_configuration()
    return len(issues) == 0

def test_individual_record():
    """Test individual record analysis."""
    bot = LNABot()
    record = LNARecord(
        id="TEST001",
        submission=datetime.now(),
        priority=PriorityLevel.HIGH,
        competency_type=CompetencyType.TECHNICAL,
        job_families="Test",
        targeted_competencies="Patient Safety",
        request_type=RequestType.NEW_TRAINING,
        targeted_audience="Test",
        estimated_trainees=25,
        comment="Test",
        year=2024,
        division="Test",
        department="Test",
        section="Test"
    )
    result = bot.analyze_single_record(record)
    return result.recommendation.training_type.value == "SDP"

def test_csv_analysis():
    """Test CSV file analysis."""
    bot = LNABot()
    csv_path = Path("Testing/TestData/lna_report_2024_q1.csv")
    if not csv_path.exists():
        return False
    results, summary = bot.analyze_csv_file(csv_path)
    return len(results) == 20 and summary.total_entries == 20

def test_business_rules_validation():
    """Test business rules."""
    bot = LNABot()
    
    # Test external (≤10)
    rec1 = bot.get_training_recommendation(5, "Patient Safety")
    if rec1['training_type'].value != "External":
        return False
    
    # Test SDP (11-50)
    rec2 = bot.get_training_recommendation(25, "Communication Skills")
    if rec2['training_type'].value != "SDP":
        return False
    
    # Test In-house (>50)
    rec3 = bot.get_training_recommendation(75, "Patient Safety")
    if rec3['training_type'].value != "In-house":
        return False
    
    return True

def test_export_functions():
    """Test export functionality."""
    bot = LNABot()
    csv_path = Path("Testing/TestData/lna_report_2024_q1.csv")
    if not csv_path.exists():
        return False
    
    results, summary = bot.analyze_csv_file(csv_path)
    
    # Test JSON export
    test_file = Path("test_export.json")
    bot.export_results_to_json(results, summary, test_file)
    success = test_file.exists()
    
    if success:
        test_file.unlink()  # Clean up
    
    return success

def test_error_handling():
    """Test error handling."""
    bot = LNABot()
    
    # Test non-existent file
    try:
        bot.analyze_csv_file(Path("non_existent.csv"))
        return False  # Should have raised an exception
    except:
        pass  # Expected
    
    # Test unknown competency (should not crash)
    try:
        bot.get_training_recommendation(25, "UnknownCompetency")
        return True  # Should handle gracefully
    except:
        return False

def main():
    """Main application loop."""
    while True:
        print_menu()
        
        try:
            choice = input("Select option (1-7): ").strip()
            
            if choice == "1":
                analyze_csv()
            elif choice == "2":
                single_record_analysis()
            elif choice == "3":
                test_business_rules()
            elif choice == "4":
                view_configuration()
            elif choice == "5":
                export_analysis()
            elif choice == "6":
                run_all_tests()
            elif choice == "7":
                print("\nGoodbye!")
                break
            else:
                print("Invalid choice! Please select 1-7.")
                
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()