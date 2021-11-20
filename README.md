# File Organizer

Automatically sort files in a directory into categorized folders based on file extension.

## Features

- Sorts files into 9 categories: Images, Documents, Videos, Audio, Archives, Code, Data, Executables, Fonts
- Watch mode: monitors a directory and auto-sorts new files in real-time
- Dry-run mode to preview changes before moving
- Handles duplicate filenames
- Category summary view

## Usage

```bash
pip install -r requirements.txt

# Organize current directory
python main.py

# Organize a specific directory
python main.py /path/to/messy/folder

# Preview without moving (dry run)
python main.py /path/to/folder --dry-run

# Watch for new files
python main.py /path/to/folder --watch

# Show summary of organized files
python main.py /path/to/folder --summary
```
