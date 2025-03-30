# Quick CD CLI

Quick CD CLI (`qcd`) is a command-line tool for managing and navigating directory aliases efficiently.

For example, if you frequently navigate to a specific directory, you can set an alias for it and quickly switch to that directory using the alias.

```bash
    qcd set projects # Sets the current directory as an alias 'projects'
    qcd projects     # Navigates to the 'projects' directory, regardless of the current working directory
```

## Features

- Set aliases for directories.
- List all saved aliases.
- Remove aliases.
- Navigate to directories using aliases.

## Prerequisites

- Bash shell (for running the `qcd` script).
- Python (for building or executing the script directly).

## Setup

1. **Clone the Repository**:

   ```bash
   git clone git@github.com:aboutBlank-dev/quick-cd-cli.git
   cd quick-cd-cli
   ```

2. **Install Dependencies**:

   ```bash
   pip install pyinstaller
   ```

3. **Build the Executable**:
   Use PyInstaller to create a standalone executable:

   ```bash
   pyinstaller --onedir qcd.py
   ```

   This will create an executable named `qcd` in the `dist` directory.

4. **Make the `qcd` bash Script Executable**:

   ```bash
   chmod +x qcd
   ```

5. **Add `qcd` as an alias in your shell configuration file**:
   Add the following line to your shell configuration file (e.g., `~/.bashrc`, `~/.zshrc`):

   ```bash
    alias qcd= "source /path/to/quick-cd-cli/qcd"
   ```

   Replace `/path/to/quick-cd-cli/qcd with` the full path to the qcd bash script.

   `source` command is required to change the current directory when using the script.

6. **Reload Your Shell**:
   ```bash
   source ~/.bashrc  # or ~/.zshrc
   ```

## Usage

- **Set an Alias**:

  ```bash
  qcd set <alias>
  ```

  This sets the current directory as the alias.

- **List All Aliases**:

  ```bash
  qcd list
  ```

- **Remove an Alias**:

  ```bash
  qcd remove <alias>
  ```

- **Navigate to an Alias**:
  ```bash
  qcd <alias>
  ```

## Notes

- Aliases are stored in a JSON file located at `~/.qcd_aliases.json`.
- Reserved commands (`set`, `list`, `remove`, `help`) cannot be used as aliases.
- The bash script relies on the fact that the qcd executable is in <repo>/dist/qcd/qcd (if you change the build directory, or build it differently, you may need to change the bash script).

## Development

To run the Python script directly for testing:

```bash
python qcd.py <command> [arguments]
```
