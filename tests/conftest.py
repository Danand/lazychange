import pytest

import os
import subprocess
import shutil

from typing import Generator, cast

from _pytest._py.path import LocalPath

@pytest.fixture(scope="function")
def dummy_git_repo(tmpdir: LocalPath) -> Generator[LocalPath, None, None]:
    origin_path = tmpdir.join(cast(os.PathLike[str], "dummy_origin"))

    os.makedirs(origin_path)

    subprocess.run(["git", "init", "--bare", origin_path], check=True)

    repo_path = tmpdir.join(cast(os.PathLike[str], "dummy_repo"))

    os.makedirs(repo_path)

    subprocess.run(["git", "init", repo_path], check=True)
    subprocess.run(["git", "-C", repo_path, "config", "user.name", "Jane Doe"], check=True)
    subprocess.run(["git", "-C", repo_path, "config", "user.email", "jane_doe@acme.com"], check=True)
    subprocess.run(["git", "-C", repo_path, "remote", "add", "origin", origin_path], check=True)
    subprocess.run(["git", "-C", repo_path, "commit", "--allow-empty", "-m", "Initial commit"], check=True)
    subprocess.run(["git", "-C", repo_path, "tag", "0.1.0"], check=True)
    subprocess.run(["git", "-C", repo_path, "push", "-u", "origin", "main"], check=True)
    subprocess.run(["git", "-C", repo_path, "push", "--tags"], check=True)

    yield repo_path

    shutil.rmtree(repo_path)
    shutil.rmtree(origin_path)
