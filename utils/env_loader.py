import os
from pathlib import Path

def load_env(override: bool = True):
    """Load environment variables from .env file"""
    env_path = Path(__file__).parent.parent / ".env"
    
    if not env_path.exists():
        print("Warning: .env file not found. Please create one with your API keys.")
        return
    
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                
                if override or key not in os.environ:
                    os.environ[key] = value