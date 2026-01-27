"""Command-line interface for BlackRoad Deploy."""

import argparse
import sys

from .deploy import Deployer
from .config import load_config


def main():
    parser = argparse.ArgumentParser(
        prog="blackroad_deploy",
        description="Deployment utility for BlackRoad OS applications"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Deploy command
    deploy_parser = subparsers.add_parser("deploy", help="Deploy application")
    deploy_parser.add_argument("--env", required=True, help="Target environment")
    deploy_parser.add_argument("--config", default="config.yaml", help="Config file path")
    deploy_parser.add_argument("--dry-run", action="store_true", help="Simulate deployment")

    # Status command
    status_parser = subparsers.add_parser("status", help="Check deployment status")
    status_parser.add_argument("--env", required=True, help="Target environment")
    status_parser.add_argument("--config", default="config.yaml", help="Config file path")

    # Rollback command
    rollback_parser = subparsers.add_parser("rollback", help="Rollback to previous version")
    rollback_parser.add_argument("--env", required=True, help="Target environment")
    rollback_parser.add_argument("--config", default="config.yaml", help="Config file path")
    rollback_parser.add_argument("--version", help="Specific version to rollback to")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    config = load_config(args.config)
    deployer = Deployer(config)

    if args.command == "deploy":
        success = deployer.deploy(args.env, dry_run=args.dry_run)
        sys.exit(0 if success else 1)
    elif args.command == "status":
        deployer.status(args.env)
    elif args.command == "rollback":
        success = deployer.rollback(args.env, version=getattr(args, "version", None))
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
