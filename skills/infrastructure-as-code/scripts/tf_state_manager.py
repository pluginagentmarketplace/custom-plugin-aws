#!/usr/bin/env python3
"""
Terraform State Management Utility
Manages remote state, workspaces, and drift detection.
"""

import subprocess
import json
import os
from pathlib import Path
from typing import Dict, List, Optional


class TerraformStateManager:
    """Manage Terraform state operations."""

    def __init__(self, working_dir: str = "."):
        self.working_dir = Path(working_dir)
        self.state_file = self.working_dir / "terraform.tfstate"

    def run_terraform(self, *args) -> Dict:
        """Run terraform command and return output."""
        cmd = ["terraform", *args]
        result = subprocess.run(
            cmd,
            cwd=self.working_dir,
            capture_output=True,
            text=True
        )
        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    def init(self, backend_config: Optional[Dict] = None) -> bool:
        """Initialize Terraform with optional backend configuration."""
        args = ["init", "-input=false"]

        if backend_config:
            for key, value in backend_config.items():
                args.append(f"-backend-config={key}={value}")

        result = self.run_terraform(*args)
        return result["returncode"] == 0

    def list_workspaces(self) -> List[str]:
        """List all available workspaces."""
        result = self.run_terraform("workspace", "list")
        if result["returncode"] != 0:
            return []

        workspaces = []
        for line in result["stdout"].strip().split("\n"):
            ws = line.strip().lstrip("* ")
            if ws:
                workspaces.append(ws)
        return workspaces

    def select_workspace(self, name: str) -> bool:
        """Select or create a workspace."""
        result = self.run_terraform("workspace", "select", name)
        if result["returncode"] != 0:
            result = self.run_terraform("workspace", "new", name)
        return result["returncode"] == 0

    def get_state_resources(self) -> List[Dict]:
        """Get list of resources in current state."""
        result = self.run_terraform("state", "list")
        if result["returncode"] != 0:
            return []

        resources = []
        for line in result["stdout"].strip().split("\n"):
            if line:
                resources.append({"address": line.strip()})
        return resources

    def show_resource(self, address: str) -> Optional[Dict]:
        """Show details of a specific resource."""
        result = self.run_terraform("state", "show", "-json", address)
        if result["returncode"] != 0:
            return None
        try:
            return json.loads(result["stdout"])
        except json.JSONDecodeError:
            return None

    def detect_drift(self) -> Dict:
        """Detect configuration drift."""
        result = self.run_terraform("plan", "-detailed-exitcode", "-json")

        drift_report = {
            "has_drift": False,
            "changes": {"add": 0, "change": 0, "destroy": 0},
            "resources": []
        }

        if result["returncode"] == 2:
            drift_report["has_drift"] = True
            try:
                for line in result["stdout"].strip().split("\n"):
                    data = json.loads(line)
                    if data.get("type") == "resource_drift":
                        drift_report["resources"].append({
                            "address": data.get("change", {}).get("resource", {}).get("addr"),
                            "action": data.get("change", {}).get("action")
                        })
            except json.JSONDecodeError:
                pass

        return drift_report

    def backup_state(self, backup_path: str) -> bool:
        """Create backup of current state."""
        result = self.run_terraform("state", "pull")
        if result["returncode"] != 0:
            return False

        with open(backup_path, "w") as f:
            f.write(result["stdout"])
        return True

    def import_resource(self, address: str, resource_id: str) -> bool:
        """Import existing resource into state."""
        result = self.run_terraform("import", address, resource_id)
        return result["returncode"] == 0

    def remove_resource(self, address: str) -> bool:
        """Remove resource from state (not destroy)."""
        result = self.run_terraform("state", "rm", address)
        return result["returncode"] == 0

    def move_resource(self, source: str, destination: str) -> bool:
        """Move/rename resource in state."""
        result = self.run_terraform("state", "mv", source, destination)
        return result["returncode"] == 0


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Terraform State Manager")
    parser.add_argument("--dir", default=".", help="Terraform working directory")

    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("list", help="List all resources")
    subparsers.add_parser("workspaces", help="List workspaces")
    subparsers.add_parser("drift", help="Detect drift")

    backup_parser = subparsers.add_parser("backup", help="Backup state")
    backup_parser.add_argument("path", help="Backup file path")

    args = parser.parse_args()

    manager = TerraformStateManager(args.dir)

    if args.command == "list":
        resources = manager.get_state_resources()
        for r in resources:
            print(r["address"])

    elif args.command == "workspaces":
        for ws in manager.list_workspaces():
            print(ws)

    elif args.command == "drift":
        report = manager.detect_drift()
        print(json.dumps(report, indent=2))

    elif args.command == "backup":
        success = manager.backup_state(args.path)
        print(f"Backup {'successful' if success else 'failed'}")


if __name__ == "__main__":
    main()
