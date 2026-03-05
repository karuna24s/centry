import os
import requests

def run_audit(target_dir: str, file_ext: str = ".rb"):
    """Crawls a directory and sends each file to our Centry API."""
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file.endswith(file_ext):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    content = f.read()

                # Hit our own FastAPI endpoint
                try:
                    response = requests.post(
                        "http://127.0.0.1:8000/analyze",
                        json={"content": content, "context": f"File: {file}"}
                    )
                    print(f"--- Audit Report for {file} ---")
                    print(response.json().get("analysis"))
                    print("\n" + "="*40 + "\n")
                except Exception as e:
                    print(f"Error connecting to Centry API: {e}")

if __name__ == "__main__":
    # Default to scanning the current directory for Ruby files
    # You can change '.' to a specific path of your Rails code
    print("🚀 Centry Scanner starting...")
    run_audit('.', '.rb')