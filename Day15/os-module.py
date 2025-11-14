import os

print("Current Working Directory:", os.getcwd())

# print("List of files and directories in the current directory:", os.listdir("c:/Users/bhado/OneDrive/Documents/AugustBootcamp2025/bootcampAug2025/Day8"))

# for root, dirs, files in os.walk(os.getcwd()):
#     print("Root:", root)
#     for d in dirs:
#         print("  Dir:", d)
#     for f in files:
#         print("  File:", f)
#     print("-" * 40)

def get_files_smaller_than(dir_path=None, max_kb=10):
    """Return a list of file paths under dir_path that are smaller than max_kb kilobytes."""
    if dir_path is None:
        dir_path = os.getcwd()
    threshold = max_kb * 1024
    small_files = []
    for root, _, files in os.walk(dir_path):
        for name in files:
            path = os.path.join(root, name)
            try:
                if os.path.getsize(path) < threshold:
                    small_files.append(os.path.abspath(path))
            except OSError:
                # skip files we can't access
                continue
    return small_files


print(dir(os))