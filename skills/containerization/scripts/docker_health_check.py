#!/usr/bin/env python3
"""
Docker Container Health Check Utility
Monitor and analyze container health and resource usage.
"""

import subprocess
import json
from datetime import datetime
from typing import Dict, List, Optional


class DockerHealthChecker:
    """Monitor Docker container health and resources."""

    def list_containers(self, all_containers: bool = False) -> List[Dict]:
        """List running containers with status."""
        cmd = ["docker", "ps", "--format", "{{json .}}"]
        if all_containers:
            cmd.insert(2, "-a")

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            return []

        containers = []
        for line in result.stdout.strip().split("\n"):
            if line:
                containers.append(json.loads(line))
        return containers

    def get_container_stats(self, container_id: str) -> Optional[Dict]:
        """Get resource stats for a container."""
        cmd = ["docker", "stats", container_id, "--no-stream", "--format", "{{json .}}"]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            return None

        try:
            return json.loads(result.stdout.strip())
        except json.JSONDecodeError:
            return None

    def get_container_logs(self, container_id: str, lines: int = 100) -> str:
        """Get recent container logs."""
        cmd = ["docker", "logs", container_id, "--tail", str(lines)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout + result.stderr

    def inspect_container(self, container_id: str) -> Optional[Dict]:
        """Get detailed container information."""
        cmd = ["docker", "inspect", container_id]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            return None

        try:
            return json.loads(result.stdout)[0]
        except (json.JSONDecodeError, IndexError):
            return None

    def check_health(self, container_id: str) -> Dict:
        """Check container health status."""
        info = self.inspect_container(container_id)
        if not info:
            return {"status": "error", "message": "Container not found"}

        state = info.get("State", {})
        health = state.get("Health", {})

        return {
            "container_id": container_id[:12],
            "name": info.get("Name", "").lstrip("/"),
            "status": state.get("Status"),
            "running": state.get("Running"),
            "health_status": health.get("Status", "no healthcheck"),
            "restarts": info.get("RestartCount", 0),
            "started_at": state.get("StartedAt"),
            "last_health_check": health.get("Log", [{}])[-1] if health.get("Log") else None
        }

    def get_all_stats(self) -> List[Dict]:
        """Get stats for all running containers."""
        cmd = ["docker", "stats", "--no-stream", "--format", "{{json .}}"]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            return []

        stats = []
        for line in result.stdout.strip().split("\n"):
            if line:
                try:
                    stats.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        return stats

    def check_image_vulnerabilities(self, image: str) -> Dict:
        """Check image for vulnerabilities using docker scout."""
        cmd = ["docker", "scout", "cves", image, "--format", "json"]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            return {"error": "Docker Scout not available or scan failed"}

        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return {"error": "Failed to parse scan results"}

    def full_health_report(self) -> Dict:
        """Generate full health report for all containers."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "containers": [],
            "summary": {
                "total": 0,
                "running": 0,
                "healthy": 0,
                "unhealthy": 0,
                "no_healthcheck": 0
            }
        }

        containers = self.list_containers()
        report["summary"]["total"] = len(containers)

        for container in containers:
            container_id = container.get("ID", "")
            health = self.check_health(container_id)
            stats = self.get_container_stats(container_id)

            container_report = {
                **health,
                "stats": stats
            }
            report["containers"].append(container_report)

            if health.get("running"):
                report["summary"]["running"] += 1

            health_status = health.get("health_status", "")
            if health_status == "healthy":
                report["summary"]["healthy"] += 1
            elif health_status == "unhealthy":
                report["summary"]["unhealthy"] += 1
            else:
                report["summary"]["no_healthcheck"] += 1

        return report


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Docker Health Checker")
    parser.add_argument("--container", "-c", help="Specific container ID or name")
    parser.add_argument("--format", choices=["json", "table"], default="json")
    parser.add_argument("--logs", type=int, help="Show last N log lines")

    args = parser.parse_args()
    checker = DockerHealthChecker()

    if args.container:
        if args.logs:
            print(checker.get_container_logs(args.container, args.logs))
        else:
            result = checker.check_health(args.container)
            print(json.dumps(result, indent=2))
    else:
        report = checker.full_health_report()
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
