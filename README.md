# CS50P PYTHON REVIEWER


## Overview & Motivation
The **CS50P Python Reviewer** is an interactive, command-line interface (CLI) study application designed specifically for students taking **CS50's Introduction to Programming with Python (CS50P)**. As learners progress from foundational concepts like basic functions to advanced object-oriented programming, retaining syntax and theoretical nuances can become challenging.

This project was built to provide a gamified, terminal-based review platform covering all major course modules (Weeks 0 through 8). Rather than relying on static flashcards, students can test their knowledge through randomized multiple-choice and short-answer questions, receive instant terminal feedback with helpful explanations, review missed questions in a dedicated retry loop, and track their long-term progress via persistent CSV score history logging. Furthermore, the application has been packaged and published globally on PyPI (`cs50p-python-reviewer-ian`), allowing anyone to install and run it instantly with a simple `pip install` command.

---

## Project Structure & File Descriptions

The project repository is structured as a standard, scalable Python package layout to support both local execution and global PyPI distribution:

- **`pyproject.toml`**: The core configuration file for modern Python packaging. It defines project metadata, author information, build-system requirements using `setuptools`, dependencies (such as the `rich` library), package scripts (`cs50p-review`), and instructions to bundle non-code data files.
- **`README.md`**: The official documentation file (this document) that details project functionality, file breakdowns, design choices, and links to the required video presentation.
- **`requirements.txt`**: Lists external Python library dependencies required by the project (specifically `rich>=10.0.0`), ensuring easy dependency resolution for local environments.
- **`MANIFEST.in`**: Explicitly instructs the setuptools package builder to include data files like `questions.json` when generating distribution archives.
- **`cs50p_reviewer/`**: The main package directory containing the source code logic and assets.
  - **`__init__.py`**: An initialization file that marks the directory as a standard Python package module.
  - **`project.py`**: The primary script housing the core application logic. It manages the main menu loop, module selection, quiz execution, user answer evaluation, score calculations, CSV history management, and the interactive missed-questions review round.
  - **`questions.json`**: A structured JSON data bank containing categorized review questions, options, correct answers, question types (multiple choice vs. short answer), and educational explanations mapped across modules 0 through 8.
- **`score_history.csv`**: A locally generated persistent data file that records timestamped user performance logs, tracking scores, percentages, and Pass/Fail verdicts.
- **`test_project.py`**: A comprehensive test suite leveraging `pytest` to validate critical backend functions (`load_module_data`, `check_answer`, and `calculate_score`) to ensure robust error handling and logical accuracy.

---

## Design Choices & Implementation Details

### 1. Terminal UI Enhancement with `Rich`
Standard terminal outputs can look plain and text-heavy. To elevate the user experience, the **`rich`** library was integrated. By utilizing `rich.panel.Panel`, `rich.table.Table`, and stylized console prints, the application presents cleanly formatted menus, bordered containers, color-coded success/error feedback (`✔` and `✖`), and bold visual highlights. This makes CLI navigation feel modern and engaging.

### 2. Decoupling Data via JSON
Initially, embedding questions directly into Python scripts was considered; however, it tightly coupled content with execution logic. Moving questions to **`questions.json`** allowed for clean separation of concerns. It makes the question bank modular, easy to scale, and simple to expand with new modules or community-contributed questions without modifying the core codebase.

### 3. Persistent History and CSV Logging
To give students a sense of progression, the app records every completed session into **`score_history.csv`**. Using Python's built-in `csv` and `os` libraries, the program automatically appends headers and session rows with explicit file flushing (`os.fsync`) to prevent data corruption. Users can view past performance filtered dynamically by their profile name, encouraging iterative learning.

### 4. Interactive Remediation (Missed Questions Loop)
A key pedagogical choice was implementing a secondary review round for incorrect answers. Instead of simply showing the correct answer and moving on, the app stores missed questions in a local list and offers an immediate remediation loop, reinforcing weak spots before finalizing the session score.

---

## Installation & Usage

### Installing from PyPI
Anyone can install and run the tool globally on any machine with Python:
```bash
pip install cs50p-python-reviewer-ian

Once installed, execute the command-line script from any terminal:
cs50p-review
