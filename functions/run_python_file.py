import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_file.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: File "{file_path}" not found.'
    if not target_file.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        result = subprocess.run(["python", file_path] + args, cwd = abs_working_dir, capture_output = True, timeout = 30, text = True)
        outputs = []
        if result.stdout:
            outputs.append("STDOUT: " + result.stdout.strip())
        if result.stderr:
            outputs.append("STDERR: " + result.stderr.strip())
        answer = "\n".join(outputs)
        if answer == "":
            return "No output produced."
        if result.returncode != 0:
            if answer:
                answer += f"\nProcess exited with code {result.returncode}"
            else:
                answer = f"Process exited with code {result.returncode}"
        return answer
    except Exception as e:
        return f"Error: executing Python file: {e}"