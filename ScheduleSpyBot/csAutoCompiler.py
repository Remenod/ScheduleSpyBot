import os
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
        current_dir = os.path.dirname(os.path.abspath(__file__))
        comparer_dir = os.path.abspath(os.path.join(current_dir, "..", "comparer"))
        
        build_result = subprocess.run(["dotnet", "build", comparer_dir], capture_output=True, text=True)
        if build_result.returncode != 0:
            log(f"Comparer Build Error: {build_result.stderr.strip()}")
            return None
        log("Comparer compiled successfully.")

    except FileNotFoundError:
        log("Comparer Build Error: .NET SDK not found. Ensure `dotnet` is installed and in PATH.")
        return None

def CompileScheduleClass():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        scheduleClass_dir = os.path.abspath(os.path.join(current_dir, "..", "scheduleClass"))
        
        build_result = subprocess.run(["dotnet", "build", scheduleClass_dir], capture_output=True, text=True)        
        if build_result.returncode != 0:
            log(f"ScheduleClass Build Error:{build_result.stderr.strip()}")
            return None
        log("ScheduleClass compiled successfully.")
    except FileNotFoundError:
        log("ScheduleClass Build Error: .NET SDK not found. Ensure `dotnet` is installed and in PATH.")
        return None

def CompileParser():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parser_dir = os.path.abspath(os.path.join(current_dir, "..", "parser"))
 
        build_result = subprocess.run(["dotnet", "build", parser_dir], capture_output=True, text=True)        
        if build_result.returncode != 0:
            log(f"Parser Build Error:{build_result.stderr.strip()}")
            return None
        log("Parser compiled successfully.")
    except FileNotFoundError:
        log("Parser Build Error: .NET SDK not found. Ensure `dotnet` is installed and in PATH.")
        return None