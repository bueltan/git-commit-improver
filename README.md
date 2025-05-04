# Git Commit Message Improver

An intelligent Git hook system that automatically improves commit messages using LLaMA AI model.

## Overview

This project provides a Git hook that automatically enhances commit messages by:
- Fixing spelling and grammar errors
- Improving message clarity and structure
- Maintaining the original intent of the commit message

The tool leverages the LLaMA AI model running locally through Ollama to provide intelligent suggestions for commit message improvements.

## Requirements

- Python 3.x (no external dependencies required)
- Ollama with LLaMA 3.2 model installed and running on localhost:11434
- Git

## Installation

1. Install Ollama and the LLaMA 3.2 model:
   ```bash
   ollama pull llama3.2
   ```

2. Start Ollama service:
   ```bash
   ollama serve
   ```

3. Configure as a global template (recommended):

   a. Make both scripts executable:
   ```bash
   chmod +x ~/.git-templates/hooks/modify_commit_msg.py
   chmod +x ~/.git-templates/hooks/prepare-commit-msg
   ```

   b. Tell Git to use your template:
   ```bash
   git config --global init.templateDir ~/.git-templates
   ```

   This means any new Git repo you create with `git init` will automatically have this hook installed.

   Or copy the hook files to your repository's `.git/hooks` directory:
   ```bash
   cp hooks/prepare-commit-msg .git/hooks/
   cp hooks/modify_commit_msg.py .git/hooks/
   ```

## How It Works

1. When you create a commit, Git triggers the `prepare-commit-msg` hook
2. The hook passes your commit message to `modify_commit_msg.py`
3. `modify_commit_msg.py` sends the message to the local LLaMA instance
4. The AI model processes the message and returns an improved version
5. The improved message is saved back to the commit message file

## Usage

The hook works automatically when you create commits. Simply write your commit message as usual, and the tool will automatically enhance it before finalizing the commit.

If the AI processing fails for any reason, the original commit message will be preserved as a fallback.

## Testing

### Unit Tests

Run the unit tests to verify the script's functionality:

```bash
python hooks/test_modify_commit_msg_ollama.py
```

These tests verify that:
- The script correctly sends prompts to the LLaMA API
- The response is properly processed and saved
- The script handles errors gracefully

### Integration Tests

Run the integration tests to verify the connection to your local LLaMA instance:

```bash
python hooks/test_integration_with_ollama.py
```

These tests:
- Send real prompts to your local LLaMA instance
- Verify the responses contain expected keywords
- Print the LLaMA output for manual inspection

## Configuration

You can customize the AI model and API endpoint by modifying these variables in `modify_commit_msg.py`:
- `OLLAMA_URL`: The URL where your Ollama instance is running
- `MODEL`: The name of the LLaMA model to use (default: llama3.2)

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.