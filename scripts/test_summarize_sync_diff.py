#!/usr/bin/env python3
"""Tests for the sync diff summariser. Run: python -m unittest discover -s scripts"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from summarize_sync_diff import classify, render  # noqa: E402

OLD, NEW = "c6a9a72", "323524c"


def card(name, old=OLD, new=NEW, extra=""):
    """One card whose stamp moved, optionally with a real change beside it."""
    path = f"dax-reference/generated/library/{name}.md"
    return (f"diff --git a/{path} b/{path}\n"
            f"--- a/{path}\n+++ b/{path}\n"
            f"@@ -8 +8 @@\n"
            f"-source: query-languages/dax/{name}-function-dax.md@{old}\n"
            f"+source: query-languages/dax/{name}-function-dax.md@{new}\n"
            f"{extra}")


class StampOnly(unittest.TestCase):
    """516 ficheros, 517 lineas, cero cambios reales: eso fue la primera corrida."""

    def test_a_card_whose_only_change_is_the_stamp(self):
        substantive, stamp = classify(card("abs"), OLD, NEW)
        self.assertEqual(substantive, [])
        self.assertEqual(stamp, ["dax-reference/generated/library/abs.md"])

    def test_the_index_moves_its_commit_date_too(self):
        path = "dax-reference/generated/catalog.json"
        diff = (f"diff --git a/{path} b/{path}\n--- a/{path}\n+++ b/{path}\n@@ -2,2 +2,2 @@\n"
                f'-  "source": "MicrosoftDocs/query-docs@{OLD}",\n'
                f'-  "sourceCommitDate": "2026-08-04T22:03:23Z",\n'
                f'+  "source": "MicrosoftDocs/query-docs@{NEW}",\n'
                f'+  "sourceCommitDate": "2026-08-13T16:02:28Z",\n')
        substantive, stamp = classify(diff, OLD, NEW)
        self.assertEqual((substantive, stamp), ([], [path]))

    def test_the_catalog_carries_sha_and_date_on_the_same_line(self):
        # catalog.md pone el commit y la fecha juntos, sin la clave sourceCommitDate. Esa
        # linea solo se aplana por llevar el SHA, y sin esa mitad se reportaba como
        # cambio real cada semana.
        path = "dax-reference/generated/catalog.md"
        diff = (f"diff --git a/{path} b/{path}\n--- a/{path}\n+++ b/{path}\n@@ -3 +3 @@\n"
                f"-> Fuente: `MicrosoftDocs/query-docs@{OLD}` · commit 2026-08-04T22:03:23Z\n"
                f"+> Fuente: `MicrosoftDocs/query-docs@{NEW}` · commit 2026-08-13T16:02:28Z\n")
        substantive, stamp = classify(diff, OLD, NEW)
        self.assertEqual((substantive, stamp), ([], [path]))

    def test_many_stamped_cards_stay_out_of_the_way(self):
        diff = "".join(card(n) for n in ("abs", "acos", "asin", "atan"))
        substantive, stamp = classify(diff, OLD, NEW)
        self.assertEqual(substantive, [])
        self.assertEqual(len(stamp), 4)


class Substantive(unittest.TestCase):
    def test_a_real_content_change_is_reported(self):
        diff = card("dateadd", extra="@@ -20 +20 @@\n-Returns a table.\n"
                                     "+Returns a table of dates.\n")
        substantive, stamp = classify(diff, OLD, NEW)
        self.assertEqual(substantive, ["dax-reference/generated/library/dateadd.md"])
        self.assertEqual(stamp, [])

    def test_a_new_function_is_never_filed_as_noise(self):
        # Una funcion que aparece upstream es lo mas interesante que este pipeline puede
        # reportar. Su fichero nuevo trae una sola linea, y esa linea es el sello.
        path = "dax-reference/generated/library/newfunc.md"
        diff = (f"diff --git a/{path} b/{path}\nnew file mode 100644\n"
                f"--- /dev/null\n+++ b/{path}\n@@ -0,0 +1 @@\n"
                f"+source: query-languages/dax/newfunc-function-dax.md@{NEW}\n")
        substantive, stamp = classify(diff, OLD, NEW)
        self.assertEqual((substantive, stamp), ([path], []))

    def test_a_deleted_function_is_reported(self):
        path = "dax-reference/generated/library/gone.md"
        diff = (f"diff --git a/{path} b/{path}\ndeleted file mode 100644\n"
                f"--- a/{path}\n+++ /dev/null\n@@ -1 +0,0 @@\n"
                f"-source: query-languages/dax/gone-function-dax.md@{OLD}\n")
        substantive, stamp = classify(diff, OLD, NEW)
        self.assertEqual((substantive, stamp), ([path], []))

    def test_a_deleted_dax_comment_is_not_mistaken_for_a_file_header(self):
        # Un comentario DAX empieza por `--`, asi que borrado llega como `--- ...` y
        # saltarse las cabeceras por su texto se lo comia. Con el sello al lado, la
        # ficha pasaba como «nada que revisar».
        path = "dax-reference/generated/library/calculate.md"
        diff = (f"diff --git a/{path} b/{path}\n--- a/{path}\n+++ b/{path}\n"
                f"@@ -8 +8 @@\n"
                f"-source: query-languages/dax/calculate-function-dax.md@{OLD}\n"
                f"+source: query-languages/dax/calculate-function-dax.md@{NEW}\n"
                f"@@ -40 +40 @@\n"
                f"--- Suma las ventas del anio\n"
                f"+-- Suma las ventas del anio en curso\n")
        substantive, stamp = classify(diff, OLD, NEW)
        self.assertEqual((substantive, stamp), ([path], []))

    def test_a_hunk_that_only_deletes_dax_comments_is_a_change(self):
        # El caso que de verdad se escondia: si las cabeceras se saltan por su texto,
        # `--- comentario` desaparece de los dos lados y el hunk queda vacio. Vacio
        # contra vacio son iguales, asi que la ficha salia como sello y nadie miraba
        # que upstream habia borrado los comentarios del ejemplo.
        path = "dax-reference/generated/library/comments.md"
        diff = (f"diff --git a/{path} b/{path}\n--- a/{path}\n+++ b/{path}\n"
                f"@@ -40,2 +39,0 @@\n"
                f"--- Suma las ventas\n"
                f"--- y las devuelve\n")
        substantive, stamp = classify(diff, OLD, NEW)
        self.assertEqual((substantive, stamp), ([path], []))

    def test_text_moved_within_a_card_is_a_change(self):
        # Quitada arriba y puesta abajo: agrupando el fichero entero se cancelan y el
        # movimiento desaparece del informe. Hay que comparar hunk a hunk.
        path = "dax-reference/generated/library/moved.md"
        diff = (f"diff --git a/{path} b/{path}\n--- a/{path}\n+++ b/{path}\n"
                f"@@ -10 +9,0 @@\n-See also RELATED.\n"
                f"@@ -50,0 +50 @@\n+See also RELATED.\n")
        substantive, stamp = classify(diff, OLD, NEW)
        self.assertEqual((substantive, stamp), ([path], []))

    def test_a_pure_rename_is_a_change_not_noise(self):
        # Sin lineas +/- que comparar. «No comparamos nada» no es «no cambio nada»: si
        # upstream renombra una funcion, hay que mirarlo.
        old = "dax-reference/generated/library/oldname.md"
        new = "dax-reference/generated/library/newname.md"
        diff = (f"diff --git a/{old} b/{new}\nsimilarity index 100%\n"
                f"rename from {old}\nrename to {new}\n")
        substantive, stamp = classify(diff, OLD, NEW)
        self.assertEqual((substantive, stamp), ([new], []))

    def test_a_rename_with_the_stamp_move_beside_it_is_still_a_change(self):
        # El caso de verdad: el sello se mueve en TODOS los ficheros cada sync, asi que
        # un rename real nunca llega solo. Su hunk cuadra, y juzgando solo por hunks el
        # rename entero se archivaba como ruido y desaparecia del informe.
        old = "dax-reference/generated/library/oldname.md"
        new = "dax-reference/generated/library/newname.md"
        diff = (f"diff --git a/{old} b/{new}\nsimilarity index 98%\n"
                f"rename from {old}\nrename to {new}\n"
                f"--- a/{old}\n+++ b/{new}\n@@ -8 +8 @@\n"
                f"-source: query-languages/dax/oldname-function-dax.md@{OLD}\n"
                f"+source: query-languages/dax/oldname-function-dax.md@{NEW}\n")
        substantive, stamp = classify(diff, OLD, NEW)
        self.assertEqual((substantive, stamp), ([new], []))

    def test_a_rename_does_not_leak_onto_the_next_file(self):
        old = "dax-reference/generated/library/oldname.md"
        new = "dax-reference/generated/library/newname.md"
        diff = (f"diff --git a/{old} b/{new}\nrename from {old}\nrename to {new}\n"
                + card("abs"))
        substantive, stamp = classify(diff, OLD, NEW)
        self.assertEqual(substantive, [new])
        self.assertEqual(stamp, ["dax-reference/generated/library/abs.md"])

    def test_reordered_lines_are_a_change_not_noise(self):
        # Comparar como conjuntos diria que aqui no paso nada.
        path = "dax-reference/generated/library/swap.md"
        diff = (f"diff --git a/{path} b/{path}\n--- a/{path}\n+++ b/{path}\n@@ -1,2 +1,2 @@\n"
                f"-alpha\n-beta\n+beta\n+alpha\n")
        substantive, _ = classify(diff, OLD, NEW)
        self.assertEqual(substantive, [path])

    def test_the_full_sha_from_ls_remote_matches_the_short_one_in_the_card(self):
        # El workflow saca el SHA de `git ls-remote`: 40 caracteres. La ficha lleva los 7
        # de `rev-parse --short`. Comparandolos literalmente no coincidia ninguno y los
        # 516 ficheros de sello salian como cambios reales.
        full_new = "323524cfacf169fae6a370b5bf01fdcb4a8c9a1f"
        substantive, stamp = classify(card("abs"), OLD, full_new)
        self.assertEqual(substantive, [])
        self.assertEqual(len(stamp), 1)

    def test_a_short_sha_from_the_caller_matches_a_long_one_in_the_file(self):
        # La otra mitad de _same_commit, y no es hipotetica: correr el script a mano
        # pasando el sha corto es lo primero que se hace. Sin este test se podia borrar
        # `token.startswith(sha)` entero y todo seguia en verde.
        full = "323524cfacf169fae6a370b5bf01fdcb4a8c9a1f"
        substantive, stamp = classify(card("abs", old=OLD, new=full), OLD, NEW)
        self.assertEqual(substantive, [])
        self.assertEqual(len(stamp), 1)

    def test_a_full_old_sha_matches_too(self):
        full_old = "c6a9a72000000000000000000000000000000000"
        substantive, stamp = classify(card("abs"), full_old, NEW)
        self.assertEqual((substantive, len(stamp)), ([], 1))

    def test_a_date_in_the_prose_is_not_flattened(self):
        # Las funciones de fecha estan llenas de ejemplos con timestamps. Aplanar
        # cualquier fecha convertia un cambio real en «no cambio nada», que es la
        # direccion peligrosa: esconde lo que upstream hizo.
        path = "dax-reference/generated/library/datevalue.md"
        diff = (f"diff --git a/{path} b/{path}\n--- a/{path}\n+++ b/{path}\n@@ -30 +30 @@\n"
                f"-Returns 2026-08-04T22:03:23 for that input.\n"
                f"+Returns 2027-01-31T09:00:00 for that input.\n")
        substantive, stamp = classify(diff, OLD, NEW)
        self.assertEqual((substantive, stamp), ([path], []))

    def test_a_hex_word_that_is_not_either_commit_is_left_alone(self):
        # Aplanar todo lo que parezca hex escondería un cambio real.
        path = "dax-reference/generated/library/hex.md"
        diff = (f"diff --git a/{path} b/{path}\n--- a/{path}\n+++ b/{path}\n@@ -1 +1 @@\n"
                f"-The default is deadbeef1234567 here.\n"
                f"+The default is 0123456789abcdef here.\n")
        substantive, _ = classify(diff, OLD, NEW)
        self.assertEqual(substantive, [path])

    def test_without_the_shas_a_stamp_move_reads_as_a_change(self):
        # Sobre-reportar es el lado seguro: pide una lectura de mas, nunca una de menos.
        substantive, stamp = classify(card("abs"), "", "")
        self.assertEqual(len(substantive), 1)
        self.assertEqual(stamp, [])

    def test_a_mixed_diff_separates_the_two(self):
        diff = card("abs") + card("dateadd", extra="@@ -20 +20 @@\n-old\n+new\n") + card("acos")
        substantive, stamp = classify(diff, OLD, NEW)
        self.assertEqual(substantive, ["dax-reference/generated/library/dateadd.md"])
        self.assertEqual(len(stamp), 2)


class Body(unittest.TestCase):
    """El cuerpo del PR es la superficie de review. Si miente, el PR no sirve."""

    def test_a_stamp_only_run_says_there_is_nothing_to_read(self):
        body = render([], ["a.md", "b.md"], OLD, NEW)
        self.assertIn("Nothing changed except the stamp", body)
        self.assertIn("0 substantive", body)

    def test_a_substantive_run_names_the_functions(self):
        body = render(["dax-reference/generated/library/dateadd.md"], ["a.md"], OLD, NEW)
        self.assertIn("`dateadd`", body)
        self.assertIn("Read these", body)
        self.assertNotIn("Nothing changed", body)

    def test_a_concept_page_is_named_by_its_slug_too(self):
        body = render(["dax-reference/generated/concepts/dax-glossary.md"], [], OLD, NEW)
        self.assertIn("`dax-glossary`", body)

    def test_anything_outside_the_two_folders_keeps_its_path(self):
        body = render(["dax-reference/generated/catalog.json"], [], OLD, NEW)
        self.assertIn("`dax-reference/generated/catalog.json`", body)

    def test_a_long_list_is_cut_and_says_so(self):
        many = [f"dax-reference/generated/library/f{i}.md" for i in range(50)]
        body = render(many, [], OLD, NEW, limit=10)
        self.assertIn("and 40 more", body)

    def test_an_empty_diff_is_reported_as_suspicious_not_as_success(self):
        # Si el commit se movio y no cambio ni el sello, el sync no corrio. Se afirma el
        # mensaje entero: cambiar la primera frase por un «todo bien» dejaba pasar el
        # test porque la segunda seguia diciendo lo correcto.
        body = render([], [], OLD, NEW)
        self.assertIn("not even the stamp", body)
        self.assertIn("should be impossible", body)
        self.assertNotIn("substantive", body)


class TheRealDiff(unittest.TestCase):
    """La corrida real que motivo el script, congelada como fixture."""

    DIFF = "".join(card(n) for n in (f"fn{i}" for i in range(516)))

    def test_five_hundred_stamps_produce_no_reading(self):
        substantive, stamp = classify(self.DIFF, OLD, NEW)
        self.assertEqual(substantive, [])
        self.assertEqual(len(stamp), 516)
        self.assertIn("nothing to review", render(substantive, stamp, OLD, NEW))


if __name__ == "__main__":
    unittest.main()
