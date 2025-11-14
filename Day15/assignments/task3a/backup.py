# 8. Create a backup system that:
#    - Creates timestamped backup folders
#    - Copies all .config files to the backup folder
#    - Lists all available backups sorted by date

import datetime
import os 

backup_base = "test_deployment/backups"
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
backup_path = os.path.join(backup_base, f"backup_{timestamp}")

os.makedirs(backup_path, exist_ok=True)
print(f"Created backup directory: {backup_path}")

config_source = os.path.join("test_deployment", "application.config")
if os.path.exists(config_source):
    import shutil 

    config_backup = os.path.join(backup_path, "application.config")
    shutil.copy2(config_source, config_backup)
    print(f"Backed up configuration file to: {config_backup}")

if os.path.exists(backup_base):
    backups = sorted(os.listdir(backup_base), reverse=True)
    for backup in backups:
        backup_path = os.path.join(backup_base, backup)
        if os.path.isdir(backup_path):
            backup_size = sum(
                os.path.getsize(os.path.join(backup_path, f))
                for f in os.listdir(backup_path)
                if os.path.isfile(os.path.join(backup_path, f))
            )
            print(f"Backup: {backup} - Size: {backup_size} bytes")


