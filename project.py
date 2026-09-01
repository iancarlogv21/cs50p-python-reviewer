import json
import sys
import csv
import os
import random
import time
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

console = Console()
HISTORY_FILE = "score_history.csv"

MODULE_NAMES = {
    "0": "Week 0: Functions, Variables",
    "1": "Week 1: Conditionals",
    "2": "Week 2: Loops",
    "3": "Week 3: Exceptions",
    "4": "Week 4: Libraries",
    "5": "Week 5: Unit Tests",
    "6": "Week 6: File I/O",
    "7": "Week 7: Regular Expressions",
    "8": "Week 8: Object-Oriented Programming"
}

def main():
    console.clear()
    console.print(Panel("WELCOME TO THE CS50P PYTHON REVIEWER", style="bold cyan"))
    user_name = Prompt.ask("Enter your name").strip().title()

    menu_options = {
        "1": "Start Module Review",
        "2": "View Past Review History",
        "3": "Exit Program"
    }

    while True:
        console.clear()
        table = Table(title=f"CS50P PYTHON REVIEWER (User: {user_name})", style="cyan")
        table.add_column("Option", justify="center", style="magenta", no_wrap=True)
        table.add_column("Action", style="green")

        for key, title in menu_options.items():
            table.add_row(f"[{key}]", title)

        console.print(table)
        choice = Prompt.ask("Select an option", choices=["1", "2", "3"])

        if choice == "1":
            run_quiz_session(user_name)
        elif choice == "2":
            view_score_history(user_name)
        elif choice == "3":
            console.print("[bold yellow]Exiting reviewer. Good luck with CS50P![/bold yellow]")
            sys.exit(0)

def run_quiz_session(user_name):
    console.clear()

    mod_table = Table(title="SELECT A REVIEW MODULE", style="blue")
    mod_table.add_column("Module", justify="center", style="magenta", no_wrap=True)
    mod_table.add_column("Topic Name", style="green")

    for key, name in MODULE_NAMES.items():
        mod_table.add_row(f"[{key}]", name)
    mod_table.add_row("[9]", "[yellow]Back to Main Menu[/yellow]")

    console.print(mod_table)

    module_choice = Prompt.ask("Select a module number", choices=[str(i) for i in range(10)])

    if module_choice == "9":
        return

    try:
        questions = load_module_data("questions.json", module_choice)
    except FileNotFoundError:
        console.print("[bold red]Error: questions.json file was not found.[/bold red]")
        time.sleep(2)
        return
    except KeyError:
        console.print("[bold red]Error: Invalid module selection.[/bold red]")
        time.sleep(2)
        return

    random.shuffle(questions)

    score = 0
    total = len(questions)
    missed_questions = []

    console.print(Panel(f"Reviewing: {MODULE_NAMES[module_choice]} ({total} Questions)", style="bold blue"))
    time.sleep(1)

    for idx, q in enumerate(questions, start=1):
        console.print(f"\n[bold yellow]Question {idx}/{total}:[/bold yellow] {q['question']}")

        if q["type"] == "multiple_choice":
            for option in q["options"]:
                console.print(f"  [cyan]{option}[/cyan]")
            user_input = Prompt.ask("Enter option letter", choices=["A", "B", "C", "D"], show_choices=False)
        else:
            user_input = Prompt.ask("Answer (one word/symbol)")

        if check_answer(user_input, q["answer"]):
            console.print("[bold green]✔ Correct![/bold green]")
            if "explanation" in q:
                console.print(f"[italic cyan]💡 Explanation: {q['explanation']}[/italic cyan]")
            score += 1
        else:
            console.print(f"[bold red]✖ Incorrect.[/bold red] Expected: [bold white]{q['answer']}[/bold white]")
            if "explanation" in q:
                console.print(f"[italic cyan]💡 Explanation: {q['explanation']}[/italic cyan]")
            missed_questions.append(q)

    percentage, verdict = calculate_score(score, total)
    save_score_history(user_name, MODULE_NAMES[module_choice], score, total, percentage, verdict)

    result_color = "green" if verdict == "Pass" else "red"
    result_text = f"Final Score: {score}/{total} ({percentage}%)\nVerdict: {verdict}"
    console.print(Panel(result_text, title="REVIEW RESULT", style=f"bold {result_color}"))

    if missed_questions:
        review_choice = Prompt.ask("\nWould you like to review and retry the questions you missed?", choices=["y", "n"], default="y")
        if review_choice == "y":
            console.print(Panel("MISSED QUESTIONS REVIEW ROUND", style="bold yellow"))
            for mq in missed_questions:
                console.print(f"\n[bold yellow]Question:[/bold yellow] {mq['question']}")
                if mq["type"] == "multiple_choice":
                    for option in mq["options"]:
                        console.print(f"  [cyan]{option}[/cyan]")
                retry_input = Prompt.ask("Retry Answer")
                if check_answer(retry_input, mq["answer"]):
                    console.print("[bold green]✔ Correct on review![/bold green]")
                else:
                    console.print(f"[bold red]Still incorrect.[/bold red] Correct answer: [bold white]{mq['answer']}[/bold white]")
                if "explanation" in mq:
                    console.print(f"[italic cyan]💡 Explanation: {mq['explanation']}[/italic cyan]")

    console.print("\n[bold green]📊 Displaying your updated score history automatically:[/bold green]")
    time.sleep(1)
    view_score_history(user_name, auto_display=True)

def view_score_history(current_user, auto_display=False):
    if not auto_display:
        console.clear()

    table = Table(title=f"PAST REVIEW HISTORY FOR {current_user.upper()}", style="cyan")
    table.add_column("Timestamp", style="magenta")
    table.add_column("Module", style="green")
    table.add_column("Score", justify="center", style="yellow")
    table.add_column("Percentage", justify="center", style="blue")
    table.add_column("Verdict", justify="center", style="bold")

    records_found = False
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, mode="r", encoding="utf-8") as file:
                lines = file.readlines()
                if len(lines) > 1:
                    for line in lines[1:]:
                        parts = line.strip().split(",")
                        if len(parts) >= 6:
                            timestamp, row_user, module, score, total, percentage, verdict = parts[:7] if len(parts) >= 7 else (parts[0], current_user, parts[1], parts[2], parts[3], parts[4], parts[5])
                            if row_user.strip().lower() == current_user.strip().lower():
                                records_found = True
                                verdict_style = "green" if verdict.strip() == "Pass" else "red"
                                table.add_row(
                                    timestamp.strip(),
                                    module.strip(),
                                    f"{score.strip()}/{total.strip()}",
                                    f"{percentage.strip()}%",
                                    f"[{verdict_style}]{verdict.strip()}[/{verdict_style}]"
                                )
        except Exception:
            pass

    if not records_found:
        console.print(f"[bold yellow]No history found for '{current_user}'. Complete a review first![/bold yellow]")
    else:
        console.print(table)

    Prompt.ask("\nPress Enter to continue")

def save_score_history(user_name, module, score, total, percentage, verdict):
    file_exists = os.path.exists(HISTORY_FILE)
    with open(HISTORY_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Timestamp", "User", "Module", "Score", "Total", "Percentage", "Verdict"])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            user_name,
            module,
            score,
            total,
            percentage,
            verdict
        ])
        file.flush()
        os.fsync(file.fileno())

def load_module_data(filepath, module_id):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, filepath)
    with open(json_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    if str(module_id) not in data:
        raise KeyError(f"Module '{module_id}' does not exist.")
    return data[str(module_id)]

def check_answer(user_answer, correct_answer):
    if not isinstance(user_answer, str) or not isinstance(correct_answer, str):
        return False
    return user_answer.strip().lower() == correct_answer.strip().lower()

def calculate_score(correct, total):
    if total <= 0:
        return 0.0, "Fail"
    percentage = round((correct / total) * 100, 1)
    verdict = "Pass" if percentage >= 70.0 else "Fail"
    return percentage, verdict

if __name__ == "__main__":
    main()
