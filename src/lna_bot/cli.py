"""
Command Line Interface for LNA Bot.

This module provides a comprehensive CLI interface for the LNA Bot
using Click framework with rich formatting for better user experience.
"""

import click
import logging
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track
from rich.prompt import Confirm, Prompt
from rich.text import Text
from typing import Optional, List
import sys
import json

from . import LNABot, LNABotError
from .models import TrainingType

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('lna_bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
console = Console()


def print_banner():
    """Print the application banner."""
    banner = """
    ██╗     ███╗   ██╗ █████╗     ██████╗  ██████╗ ████████╗
    ██║     ████╗  ██║██╔══██╗    ██╔══██╗██╔═══██╗╚══██╔══╝
    ██║     ██╔██╗ ██║███████║    ██████╔╝██║   ██║   ██║   
    ██║     ██║╚██╗██║██╔══██║    ██╔══██╗██║   ██║   ██║   
    ███████╗██║ ╚████║██║  ██║    ██████╔╝╚██████╔╝   ██║   
    ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝    ╚═════╝  ╚═════╝    ╚═╝   
    
    Learning Need Analysis Bot - AI-Powered Training Recommendations
    """
    console.print(banner, style="bold blue")


def handle_errors(func):
    """Decorator to handle common CLI errors."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except LNABotError as e:
            console.print(f"[red]Error: {str(e)}[/red]")
            sys.exit(1)
        except FileNotFoundError as e:
            console.print(f"[red]File not found: {str(e)}[/red]")
            sys.exit(1)
        except Exception as e:
            console.print(f"[red]Unexpected error: {str(e)}[/red]")
            logger.exception("Unexpected error occurred")
            sys.exit(1)
    return wrapper


@click.group()
@click.option('--config-dir', '-c', type=click.Path(exists=True, path_type=Path),
              help='Configuration directory path')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.pass_context
def cli(ctx, config_dir: Optional[Path], verbose: bool):
    """
    LNA Bot - AI-Powered Learning Need Analysis Tool
    
    This tool analyzes Learning Need Analysis reports and provides
    intelligent recommendations for training delivery methods.
    """
    # Ensure context object exists
    ctx.ensure_object(dict)
    
    # Set up logging level
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        console.print("[dim]Verbose logging enabled[/dim]")
    
    # Store configuration
    ctx.obj['config_dir'] = config_dir
    ctx.obj['verbose'] = verbose
    
    # Print banner for main commands
    if ctx.invoked_subcommand in ['analyze', 'interactive']:
        print_banner()


@cli.command()
@click.argument('csv_file', type=click.Path(exists=True, path_type=Path))
@click.option('--output', '-o', type=click.Path(path_type=Path),
              help='Output JSON file path')
@click.option('--summary-only', '-s', is_flag=True,
              help='Show only summary information')
@click.option('--export-detailed', '-d', is_flag=True,
              help='Export detailed results to JSON')
@click.pass_context
@handle_errors
def analyze(ctx, csv_file: Path, output: Optional[Path], 
           summary_only: bool, export_detailed: bool):
    """
    Analyze an LNA CSV file and generate training recommendations.
    
    CSV_FILE: Path to the LNA CSV file to analyze
    """
    console.print(f"[bold green]Analyzing LNA file:[/bold green] {csv_file}")
    
    # Initialize bot
    with console.status("[bold green]Initializing LNA Bot..."):
        bot = LNABot(config_dir=ctx.obj.get('config_dir'))
    
    # Perform analysis
    with console.status("[bold green]Processing LNA data..."):
        results, summary = bot.analyze_csv_file(csv_file)
    
    console.print(f"[green]✓[/green] Analysis complete! Processed {len(results)} records")
    
    # Display summary
    display_summary(summary, bot)
    
    if not summary_only:
        display_results(results)
    
    # Export results if requested
    if export_detailed or output:
        if not output:
            output = csv_file.with_suffix('.json')
        
        with console.status(f"[bold green]Exporting results to {output}..."):
            bot.export_results_to_json(results, summary, output)
        
        console.print(f"[green]✓[/green] Results exported to: {output}")


@cli.command()
@click.pass_context
@handle_errors
def interactive(ctx):
    """
    Start interactive mode for single record analysis.
    """
    console.print("[bold green]Starting Interactive Mode[/bold green]")
    console.print("Enter LNA record details for analysis\n")
    
    # Initialize bot
    with console.status("[bold green]Initializing LNA Bot..."):
        bot = LNABot(config_dir=ctx.obj.get('config_dir'))
    
    while True:
        try:
            # Get input from user
            record_data = get_interactive_input(bot)
            if not record_data:
                break
            
            # Get recommendation
            recommendation = bot.get_training_recommendation(
                estimated_trainees=record_data['trainees'],
                competency=record_data['competency']
            )
            
            # Display recommendation
            display_recommendation(recommendation)
            
            # Ask if user wants to continue
            if not Confirm.ask("\nAnalyze another record?"):
                break
                
        except KeyboardInterrupt:
            console.print("\n[yellow]Goodbye![/yellow]")
            break
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")
            if not Confirm.ask("Continue with interactive mode?"):
                break


@cli.command()
@click.pass_context
@handle_errors
def config(ctx):
    """
    Display current configuration information.
    """
    console.print("[bold green]LNA Bot Configuration[/bold green]\n")
    
    # Initialize bot
    with console.status("[bold green]Loading configuration..."):
        bot = LNABot(config_dir=ctx.obj.get('config_dir'))
    
    # Get configuration info
    config_info = bot.get_business_rules_info()
    
    # Display configuration table
    table = Table(title="Business Rules Configuration")
    table.add_column("Setting", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")
    
    table.add_row("External Threshold", f"≤ {config_info['external_threshold']} trainees")
    table.add_row("In-house Threshold", f"> {config_info['in_house_threshold']} trainees")
    table.add_row("Priority Weights", str(config_info['priority_weights']))
    table.add_row("Niche Competencies", str(config_info['niche_competencies_count']))
    table.add_row("Common Competencies", str(config_info['common_competencies_count']))
    table.add_row("Total Skills Mapped", str(config_info['total_skills_mapped']))
    
    console.print(table)
    
    # Validate configuration
    issues = bot.validate_configuration()
    if issues:
        console.print("\n[red]Configuration Issues:[/red]")
        for issue in issues:
            console.print(f"[red]• {issue}[/red]")
    else:
        console.print("\n[green]✓ Configuration is valid[/green]")


@cli.command()
@click.argument('competency', type=str)
@click.pass_context
@handle_errors
def skills(ctx, competency: str):
    """
    Show skills associated with a competency.
    
    COMPETENCY: Name of the competency to look up
    """
    # Initialize bot
    with console.status("[bold green]Loading skills mapping..."):
        bot = LNABot(config_dir=ctx.obj.get('config_dir'))
    
    # Get skills
    skills_list = bot.get_competency_skills(competency)
    
    if skills_list:
        console.print(f"[bold green]Skills for '{competency}':[/bold green]")
        for skill in skills_list:
            console.print(f"[cyan]• {skill}[/cyan]")
    else:
        console.print(f"[yellow]No skills found for competency: '{competency}'[/yellow]")
        console.print("[dim]Check competency name or skills mapping configuration[/dim]")


def get_interactive_input(bot: LNABot) -> Optional[dict]:
    """Get input from user in interactive mode."""
    try:
        console.print("[bold cyan]Enter Record Details:[/bold cyan]")
        
        # Get competency
        competency = Prompt.ask("Competency name")
        if not competency.strip():
            return None
        
        # Get number of trainees
        while True:
            try:
                trainees_str = Prompt.ask("Estimated number of trainees")
                trainees = int(trainees_str)
                if trainees <= 0:
                    console.print("[red]Number of trainees must be positive[/red]")
                    continue
                break
            except ValueError:
                console.print("[red]Please enter a valid number[/red]")
        
        return {
            'competency': competency.strip(),
            'trainees': trainees
        }
        
    except KeyboardInterrupt:
        return None


def display_summary(summary, bot: LNABot):
    """Display analysis summary."""
    console.print("\n[bold green]Analysis Summary[/bold green]")
    
    # Create summary table
    table = Table()
    table.add_column("Training Type", style="cyan", no_wrap=True)
    table.add_column("Count", style="magenta")
    table.add_column("Percentage", style="green")
    
    table.add_row("In-house", str(summary.in_house_count), 
                  f"{summary.in_house_percentage:.1f}%")
    table.add_row("SDP", str(summary.sdp_count), 
                  f"{summary.sdp_percentage:.1f}%")
    table.add_row("External", str(summary.external_count), 
                  f"{summary.external_percentage:.1f}%")
    table.add_row("[bold]Total", f"[bold]{summary.total_records}",
                  "[bold]100.0%")
    
    console.print(table)
    
    # Show top competencies
    if summary.top_competencies:
        console.print("\n[bold green]Top Competencies:[/bold green]")
        for i, (comp, count) in enumerate(summary.top_competencies[:5], 1):
            console.print(f"[cyan]{i}. {comp}[/cyan] ({count} records)")


def display_results(results: List):
    """Display detailed analysis results."""
    if not results:
        return
        
    console.print(f"\n[bold green]Detailed Results ({len(results)} records)[/bold green]")
    
    # Create results table
    table = Table()
    table.add_column("ID", style="dim", width=8)
    table.add_column("Competency", style="cyan")
    table.add_column("Trainees", style="magenta", justify="right")
    table.add_column("Training Type", style="green")
    table.add_column("Priority", style="yellow", justify="right")
    
    for result in results[:20]:  # Show first 20 results
        competency_name = result.record.targeted_competencies
        table.add_row(
            result.record.id,
            competency_name[:30] + "..." if len(competency_name) > 30 else competency_name,
            str(result.record.estimated_trainees),
            result.recommendation.training_type.value,
            result.record.priority.value
        )
    
    console.print(table)
    
    if len(results) > 20:
        console.print(f"[dim]... and {len(results) - 20} more records[/dim]")


def display_recommendation(recommendation: dict):
    """Display a single recommendation."""
    training_type = recommendation['training_type']
    
    # Color based on training type
    type_colors = {
        TrainingType.IN_HOUSE: "green",
        TrainingType.SDP: "yellow", 
        TrainingType.EXTERNAL: "blue"
    }
    
    color = type_colors.get(training_type, "white")
    
    # Create recommendation panel
    content = f"""
[bold]Competency:[/bold] {recommendation['competency']}
[bold]Estimated Trainees:[/bold] {recommendation['estimated_trainees']}
[bold]Classification:[/bold] {recommendation['competency_classification'].value}
[bold]Recommendation:[/bold] [{color}]{training_type.value}[/{color}]

[bold]Reasoning:[/bold]
{recommendation['reasoning']}
"""
    
    if recommendation['associated_skills']:
        content += f"\n[bold]Associated Skills:[/bold]\n"
        for skill in recommendation['associated_skills'][:5]:  # Show first 5 skills
            content += f"• {skill}\n"
        if len(recommendation['associated_skills']) > 5:
            content += f"... and {len(recommendation['associated_skills']) - 5} more skills"
    
    panel = Panel(content, title="Training Recommendation", border_style=color)
    console.print(panel)


if __name__ == '__main__':
    cli()