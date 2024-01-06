from pathlib import Path

from setuptools import find_packages, setup

working_dir = Path(__file__).parent.resolve()


def read_requirements(path):
    return Path(path).resolve().read_text().splitlines()


setup(
    author="bpl",
    install_requires=read_requirements(working_dir / "requirements.txt"),
    license="MIT",
    name="fastapi_vs_litestar",
    packages=find_packages(),
    test_suite="test",
    version="0.0.1",
)
