#!/usr/bin/env python3
"""Read-only AI candidate inventory. Paths are project-relative; file_type is
file/symlink/other. staged/worktree use porcelain column codes, '' means clean,
and null means unknown. Exit 0: complete; 1: limited/refused; 2: invalid arguments.
"""
import argparse
import json
import os
import re
import shutil
import stat
import subprocess

PROVIDERS = {".agents": "shared", **{"." + p: p for p in
             ("qoder", "codex", "cursor", "codebuddy", "trae")}}
SECTIONS = {"skills": "skill", "rules": "rule", "agents": "agent",
            "knowledge": "knowledge", "templates": "template"}
ENTRIES = {"AGENTS.md": ("shared", "entry"),
           "AGENTS.override.md": ("codex", "entry"),
           "AGENTS.local.md": ("unknown", "entry"),
           "CODEBUDDY.md": ("codebuddy", "entry"),
           "CLAUDE.md": ("unknown", "entry"),
           "AI-CODING.md": ("shared", "manual"),
           ".qoderignore": ("qoder", "native-config"),
           ".cursorignore": ("cursor", "native-config"),
           ".cursorindexingignore": ("cursor", "native-config"),
           ".codebuddyignore": ("codebuddy", "native-config"),
           ".traeignore": ("trae", "native-config")}
PRIVATE = {"key", "keys", "credential", "credentials", "secret", "secrets",
           "memory", "memories", "plan", "plans", "session", "sessions",
           "chat", "chats", "history", "log", "logs", "ssh", "aws", "gnupg",
           "token", "tokens", "password", "passwords", "netrc", "pypirc",
           "conversation", "conversations", "transcript", "transcripts"}
DIRECTORY_FLAGS = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)


def private(name):
    lower = name.lower()
    return (lower.startswith((".env", ".npmrc", "id_rsa", "id_dsa", "id_ecdsa", "id_ed25519"))
            or lower in {".git", ".hg", ".svn"}
            or bool(PRIVATE.intersection(re.split(r"[._\s-]+", lower)))
            or lower.endswith((".pem", ".key", ".p12", ".pfx")))


def open_project(project):
    """Validate every original component, including components preceding '..'."""
    absolute = project if os.path.isabs(project) else os.path.join(os.getcwd(), project)
    fd = os.open(os.path.sep, DIRECTORY_FLAGS)
    try:
        for component in absolute.split(os.path.sep):
            if component and component != ".":
                child = os.open(component, DIRECTORY_FLAGS, dir_fd=fd)
                os.close(fd)
                fd = child
        return os.path.abspath(absolute), fd
    except OSError:
        os.close(fd)
        raise


def inventory(project, max_depth=8, max_files=2000):
    result = {"project_path": os.path.abspath(project),
              "git": {"available": None, "root": None, "status": "not_checked",
                      "git_marker": None, "rename_detection": False},
              "assets": [], "warnings": [], "scan_complete": True}
    warnings = result["warnings"]
    warnings.extend([
        "Candidates only: presence does not establish activation or a host IDE.",
        "Scope: target root whitelist only; parent inheritance is not read, and nested projects are not discovered.",
        "Private/sensitive names and nested repositories are excluded; symlinks are never followed.",
        "Only existing filesystem candidates are inventoried, not deleted-only Git entries. Renames are reported as add/delete.",
        "Metadata snapshot, not an atomic snapshot against concurrent changes; Git may hash candidate files internally.",
    ])

    def incomplete(message):
        result["scan_complete"] = False
        if message not in warnings:
            warnings.append(message)

    if os.name != "posix" or not hasattr(os, "O_DIRECTORY") or not hasattr(os, "O_NOFOLLOW"):
        result["git"]["status"] = "unsupported_platform"
        incomplete("Safe directory-handle scanning unavailable; use host read-only file/Git tools. No scan performed.")
        return result

    try:
        project, root_fd = open_project(project)
        result["project_path"] = project
    except OSError:
        result["git"]["status"] = "unsafe_or_invalid_project"
        incomplete("Project refused: missing/inaccessible directory or symlink in the selected path/ancestors.")
        return result

    stopped = False
    gitlinks = set()
    can_descend = False

    def visit(parent_fd, name, path, provider, kind, depth, children=None, recursive=False):
        nonlocal stopped
        if stopped:
            return
        # Check the index boundary before even inspecting/opening this path:
        # an uninitialized or damaged submodule need not contain a .git marker.
        if path in gitlinks:
            warnings.append("Gitlink boundary not traversed: " + path)
            return
        try:
            info = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
        except FileNotFoundError:
            return
        except OSError:
            incomplete("Cannot lstat candidate: " + path)
            return
        if depth > max_depth:
            incomplete("max_depth reached; some candidates were not enumerated.")
            return
        if stat.S_ISDIR(info.st_mode):
            if not can_descend:
                incomplete("Directory not traversed: Gitlink boundaries unverified: " + path)
                return
            if children is None and not recursive:
                incomplete("Expected a file, found a directory (not traversed): " + path)
                return
            fd = None
            try:
                fd = os.open(name, DIRECTORY_FLAGS, dir_fd=parent_fd)
                current = os.fstat(fd)
                if (current.st_dev, current.st_ino) != (info.st_dev, info.st_ino):
                    incomplete("Directory changed during scan: " + path)
                    return
                try:
                    os.stat(".git", dir_fd=fd, follow_symlinks=False)
                except FileNotFoundError:
                    pass
                else:
                    warnings.append("Nested repository boundary not traversed: " + path)
                    return
                if children is not None:
                    for child, (child_kind, grandchildren, recurse) in children.items():
                        visit(fd, child, path + "/" + child, provider, child_kind,
                              depth + 1, grandchildren, recurse)
                else:
                    with os.scandir(fd) as entries:
                        for entry in entries:
                            if stopped:
                                break
                            if not private(entry.name):
                                visit(fd, entry.name, path + "/" + entry.name,
                                      provider, kind, depth + 1, recursive=True)
            except OSError:
                incomplete("Cannot safely enumerate directory: " + path)
            finally:
                if fd is not None:
                    os.close(fd)
            return
        if len(result["assets"]) >= max_files:
            stopped = True
            incomplete("max_files reached; some candidates were not enumerated.")
            return
        file_type = ("symlink" if stat.S_ISLNK(info.st_mode) else
                     "file" if stat.S_ISREG(info.st_mode) else "other")
        result["assets"].append({"path": path, "provider": provider, "kind": kind,
                                 "file_type": file_type, "staged": None,
                                 "worktree": None, "tracked": None, "ignored": None,
                                 "size": info.st_size, "mtime_ns": info.st_mtime_ns,
                                 "hardlink_count": info.st_nlink})
        if file_type != "file":
            warnings.append("Link/special file recorded only; Git state unknown: " + path)
        elif info.st_nlink > 1:
            warnings.append("Hardlink detected; other link locations are not inspected: " + path)

    try:
        try:
            marker = os.stat(".git", dir_fd=root_fd, follow_symlinks=False)
            result["git"]["git_marker"] = ("symlink" if stat.S_ISLNK(marker.st_mode)
                                             else "directory" if stat.S_ISDIR(marker.st_mode)
                                             else "file" if stat.S_ISREG(marker.st_mode) else "other")
            if result["git"]["git_marker"] == "file":
                warnings.append(".git file detected (linked worktree/submodule); marker contents are not read by this scanner.")
        except FileNotFoundError:
            result["git"]["git_marker"] = "absent"
        except OSError:
            incomplete("Cannot inspect .git marker metadata.")
        context = prepare_git(result, incomplete)
        can_descend = context is not None or result["git"]["status"] == "not_repository"
        if context is None and not can_descend:
            incomplete("Gitlink boundaries not verified; AI directories are not traversed.")
        elif context is not None:
            gitlinks = context[2]
        for name, (provider, kind) in ENTRIES.items():
            visit(root_fd, name, name, provider, kind, 1)
        for name, provider in PROVIDERS.items():
            children = {section: (kind, None, True) for section, kind in SECTIONS.items()}
            children["AI-CODING.md"] = ("manual", None, False)
            if provider != "shared":
                children["settings.json"] = ("native-config", None, False)
                children["config.toml"] = ("native-config", None, False)
            if provider == "qoder":
                children["repowiki"] = ("other", {"wiki_plan.yaml": ("native-config", None, False)}, False)
            visit(root_fd, name, name, provider, "other", 1, children)
        result["assets"].sort(key=lambda asset: asset["path"])
        if context is not None:
            git_inventory(result, incomplete, context)
    finally:
        os.close(root_fd)
    return result


def prepare_git(result, incomplete):
    """Prepare safe Git commands and verify index boundaries before traversal."""
    git = result["git"]
    executable = shutil.which("git")
    git["available"] = executable is not None
    if executable is None:
        git["status"] = "unavailable"
        incomplete("Git executable unavailable; filesystem candidates retained, Git fields unknown.")
        return
    if git["git_marker"] not in {"file", "directory", "absent"}:
        git["status"] = "unsafe_git_marker"
        incomplete("Git disabled: unsafe or unreadable .git marker.")
        return
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(GIT_OPTIONAL_LOCKS="0", GIT_CONFIG_NOSYSTEM="1",
               GIT_CONFIG_GLOBAL=os.devnull, GIT_TERMINAL_PROMPT="0", LC_ALL="C")
    result["warnings"].append("Git system/global configuration is disabled; global ignore rules are not evaluated.")
    command = [executable, "--no-optional-locks", "-c", "core.fsmonitor=false",
               "-c", "core.untrackedCache=false", "-c", "core.hooksPath=" + os.devnull,
               "-c", "diff.external=", "-C", result["project_path"]]

    def run(args, check=True, input=None):
        return subprocess.run(command + args, env=env, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, timeout=10, check=check, input=input)

    try:
        ancestor = result["project_path"]
        while True:
            try:
                marker = os.lstat(os.path.join(ancestor, ".git"))
                if not (stat.S_ISREG(marker.st_mode) or stat.S_ISDIR(marker.st_mode)):
                    raise ValueError("unsafe ancestor Git marker")
                break
            except FileNotFoundError:
                parent = os.path.dirname(ancestor)
                if parent == ancestor:
                    break
                ancestor = parent
        raw_root = run(["rev-parse", "--show-toplevel"]).stdout
        root = os.fsdecode(raw_root[:-1] if raw_root.endswith(b"\n") else raw_root)
        if not os.path.isabs(root) or os.path.commonpath([root, result["project_path"]]) != root:
            raise ValueError("unexpected Git root")
        _, fd = open_project(root)
        try:
            # Also refuse an ancestor repository's symlinked .git marker.
            marker = os.stat(".git", dir_fd=fd, follow_symlinks=False)
            if not (stat.S_ISREG(marker.st_mode) or stat.S_ISDIR(marker.st_mode)):
                raise ValueError("unsafe Git marker")
        finally:
            os.close(fd)
        git["root"] = root
        # status can invoke clean/process filters while hashing. Read key names
        # (never values), then disable every configured filter and diff driver.
        pattern = r"^(filter\..*\.(clean|smudge|process|required)|diff\..*\.(command|textconv))$"
        drivers = run(["config", "--null", "--name-only", "--get-regexp", pattern], check=False)
        if drivers.returncode not in (0, 1):
            raise subprocess.CalledProcessError(drivers.returncode, "config", stderr=drivers.stderr)
        filter_drivers = set()
        for raw in drivers.stdout.split(b"\0"):
            if raw:
                key = raw.decode("ascii")
                if not re.fullmatch(r"[A-Za-z0-9_.-]+", key) or not re.fullmatch(pattern, key):
                    raise ValueError("unsafe driver key")
                if key.startswith("filter.") and key.endswith((".clean", ".process")):
                    filter_drivers.add(key[7:].rsplit(".", 1)[0].encode("ascii"))
                command.extend(["-c", key + ("=false" if key.endswith(".required") else "=")])
        # Broad whitelist paths are used ONLY for index metadata, never status
        # or hashing. This must finish before visit can enter any AI directory.
        paths = [":(literal)" + name for name in (*ENTRIES, *PROVIDERS)]
        indexed = run(["ls-files", "--cached", "--stage", "-z", "--", *paths]).stdout
        if indexed and not indexed.endswith(b"\0"):
            raise ValueError("truncated boundary index output")
        gitlinks = set()
        for record in indexed.split(b"\0"):
            if record:
                metadata, path = record.split(b"\t", 1)
                mode, object_id, stage = metadata.split()
                if (mode not in {b"100644", b"100755", b"120000", b"160000"}
                        or stage not in {b"0", b"1", b"2", b"3"} or not path):
                    raise ValueError("malformed boundary index record")
                if mode == b"160000":
                    gitlinks.add(os.fsdecode(path))
        prefix = os.path.relpath(result["project_path"], root)
        prefix = "" if prefix == "." else prefix + "/"
        return run, prefix, gitlinks, filter_drivers
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, OSError, ValueError) as error:
        git_failure(result, incomplete, error)


def git_inventory(result, incomplete, context):
    git = result["git"]
    run, prefix, _, filter_drivers = context
    limited = False
    try:
        assets = [a for a in result["assets"] if a["file_type"] == "file"]
        for offset in range(0, len(assets), 64):
            batch = assets[offset:offset + 64]
            # Both commands use literal, existing file paths, never broad AI roots.
            paths = [":(literal)" + a["path"] for a in batch]
            indexed = run(["ls-files", "--stage", "-z", "--", *paths]).stdout
            status = run(["status", "--porcelain=v1", "-z", "--no-renames",
                          "--untracked-files=all", "--ignored=matching",
                          "--ignore-submodules=all", "--", *paths]).stdout
            tracked = set()
            for record in indexed.split(b"\0"):
                if record:
                    metadata, path = record.split(b"\t", 1)
                    if len(metadata.split()) != 3:
                        raise ValueError("malformed index record")
                    tracked.add(os.fsdecode(path))  # ls-files paths are relative to -C.
            states = {}
            for record in status.split(b"\0"):
                if not record:
                    continue
                if len(record) < 4 or record[2:3] != b" " or b"R" in record[:2] or b"C" in record[:2]:
                    raise ValueError("malformed porcelain record")
                state = states.setdefault(os.fsdecode(record[3:]), ["", "", False])
                x, y = record[:2].decode("ascii")
                if x not in " ?!":
                    state[0] = x
                if y != " ":
                    state[1] = y
                state[2] = state[2] or x == "!"
            ignored_dirs = [p for p, state in states.items() if p.endswith("/") and state[2]]
            worktree = {}
            for asset in batch:
                path = prefix + asset["path"]
                x, y, ignored = states.get(path, ["", "", False])
                is_tracked = asset["path"] in tracked
                if not is_tracked and any(path.startswith(p) for p in ignored_dirs):
                    ignored, y = True, "!"  # matching mode may collapse an ignored directory.
                # Preserve index/ignore metadata even if the attribute query fails.
                # A tracked worktree comparison is unknown until filters are checked.
                asset.update(tracked=is_tracked, ignored=ignored, staged=x,
                             worktree=None if is_tracked else y)
                if is_tracked:
                    worktree[asset["path"]] = y
            if worktree:
                # check-attr resolves effective attributes without executing drivers
                # or reading candidate bodies. NUL input preserves literal filenames.
                raw = run(["check-attr", "-z", "--stdin", "filter"],
                          input=b"".join(os.fsencode(p) + b"\0" for p in worktree)).stdout
                fields = raw.split(b"\0")
                if fields[-1] != b"" or (len(fields) - 1) % 3:
                    raise ValueError("malformed filter attributes")
                attributes = {}
                for offset in range(0, len(fields) - 1, 3):
                    path, attribute, value = fields[offset:offset + 3]
                    path = os.fsdecode(path)
                    if attribute != b"filter" or path not in worktree or path in attributes:
                        raise ValueError("unexpected filter attribute")
                    attributes[path] = value
                if attributes.keys() != worktree.keys():
                    raise ValueError("missing filter attributes")
                for asset in batch:
                    path = asset["path"]
                    if path not in worktree:
                        continue
                    # check-attr uses the same spelling for sentinel values and
                    # literal driver names "unset"/"unspecified"; be conservative
                    # when a configured conversion driver makes these ambiguous.
                    if (attributes[path] not in {b"unspecified", b"unset"}
                            or attributes[path] in filter_drivers):
                        limited = True
                        incomplete("Filter attribute may require disabled/unverified conversion; worktree state unknown: " + path)
                    else:
                        asset["worktree"] = worktree[path]
        git["status"] = "limited" if limited else "ok"
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, OSError, ValueError) as error:
        git_failure(result, incomplete, error)


def git_failure(result, incomplete, error):
    git = result["git"]
    if isinstance(error, subprocess.TimeoutExpired):
        git["status"] = "timeout"
        incomplete("Git command timed out; unprocessed Git fields remain unknown.")
    elif isinstance(error, subprocess.CalledProcessError):
        git["status"] = ("not_repository" if b"not a git repository" in (error.stderr or b"")
                         else "error")
        incomplete("Git " + git["status"] + "; filesystem candidates retained. Git stderr is suppressed to avoid sensitive output.")
    else:
        git["status"] = "error"
        incomplete("Git execution, repository boundary, or output validation failed; unprocessed Git fields remain unknown.")


def nonnegative(value):
    number = int(value)
    if number < 0:
        raise argparse.ArgumentTypeError("must be nonnegative")
    return number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project")
    parser.add_argument("--max-depth", type=nonnegative, default=8,
                        help="maximum project-relative component depth (default: 8)")
    parser.add_argument("--max-files", type=nonnegative, default=2000,
                        help="maximum candidate records (default: 2000)")
    args = parser.parse_args()
    result = inventory(args.project, args.max_depth, args.max_files)
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0 if result["scan_complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
