#!/usr/bin/env python3
"""
Deployment Manager
Manages deployments with rollback capabilities.
"""

import subprocess
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path


class DeploymentManager:
    """Manage Kubernetes deployments with health checks and rollback."""

    def __init__(self, namespace: str = "default", kubeconfig: str = None):
        self.namespace = namespace
        self.kubeconfig = kubeconfig
        self.history: List[Dict] = []

    def _run_kubectl(self, *args, capture: bool = True) -> Dict:
        """Run kubectl command."""
        cmd = ["kubectl"]
        if self.kubeconfig:
            cmd.extend(["--kubeconfig", self.kubeconfig])
        cmd.extend(["-n", self.namespace])
        cmd.extend(args)

        result = subprocess.run(
            cmd,
            capture_output=capture,
            text=True
        )

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }

    def get_deployment(self, name: str) -> Optional[Dict]:
        """Get deployment details."""
        result = self._run_kubectl("get", "deployment", name, "-o", "json")
        if not result["success"]:
            return None
        try:
            return json.loads(result["stdout"])
        except json.JSONDecodeError:
            return None

    def get_deployment_status(self, name: str) -> Dict:
        """Get deployment rollout status."""
        deployment = self.get_deployment(name)
        if not deployment:
            return {"status": "not_found"}

        status = deployment.get("status", {})
        spec = deployment.get("spec", {})

        return {
            "name": name,
            "replicas": spec.get("replicas", 0),
            "ready": status.get("readyReplicas", 0),
            "updated": status.get("updatedReplicas", 0),
            "available": status.get("availableReplicas", 0),
            "conditions": status.get("conditions", [])
        }

    def deploy(self, name: str, image: str, wait: bool = True, timeout: int = 300) -> Dict:
        """Deploy new image to deployment."""
        deploy_record = {
            "timestamp": datetime.now().isoformat(),
            "deployment": name,
            "image": image,
            "status": "starting"
        }

        # Get current image for rollback
        current = self.get_deployment(name)
        if current:
            containers = current.get("spec", {}).get("template", {}).get("spec", {}).get("containers", [])
            if containers:
                deploy_record["previous_image"] = containers[0].get("image")

        # Update image
        result = self._run_kubectl(
            "set", "image",
            f"deployment/{name}",
            f"{name}={image}"
        )

        if not result["success"]:
            deploy_record["status"] = "failed"
            deploy_record["error"] = result["stderr"]
            self.history.append(deploy_record)
            return deploy_record

        if wait:
            # Wait for rollout
            result = self._run_kubectl(
                "rollout", "status",
                f"deployment/{name}",
                f"--timeout={timeout}s"
            )

            if result["success"]:
                deploy_record["status"] = "success"
            else:
                deploy_record["status"] = "timeout"
                deploy_record["error"] = result["stderr"]

        self.history.append(deploy_record)
        return deploy_record

    def rollback(self, name: str, revision: int = None) -> Dict:
        """Rollback deployment to previous revision."""
        rollback_record = {
            "timestamp": datetime.now().isoformat(),
            "deployment": name,
            "type": "rollback",
            "revision": revision
        }

        args = ["rollout", "undo", f"deployment/{name}"]
        if revision:
            args.extend(["--to-revision", str(revision)])

        result = self._run_kubectl(*args)

        if result["success"]:
            rollback_record["status"] = "success"
        else:
            rollback_record["status"] = "failed"
            rollback_record["error"] = result["stderr"]

        self.history.append(rollback_record)
        return rollback_record

    def scale(self, name: str, replicas: int) -> Dict:
        """Scale deployment to specified replicas."""
        result = self._run_kubectl(
            "scale", f"deployment/{name}",
            f"--replicas={replicas}"
        )

        return {
            "deployment": name,
            "replicas": replicas,
            "success": result["success"],
            "error": result["stderr"] if not result["success"] else None
        }

    def get_rollout_history(self, name: str) -> List[Dict]:
        """Get deployment rollout history."""
        result = self._run_kubectl(
            "rollout", "history",
            f"deployment/{name}",
            "-o", "json"
        )

        if not result["success"]:
            return []

        try:
            return json.loads(result["stdout"])
        except json.JSONDecodeError:
            return []

    def health_check(self, name: str, timeout: int = 60) -> Dict:
        """Perform health check on deployment."""
        start_time = time.time()
        checks = []

        while time.time() - start_time < timeout:
            status = self.get_deployment_status(name)

            check = {
                "timestamp": datetime.now().isoformat(),
                "ready": status.get("ready", 0),
                "replicas": status.get("replicas", 0)
            }

            if status.get("ready") == status.get("replicas") and status.get("ready") > 0:
                check["healthy"] = True
                checks.append(check)
                return {
                    "deployment": name,
                    "healthy": True,
                    "checks": checks
                }

            check["healthy"] = False
            checks.append(check)
            time.sleep(5)

        return {
            "deployment": name,
            "healthy": False,
            "checks": checks,
            "error": "Timeout waiting for healthy state"
        }


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Deployment Manager")
    parser.add_argument("--namespace", "-n", default="default")
    parser.add_argument("--kubeconfig", "-k")

    subparsers = parser.add_subparsers(dest="command")

    # Deploy command
    deploy_parser = subparsers.add_parser("deploy")
    deploy_parser.add_argument("name", help="Deployment name")
    deploy_parser.add_argument("image", help="Container image")
    deploy_parser.add_argument("--no-wait", action="store_true")

    # Rollback command
    rollback_parser = subparsers.add_parser("rollback")
    rollback_parser.add_argument("name", help="Deployment name")
    rollback_parser.add_argument("--revision", "-r", type=int)

    # Status command
    status_parser = subparsers.add_parser("status")
    status_parser.add_argument("name", help="Deployment name")

    # Scale command
    scale_parser = subparsers.add_parser("scale")
    scale_parser.add_argument("name", help="Deployment name")
    scale_parser.add_argument("replicas", type=int)

    args = parser.parse_args()

    manager = DeploymentManager(
        namespace=args.namespace,
        kubeconfig=args.kubeconfig
    )

    if args.command == "deploy":
        result = manager.deploy(args.name, args.image, wait=not args.no_wait)
    elif args.command == "rollback":
        result = manager.rollback(args.name, args.revision)
    elif args.command == "status":
        result = manager.get_deployment_status(args.name)
    elif args.command == "scale":
        result = manager.scale(args.name, args.replicas)
    else:
        parser.print_help()
        return

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
