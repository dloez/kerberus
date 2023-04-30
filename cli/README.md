# Kerberus Backend

The Kerberus CLI is a rust application. This documentation is under development, it only includes development instructions.

## Development
This documentation assumes that you have followed the documentation section defined in [the project README](https://github.com/dloez/kerberus/blob/main/README.md) and that you already have a development environment inside a devcontainer.

### Bazel targets
- Run rust binary:
```bash
bazel run //cli:kerberus-cli
```

You can pass parameters adding `-- PARAMETERS`. For example, you can pass the `-p` parameter to specify the project directory where the CLI should perform a scan by running `bazel run //cli:kerberus-cli -- -p /PROJECT_DIR`. Make sure to use absolute paths while running the CLI as the binary is not being executed from the current working directory, it is being executed undir bazel output directory.
