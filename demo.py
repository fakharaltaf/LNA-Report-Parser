"""
Demonstration script showing LNA Bot functionality.
"""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"  
sys.path.insert(0, str(src_path))

from lna_bot import LNABot
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def main():
    """Demonstrate LNA Bot functionality."""
    
    # Print banner
    console.print("\n[bold blue]LNA Bot - AI-Powered Training Recommendations[/bold blue]\n")
    
    try:
        # Initialize bot
        console.print("[green]Initializing LNA Bot...[/green]")
        bot = LNABot()
        
        # Show configuration info
        console.print("\n[bold green]Configuration Information:[/bold green]")
        config_info = bot.get_business_rules_info()
        
        config_table = Table()
        config_table.add_column("Setting", style="cyan")
        config_table.add_column("Value", style="magenta")
        
        config_table.add_row("External Threshold", f"≤ {config_info['external_threshold']} trainees")
        config_table.add_row("In-house Threshold", f"> {config_info['in_house_threshold']} trainees") 
        config_table.add_row("Total Skills Mapped", str(config_info['total_skills_mapped']))
        config_table.add_row("Niche Competencies", str(config_info['niche_competencies_count']))
        config_table.add_row("Common Competencies", str(config_info['common_competencies_count']))
        
        console.print(config_table)
        
        # Analyze a sample file
        csv_file = Path("Testing/TestData/lna_report_2024_q1.csv")
        console.print(f"\n[green]Analyzing sample file: {csv_file}[/green]")
        
        results, summary = bot.analyze_csv_file(csv_file)
        
        # Show summary
        console.print(f"\n[bold green]Analysis Summary:[/bold green]")
        summary_table = Table()
        summary_table.add_column("Training Type", style="cyan")
        summary_table.add_column("Count", style="magenta")
        summary_table.add_column("Percentage", style="green")
        
        total = summary.total_entries
        type_dist = summary.training_type_distribution
        
        in_house = type_dist.get('In-house', 0)
        sdp = type_dist.get('SDP', 0)
        external = type_dist.get('External', 0)
        
        summary_table.add_row("In-house", str(in_house), f"{(in_house/total*100):.1f}%")
        summary_table.add_row("SDP", str(sdp), f"{(sdp/total*100):.1f}%")
        summary_table.add_row("External", str(external), f"{(external/total*100):.1f}%")
        summary_table.add_row("[bold]Total", f"[bold]{total}", "[bold]100.0%")
        
        console.print(summary_table)
        
        # Show sample recommendations
        console.print(f"\n[bold green]Sample Recommendations (first 5):[/bold green]")
        results_table = Table()
        results_table.add_column("ID", width=8)
        results_table.add_column("Competency", style="cyan")
        results_table.add_column("Trainees", style="magenta", justify="right")
        results_table.add_column("Training Type", style="green")
        results_table.add_column("Priority", style="yellow")
        
        for result in results[:5]:
            competency_name = result.record.targeted_competencies
            # Handle enum values properly
            training_type = result.recommendation.training_type
            priority = result.record.priority
            
            training_type_str = training_type.value if hasattr(training_type, 'value') else str(training_type)
            priority_str = priority.value if hasattr(priority, 'value') else str(priority)
            
            results_table.add_row(
                result.record.id,
                competency_name[:30] + "..." if len(competency_name) > 30 else competency_name,
                str(result.record.estimated_trainees),
                training_type_str,
                priority_str
            )
        
        console.print(results_table)
        
        # Show example reasoning
        if results:
            first_result = results[0]
            reasoning_panel = Panel(
                f"[bold]Competency:[/bold] {first_result.record.targeted_competencies}\n"
                f"[bold]Trainees:[/bold] {first_result.record.estimated_trainees}\n"
                f"[bold]Recommendation:[/bold] {first_result.recommendation.training_type.value if hasattr(first_result.recommendation.training_type, 'value') else str(first_result.recommendation.training_type)}\n\n"
                f"[bold]Reasoning:[/bold]\n{first_result.recommendation.reasoning}",
                title=f"Example Recommendation - {first_result.record.id}",
                border_style="blue"
            )
            console.print(f"\n{reasoning_panel}")
        
        # Show single record analysis example
        console.print(f"\n[bold green]Interactive Example:[/bold green]")
        recommendation = bot.get_training_recommendation(
            estimated_trainees=25,
            competency="Patient Safety"
        )
        
        interactive_panel = Panel(
            f"[bold]Input:[/bold]\n"
            f"• Competency: Patient Safety\n"
            f"• Estimated Trainees: 25\n\n"
            f"[bold]Recommendation:[/bold] {recommendation['training_type'].value}\n"
            f"[bold]Classification:[/bold] {recommendation['competency_classification'].value}\n\n"
            f"[bold]Reasoning:[/bold]\n{recommendation['reasoning']}\n\n"
            f"[bold]Associated Skills:[/bold] {len(recommendation['associated_skills'])} skills mapped",
            title="Interactive Analysis Example",
            border_style="green"
        )
        console.print(interactive_panel)
        
        console.print(f"\n[bold green]✓ Demonstration complete![/bold green]")
        console.print(f"[dim]Processed {len(results)} records from {csv_file}[/dim]")
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise

if __name__ == "__main__":
    main()