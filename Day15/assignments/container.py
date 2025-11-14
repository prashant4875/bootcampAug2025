import docker

def cleanup_stopped_containers():
    # Connect to the Docker daemon
    client = docker.from_env()

    # List all containers (including stopped ones)
    containers = client.containers.list(all=True)
    print(f"containers - {containers}")

    deleted = []
    for container in containers:
        container_status = container.status
        print(f"container_status - {container_status}")
        if container_status != "running":
            print(f"🗑️  Removing container: {container.name} ({container.short_id}) - Status: {container_status}")
            container.remove(force=True)
            deleted.append(container.name)

    if not deleted:
        print("✅ No stopped containers found.")
    else:
        print(f"\n✅ Removed containers: {', '.join(deleted)}")

if __name__ == "__main__":
    cleanup_stopped_containers()
