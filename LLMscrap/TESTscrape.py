from utils import parse_with_ollama

if __name__ == "__main__":
    content = ["Sample text"]
    query = "Extract text"
    print(parse_with_ollama(content, query))