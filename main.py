import argparse
import json
import sys
from pathlib import Path

ALIASES_FILE = Path.home() / ".qcd_aliases.json"
RESERVED_COMMANDS = {"set", "list", "remove"}

def load_aliases():
    if not ALIASES_FILE.exists():
        return {}
    with open(ALIASES_FILE, "r") as f:
        return json.load(f)

def save_aliases(aliases):
    with open(ALIASES_FILE, "w") as f:
        json.dump(aliases, f, indent=2)

def set_alias(alias, aliases):
    path = str(Path.cwd())

    if alias in RESERVED_COMMANDS:
        print(f"Error: '{alias}' is a reserved command and cannot be used as an alias.", file=sys.stderr)
        return

    aliases[alias] = path
    save_aliases(aliases)
    print(f"Alias '{alias}' set to '{path}'")

def list_aliases(aliases):
    if not aliases:
        print("No aliases set.")
    for name, path in aliases.items():
        print(f"{name} => {path}")

def remove_alias(alias, aliases):
    if alias in RESERVED_COMMANDS:
        print(f"Error: '{alias}' is a reserved command and cannot be removed.", file=sys.stderr)
        return

    if alias in aliases:
        del aliases[alias]
        save_aliases(aliases)
        print(f"Removed alias '{alias}'")
    else:
        print(f"Alias '{alias}' not found.", file=sys.stderr)

def navigate_to_alias(alias, aliases):
    if alias in aliases:
        print(aliases[alias])  # This gets used in `cd "$(qcd alias)"`
    else:
        print(f"Alias '{alias}' not found.", file=sys.stderr)

def main():
    aliases = load_aliases()

    # go to alias
    if len(sys.argv) == 2:
        alias = sys.argv[1]
        if alias not in RESERVED_COMMANDS:
            navigate_to_alias(alias, aliases)
            return

    parser = argparse.ArgumentParser()
    
    # Create a subparser for 'set', 'remove', and 'list'
    subparsers = parser.add_subparsers(dest="command")

    # Set subcommand
    set_parser = subparsers.add_parser("set", help="Set an alias")
    set_parser.add_argument("alias", help="The alias to set")

    # List subcommand
    subparsers.add_parser("list", help="List all aliases")

    # Remove subcommand
    remove_parser = subparsers.add_parser("remove", help="Remove an alias")
    remove_parser.add_argument("alias", help="The alias to remove")

    args = parser.parse_args()
    if args.command == "set":
        set_alias(args.alias, aliases)
    elif args.command == "list":
        list_aliases(aliases)
    elif args.command == "remove":
        remove_alias(args.alias, aliases)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()