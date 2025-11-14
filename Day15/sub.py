import subprocess

subprocess.run('dir', shell=True)

result = subprocess.run(['echo', 'os-module.py'], stdout=subprocess.PIPE, text=True)
print(result.stdout)