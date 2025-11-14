import os 

relative_path = "test_deployment"
absolute_path = os.path.abspath(relative_path)
print(f"\nRelative path: {relative_path}")
print(f"Absolute path: {absolute_path}")

# TODO: Create a log directory structure
log_base = "test_deployment/logs"

services = ["nginx", "app", "database"]
log_types = ["access", "error"]

print("Creating log directory structure:")
for service in services:
    for log_type in log_types:
        log_dir = os.path.join(log_base, service, log_type)
        os.makedirs(log_dir, exist_ok=True)
        print(f"  Created: {log_dir}")

        # Create a sample log file
        log_file = os.path.join(log_dir, f"{service}_{log_type}.log")
        with open(log_file, "w") as f:
            f.write(f"# {service} {log_type} log\n")
            f.write(f"2024-01-15 10:00:00 Sample log entry\n")

# TODO: Find all .log files
print(f"\nAll .log files in {log_base}:")
log_files = []
for root, dirs, files in os.walk(log_base):
    print(f"root - {root}, dirs - {dirs}, files - {files}")
    for file in files:
        if file.endswith(".log"):
            print(f"root - {root}")
            full_path = os.path.join(root, file)
            log_files.append(full_path)
            file_size = os.path.getsize(full_path)
            print(f"  {full_path} ({file_size} bytes)")
print(f"log_files - {log_files}")

print(f"\nTotal log files found: {len(log_files)}")

print()

# 1. Create a directory structure for a web application:
#    - app/static/css
#    - app/static/js
#    - app/templates
#    - app/logs

app_base = "app"
subdirs = [
    os.path.join("static", "css"),
    os.path.join("static", "js"),
    "templates",
    "logs"
]

for subdir in subdirs:
    dir_path = os.path.join(app_base, subdir)
    os.makedirs(dir_path, exist_ok=True)
    print(f"Created directory: {dir_path}")

# 2. Write code to find all Python files (.py) in the current directory and subdirectories

l = []
print(f"\nSearching for .py files in {os.getcwd()}:")
for root, dirs, files in os.walk(os.getcwd()):
    for name in files:
        if name.endswith(".py"):
            path = os.path.join(root, name)  # Joins directory path (root) with filename (name)
            l.append(path)
            print(f"Found Python file: {path}")

print(f"\nTotal Python files found: {len(l)}")


# 3. Create a function that checks if a directory exists, if not, creates it

def ensure_directory(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"Directory created: {dir_path}")
    else:
        print(f"Directory already exists: {dir_path}")

# Example usage
dir_to_check = "example_dir/subdir"
ensure_directory(dir_to_check)

# 4. Get the size of all files in a directory and calculate total size

total_size = 0 

print(f"\nCalculating total size of files in {os.getcwd()}:")

for root, dirs, files in os.walk(os.getcwd()):
    for name in files:
        path = os.path.join(root, name)
        size = os.path.getsize(path)
        total_size += size
        print(f"File: {path} - Size: {size} bytes")

print(f"\nTotal size of all files: {total_size} bytes")

# 5. Read the PATH environment variable and print each path on a new line

path_env = os.environ.get("PATH", "")

print(f"path environment {type(path_env)}")

print("\nPATH environment variable paths:")
for p in path_env.split(os.pathsep):    
    print(p)

# 6. Create a script that organizes files by extension:
#    - Create folders for each extension found
#    - Move files to their respective folders

for root, dirs, files in os.walk(os.getcwd()):
    for name in files:
        file_path = os.path.join(root, name)
        _, ext = os.path.splitext(name)
        if ext:  # Only process files with an extension
            ext_dir = os.path.join(root, ext.lstrip('.'))  # Remove leading dot for directory name
            os.makedirs(ext_dir, exist_ok=True)
            new_path = os.path.join(ext_dir, name)
            os.rename(file_path, new_path)
            print(f"Moved {file_path} to {new_path}")

# 7. Write code to find the largest file in a directory

for root, dirs, files in os.walk(os.getcwd()):
    largest_file = None
    largest_size = 0
    for name in files:
        path = os.path.join(root, name)
        size = os.path.getsize(path)
        if size > largest_size:
            largest_size = size
            largest_file = path
    if largest_file:
        print(f"Largest file in {root}: {largest_file} ({largest_size} bytes)")

