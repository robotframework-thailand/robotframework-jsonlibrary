import os
import sys
import shutil
from invoke import task


def _get_wheel_file() -> str:
    dist = "dist"
    assert len(os.listdir(dist)) > 0, "No files found in dist folder"
    wheel_file = os.path.join(dist, os.listdir(dist)[0])
    return wheel_file


@task
def clean(_):
    shutil.rmtree(
        os.path.join("tests", "__out__"),
        ignore_errors=True,
    )
    shutil.rmtree(".tox", ignore_errors=True)
    shutil.rmtree(".pytest_cache", ignore_errors=True)
    shutil.rmtree("build", ignore_errors=True)
    shutil.rmtree("dist", ignore_errors=True)
    shutil.rmtree("robotframework_jsonlibrary.egg-info", ignore_errors=True)
    for path, _, _ in os.walk("."):
        if path.endswith("__pycache__"):
            shutil.rmtree(path, ignore_errors=True)


@task(clean)
def build(ctx):
    ctx.run(f"{sys.executable} setup.py bdist_wheel", hide="both")
    wheel_file = _get_wheel_file()
    assert wheel_file.endswith(".whl")


@task
def uninstall(ctx):
    ctx.run(
        f"{sys.executable} -m pip uninstall robotframework-jsonlibrary -y", hide="both"
    )


@task(build, uninstall)
def install(ctx):
    wheel_file = _get_wheel_file()
    ctx.run(f"{sys.executable} -m pip install {wheel_file}", hide="both")


@task(install)
def test(ctx):
    ctx.run("tox -p")
    ctx.run("robot -d tests/__out__/robot acceptance")


@task
def style_check(ctx):
    ctx.run("black . --check --diff")


@task
def reformat_code(ctx):
    ctx.run("black .")


@task
def publish(ctx):
    ctx.run(f"{sys.executable} -m twine upload dist/*")


@task
def docs(ctx):
    ctx.run(f"{sys.executable} -m robot.libdoc JSONLibrary docs/JSONLibrary.html")


@task(install)
def lint(ctx):
    ctx.run("pylint JSONLibrary --disable=R,C,W0703,W0212,W1203")
    uninstall(ctx)
    clean(ctx)
