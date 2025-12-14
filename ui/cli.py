from rich.console import Console
from rich.table import Table

from core.workspace_manager import WorkspaceManager
from core.ai_agent import AIAgent


class CLI:
    """
    Command-line interface layer.
    Connects user input → manager → AI agent.
    """

    def __init__(self):
        self.console = Console()
        self.manager = WorkspaceManager()
        self.ai = AIAgent()

    # ----------------------------
    # INDEX
    # ----------------------------
    def index_directory(self, directory: str):
        self.console.print(f"[bold blue]Indexing directory:[/] {directory}")
        count = self.manager.index_directory(directory)
        self.console.print(f"[green]Indexed {count} files successfully.[/]")

    # ----------------------------
    # LIST FILES
    # ----------------------------
    def list_files(self, limit=50):
        files = self.manager.list_files(limit=limit)

        table = Table(title=f"Indexed Files (showing {limit} max)")

        table.add_column("ID", style="cyan")
        table.add_column("Name")
        table.add_column("Size")
        table.add_column("Category")
        table.add_column("Path", overflow="fold")

        for f in files:
            table.add_row(str(f[0]), f[1], str(f[2]), str(f[3]), f[4])

        self.console.print(table)

    # ----------------------------
    # SEARCH
    # ----------------------------
    def search(self, query: str):
        results = self.manager.search_files(query)

        if not results:
            self.console.print("[yellow]No results found.[/]")
            return

        table = Table(title=f"Search Results for '{query}'")

        table.add_column("ID", style="cyan")
        table.add_column("Name")
        table.add_column("Summary")
        table.add_column("Path", overflow="fold")

        for r in results:
            table.add_row(str(r[0]), r[1], (r[2] or ""), r[3])

        self.console.print(table)

    # ----------------------------
    # SUMMARIZE
    # ----------------------------
    def summarize(self, limit=10):
        self.console.print("[bold blue]Generating summaries...[/]")

        pending = self.manager.get_files_missing_summaries(limit=limit)

        if not pending:
            self.console.print("[yellow]All files already summarized![/]")
            return

        for file_id, content in pending:
            summary = self.ai.summarize_text(content)
            self.manager.update_summary(file_id, summary)

        self.console.print("[green]Summaries generated and saved![/]")
