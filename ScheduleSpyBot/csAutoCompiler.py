import subprocess

def CompileAll():
    print("Starting compilation...")
    CompileScheduleClass()
    CompileComparer()
    CompileParser()    
    print("Compilation is finished.")

def CompileComparer():
    try:
        build_result = subprocess.run(["dotnet", "build", "../comparer"], capture_output=True, text=True)
        if build_result.returncode != 0:
            print("Comparer Build Error:", build_result.stderr.strip())
            return None
        print("Comparer compiled successfully.")

    except FileNotFoundError:
        print("Comparer Build Error: .NET SDK not found. Ensure `dotnet` is installed and in PATH.")
        return None

def CompileScheduleClass():
    try:
        build_result = subprocess.run(["dotnet", "build", "../scheduleClass"], capture_output=True, text=True)
        if build_result.returncode != 0:
            print("ScheduleClass Build Error:", build_result.stderr.strip())
            return None
        print("ScheduleClass compiled successfully.")
    except FileNotFoundError:
        print("ScheduleClass Build Error: .NET SDK not found. Ensure `dotnet` is installed and in PATH.")
        return None

def CompileParser():
    try:
        build_result = subprocess.run(["dotnet", "build", "../parser"], capture_output=True, text=True)
        if build_result.returncode != 0:
            print("Parser Build Error:", build_result.stderr.strip())
            return None
        print("Parser compiled successfully.")
    except FileNotFoundError:
        print("Parser Build Error: .NET SDK not found. Ensure `dotnet` is installed and in PATH.")
        return None