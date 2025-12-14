import argparse
from ui.cli import CLI


def main():
    parser = argparse.ArgumentParser(
        description="AI Workspace Assistant — File Indexing, Organization & AI Summaries"
    )

    subparsers = parser.add_subparsers(dest="command")

    # index
    index_parser = subparsers.add_parser("index", help="Index all files within a directory")
    index_parser.add_argument("--path", type=str, required=True, help="Directory to scan")

    # list
    list_parser = subparsers.add_parser("list", help="List indexed files")
    list_parser.add_argument("--limit", type=int, default=50, help="Max results to show")

    # search
    search_parser = subparsers.add_parser("search", help="Search indexed files")
    search_parser.add_argument("--q", type=str, required=True, help="Query string")

    # summarize
    sum_parser = subparsers.add_parser("summarize", help="Generate summaries for indexed files")
    sum_parser.add_argument("--limit", type=int, default=10, help="Max files to summarize")

    args = parser.parse_args()
    cli = CLI()

    if args.command == "index":
        cli.index_directory(args.path)

    elif args.command == "list":
        cli.list_files(limit=args.limit)

    elif args.command == "search":
        cli.search(args.q)

    elif args.command == "summarize":
        cli.summarize(limit=args.limit)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
