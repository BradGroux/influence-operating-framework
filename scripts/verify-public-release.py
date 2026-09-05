#!/usr/bin/env python3
"""Read back a published calendar edition; never creates or changes a release."""
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REPO = "BradGroux/influence-operating-framework"


def run(*args):
    return subprocess.check_output(args, cwd=ROOT, text=True).strip()


def require(condition, message):
    if not condition:
        raise SystemExit(message)


def main():
    require(len(sys.argv) == 2, "Usage: scripts/verify-public-release.py vYYYY.MM.DD[.N]")
    tag = sys.argv[1]
    require(tag == "v" + (ROOT / "VERSION").read_text().strip(), "Check out the exact release before verification")
    subprocess.run(["bash", "scripts/validate-release.sh", tag], cwd=ROOT, check=True)
    local_object = run("git", "rev-parse", tag)
    commit = run("git", "rev-parse", tag + "^{commit}")
    remote = dict((line.split()[1], line.split()[0]) for line in run("git", "ls-remote", "https://github.com/" + REPO + ".git", "refs/tags/" + tag, "refs/tags/" + tag + "^{}").splitlines())
    require(remote.get("refs/tags/" + tag) == local_object, "Remote tag object mismatch")
    require(remote.get("refs/tags/" + tag + "^{}") == commit, "Remote peeled commit mismatch")
    def api(path):
        return json.loads(run("gh", "api", "--hostname", "github.com", "repos/" + REPO + path))
    ref = api("/git/ref/tags/" + tag)
    require(ref["object"]["type"] == "tag" and ref["object"]["sha"] == local_object, "API annotated tag mismatch")
    obj = api("/git/tags/" + local_object)
    require(obj["object"]["sha"] == commit and obj["object"]["type"] == "commit", "API peeled commit mismatch")
    require(obj["verification"]["verified"], "GitHub signature verification failed")
    release = api("/releases/tags/" + tag)
    require(release["author"]["login"] == "BradGroux", "Release author mismatch")
    require(release.get("performed_via_github_app") is None, "Unexpected application attribution")
    require(not release["draft"] and not release["prerelease"] and release.get("immutable") is True, "Release must be final and immutable")
    require(release["tag_name"] == tag and release["name"] == "Influence Operating Framework " + tag, "Release identity mismatch")
    require(release["assets"] == [], "Unexpected release assets")
    released = tag[1:11].replace(".", "-")
    require(release["published_at"][:10] == released, "UTC publication date does not match edition")
    notes = ROOT / f"project/releases/{tag}-release-{released}.md"
    require(release["body"].replace("\r\n", "\n").rstrip("\n") == notes.read_text().rstrip("\n"), "Release body differs from committed notes")
    print(f"PASS: public signed immutable release {tag} at {commit}")
    print(release["html_url"])


if __name__ == "__main__":
    main()
