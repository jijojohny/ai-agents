import os
from dotenv import load_dotenv
from main import DevopsPipelineAgent

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
if __name__ == "__main__":
    a = DevopsPipelineAgent("openai", "gpt-4o-mini")
    a.print_result(a.chat("Rust: fmt, clippy, cargo test, release binary to GH Releases.", verbose=True))
