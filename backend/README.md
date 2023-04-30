# Kerberus Backend

The Kerberus backend is a Django project. The main piece of this application is a versioned REST API accessed by frontend and cli applications. This documentation is under development, it only includes development instructions.

## Development
This documentation assumes that you have followed the documentation section defined in [the project README](https://github.com/dloez/kerberus/blob/main/README.md) and that you already have a development environment inside a devcontainer.

### Requirements:
- Define the environment variable `DJANGO_SECRET_KEY` for the django `SECRET_KEY` settings parameter. You can define it in your system by running `export DJANGO_SECRET_KEY=MY_SECRET` and reopen the devcontainer, this will be automatically be loaded into the devcontainers' environment variables because it is defined in the `removeEnv` section of the [`devcontainers.json` file](https://github.com/dloez/kerberus/blob/main/.devcontainer.json).
- Run `poetry install`. This will create a virtual environment in `.venv` directory. This is not required to run the application as it is built by bazel, it is only required for the editor to have a virtual environment with the required dependencies installed.

### Bazel targets
- Run `manage.py`:
```bash
bazel run //backend:dev
```

You can pass parameters adding `-- PARAMETERS`. For example, to start the development server you can run `bazel run //backend:dev -- runserver 0.0.0.0:8000` and tu run the migrations you can use `bazel run //backend:dev -- migrate`.
