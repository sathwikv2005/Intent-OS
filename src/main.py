from rich import print
from rich.console import Console
from core.handle_query import handle_query

console = Console()

while True:
    text = console.input("[bold cyan]> You:[/bold cyan] ")
    print(f"[bold green]{handle_query(text)}[/bold green]")