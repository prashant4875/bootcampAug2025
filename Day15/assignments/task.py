#1. Create a list of 5 application names you want to deploy
appName = ['todo', 'email', 'alerting', 'logsCollection', 'monitoring']

for app in appName:
    print(f"Deploying {app} application...")
    # Simulate deployment process
    print(f"{app} application deployed successfully!\n")

# 2. Create a dictionary with your server's configuration (hostname, IP, memory, CPU)
server_config = {
    'hostname': 'server01',
    'IP': '10.0.0.0/16',
    'memory': '32GB',
    'CPU': '8 cores'
}

for key, value in server_config.items():
    hostname = server_config.get('host', 'unknown')
    print(f"Configuring server {hostname}:")
    print(f"{key}: {value}")

# 3. Create a tuple with database connection info (host, port, database name)

db_connection = ('localhost', 5432, 'my_database')

host, port, db_name = db_connection

print(f"Connecting to database '{db_name}' at {host}:{port}...")

# 4. Create two sets:
#    - production_packages: packages installed in prod
#    - staging_packages: packages installed in staging
#    Then find which packages are missing in staging

production_packages = {'nginx', 'postgres', 'redis', 'docker'}
staging_packages = {'nginx', 'postgres'}

missing_packages = production_packages - staging_packages
print(f"Packages missing in staging: {missing_packages}")

# 5. Create a nested dictionary representing 3 servers with their metadata

servers = {
    "server1": {
        "hostname": "prod-server-1",
        "IP": "10.0.0.0/16",
        "roles": ["web", "db"],
    },
    "server2": {
        "hostname": "prod-server-2",
        "IP": "10.0.1.0/24",
        "roles": ["web"],
    },
    "server3": {
        "hostname": "staging-server-1",
        "IP": "10.0.2.0/24",
        "roles": ["web", "db", "cache"],
    },
}

for server_id, metadata in servers.items():
    print(f"Server ID: {server_id}")
    for key, value in metadata.items():
        print(f"  {key}: {value}")

server2_roles = servers.get("server2", {}).get("roles", [])[0]
print(f"Roles for server2: {server2_roles}")




