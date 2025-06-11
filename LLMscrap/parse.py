from utils import search_with_ollama

# Test script for the search_with_ollama function, used to validate parsing logic.
# This file serves as a standalone entry point for manual testing.
# Date: June 10, 2025

if __name__ == "__main__":
    # Sample data for testing the parsing function.
    content = ["Sample car data"]
    query = "How many miles?"
    # Execute the search_with_ollama function with test data and print the result.
    print(search_with_ollama(content, query))  # Output the parsed result for verification.