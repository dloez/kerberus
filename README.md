# Kerberus

Kerberus is a dependency analyzer tool. Kerberus uses [osv.dev](https://github.com/google/osv.dev) to get reports of vulnerabilities from scanned dependencies. This documentation is under development, it only includes development instructions.

## Development
This repository is a monorepo that is composed by:
- Backend application
- Frontend application
- CLI application

This document page explains how to setup a development environment for all applications using devcontainers.
The file `/.vscode/settings.json` is the combination of all `settings.json` defined in all child project directories. Childs `settings.json` are kept to allow the development of a single application.

### List of requirements:
- Docker.
- Any editor with support for devcontainers. VSCode is highly recommended.

### Additional requirements if you are on Windows:
- WSL (under windows). This requirement is to store the code directly in WSL to avoid performance issues.
- Docker Desktop with WSL backend configured.
- VSCode with WSL extension installed.

### Steps to create development environment using VSCode:
1. Clone the repository:
```bash
git clone https://github.com/dloez/kerberus
```
2. CD into the directory and run VSCode: 
```bash
cd kerberus; code .
```
3. Open command palette (Ctrl+Shift+p) and enter:
```
Dev Containers: Reopen in Container
```
4. Check the requirements for each application that you need to develop/use under their readme's requirements section.

### Bazel
Currently only backend and cli applications have support for Bazel. There are active efforts on adding Bazel support for the nextjs frontend application.
