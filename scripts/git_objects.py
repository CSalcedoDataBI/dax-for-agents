#!/usr/bin/env python3
"""Read a repository's whole history as text, once per distinct piece of content.

Two guards need this — the client-name one and the credential one — and both need it for
the same reason: publishing a repository publishes every commit, so the working tree says
nothing about what a `git log -p` would hand a stranger. This module is the shared part,
so that "what counts as text" and "how we walk the object graph" are answered once.
"""
import subprocess
import threading


def reachable_blobs(root):
    """Return [(sha, path)] for every blob any ref can reach, newest first.

    Deduplication is free here and that is the whole reason to walk objects instead of
    revisions: `git grep` over `git rev-list --all` re-reads the same unchanged file in
    every commit that carries it — measured on this repo, 1.055 lines of report for what
    is really nine. `rev-list --objects` visits each object once, so identical content
    committed forty times is one entry, under the path of the newest commit holding it.
    """
    p = subprocess.run(["git", "-C", root, "rev-list", "--objects", "--all"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        raise RuntimeError(f"git rev-list failed in {root}: {p.stderr.strip()}")
    out = []
    for line in p.stdout.splitlines():
        sha, _, path = line.partition(" ")
        if not path:                      # no path: a commit, not a blob or tree
            continue
        out.append((sha, path))
    return out


def historical_paths(root):
    """Return every path any commit ever recorded, sorted.

    Not derivable from the blob listing: renaming a file without touching its bytes
    reuses the same blob, and `rev-list --objects` reports it under a single path — the
    newest one. So a file renamed away from a client name looks clean there while
    `git log --stat` still prints the old name. `--name-only` prints both sides of a
    rename and covers the first commit as well; both were measured, neither needs the
    `--no-renames` or `--root` flag that the patch equivalents would. `-z` keeps git
    from octal-quoting non-ASCII paths.
    """
    p = subprocess.run(["git", "-C", root, "log", "--all",
                        "--name-only", "-z", "--format="],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        raise RuntimeError(f"git log failed in {root}: {p.stderr.strip()}")
    return sorted({s for s in p.stdout.split("\0") if s})


def read_objects(root, shas):
    """Yield (sha, kind, data) from one `git cat-file --batch`.

    One process for thousands of objects instead of one process each — on Windows the
    difference is a minute. The writer runs on its own thread because feeding every sha
    before reading any answer deadlocks as soon as git fills the output pipe.
    """
    proc = subprocess.Popen(["git", "-C", root, "cat-file", "--batch"],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def feed():
        try:
            for sha in shas:
                proc.stdin.write(sha.encode("ascii") + b"\n")
            proc.stdin.close()
        except OSError:
            pass                          # git died early; the reader reports the EOF

    writer = threading.Thread(target=feed, daemon=True)
    writer.start()
    try:
        for _ in shas:
            header = proc.stdout.readline()
            if not header:
                break
            parts = header.split()
            if len(parts) != 3:           # "<sha> missing"
                continue
            sha, kind, size = parts[0].decode(), parts[1].decode(), int(parts[2])
            data, left = b"", size
            while left > 0:               # a pipe read can come up short
                chunk = proc.stdout.read(left)
                if not chunk:
                    break
                data += chunk
                left -= len(chunk)
            proc.stdout.read(1)           # the newline git appends after the payload
            yield sha, kind, data
    finally:
        writer.join(timeout=5)
        proc.stdout.close()
        proc.wait(timeout=30)


def blob_texts(root, skip=frozenset()):
    """Yield (sha, path, text) for every readable-as-text blob in the repository.

    `skip` holds repo-relative paths in posix form. Binary is defined the way `git grep -I`
    defines it — a NUL byte anywhere — plus anything that is not valid UTF-8. The NUL rule
    is not redundant with the decode: \\x00 is perfectly valid UTF-8, so a .pbix that
    happens to decode would otherwise be scanned and produce noise.
    """
    blobs = [(sha, path) for sha, path in reachable_blobs(root) if path not in skip]
    by_sha = dict(blobs)
    for sha, kind, data in read_objects(root, [sha for sha, _ in blobs]):
        if kind != "blob" or b"\0" in data:
            continue
        try:
            yield sha, by_sha[sha], data.decode("utf-8")
        except UnicodeDecodeError:
            continue


def commit_messages(root):
    """Yield (sha, message) for every commit reachable from any reference.

    `--history` walks blobs and paths, which is what a leaked *file* needs. A commit
    MESSAGE is neither: it is not a blob and it has no path, so it was invisible to both
    of them. The gap matters most on the route this repository actually chose — publishing
    from a fresh initial commit — because that commit's message is typed by hand AFTER the
    tree has been generated and checked, and nothing was looking at it.

    The separators travel as git's own `%x00` escape and are never literal NULs in the
    argument list: Windows refuses a command-line argument containing a NUL byte, so
    building the marker in Python fails before git ever runs.
    """
    nul = chr(0)
    sep = nul * 3
    p = subprocess.run(
        ["git", "-C", root, "log", "--all", "--no-color",
         "--format=%H%x00%B%x00%x00%x00"],
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        raise RuntimeError(f"git log failed in {root}: {p.stderr.strip()}")
    for chunk in p.stdout.split(sep):
        chunk = chunk.strip("\n")
        if not chunk:
            continue
        sha, _, body = chunk.partition(nul)
        if sha.strip():
            yield sha.strip(), body


def commit_identities(root):
    """Yield (sha, "Author: Name <email>") and the committer line, per commit.

    The third piece of publishable text that is neither a blob nor a path. It is the one
    nobody thinks of because git writes it instead of a person — and on this machine an
    `includeIf` rule swaps the identity per directory, so a commit can carry a business
    name without anyone having typed it.

    Not hypothetical: this repository already holds commits authored by a client-facing
    identity, found only when a review asked whether `%B` was really everything that gets
    published. On the chosen route it matters twice over, because whoever types the public
    repository's first commit does so with whatever identity happens to be active.
    """
    p = subprocess.run(
        ["git", "-C", root, "log", "--all", "--no-color",
         "--format=%H%x09%an <%ae>%x09%cn <%ce>"],
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        raise RuntimeError(f"git log failed in {root}: {p.stderr.strip()}")
    for line in p.stdout.splitlines():
        parts = line.split("\t")
        if len(parts) != 3:
            continue
        sha, author, committer = parts
        yield sha.strip(), f"Autor: {author}"
        if committer != author:
            yield sha.strip(), f"Commiteado por: {committer}"


def ref_texts(root):
    """Yield (ref, text) for every ref NAME and every annotated tag's own payload.

    The fifth publishable surface, and the last one two independent reviews could name.
    A branch called `fix/<cliente>-algo` is rendered in GitHub's branch list and travels
    in `git push --all`; an annotated tag is a real object with its own message and its
    own tagger identity, none of which is a commit and none of which the other four scans
    reach.

    Only local refs are read (`refs/heads`, `refs/tags`): `refs/remotes` names belong to
    whoever you cloned from, not to what you are about to publish, and flagging them would
    make the guard red for reasons the person running it cannot fix.

    The records are terminated with a NUL, not a newline: an annotated tag body is free
    text and contains newlines constantly, so splitting the output on "\n" reads every line
    after the first as a malformed record and drops it. That is a false green on the exact
    surface this function was added to cover — measured with a two-line tag whose second
    line held a client name and passed clean.
    """
    fin = chr(0)
    fmt = ("%(refname)%09%(objecttype)%09%(taggername) %(taggeremail)%09%(contents)%00")
    p = subprocess.run(
        ["git", "-C", root, "for-each-ref", "refs/heads", "refs/tags", "--format", fmt],
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        raise RuntimeError(f"git for-each-ref failed in {root}: {p.stderr.strip()}")
    for bloque in p.stdout.split(fin):
        bloque = bloque.strip("\n")
        if not bloque.strip():
            continue
        partes = bloque.split("\t", 3)
        if len(partes) < 2:
            continue
        refname, objecttype = partes[0], partes[1]
        yield refname, refname
        if objecttype == "tag":
            tagger = partes[2] if len(partes) > 2 else ""
            if tagger.strip(" <>"):
                yield refname, f"Etiquetado por: {tagger}"
            cuerpo = partes[3] if len(partes) > 3 else ""
            if cuerpo.strip():
                yield refname, cuerpo
