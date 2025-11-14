import subprocess
import sys
import os 
import shutil
import socket
import platform
import re

# result = subprocess.run(["cmd", "/c", "echo", "Hello from subprocess!"])
# print(f"Return code: {result.returncode}")

# result1 = subprocess.run(["python", "--version"], capture_output=True, text=True)
# print(f"Python version: {result1.stdout.strip()}")
# print(f"Return code: {result1.returncode}")

# 1. Write code to execute 'ls -la' (or 'dir' on Windows) and print the output

result = subprocess.run(["cmd", "/c", "dir"], capture_output=True, text=True)
print(result.stdout)

# 2. Create a function that runs a command and returns True if it succeeds, False otherwise

def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            return True
        else:
            return False
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        print(f"Error executing command: {e}")
        return False
    

print(run_command("echo Testing command execution"))

# 3. Write code to check if Docker is installed and print its version

docker_check = subprocess.run(["docker", "--version"], capture_output=True, text=True)
if docker_check.returncode == 0:
    print(f"Docker is installed: {docker_check.stdout.strip()}")

# # 4. Create a script that:
#    - Creates a directory
#    - Creates a file in that directory
#    - Lists the contents using subprocess
#    - Deletes the directory

test_dir = "test_subprocess_dir"
os.makedirs(test_dir, exist_ok=True)
test_file_path = os.path.join(test_dir, "test_file.txt")

with open(test_file_path, "w") as f:
    f.write("This is a test file.")

list_result = subprocess.run(["cmd", "/c", "dir", test_dir], capture_output=True, text=True)
print(f"Contents of {test_dir}:\n{list_result.stdout}")

shutil.rmtree(test_dir)
print(f"Deleted directory: {test_dir}")

# 5. Write a function that runs a command with a timeout and handles the timeout exception

def run_command_with_timeout(command, timeout):
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
        return result.stdout
    except subprocess.TimeoutExpired:
        return "Command timed out"
    
# print(run_command_with_timeout(['ping', 'google.com'], 1))  # Windows

# 6. Use subprocess to run 'git status' and parse the output to check if there are uncommitted changes
git_status = subprocess.run("git status --porcelain", capture_output=True, text=True, shell=True)
print("STDOUT:", git_status.stdout)
print("STDERR:", git_status.stderr)
print("RETURN CODE:", git_status.returncode)
if git_status.returncode == 0:
    if git_status.stdout.strip() == "":
        print("No uncommitted changes.")
    else:
        print("There are uncommitted changes:")
        print(git_status.stdout)
else:
    print("Error running git status:", git_status.stderr)

# 7. Create a health check script that:
#    - Checks if required services are running
#    - Checks disk space
#    - Checks if required ports are available
#    - Returns a summary report

REQUIRED_SERVICES = ["postgresql", "nginx"]  # Customize
REQUIRED_PORTS = [80, 443, 5432]  # Example ports
DISK_THRESHOLD = 80  # Warning threshold in %

def run_cmd(cmd, shell=False):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=shell)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return ""
    except Exception as e:
        return ""


def check_services(services):
    print("\n[🔍] Checking required services...")
    running = []
    not_running = []

    for svc in services:
        try:
            if platform.system() == "Windows":
                # sc query service_name
                cmd = ["sc", "query", svc]
                output = run_cmd(cmd)
                if "RUNNING" in output:
                    running.append(svc)
                else:
                    not_running.append(svc)
            else:
                # systemctl is-active service_name
                cmd = ["systemctl", "is-active", "--quiet", svc]
                result = subprocess.run(cmd)
                if result.returncode == 0:
                    running.append(svc)
                else:
                    not_running.append(svc)
        except Exception:
            not_running.append(svc)
    return running, not_running

def check_disk_space():
    print("\n[💽] Checking disk space...")
    system_name = platform.system()
    usage_percent = None

    if system_name == "Windows":
        cmd = 'wmic logicaldisk get size,freespace,caption'
        output = run_cmd(cmd, shell=True)
        # Parse first drive (e.g., C:)
        lines = output.splitlines()[1:]
        for line in lines:
            parts = line.split()
            if len(parts) == 3 and parts[0].startswith("C:"):
                freespace = int(parts[1])
                total = int(parts[2])
                usage_percent = round((1 - freespace / total) * 100, 2)
                break
    else:
        cmd = ["df", "-h", "/"]
        output = run_cmd(cmd)
        lines = output.splitlines()
        if len(lines) > 1:
            data = re.split(r"\s+", lines[1])
            usage_percent = int(data[4].replace("%", ""))

    return usage_percent if usage_percent is not None else 0


def check_ports(ports):
    print("\n[🌐] Checking required ports (using subprocess)...")
    unavailable = []

    try:
        system = platform.system()

        if system == "Windows":
            # Use netstat -ano to list listening ports
            cmd = "netstat -ano"
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            output = result.stdout
            open_ports = set()

            for line in output.splitlines():
                if "LISTEN" in line or "LISTENING" in line:
                    match = re.search(r":(\d+)\s+", line)
                    if match:
                        open_ports.add(int(match.group(1)))

        else:
            # Linux / macOS: use netstat -tuln
            cmd = ["netstat", "-tuln"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            output = result.stdout
            open_ports = set()

            for line in output.splitlines():
                match = re.search(r":(\d+)\s", line)
                if match:
                    open_ports.add(int(match.group(1)))

        # Check required ports against open ports
        for port in ports:
            if port not in open_ports:
                unavailable.append(port)

    except Exception as e:
        print(f"Error checking ports: {e}")

    return unavailable

def print_report(running, not_running, disk_usage, unavailable_ports):
    print("\n============================")
    print(" 🩺 SYSTEM HEALTH REPORT")
    print("============================")
    print(f"\n✅ Running Services: {', '.join(running) if running else 'None'}")
    print(f"❌ Not Running Services: {', '.join(not_running) if not_running else 'None'}")
    print(f"\n💾 Disk Usage: {disk_usage}% used")
    if disk_usage > DISK_THRESHOLD:
        print("⚠️ Warning: Disk usage exceeds threshold!")
    print(f"\n🌐 Unavailable Ports: {', '.join(map(str, unavailable_ports)) if unavailable_ports else 'None'}")

    print("\n============================")
    if not_running or unavailable_ports or disk_usage > DISK_THRESHOLD:
        print("⚠️ Overall Status: Issues Detected")
    else:
        print("✅ Overall Status: Healthy")
    print("============================")

if __name__ == "__main__":
    running, not_running = check_services(REQUIRED_SERVICES)
    disk_usage = check_disk_space()
    unavailable_ports = check_ports(REQUIRED_PORTS)
    print_report(running, not_running, disk_usage, unavailable_ports)


# 8. Write code that runs multiple commands in sequence and stops if any command fails

commands = [
    ["python", "--version"],
    ["docker", "--version"],
    ["git", "--version"]
]
for cmd in commands:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            print(f"Command {' '.join(cmd)} failed with error: {result.stderr.strip()}")
            break
        else:
            print(f"Command {' '.join(cmd)} succeeded with output: {result.stdout.strip()}")
    except FileNotFoundError as e:
        print(f"Command {' '.join(cmd)} failed: {e}")
        break
    except subprocess.TimeoutExpired:
        print(f"Command {' '.join(cmd)} timed out.")
        break

# 9. Create a function that runs a shell command and logs both stdout and stderr to separate files

def run_and_log(command, stdout_file, stderr_file):
    with open(stdout_file, "w") as out_f, open(stderr_file, "w") as err_f:
        result = subprocess.run(command, stdout=out_f, stderr=err_f, text=True, shell=True)
    return result.returncode    

ret_code = run_and_log("python3 --version", "stdout.log", "stderr.log")
print(f"Command finished with return code: {ret_code}")

# 10. Build a simple backup script using subprocess that:
#     - Creates a tar archive of a directory (Unix) or zip (Windows)
#     - Verifies the archive was created successfully
#     - Prints the size of the backup

# def backup_directory(source_dir, backup_name):
#     print(f"source directory path {os.path.exists(source_dir)}")
#     system = platform.system()
#     if system == "Windows":
#         backup_file = f"{backup_name}.zip"
#         cmd = ["powershell.exe", "-Command", f"Compress-Archive -Path '{source_dir}' -DestinationPath '{backup_file}' -Force"]
#     else:
#         backup_file = f"{backup_name}.tar.gz"
#         cmd = ["tar", "-czf", backup_file, source_dir]
#     print(f"Creating backup: {' '.join(cmd)}")
#     result = subprocess.run(cmd, capture_output=True, text=True)
#     print(f"STDOUT: {result.stdout}")
#     if result.returncode == 0 and os.path.exists(backup_file):
#         size = os.path.getsize(backup_file)
#         print(f"Backup created successfully: {backup_file} ({size} bytes)")
#     else:
#         print(f"Backup failed: {result.stderr.strip()}")

def backup_directory(source_dir, backup_name):
    if not os.path.exists(source_dir):
        print(f"Source directory does not exist: {source_dir}")
        return

    backup_file = shutil.make_archive(backup_name, 'zip', source_dir)
    size = os.path.getsize(backup_file)
    print(f"Backup created successfully: {backup_file} ({size} bytes)")

backup_directory("python12", "python12_backup")

# import os
# import platform
# import subprocess

# def backup_directory(source_dir, backup_name):
#     print(f"Source directory exists: {os.path.exists(source_dir)}")

#     system = platform.system()
#     if system == "Windows":
#         # Use full path for reliability
#         source_dir = os.path.abspath(source_dir)
#         backup_file = os.path.abspath(f"{backup_name}.zip")

#         # Double quotes inside PowerShell are required
#         cmd = [
#             "powershell.exe",
#             "-Command",
#             f"Compress-Archive -Path \"{source_dir}\" -DestinationPath \"{backup_file}\" -Force"
#         ]
#     else:
#         backup_file = f"{backup_name}.tar.gz"
#         cmd = ["tar", "-czf", backup_file, source_dir]

#     print(f"Creating backup: {' '.join(cmd)}")

#     # Run the command
#     result = subprocess.run(cmd, capture_output=True, text=True)

#     print(f"STDOUT: {result.stdout.strip()}")
#     print(f"STDERR: {result.stderr.strip()}")

#     if result.returncode == 0 and os.path.exists(backup_file):
#         size = os.path.getsize(backup_file)
#         print(f"✅ Backup created successfully: {backup_file} ({size} bytes)")
#     else:
#         print(f"❌ Backup failed: {result.stderr.strip()}")

# # Example
# backup_directory("python12", "python12_backup")
