# TODO CLI

A small Python command-line task manager. Create tasks, view them, mark them as
complete, and delete them. Tasks are saved locally in `tasks.json` so they are
available the next time the program runs.

## Features

- Add a task with a title, description, and due date.
- List saved tasks and see whether each is pending or completed.
- Mark a task complete by its ID.
- Delete a task by its ID.
- Optionally request an AI-generated breakdown of a complex task.
- Persist task data as JSON in `tasks.json`.

## Requirements

- Python 3.10 or newer.
- `pip` to install the project dependencies.
- An OpenAI API key to start the application, because the AI service is
  initialized when the program starts. The key must be available as
  `OPENAI_API_KEY`, even if you only plan to use the regular task commands.

## Setup

From the project directory, create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell, activate it with:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Set your OpenAI API key in the environment before launching the program. For
example, on macOS or Linux:

```bash
export OPENAI_API_KEY="your-api-key"
```

In Windows PowerShell:

```powershell
$env:OPENAI_API_KEY = "your-api-key"
```

Alternatively, create a `.env` file in the project directory and add:

```dotenv
OPENAI_API_KEY=your-api-key
```

Do not commit your API key or `.env` file.

## Run the application

```bash
python main.py
```

The interactive menu uses numeric choices:

| Choice | Action |
| --- | --- |
| `1` | Add a task by entering its description, title, and due date |
| `2` | Ask the AI service to break down a complex task into subtasks |
| `3` | List all tasks |
| `4` | Mark a task complete by ID |
| `5` | Delete a task by ID |
| `6` | Exit |

Task IDs are assigned automatically. Enter due dates in `YYYY-MM-DD` format.
The program currently stores the date as entered; it does not validate the
format.

### AI-assisted task breakdown

Choose option `2` and enter a description of the larger task. The service asks
the OpenAI API for 3–5 simple subtasks. This requires a valid API key and API
access to the model configured in `ai_service.py`; API usage may incur charges.

**Current limitation:** the AI option currently calls `time.now()` in
`main.py`, which is undefined. As a result, the AI-generated subtasks cannot
currently be added successfully without correcting that date-handling code.
The other task-management options do not use that code path.

## Data storage

Tasks are written to `tasks.json` in the current working directory. Each task
contains an ID, title, description, completion status, and due date. The file
is created on the first save and is ignored by Git, so task data stays local
unless you choose to back it up or share it.

## Run the tests

The project uses Python's built-in `unittest` framework; no separate test
package is required. From the project directory run:

```bash
python -m unittest discover -v
```

To run only the task manager tests:

```bash
python -m unittest -v test_task_cli
```

The tests use a temporary JSON file and do not modify your real `tasks.json`.

## Project files

| File | Purpose |
| --- | --- |
| `main.py` | Interactive command-line menu and application entry point |
| `task_cli.py` | `Task` and `TaskManager` classes, including JSON persistence |
| `ai_service.py` | OpenAI-powered task breakdown |
| `test_task_cli.py` | Unit tests for task and task-manager behavior |
| `requirements.txt` | Python dependency list |
