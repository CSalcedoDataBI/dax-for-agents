# Thank You!! page

The first page of every report under `lab/`, and the one each opens on: who made this, and where to find more. It is the
same page `powerquery-m-for-agents` ships, kept here once and copied into each report by
[`../add_thank_you.py`](../add_thank_you.py) — edit a link here, then run:

```bash
python lab/add_thank_you.py
```

`--check` writes nothing and exits 1 if any report has drifted from this folder.

| Button | Goes to |
|---|---|
| Servicio de consultoría | https://csalcedodatabi.com/ |
| Archivos y plantillas | https://github.com/CSalcedoDataBI/PowerBI-Deneb |
| Blog | https://csalcedodatabi.com/blog/ |
| Canal de YouTube | https://www.youtube.com/@CSalcedoDataBI |
| Perfil de LinkedIn | https://www.linkedin.com/in/cristobal-salcedo |

The cover is a Deneb visual. It draws these same links and reads no data; each copy is bound
to a column and a measure of its own model only because Deneb renders nothing without fields.

## Not under the repository's MIT license

The three images embedded in the cover are **not** covered by this repository's license and
are not offered for reuse:

- the author's photograph;
- the Pesante Analytics LLC logo, which belongs to that company;
- the Microsoft Certified badge, a Microsoft trademark shown under Microsoft's terms for
  certified individuals.

If you reuse a report from this lab, delete this page or replace the cover with your own.
