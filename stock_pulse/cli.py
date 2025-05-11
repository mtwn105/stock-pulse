"""Command-line interface for Stock Pulse."""

import argparse
import sys
import json
from typing import List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.text import Text

from stock_pulse.core.analyzer import analyze_stocks
from stock_pulse.config.settings import OPENAI_API_KEY

console = Console()

def display_banner():
    """Display the Stock Pulse banner."""
    banner = Text()
    banner.append("\n")
    banner.append("███████╗████████╗ ██████╗  ██████╗██╗  ██╗    ██████╗ ██╗   ██╗██╗     ███████╗███████╗\n", style="cyan")
    banner.append("██╔════╝╚══██╔══╝██╔═══██╗██╔════╝██║ ██╔╝    ██╔══██╗██║   ██║██║     ██╔════╝██╔════╝\n", style="cyan")
    banner.append("███████╗   ██║   ██║   ██║██║     █████╔╝     ██████╔╝██║   ██║██║     ███████╗█████╗  \n", style="cyan")
    banner.append("╚════██║   ██║   ██║   ██║██║     ██╔═██╗     ██╔═══╝ ██║   ██║██║     ╚════██║██╔══╝  \n", style="cyan")
    banner.append("███████║   ██║   ╚██████╔╝╚██████╗██║  ██╗    ██║     ╚██████╔╝███████╗███████║███████╗\n", style="cyan")
    banner.append("╚══════╝   ╚═╝    ╚═════╝  ╚═════╝╚═╝  ╚═╝    ╚═╝      ╚═════╝ ╚══════╝╚══════╝╚══════╝\n", style="cyan")
    banner.append("\n")
    banner.append("Made with ❤️  by Amit Wani\n", style="magenta")
    banner.append("\n")
    
    console.print(banner)

def validate_environment():
    """Validate that required environment variables are set."""
    if not OPENAI_API_KEY:
        console.print(Panel(
            "[bold red]Error:[/bold red] OPENAI_API_KEY environment variable is not set.\n"
            "Please set it in a .env file or export it in your shell.",
            title="Environment Error",
            border_style="red"
        ))
        sys.exit(1)

def display_results(results: dict):
    """Display analysis results in a formatted table."""
    table = Table(title="Stock Analysis Results", box=box.ROUNDED)
    
    table.add_column("Ticker", style="cyan", no_wrap=True)
    table.add_column("Company", style="magenta")
    table.add_column("Signal", style="bold")
    table.add_column("Reasoning", style="green")
    
    for ticker, result in results.items():
        if result.get('success', False):
            signal = result['signal']
            signal_style = {
                'BUY': '[bold green]BUY[/bold green]',
                'SELL': '[bold red]SELL[/bold red]',
                'HOLD': '[bold yellow]HOLD[/bold yellow]'
            }.get(signal, signal)
            
            table.add_row(
                ticker,
                result.get('name', ticker),
                signal_style,
                result.get('reasoning', 'No reasoning provided')
            )
        else:
            table.add_row(
                ticker,
                result.get('name', ticker),
                '[bold red]ERROR[/bold red]',
                result.get('error', 'Unknown error')
            )
    
    console.print(table)
    
    # Display detailed analysis for each stock
    for ticker, result in results.items():
        if result.get('success', False):
            console.print(f"\n[bold cyan]{ticker}[/bold cyan]: [magenta]{result.get('name', ticker)}[/magenta]")
            console.print(f"[bold]Signal:[/bold] {result['signal']}")
            console.print(f"[bold]Reasoning:[/bold] {result['reasoning']}")
            
            console.print("[bold]Key Factors:[/bold]")
            for factor in result.get('key_factors', []):
                console.print(f"  • {factor}")
                
            console.print("[bold]Risks:[/bold]")
            for risk in result.get('risks', []):
                console.print(f"  • {risk}")
            
            # Display recent news
            if 'news' in result and result['news']:
                console.print("\n[bold]Recent News:[/bold]")
                news_table = Table(show_header=True, header_style="bold", box=box.SIMPLE)
                news_table.add_column("Date", style="cyan", width=12)
                news_table.add_column("Source", style="magenta", width=15)
                news_table.add_column("Title", style="white")
                news_table.add_column("URL", style="blue")
                
                for article in result['news']:
                    if article.get('title') and article.get('publisher'):  # Only show articles with valid data
                        news_table.add_row(
                            article.get('published', 'N/A'),
                            article.get('publisher', 'N/A'),
                            article.get('title', 'N/A'),
                            article.get('link', 'N/A')
                        )
                
                if news_table.row_count > 0:
                    console.print(news_table)
                else:
                    console.print("  No recent news available.")
            else:
                console.print("\n[bold]Recent News:[/bold] No news available.")
            
            console.print("─" * 80)
    
    # Display disclaimer
    disclaimer = Panel(
        "[bold]DISCLAIMER:[/bold] The analysis provided by Stock Pulse is for informational purposes only and does not "
        "constitute investment advice. Stock market investments involve risk, and past performance is not indicative of "
        "future results. Always conduct your own research and consult with a qualified financial advisor before making "
        "investment decisions.",
        title="Important Notice",
        border_style="yellow",
        padding=(1, 2)
    )
    console.print(disclaimer)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Stock Pulse - Analyze stocks with news trends and emotional tone"
    )
    parser.add_argument(
        "tickers",
        nargs="+",
        help="Stock ticker symbols to analyze (e.g., AAPL MSFT GOOGL)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format"
    )
    
    return parser.parse_args()

def main():
    """Main entry point for the CLI."""
    # Display banner
    display_banner()
    
    args = parse_args()
    validate_environment()
    
    tickers = [ticker.upper() for ticker in args.tickers]
    
    with console.status(f"Analyzing {len(tickers)} stocks...", spinner="dots"):
        results = analyze_stocks(tickers)
    
    if args.json:
        # Add disclaimer to JSON output
        output = {
            "results": results,
            "disclaimer": "DISCLAIMER: The analysis provided is for informational purposes only and does not constitute investment advice. Always conduct your own research and consult with a qualified financial advisor before making investment decisions."
        }
        print(json.dumps(output, indent=2))
    else:
        display_results(results)

if __name__ == "__main__":
    main()
