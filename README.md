# BlackRoad Deploy

A lightweight deployment utility for BlackRoad OS applications.

## Features

- Multi-environment deployment (development, staging, production)
- Configuration management
- Health checks and rollback support
- Deployment logging and notifications

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Deploy to an environment
python -m blackroad_deploy deploy --env production --config config.yaml

# Check deployment status
python -m blackroad_deploy status --env production

# Rollback to previous version
python -m blackroad_deploy rollback --env production
```

## Configuration

Copy `config.example.yaml` to `config.yaml` and update with your settings:

```yaml
environments:
  production:
    host: prod.example.com
    port: 22
    user: deploy
```

## License

Proprietary - See LICENSE file for details.
