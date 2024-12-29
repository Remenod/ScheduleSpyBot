import subprocess

def CompileAll():
    print("Starting compilation...")
    CompileComparer()    
    print("Compilation completed.")

def CompileComparer():  
    try:
        build_result = subprocess.run(["dotnet", "build", "../comparer"], capture_output=True, text=True)
        if build_result.returncode != 0:
            print("Build Error:", build_result.stderr.strip())
            return None
        print("Comparer compiled successfully.")

    except FileNotFoundError:
        print("Error: .NET SDK not found. Ensure `dotnet` is installed and in PATH.")
        return None
