import importlib
import os
import sys

def test_imports(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                module_path = os.path.join(root, file)
                module_name = os.path.splitext(file)[0]
                
                try:
                    module = importlib.import_module(module_name)
                    print(f"Successfully imported: {module_name}")
                except ImportError as e:
                    print(f"Error importing {module_name}: {str(e)}")
                except Exception as e:
                    print(f"Error in {module_name}: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the directory path as a command-line argument.")
    else:
        directory = sys.argv[1]
        test_imports(directory)
