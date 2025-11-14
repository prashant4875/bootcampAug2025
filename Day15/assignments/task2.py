matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [num for row in matrix for num in row]
print(f"Matrix: {matrix}")
print(f"Flattened: {flattened}")

server_list = ["web-1", "web-2", "db-1"]
server_ports = {server: 8080 if "web" in server else 5432 for server in server_list}
print(f"Server ports: {server_ports}")

deployments = ["prod-web-1", "staging-web-1", "prod-db-1", "dev-web-1", "staging-db-1"]
environments = {deploy.split("-")[0] for deploy in deployments}
print(f"Unique environments: {environments}")

# 1. Write a conditional that checks if disk usage is above 90% and prints appropriate warnings

disk_usage_percent = 92  # Example value; in real code, fetch this from system metrics
if disk_usage_percent > 90:
    print("Warning: Disk usage is above 90%! Consider cleaning up space.")
else:
    print("Disk usage is within acceptable limits.")

# 2. Create a for loop that iterates through a list of 10 IP addresses and prints each one

ip_list = [i + ' 10.0.0./32' for i in ['10.0.0.0/16', '10.0.0.0/24']]

print(ip_list)

# 3. Write a while loop that simulates checking server health every iteration until status is "healthy"

status = "unhealthy"
while True:
    print("Checking server health...")
    # Simulate health check logic
    status = "healthy"  # In real code, update this based on actual health check
    if status == "healthy":
        print("Server is healthy.")
        break

# 4.Use a list comprehension to create a list of port numbers from 8000 to 8010

port = [i for i in range(8000, 8011)]

print(port)

# 5. Write a nested loop that checks 5 servers, each running 3 services, and prints the status
servers = ['server1', 'server2', 'server3', 'server4', 'server5']
services = ['web', 'db', 'cache']

for server in servers:
    for service in services:
        print(f"Checking {service} service on {server}... Status: OK")


# 6. Use break to stop processing a list of logs when you find the first CRITICAL error
logs = ["INFO: All systems operational", "WARNING: High memory usage", "CRITICAL: Disk failure detected", "INFO: Backup completed"]

for log in logs:
    print(f"Processing log: {log}")
    if "CRITICAL" in log:
        print(f"Alert! {log}")
        break

# 7. Create a dictionary comprehension that maps server names to their status
server_names = ['web-1', 'db-1', 'cache-1']
server_status = {server: "active" if "web" in server else "standby" for server in server_names}
print(f"Server status: {server_status}")

# 8. Parse a list of log entries and count how many of each log level (INFO, WARNING, ERROR) exist

log_entries = [
    "2024-01-15 10:23:45 INFO User login successful",
    "2024-01-15 10:24:12 ERROR Database connection failed",
    "2024-01-15 10:24:15 INFO Retrying database connection",
    "2024-01-15 10:24:18 ERROR Database connection failed",
    "2024-01-15 10:25:01 WARNING High memory usage detected",
    "2024-01-15 10:25:30 INFO User logout",
    "2024-01-15 10:26:00 ERROR API request timeout",
    "2024-01-15 10:26:15 INFO Cache cleared",
]

log_level_counts = {"INFO": 0, "WARNING": 0, "ERROR": 0}
for entry in log_entries:
    if "INFO" in entry:
        log_level_counts["INFO"] += 1
    elif "WARNING" in entry:
        log_level_counts["WARNING"] += 1
    elif "ERROR" in entry:
        log_level_counts["ERROR"] += 1

print(f"Log level counts: {log_level_counts}")
