import connect
import time
import sys
import os


def print_chatdb_logo():
    logo = """
    \033[1;36m
    ██████╗██╗  ██╗ █████╗ ████████╗██████╗ ██████╗ 
    ██╔════╝██║  ██║██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗
    ██║     ███████║███████║   ██║   ██║  ██║██████╔╝
    ██║     ██╔══██║██╔══██║   ██║   ██║  ██║██╔══██╗
    ╚██████╗██║  ██║██║  ██║   ██║   ██████╔╝██████╔╝
     ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═════╝ ╚═════╝ 
    \033[0m"""

    subtitle = """
    \033[1;33m📊 Your Interactive SQL Learning Companion 📊\033[0m
    """

    features = """
    \033[1;32m╔════════════════════════════════════════════╗
    ║  • Get SQL Introductions and Tutorials     ║
    ║  • Learn SQL Through Natural Conversation  ║
    ║  • Execute Real-time Database Queries      ║
    ║  • Practice Problems Provided              ║
    ╚════════════════════════════════════════════╝\033[0m
    """

    team_info = """
    \033[1;34m 📚University of Southern California DSCI-551 | Team: Jason Huang\033[0m
    """

    print(logo)
    print(subtitle)
    print(features)
    print(team_info)


def print_help_message():
    help_text = """
    \033[1;37m
    Available Commands:
    🔍  1. Explore Datasets
    ⌨️   2. Execute SQL Query
    💭  3. Natural Language Query
    ❌  4. Exit

    Tips:
    💡 Explore schema before writing queries
    💡 Check example queries for reference
    💡 Use natural language to generate queries
    \033[0m
    """
    print(help_text)


def print_welcome():
    # # Clear screen (works on both Windows and Unix-like systems)
    # os.system('cls' if os.name == 'nt' else 'clear')
    # Print logo and welcome message
    print_chatdb_logo()
    # Small delay for dramatic effect
    time.sleep(1)
    # Print help message
    print_help_message()
