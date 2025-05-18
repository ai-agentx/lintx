# !/usr/bin/env python3

import argparse
import os

from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.societies import RolePlaying
from camel.types import ModelType, RoleType
from dotenv import load_dotenv

load_dotenv()


def create_linting_agent(code_file: str, language: str = None) -> None:
    """
    Create a code linting agent that analyzes code and provides improvement suggestions.

    Args:
        code_file: Path to the code file to be linted
        language: Programming language of the code file (if None, will be inferred from file extension)
    """
    # Check if the file exists
    if not os.path.exists(code_file):
        print(f"Error: File '{code_file}' does not exist.")
        return

    # Read the code file
    with open(code_file, 'r') as f:
        code_content = f.read()

    # Infer language from file extension if not provided
    if language is None:
        extension = os.path.splitext(code_file)[1]
        language_map = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.rs': 'Rust',
            '.go': 'Go',
            '.c': 'C',
            '.cpp': 'C++',
            '.h': 'C/C++ Header',
            '.sh': 'Bash',
            '.java': 'Java',
            '.rb': 'Ruby',
            '.php': 'PHP',
        }
        language = language_map.get(extension, 'Unknown')

    # Define agent system prompts
    linter_prompt = f"""
    You are an expert code linter for {language} code. Your job is to analyze code and provide detailed 
    feedback on:

    1. Code style and formatting issues
    2. Potential bugs or logic errors
    3. Performance optimizations
    4. Security vulnerabilities
    5. Best practices and design patterns

    For each issue:
    - Identify the specific line or section
    - Explain the problem in detail
    - Provide a concrete solution or improvement
    - Reference relevant style guides or documentation

    Be thorough, specific, and provide actionable advice. Include code examples where appropriate.
    """

    coder_prompt = f"""
    You are a skilled {language} developer who has written some code that needs review. 
    You'll provide the code and ask for specific feedback on how to improve it.
    Your goal is to get constructive feedback on code quality, performance, and adherence to best practices.
    """

    # Create the agents
    linter_agent = ChatAgent(model_type=ModelType.GPT_4_TURBO, system_prompt=linter_prompt)
    coder_agent = ChatAgent(model_type=ModelType.GPT_4_TURBO, system_prompt=coder_prompt)

    # Set up the role-playing session
    role_playing = RolePlaying(
        alice=coder_agent,
        bob=linter_agent,
        alice_role_name="Developer",
        bob_role_name="CodeLinter",
    )

    # Initial message from the coder
    initial_message = f"""
    I've written the following {language} code and would like you to review it for improvements:

    ```{language}
    {code_content}
    ```

    Please analyze this code and provide detailed feedback on style, bugs, performance, security, and best practices.
    """

    # Start the conversation
    print(f"Starting code linting for {code_file}...")
    chat_history = role_playing.init_chat(initial_message)

    # Run for a set number of turns to get comprehensive feedback
    max_turns = 3
    for i in range(max_turns):
        print(f"\n--- Turn {i + 1}/{max_turns} ---")
        chat_history = role_playing.step()

        # Print the linter's response
        linter_message = chat_history[-1] if chat_history[-1].role_name == "CodeLinter" else chat_history[-2]
        print(f"\nLinter's feedback (Turn {i + 1}):")
        print(linter_message.content)

        # Check if the conversation has reached a natural conclusion
        if "CAMEL_TASK_DONE" in chat_history[-1].content:
            break

    print("\nCode linting completed!")


def main():
    parser = argparse.ArgumentParser(description="lintx")
    parser.add_argument("file", help="Path to the code file to be linted")
    parser.add_argument("--language", help="Programming language of the code (optional)")

    args = parser.parse_args()
    create_linting_agent(args.file, args.language)


if __name__ == "__main__":
    main()
