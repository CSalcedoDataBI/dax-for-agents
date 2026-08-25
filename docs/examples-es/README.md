# The examples, as they were written in Spanish

This is a frozen copy of `skills/dax-reference/examples/` as it stood on 2026-08-25, the day the
tree was translated to English.

It is kept for one reason: the prose was written in Spanish first, and translating it is the only
step in the migration where meaning could have drifted without any gate noticing. The queries
could not drift — every ```dax and ```result block was hashed before the first edit and checked
after the last, and they are byte-identical here and there. The sentences around them are the
part a reader has to take on trust, and this is what they can check it against.

**It is not the live tree.** It lives outside `skills/` on purpose:

- The plugin ships `skills/`, so a copy inside it would double what an agent loads.
- `check_examples.py` counts covered functions by walking that tree; a copy there would report
  198 of 479 and the ratchet would be meaningless.
- `lab/check_lab.py examples` runs every example against a live model; a copy there would run
  each query twice.

So nothing reads this directory. It ages on the record, and the doc-claims gate is told as much.
If an example is corrected in the live tree, this copy is **not** updated to match — that is what
makes it a snapshot rather than a second copy to keep in step.

The live, maintained examples are in
[`skills/dax-reference/examples/`](../../skills/dax-reference/examples/). The reasoning behind
the language decision is in
[the decision record](../decisions/2026-08-25-english-as-the-repository-language.md).
