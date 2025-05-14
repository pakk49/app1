import sys
import os

def check_environment():
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Working directory: {os.getcwd()}")
    print("\nPython path:")
    for path in sys.path:
        print(f"  {path}")
    
    try:
        import flask
        print("\nFlask installed version:", flask.__version__)
    except ImportError:
        print("\nFlask not installed")
    
    try:
        import waitress
        print("Waitress installed version:", waitress.__version__)
    except ImportError:
        print("Waitress not installed")

if __name__ == "__main__":
    check_environment()
