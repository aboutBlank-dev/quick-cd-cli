import argparse
import json
import sys
from pathlib import Path

ALIASES_FILE = Path.home() / ".qcd_aliases.json"
RESERVED_COMMANDS = {"set", "list", "remove", "help"}

def send_error(message):
    print(f"error:{message}", file=sys.stderr)

def send_message(message):
    print(f"message:{message}")

def send_navigate(path):
    print(f"navigate:{path}")

def load_aliases():
    if not ALIASES_FILE.exists():
        return {}
    with open(ALIASES_FILE, "r") as f:
        return json.load(f)

def save_aliases(aliases):
    with open(ALIASES_FILE, "w") as f:
        json.dump(aliases, f, indent=2)

def set_alias(alias):
    aliases = load_aliases()
    path = str(Path.cwd())

    if alias in RESERVED_COMMANDS:
        send_error(f"'{alias}' is a reserved command and cannot be used as an alias.")
        return

    aliases[alias] = path
    save_aliases(aliases)
    send_message(f"Alias '{alias}' set to '{path}'.")

def list_aliases():
    aliases = load_aliases()
    if not aliases:
        send_message("No aliases set.")
        return
    
    message = "Aliases:\n"
    for name, path in aliases.items():
        message += f"  {name}: {path}\n"

    send_message(message.strip())

def remove_alias(alias):
    aliases = load_aliases()
    if alias in RESERVED_COMMANDS:
        send_error(f"'{alias}' is a reserved command and cannot be removed.")
        return

    if alias in aliases:
        del aliases[alias]
        save_aliases(aliases)
        send_message(f"Alias '{alias}' removed.")
    else:
        send_error(f"Alias '{alias}' not found.")

def navigate_to_alias(alias):
    aliases = load_aliases()
    if alias in aliases:
        send_navigate(aliases[alias])
    else:
        send_error(f"Alias '{alias}' not found.")

def main():
    # First, try go to alias
    if len(sys.argv) >= 2:
        alias = sys.argv[1]
        if alias not in RESERVED_COMMANDS:
            navigate_to_alias(alias)
            return

    parser = argparse.ArgumentParser()
    
    # Create a subparser for 'set', 'remove', and 'list'
    subparsers = parser.add_subparsers(dest="command")

    # Set subcommand
    set_parser = subparsers.add_parser("set", help="Set an alias")
    set_parser.add_argument("alias", help="The alias to set")

    # List subcommand
    subparsers.add_parser("list", help="List all aliases")

    # Help subcommand
    subparsers.add_parser("help", help="Show help message")

    # Remove subcommand
    remove_parser = subparsers.add_parser("remove", help="Remove an alias")
    remove_parser.add_argument("alias", help="The alias to remove")

    args, unknown_args = parser.parse_known_args()
    if args.command == "set":
        set_alias(args.alias)
    elif args.command == "list":
        list_aliases()
    elif args.command == "remove":
        remove_alias(args.alias)
    elif args.command == "help":
        send_message(parser.format_help());

if __name__ == "__main__":
    main()