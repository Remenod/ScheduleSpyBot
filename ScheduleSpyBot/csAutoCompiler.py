import subprocess
from logger import log

def CompileAll():
    log("Starting compilation...")
    CompileScheduleClass()
    CompileComparer()
    CompileParser()    
    log("Compilation is finished.")

def CompileComparer():
    try:
        build_result = subprocess.run(["dotnet", "build", "../comparer"], capture_output=True, text=True)
        if build_result.returncode != 0:
            log(f"Comparer Build Error: {build_result.stderr.strip()}")
            return None
        log("Comparer compiled successfully.")

    except FileNotFoundError:
        log("Comparer Build Error: .NET SDK not found. Ensure `dotnet` is installed and in PATH.")
        return None

def CompileScheduleClass():
    try:
        build_result = subprocess.run(["dotnet", "build", "../scheduleClass"], capture_output=True, text=True)
        if build_result.returncode != 0:
            log(f"ScheduleClass Build Error:{build_result.stderr.strip()}")
            return None
        log("ScheduleClass compiled successfully.")
    except FileNotFoundError:
        log("ScheduleClass Build Error: .NET SDK not found. Ensure `dotnet` is installed and in PATH.")
        return None

def CompileParser():
    try:
        build_result = subprocess.run(["dotnet", "build", "../parser"], capture_output=True, text=True)
        if build_result.returncode != 0:
            log(f"Parser Build Error:{build_result.stderr.strip()}")
            return None
        log("Parser compiled successfully.")
    except FileNotFoundError:
        log("Parser Build Error: .NET SDK not found. Ensure `dotnet` is installed and in PATH.")
        return None