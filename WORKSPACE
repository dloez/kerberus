load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
http_archive(
    name = "rules_python",
    sha256 = "a644da969b6824cc87f8fe7b18101a8a6c57da5db39caa6566ec6109f37d2141",
    strip_prefix = "rules_python-0.20.0",
    url = "https://github.com/bazelbuild/rules_python/releases/download/0.20.0/rules_python-0.20.0.tar.gz",
)

http_archive(
    name = "rules_python_poetry",
    sha256 = "d6d1d09ffcfcec5eccd4c91d6cb85bfc3c2014f97ad9dc51843c0fe70575bcf8",
    strip_prefix = "rules_python_poetry-1fc695ec467e01e1be11e8feb1b6b7fda614ecb7",
    urls = ["https://github.com/AndrewGuenther/rules_python_poetry/archive/1fc695ec467e01e1be11e8feb1b6b7fda614ecb7.tar.gz"],
)

load("@rules_python//python:repositories.bzl", "py_repositories")
py_repositories()

load("@rules_python//python/pip_install:repositories.bzl", "pip_install_dependencies")
pip_install_dependencies()

load("@rules_python//python:repositories.bzl", "python_register_toolchains")
python_register_toolchains(
    name = "python311",
    python_version = "3.11",
)

load("@rules_python_poetry//rules_python_poetry:poetry.bzl", "poetry_lock")
poetry_lock(
    name = "requirements",
    lockfile = "//backend:poetry.lock",
)

load("@rules_python//python:pip.bzl", "pip_parse")
pip_parse(
    name = "backend_deps",
    requirements_lock = "@requirements//:requirements_lock.txt",
)

load("@backend_deps//:requirements.bzl", "install_deps")
install_deps()
