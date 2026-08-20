#!/usr/bin/env python3
"""Tests for the doc-claim gate. Run: python -m unittest discover -s scripts"""
import io
import os
import sys
import json
import shutil
import contextlib
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from check_doc_claims import (  # noqa: E402
    check, claims_in, main, stale_stamps, unlisted_documents,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Fixture:
    """A throwaway repo with 2 cards, 1 concept, 3 notes and 1 skill."""

    def __init__(self, doc=""):
        self.dir = tempfile.mkdtemp()
        gen = os.path.join(self.dir, "dax-reference", "generated")
        for sub, names in [(os.path.join(gen, "library"), ["abs.md", "acos.md"]),
                           (os.path.join(gen, "concepts"), ["dax-glossary.md"]),
                           (os.path.join(self.dir, "dax-reference", "notes"),
                            ["abs.md", "acos.md", "sumx.md"])]:
            os.makedirs(sub)
            for n in names:
                open(os.path.join(sub, n), "w", encoding="utf-8").close()
        os.makedirs(os.path.join(self.dir, "una-skill"))
        open(os.path.join(self.dir, "una-skill", "SKILL.md"), "w", encoding="utf-8").close()
        with open(os.path.join(self.dir, "DOC.md"), "w", encoding="utf-8") as f:
            f.write(doc)

    def check(self):
        return check(root=self.dir, docs=["DOC.md"])

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        shutil.rmtree(self.dir, ignore_errors=True)


class Agreeing(unittest.TestCase):
    def test_the_right_numbers_pass(self):
        with Fixture("Tiene 2 fichas, 1 concepts, 3 field notes y 1 skill.") as f:
            self.assertEqual(f.check(), [])

    def test_a_document_with_no_numbers_passes(self):
        with Fixture("Nada que contar aqui.") as f:
            self.assertEqual(f.check(), [])


class Disagreeing(unittest.TestCase):
    """El fallo real: la cifra se queda quieta mientras el arbol crece."""

    def test_a_stale_card_count_fails(self):
        with Fixture("Tiene 479 functions.") as f:
            errors = f.check()
        self.assertEqual(len(errors), 1)
        self.assertIn("479 functions", errors[0])
        self.assertIn("2 cards", errors[0])

    def test_a_stale_note_count_fails(self):
        # Exactamente lo que paso: SKILL.md decia 18 mientras notes/ tenia 19.
        with Fixture("Hay 18 field notes.") as f:
            self.assertEqual(len(f.check()), 1)

    def test_the_bare_noun_counts_too(self):
        # El primer fallo vivo que encontro este gate fue "The 18 notes already here" en
        # CONTRIBUTING.md, invisible mientras solo estaban las formas con adjetivo.
        with Fixture("The 18 notes already here carry their query.") as f:
            errors = f.check()
        self.assertEqual(len(errors), 1)
        self.assertIn("3 notes", errors[0])
        with Fixture("Las primeras 18 notas fueron medidas.") as f:
            self.assertEqual(len(f.check()), 1)

    def test_spanish_and_english_are_both_checked(self):
        with Fixture("479 fichas y 61 conceptual pages.") as f:
            self.assertEqual(len(f.check()), 2)

    def test_funciones_counts_as_cards(self):
        # docs/REVIEW.md dice "Son 479 funciones" y el gate no lo veia: 'fichas' estaba
        # en la lista y 'funciones' no. Quitarla no hacia fallar nada porque la cifra era
        # correcta — una afirmacion sin comprobar que parecia comprobada.
        self.assertEqual([(q, n) for q, n, _ in claims_in("Son 479 funciones.")],
                         [("cards", 479)])
        with Fixture("Son 479 funciones.") as f:
            errors = f.check()
        self.assertEqual(len(errors), 1)
        self.assertIn("2 cards", errors[0])

    def test_a_thousands_separator_is_one_number(self):
        # Sobre el numero leido, no sobre el error: '1.234' truncado a '1' tampoco es 2,
        # asi que el fallo seguia saliendo y el test pasaba con el separador roto.
        self.assertEqual([n for _, n, _ in claims_in("Tiene 1.234 fichas.")], [1234])
        self.assertEqual([n for _, n, _ in claims_in("It has 1,234 functions.")], [1234])
        with Fixture("Tiene 1.234 fichas.") as f:
            self.assertEqual(len(f.check()), 1)


class MoreThanTheLibrarySize(unittest.TestCase):
    """El paquete de revision afirma mas que fichas y notas, y todo eso se pudre igual."""

    def test_workflows_scenarios_terms_tests_and_plugins_are_counted(self):
        for phrase, quantity in [("6 workflows", "workflows"),
                                 ("2 lab scenarios", "scenarios"),
                                 ("11 forbidden terms", "terms"),
                                 ("383 tests", "tests"),
                                 ("1 plugin", "plugins")]:
            self.assertEqual([q for q, _, _ in claims_in(phrase)], [quantity], phrase)

    def test_every_counted_quantity_has_a_noun_and_the_other_way_round(self):
        # Sin esto, anadir una cantidad a _counts y olvidar su sustantivo la deja sin
        # comprobar para siempre, que es como '1 plugin' paso desapercibido. Y un
        # sustantivo sin cantidad reventaria al comparar.
        from check_doc_claims import NOUNS, _counts
        self.assertEqual(sorted(NOUNS), sorted(_counts(ROOT)))

    def test_the_nouns_are_valid_word_bounded_patterns(self):
        # Un heredoc convirtio '\\b' en un backspace literal aqui, y el patron seguia
        # compilando: 'plugins?\x08' no casaba con nada y el gate decia OK.
        import re as _re
        from check_doc_claims import NOUNS
        for quantity, patterns in NOUNS.items():
            for pattern in patterns:
                self.assertNotIn("\x08", pattern, f"{quantity}: backspace, not \\b")
                _re.compile(pattern)

    def test_a_multi_word_noun_survives_a_line_break(self):
        # REVIEW.md escribe "11 términos\n   prohibidos" partido. Con el espacio literal
        # del patron, esa afirmacion era invisible mientras la misma frase en una linea si
        # casaba — el peor tipo de cobertura, la que depende de donde cae el margen.
        self.assertEqual([n for _, n, _ in claims_in("sobre 11 términos\n   prohibidos y")],
                         [11])
        self.assertEqual([n for _, n, _ in claims_in("las 30 field\nnotes de aqui")], [30])

    def test_the_reported_phrase_is_readable_after_a_wrap(self):
        self.assertEqual([p for _, _, p in claims_in("11 términos\n   prohibidos")],
                         ["11 términos prohibidos"])


class NumbersWrittenAsWords(unittest.TestCase):
    """«The four skills sit flat…» y «Cuatro skills, una sola idea» tambien son cifras."""

    def test_a_word_number_that_agrees_passes(self):
        with Fixture("The two cards and the three field notes.") as f:
            self.assertEqual(f.check(), [])

    def test_a_stale_word_number_fails(self):
        with Fixture("The four skills sit flat at the repo root.") as f:
            errors = f.check()
        self.assertEqual(len(errors), 1)
        self.assertIn("1 skills", errors[0])

    def test_spanish_word_numbers_too(self):
        with Fixture("Cuatro skills, una sola idea.") as f:
            self.assertEqual(len(f.check()), 1)

    def test_the_indefinite_article_is_not_the_number_one(self):
        # El motivo de empezar en DOS. En espanol 'una' va pegada a estos sustantivos
        # constantemente sin contar nada, y leerla como 1 seria alarma falsa sobre prosa
        # correcta. Las tres frases son reales, de INDEX.md y lab/README.md.
        #
        # Se afirma sobre claims_in, no sobre check(): el fixture tiene 1 skill, asi que
        # leer 'una skill' como 1 COINCIDIRIA con el arbol y check() seguiria devolviendo
        # []. El test pasaba con el fallo reintroducido.
        for prosa in ("**Una skill = una carpeta** con `SKILL.md`.",
                      "una nota sin demostrar no se escribe",
                      "sospecha de una nota"):
            self.assertEqual(claims_in(prosa), [], prosa)

    def test_one_in_english_is_not_counted_either(self):
        self.assertEqual(claims_in("one skill per folder"), [])


class NotAClaim(unittest.TestCase):
    """Un comprobador que grita sobre prosa correcta se acaba apagando."""

    def test_someone_elses_repository_is_not_a_claim_about_this_one(self):
        # README.md dice "191 Azure skills" de MicrosoftDocs/Agent-Skills. Con palabras
        # permitidas entre el numero y el sustantivo, esto fallaba.
        self.assertEqual(claims_in("MicrosoftDocs/Agent-Skills tiene 191 Azure skills."), [])

    def test_an_ordered_list_marker_is_not_a_count(self):
        # Igual que el articulo: '1. **Una skill**' y '2. Find the function' darian 1 skill
        # y 2 cards, que son exactamente los conteos del fixture, asi que check() no notaba
        # nada. Solo claims_in distingue "no es una cifra" de "la cifra coincide".
        self.assertEqual(
            claims_in("1. **Una skill** por carpeta.\n2. Find the function.\n"), [])

    def test_the_noun_must_follow_the_number(self):
        self.assertEqual(claims_in("skills: 4 en total"), [])


class Wiring(unittest.TestCase):
    def test_a_missing_document_is_reported(self):
        with Fixture("") as f:
            errors = check(root=f.dir, docs=["NO-EXISTE.md"])
        self.assertEqual(len(errors), 1)
        self.assertIn("is missing", errors[0])

    def test_an_empty_tree_is_refused_rather_than_passing_everything(self):
        # Sin nada contado, cualquier cifra "coincidiria" con cero y el gate diria OK
        # sobre un repo vacio.
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "DOC.md"), "w", encoding="utf-8") as f:
                f.write("479 functions")
            errors = check(root=d, docs=["DOC.md"])
        self.assertEqual(len(errors), 1)
        self.assertIn("nothing was counted", errors[0])

    def test_documents_that_state_nothing_at_all_are_refused(self):
        # Arbol contado, documentos leidos, y ni una cifra entre todos. Eso es prosa que
        # perdio sus numeros o patrones que dejaron de encontrarlos, y desde aqui las dos
        # se ven igual: una corrida verde que no comparo nada.
        from check_doc_claims import DOCS
        with Fixture("") as f:
            for rel in DOCS:
                path = os.path.join(f.dir, rel)
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write("Prosa sin una sola cifra.\n")
            errors = check(root=f.dir)
        self.assertEqual(len(errors), 1)
        self.assertIn("nothing was compared", errors[0])

    def test_main_prints_the_counts_it_compared(self):
        # main() reads the real DOCS list, so the fixture needs those five paths to exist;
        # only one of them says anything.
        from check_doc_claims import DOCS
        with Fixture("") as f:
            for rel in DOCS:
                path = os.path.join(f.dir, rel)
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write("2 fichas\n" if rel == "README.md" else "")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = main(f.dir)
        self.assertEqual(code, 0, out.getvalue())
        self.assertIn("2 cards", out.getvalue())


class TheUpstreamStamp(unittest.TestCase):
    """El sync reescribe el sello de cada ficha y no toca la prosa. Paso de verdad al
    mergear la primera PR de sync: dos ficheros se quedaron nombrando el commit viejo."""

    def _fixture(self, stamped, prose):
        f = Fixture("")
        gen = os.path.join(f.dir, "dax-reference", "generated")
        with open(os.path.join(gen, "catalog.json"), "w", encoding="utf-8") as fh:
            json.dump({"source": f"MicrosoftDocs/query-docs@{stamped}"}, fh)
        with open(os.path.join(f.dir, "DOC.md"), "w", encoding="utf-8") as fh:
            fh.write(prose)
        return f

    def assertAccepts(self, stamped, prose, sha):
        """La prosa nombra `sha`, se ve, y no esta desfasada.

        Las dos mitades, siempre. Afirmar solo que no hay error es la trampa que se repitio
        cuatro veces en esta rama: un comprobador que no mira devuelve exactamente lo mismo
        que uno que mira y no encuentra nada malo. Un test negativo sobre algo que puede
        dejar de mirar tiene que decir primero que miro.
        """
        from check_doc_claims import _STAMP_IN_PROSE
        self.assertEqual(_STAMP_IN_PROSE.findall(prose), [sha],
                         f"el sello {sha} ni siquiera se ve en la prosa")
        with self._fixture(stamped, prose) as f:
            self.assertEqual(stale_stamps(f.dir, ["DOC.md"]), [])

    def test_prose_naming_the_stamped_commit_passes(self):
        self.assertAccepts("323524c",
                           "Derivado de `MicrosoftDocs/query-docs@323524c`.", "323524c")

    def test_prose_naming_an_older_commit_fails(self):
        with self._fixture("323524c", "Derivado de `MicrosoftDocs/query-docs@c6a9a72`.") as f:
            errors = stale_stamps(f.dir, ["DOC.md"])
        self.assertEqual(len(errors), 1)
        self.assertIn("c6a9a72", errors[0])
        self.assertIn("323524c", errors[0])

    def test_a_long_sha_matches_the_short_stamp(self):
        # `ls-remote` da 40 caracteres y la ficha lleva 7. Es el mismo commit. Con el
        # patron recortado a {7} solo leeria los 7 primeros, que coinciden con el sello:
        # assertAccepts lo caza porque exige la captura entera.
        largo = "323524cfacf169fae6a370b5bf01fdcb4a8c9a1f"
        self.assertAccepts("323524c", f"de `MicrosoftDocs/query-docs@{largo}`", largo)

    def test_prose_with_no_stamp_says_nothing(self):
        with self._fixture("323524c", "Sin sellos aqui.") as f:
            self.assertEqual(stale_stamps(f.dir, ["DOC.md"]), [])

    def test_check_reports_it_too(self):
        # Los demas tests llaman a stale_stamps directamente, asi que desconectarlo de
        # check() no hacia fallar nada: la comprobacion existia y no la corria nadie.
        with self._fixture("323524c", "de `MicrosoftDocs/query-docs@c6a9a72`.") as f:
            errors = check(root=f.dir, docs=["DOC.md"])
        self.assertEqual(len(errors), 1)
        self.assertIn("c6a9a72", errors[0])

    def test_an_unreadable_catalog_is_reported_rather_than_passing(self):
        # Devolver [] ahi dice "ningun sello desfasado" cuando la verdad es "no se pudo
        # comprobar", que es el paso en vacio de siempre.
        with self._fixture("323524c", "de `MicrosoftDocs/query-docs@c6a9a72`.") as f:
            os.remove(os.path.join(f.dir, "dax-reference", "generated", "catalog.json"))
            errors = stale_stamps(f.dir, ["DOC.md"])
        self.assertEqual(len(errors), 1)
        self.assertIn("cannot be checked", errors[0])

    def test_a_catalog_without_a_source_is_reported(self):
        with self._fixture("323524c", "de `MicrosoftDocs/query-docs@c6a9a72`.") as f:
            path = os.path.join(f.dir, "dax-reference", "generated", "catalog.json")
            with open(path, "w", encoding="utf-8") as fh:
                json.dump({"functions": []}, fh)
            errors = stale_stamps(f.dir, ["DOC.md"])
        self.assertEqual(len(errors), 1)
        self.assertIn("does not say which one", errors[0])

    def test_an_uppercase_sha_is_the_same_commit(self):
        self.assertAccepts("323524c", "de `MicrosoftDocs/query-docs@323524C`.", "323524C")

    def test_a_stale_uppercase_sha_is_still_caught(self):
        # Sin ignorar mayusculas, el patron no encontraba nada y el gate decia OK.
        with self._fixture("323524c", "de `MicrosoftDocs/query-docs@C6A9A72`.") as f:
            errors = stale_stamps(f.dir, ["DOC.md"])
        self.assertEqual(len(errors), 1)

    def test_a_document_outside_DOCS_that_names_a_commit_is_flagged(self):
        # Sin cifras no lo veia el meta-check, y sin estar en DOCS no lo veia el de
        # sellos: un documento podia nombrar un commit viejo y pasar por los dos huecos.
        with self._fixture("323524c", "") as f:
            os.makedirs(os.path.join(f.dir, "docs"))
            with open(os.path.join(f.dir, "docs", "SUELTO.md"), "w", encoding="utf-8") as fh:
                fh.write("Derivado de `MicrosoftDocs/query-docs@c6a9a72`, sin cifras.\n")
            errors = check(root=f.dir, docs=["DOC.md"])
        self.assertEqual(len(errors), 1)
        self.assertIn("docs/SUELTO.md", errors[0])

    def test_a_bare_sha_is_prose_about_history_not_a_stamp(self):
        # La valvula de escape: el patron exige la forma repo@sha, asi que una frase sobre
        # el commit viejo se escribe sin el prefijo y no dispara.
        with self._fixture("323524c", "Antes el arbol venia de c6a9a72, ahora no.") as f:
            self.assertEqual(stale_stamps(f.dir, ["DOC.md"]), [])

    def test_the_real_repo_prose_names_the_commit_it_was_built_from(self):
        # Afirmar solo que no hay sellos desfasados pasaria tambien si stale_stamps fuera
        # un no-op. Se comprueba primero que HAY algo que comparar.
        import re as _re
        from check_doc_claims import DOCS, _STAMP_IN_PROSE
        named = [rel for rel in DOCS
                 if _STAMP_IN_PROSE.search(
                     open(os.path.join(ROOT, rel), encoding="utf-8").read())]
        self.assertTrue(named, "ningun documento nombra el commit: no se compara nada")
        self.assertEqual(stale_stamps(ROOT), [])


class TheListThatRechecksItself(unittest.TestCase):
    """DOCS es una lista, y una lista que nadie repasa es como se pudrio el techo viejo."""

    def test_a_new_document_with_counts_is_not_silently_unchecked(self):
        with Fixture("") as f:
            os.makedirs(os.path.join(f.dir, "docs"))
            with open(os.path.join(f.dir, "docs", "NUEVO.md"), "w", encoding="utf-8") as fh:
                fh.write("Tiene 999 fichas.\n")
            errors = check(root=f.dir, docs=["DOC.md"])
        self.assertEqual(len(errors), 1)
        self.assertIn("docs/NUEVO.md", errors[0])
        self.assertIn("neither in DOCS nor in HISTORICAL", errors[0])

    def test_a_document_with_no_counts_is_not_flagged(self):
        with Fixture("") as f:
            os.makedirs(os.path.join(f.dir, "docs"))
            with open(os.path.join(f.dir, "docs", "PROSA.md"), "w", encoding="utf-8") as fh:
                fh.write("Solo texto, sin cifras.\n")
            self.assertEqual(check(root=f.dir, docs=["DOC.md"]), [])

    def test_the_historical_records_may_keep_their_old_numbers(self):
        # Un registro que explica que el spec decia 61 tiene que seguir diciendo 61.
        with Fixture("") as f:
            os.makedirs(os.path.join(f.dir, "docs", "decisions"))
            with open(os.path.join(f.dir, "docs", "decisions", "vieja.md"), "w",
                      encoding="utf-8") as fh:
                fh.write("El spec prometia 61 conceptual pages.\n")
            self.assertEqual(check(root=f.dir, docs=["DOC.md"]), [])

    def test_a_sibling_skill_talking_about_other_functions_is_out_of_scope(self):
        # dax-udf-authoring dice "1,649 functions" del catalogo de daxlib. Es cierto, y de
        # otra cosa: discutirselo seria el gate equivocandose.
        with Fixture("") as f:
            os.makedirs(os.path.join(f.dir, "otra-skill"))
            with open(os.path.join(f.dir, "otra-skill", "SKILL.md"), "w",
                      encoding="utf-8") as fh:
                fh.write("daxlib publica 1,649 functions.\n")
            self.assertEqual(check(root=f.dir, docs=["DOC.md"]), [])

    def test_an_example_counting_dax_functions_is_out_of_scope(self):
        # floor.md dice "Tres funciones, dos comportamientos" de FLOOR, INT y ROUNDDOWN.
        # Es prosa sobre lo que hace DAX, no sobre lo que tiene el repo. Sus cifras las
        # comprueba check_examples.py contra el motor, que es quien puede.
        with Fixture("") as f:
            os.makedirs(os.path.join(f.dir, "dax-reference", "examples", "math-and-trig"))
            with open(os.path.join(f.dir, "dax-reference", "examples", "math-and-trig",
                                   "floor.md"), "w", encoding="utf-8") as fh:
                fh.write("Tres funciones, dos comportamientos.\n")
            self.assertEqual(check(root=f.dir, docs=["DOC.md"]), [])

    def test_the_exclusion_stops_at_the_examples_directory(self):
        # Solo `examples`. Una nota de campo que cuente fichas sigue teniendo que cuadrar:
        # sin este limite, exceptuar la prosa didactica apagaria el gate en todo el arbol.
        with Fixture("") as f:
            os.makedirs(os.path.join(f.dir, "dax-reference", "notes"), exist_ok=True)
            with open(os.path.join(f.dir, "dax-reference", "notes", "nueva.md"), "w",
                      encoding="utf-8") as fh:
                fh.write("Tiene 999 fichas.\n")
            errors = check(root=f.dir, docs=["DOC.md"])
        self.assertEqual(len(errors), 1)
        self.assertIn("dax-reference/notes/nueva.md", errors[0])

    def test_a_session_handoff_keeps_its_snapshot_numbers(self):
        # HANDOFF.md lo escribe /board handoff y dice cosas como "191 consultas, 0 fallas".
        # Es un registro de lo que era cierto al guardarlo, igual que un decision record: si
        # el gate se lo discutiera, cada sesion tendria que reescribir su propio historial.
        with Fixture("") as f:
            with open(os.path.join(f.dir, "HANDOFF.md"), "w", encoding="utf-8") as fh:
                fh.write("Se midieron 999 fichas en esta sesion.\n")
            self.assertEqual(check(root=f.dir, docs=["DOC.md"]), [])

    def test_the_real_repo_has_nothing_unlisted(self):
        self.assertEqual(unlisted_documents(ROOT), [])


class TheRealRepo(unittest.TestCase):
    def test_this_repo_agrees_with_itself(self):
        errors = check(ROOT)
        self.assertEqual(errors, [], "\n".join(errors or []))

    def test_the_real_docs_actually_state_something(self):
        # Si los patrones dejaran de encontrar nada, el gate pasaria sin comprobar.
        with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as f:
            self.assertGreaterEqual(len(claims_in(f.read())), 3)


if __name__ == "__main__":
    unittest.main()
