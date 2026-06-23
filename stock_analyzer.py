#!/usr/bin/env python3
import os
import sys

def main():
    # Identify the modular main.py inside the workspace
    current_dir = os.path.dirname(os.path.abspath(__file__))
    main_py = os.path.join(current_dir, "main.py")
    
    # Execute main.py, replacing the current process and forwarding all arguments transparently
    os.execv(sys.executable, [sys.executable, main_py] + sys.argv[1:])

if __name__ == "__main__":
    main()
