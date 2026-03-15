import os
import sys
import subprocess
import time

def check_and_install_dependencies():
    """Checks for required dependencies and installs them if missing."""
    required_packages = ["flask", "pandas", "chromadb", "openai", "python-dotenv"]
    print("Checking dependencies...")
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is already installed.")
        except ImportError:
            print(f"❌ {package} is missing. Installing...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ Successfully installed {package}.")
            except Exception as e:
                print(f"⚠️ Failed to install {package}: {e}")
                sys.exit(1)

def run_import_script():
    """Runs the import script in the current directory."""
    print("\nStarting data import to ChromaDB...")
    try:
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        import_script = os.path.join(script_dir, "import_products.py")
        
        # Run import_products.py using its full path
        result = subprocess.run([sys.executable, import_script], capture_output=True, text=True, cwd=script_dir)
        if result.returncode == 0:
            print("✅ Data import successful!")
            print(result.stdout)
        else:
            print("❌ Data import failed!")
            print(result.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"❌ An error occurred during import: {e}")
        sys.exit(1)

def start_flask_app():
    """Starts the Flask application."""
    print("\nStarting Flask web server...")
    print("Visit http://127.0.0.1:5001 to use the AI Product Search.")
    print("Press Ctrl+C to stop the server.")
    
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        app_script = os.path.join(script_dir, "app.py")
        
        # Run app.py using its full path and set CWD to ensure it finds its dependencies
        subprocess.run([sys.executable, app_script], cwd=script_dir)
    except KeyboardInterrupt:
        print("\nStopping server...")
    except Exception as e:
        print(f"❌ An error occurred while running the app: {e}")

if __name__ == "__main__":
    print("="*40)
    print("🚀 Vector DB Demo Project Setup & Run")
    print("="*40)
    
    check_and_install_dependencies()
    run_import_script()
    start_flask_app()
