load("@backend_deps//:requirements.bzl", "requirement")

py_binary(
    name = "dev",
    main = "manage.py",
    srcs = glob(["**/*.py"]),
    imports = ["."],
    deps = [
        requirement("django"),
        requirement("djangorestframework")
    ],
)
