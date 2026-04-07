from rich import print

def print_debug(text: str):
    print(f"[bold yellow][DEBUG][/bold yellow] [dim]{text}[/dim]")


def print_info(text: str):
    print(f"[bold blue][INFO][/bold blue] [white]{text}[/white]")