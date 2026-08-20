#!/usr/bin/env python3
"""Tests for the Actions cost gate. Run: python -m unittest discover -s scripts"""
import io
import os
import sys
import contextlib
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from check_workflow_cost import (  # noqa: E402
    MAX_TIMEOUT, _runner_alternatives, check_tree, cron_is_weekly_or_rarer, main,
)


def write(dirpath, name, body):
    with open(os.path.join(dirpath, name), "w", encoding="utf-8") as f:
        f.write(body)


def check_tree_of(_test, body):
    """Run the gate over a single throwaway workflow."""
    with tempfile.TemporaryDirectory() as d:
        write(d, "w.yml", body)
        return check_tree(d)


GOOD = """\
name: Fine
on:
  pull_request:
jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - run: echo hi
"""


class Timeout(unittest.TestCase):
    """R3. The default is 360 minutes: one hung job is 12% of the monthly quota."""

    def check(self, body, name="w.yml"):
        with tempfile.TemporaryDirectory() as d:
            write(d, name, body)
            return check_tree(d)

    def test_a_compliant_workflow_passes(self):
        self.assertEqual(self.check(GOOD), [])

    def test_a_job_without_timeout_fails(self):
        errors = self.check(GOOD.replace("    timeout-minutes: 10\n", ""))
        self.assertEqual(len(errors), 1)
        self.assertIn("build", errors[0])
        self.assertIn("timeout-minutes", errors[0])

    def test_every_job_is_checked_not_just_the_first(self):
        # En visual-studio-pbi se colaron 2 de 4 jobs sin limite por mirar solo los
        # que mencionaba el ticket. El gate cuenta los jobs del archivo.
        errors = self.check(GOOD + """\
  second:
    runs-on: ubuntu-latest
    steps:
      - run: echo hi
  third:
    runs-on: ubuntu-latest
    steps:
      - run: echo hi
""")
        self.assertEqual(len(errors), 2)
        self.assertTrue(any("second" in e for e in errors))
        self.assertTrue(any("third" in e for e in errors))

    def test_a_timeout_above_the_cap_fails(self):
        # 360 declarado a mano es el default con otro nombre.
        errors = self.check(GOOD.replace("timeout-minutes: 10", "timeout-minutes: 360"))
        self.assertEqual(len(errors), 1)
        self.assertIn(str(MAX_TIMEOUT), errors[0])

    def test_the_cap_itself_is_allowed(self):
        self.assertEqual(self.check(GOOD.replace("timeout-minutes: 10",
                                                 f"timeout-minutes: {MAX_TIMEOUT}")), [])

    def test_one_minute_over_the_cap_fails(self):
        # El par con el de arriba: solos, cualquiera de los dos pasaria con la
        # comprobacion del tope borrada. Juntos fijan el limite exacto.
        errors = self.check(GOOD.replace("timeout-minutes: 10",
                                         f"timeout-minutes: {MAX_TIMEOUT + 1}"))
        self.assertEqual(len(errors), 1)

    def test_a_timeout_written_as_a_string_still_meets_the_cap(self):
        # YAML lo entrega como str, y saltarse el tope ahi dejaba sin mirar
        # justamente el limite mas alto del archivo.
        errors = self.check(GOOD.replace("timeout-minutes: 10",
                                         'timeout-minutes: "120"'))
        self.assertEqual(len(errors), 1)
        self.assertIn("120", errors[0])

    def test_a_string_within_the_cap_passes(self):
        self.assertEqual(self.check(GOOD.replace("timeout-minutes: 10",
                                                 'timeout-minutes: "10"')), [])

    def test_zero_minutes_is_not_a_shorter_limit(self):
        # '0 > 60' es falso, asi que pasaba. Cero no es un limite mas corto.
        errors = self.check(GOOD.replace("timeout-minutes: 10", "timeout-minutes: 0"))
        self.assertEqual(len(errors), 1)

    def test_a_negative_timeout_fails(self):
        errors = self.check(GOOD.replace("timeout-minutes: 10", "timeout-minutes: -1"))
        self.assertEqual(len(errors), 1)

    def test_an_unreadable_timeout_is_reported_not_ignored(self):
        errors = self.check(GOOD.replace("timeout-minutes: 10",
                                         "timeout-minutes: ${{ inputs.limit }}"))
        self.assertEqual(len(errors), 1)
        self.assertIn("not a number", errors[0])

    def test_a_reusable_workflow_call_is_exempt(self):
        # `jobs.<id>.uses` no acepta timeout-minutes: el limite vive en el workflow
        # llamado. Exigirlo aqui seria un error que no se puede arreglar.
        self.assertEqual(self.check("""\
name: Caller
on: [pull_request]
jobs:
  call:
    uses: ./.github/workflows/other.yml
"""), [])


class CronCadence(unittest.TestCase):
    """R7. El cron es el gasto que corre aunque no trabajes."""

    def test_weekly_is_fine(self):
        self.assertTrue(cron_is_weekly_or_rarer("17 6 * * 1"))

    def test_monthly_is_fine(self):
        self.assertTrue(cron_is_weekly_or_rarer("0 3 1 * *"))

    def test_daily_is_not(self):
        self.assertFalse(cron_is_weekly_or_rarer("30 1 * * *"))

    def test_hourly_is_not(self):
        self.assertFalse(cron_is_weekly_or_rarer("0 * * * 1"))

    def test_a_range_of_days_is_not_weekly(self):
        # Lunes a viernes son 5 runs por semana. La primera version decia que si,
        # porque miraba que el campo no fuera '*' en vez de cuantos dias elige.
        self.assertFalse(cron_is_weekly_or_rarer("0 3 * * 1-5"))

    def test_a_list_of_days_is_not_weekly(self):
        self.assertFalse(cron_is_weekly_or_rarer("0 3 * * 1,4"))

    def test_every_other_day_is_not_weekly(self):
        self.assertFalse(cron_is_weekly_or_rarer("0 3 */2 * *"))

    def test_pinning_both_day_fields_is_not_weekly(self):
        # La trampa de cron: con dia-del-mes Y dia-de-semana puestos, dispara cuando
        # coincide CUALQUIERA de los dos, no los dos.
        self.assertFalse(cron_is_weekly_or_rarer("0 3 5 * 1"))

    def test_a_step_in_the_minute_field_is_not(self):
        # */15 en los minutos son 96 runs al dia aunque el dia de la semana este fijo.
        self.assertFalse(cron_is_weekly_or_rarer("*/15 6 * * 1"))

    def test_a_malformed_cron_is_not_assumed_fine(self):
        self.assertFalse(cron_is_weekly_or_rarer("6 * * 1"))

    def test_a_day_name_is_a_valid_weekly_cron(self):
        # POSIX admite nombres. Rechazar '17 6 * * MON' seria el gate inventandose
        # una violacion sobre un cron semanal perfectamente correcto.
        self.assertTrue(cron_is_weekly_or_rarer("17 6 * * MON"))
        self.assertTrue(cron_is_weekly_or_rarer("17 6 * * sun"))

    def test_a_range_of_day_names_is_not_weekly(self):
        self.assertFalse(cron_is_weekly_or_rarer("17 6 * * MON-FRI"))

    def test_the_month_field_never_rejects(self):
        # El mes solo puede estrechar el calendario. 'Lunes de enero y junio' corre
        # MENOS que semanal: quejarse de eso es quejarse de un ahorro.
        self.assertTrue(cron_is_weekly_or_rarer("0 3 * 1,6 1"))
        self.assertTrue(cron_is_weekly_or_rarer("0 3 * */2 1"))

    def test_the_month_field_does_not_rescue_a_daily_cron(self):
        self.assertFalse(cron_is_weekly_or_rarer("0 3 * 1,6 *"))

    def test_a_couple_of_days_of_the_month_is_rarer_than_weekly(self):
        # El 1 y el 15 son dos veces al mes: menos que semanal.
        self.assertTrue(cron_is_weekly_or_rarer("0 0 1,15 * *"))

    def test_a_long_list_of_days_of_the_month_is_not(self):
        self.assertFalse(cron_is_weekly_or_rarer("0 0 1,5,10,15,20,25 * *"))

    def test_a_range_of_days_of_the_month_is_not(self):
        self.assertFalse(cron_is_weekly_or_rarer("0 0 1-15 * *"))

    def test_two_days_a_week_is_still_twice_the_budget(self):
        self.assertFalse(cron_is_weekly_or_rarer("0 0 * * 1,4"))

    def test_a_daily_schedule_is_reported(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, "w.yml", """\
name: Nightly
on:
  schedule:
    - cron: "30 1 * * *"
jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - run: echo hi
""")
            errors = check_tree(d)
        self.assertEqual(len(errors), 1)
        self.assertIn("30 1 * * *", errors[0])


class Runner(unittest.TestCase):
    """R5. Windows cuesta x2 y macOS x10 sobre la misma cuota."""

    def test_a_windows_runner_fails(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, "w.yml", GOOD.replace("ubuntu-latest", "windows-latest"))
            errors = check_tree(d)
        self.assertEqual(len(errors), 1)
        self.assertIn("windows-latest", errors[0])

    def test_a_matrix_expression_is_not_accused_of_being_a_runner(self):
        # `runs-on: ${{ matrix.os }}` parsea como string, asi que leerlo literal acusa
        # al workflow de correr en una maquina llamada '${{ matrix.os }}'.
        self.assertEqual(_runner_alternatives({
            "runs-on": "${{ matrix.os }}",
            "strategy": {"matrix": {"os": ["ubuntu-latest", "ubuntu-22.04"]}},
        }), [["ubuntu-latest"], ["ubuntu-22.04"]])

    def test_windows_hidden_in_a_matrix_is_still_found(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, "w.yml", """\
name: Matrixed
on: [pull_request]
jobs:
  build:
    runs-on: ${{ matrix.os }}
    timeout-minutes: 10
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
    steps:
      - run: echo hi
""")
            errors = check_tree(d)
        self.assertEqual(len(errors), 1)
        self.assertIn("windows-latest", errors[0])

    def test_only_the_matrix_key_the_expression_names_is_read(self):
        # Leer todos los valores de la matriz haria que '3.12' fuera un runner que no
        # empieza por ubuntu: un fallo inventado en un workflow correcto.
        self.assertEqual(_runner_alternatives({
            "runs-on": "${{ matrix.os }}",
            "strategy": {"matrix": {"os": ["ubuntu-latest"],
                                    "python-version": ["3.11", "3.12"]}},
        }), [["ubuntu-latest"]])

    def test_an_unquoted_number_in_the_matrix_is_still_a_label(self):
        # YAML entrega 22.04 como float. Descartarlo dejaba la expresion sin resolver
        # y el job entero sin comprobar: un runner de Windows tras un numero sin comillas.
        self.assertEqual(_runner_alternatives({
            "runs-on": "${{ matrix.os }}-${{ matrix.version }}",
            "strategy": {"matrix": {"os": ["windows"], "version": [2022]}},
        }), [["windows-2022"]])

    def test_a_list_of_labels_is_one_machine_not_several(self):
        # `runs-on: [ubuntu-latest, fast]` es UNA maquina con dos etiquetas. Exigir que
        # todas empiecen por ubuntu rechaza un workflow correcto.
        self.assertEqual(_runner_alternatives({"runs-on": ["ubuntu-latest", "fast"]}),
                         [["ubuntu-latest", "fast"]])
        self.assertEqual(check_tree_of(self, """\
name: Tagged
on: [pull_request]
jobs:
  build:
    runs-on: [ubuntu-latest, fast]
    timeout-minutes: 10
    steps:
      - run: echo hi
"""), [])

    def test_a_self_hosted_runner_does_not_bill_the_quota(self):
        self.assertEqual(check_tree_of(self, """\
name: Own metal
on: [pull_request]
jobs:
  build:
    runs-on: [self-hosted, linux, x64]
    timeout-minutes: 10
    steps:
      - run: echo hi
"""), [])

    def test_a_list_with_no_ubuntu_label_still_fails(self):
        errors = check_tree_of(self, """\
name: Tagged windows
on: [pull_request]
jobs:
  build:
    runs-on: [windows-latest, fast]
    timeout-minutes: 10
    steps:
      - run: echo hi
""")
        self.assertEqual(len(errors), 1)
        self.assertIn("windows-latest", errors[0])

    def test_the_mapping_form_of_runs_on_is_read(self):
        # `{group: ..., labels: ...}`. Saltarse el mapa entero dejaba pasar las
        # etiquetas que van dentro.
        errors = check_tree_of(self, """\
name: Grouped
on: [pull_request]
jobs:
  build:
    runs-on:
      group: gpu
      labels: [windows-latest]
    timeout-minutes: 10
    steps:
      - run: echo hi
""")
        self.assertEqual(len(errors), 1)
        self.assertIn("windows-latest", errors[0])

    def test_an_exclusion_only_applies_to_its_own_axis(self):
        # Excluir {tool: windows-latest} no dice nada sobre os: windows-latest. Con un
        # conjunto plano de valores, el runner desaparecia del eje equivocado.
        self.assertIn(["windows-latest"], _runner_alternatives({
            "runs-on": "${{ matrix.os }}",
            "strategy": {"matrix": {"os": ["ubuntu-latest", "windows-latest"],
                                    "tool": ["windows-latest", "linux-tool"],
                                    "exclude": [{"tool": "windows-latest"}]}},
        }))

    def test_an_unresolvable_runner_is_skipped_not_accused(self):
        self.assertEqual(_runner_alternatives({"runs-on": "${{ needs.setup.outputs.runner }}"}), [])

    def test_a_runner_added_only_by_include_is_found(self):
        # `include` puede meter un runner sin que exista el eje. Leer solo matrix[key]
        # pasa de largo por un job de Windows que factura el doble.
        self.assertEqual(_runner_alternatives({
            "runs-on": "${{ matrix.os }}",
            "strategy": {"matrix": {"include": [{"os": "windows-latest"}]}},
        }), [["windows-latest"]])

    def test_a_wholly_excluded_runner_is_not_reported(self):
        self.assertEqual(_runner_alternatives({
            "runs-on": "${{ matrix.os }}",
            "strategy": {"matrix": {"os": ["ubuntu-latest", "windows-latest"],
                                    "exclude": [{"os": "windows-latest"}]}},
        }), [["ubuntu-latest"]])

    def test_excluding_one_combination_does_not_excuse_the_runner(self):
        # Quitar (windows, 3.9) deja el job de Windows corriendo las demas versiones.
        self.assertIn(["windows-latest"], _runner_alternatives({
            "runs-on": "${{ matrix.os }}",
            "strategy": {"matrix": {"os": ["ubuntu-latest", "windows-latest"],
                                    "py": ["3.9", "3.12"],
                                    "exclude": [{"os": "windows-latest", "py": "3.9"}]}},
        }))

    def test_include_can_put_back_what_exclude_removed(self):
        # GitHub aplica `include` DESPUES de `exclude`, asi que estar excluido no
        # prueba que el job no corra: el de Windows sigue ahi.
        self.assertIn(["windows-latest"], _runner_alternatives({
            "runs-on": "${{ matrix.os }}",
            "strategy": {"matrix": {"os": ["ubuntu-latest", "windows-latest"],
                                    "exclude": [{"os": "windows-latest"}],
                                    "include": [{"os": "windows-latest",
                                                 "mode": "special"}]}},
        }))

    def test_bracket_notation_resolves_the_same_key(self):
        self.assertEqual(_runner_alternatives({
            "runs-on": "${{ matrix['os'] }}",
            "strategy": {"matrix": {"os": ["windows-latest"]}},
        }), [["windows-latest"]])

    def test_a_literal_prefix_around_the_expression_survives(self):
        # 'ubuntu-${{ matrix.version }}' es un runner de ubuntu. Quedarse con el valor
        # suelto veria '22.04' y acusaria de no-ubuntu a una matriz correcta.
        self.assertEqual(_runner_alternatives({
            "runs-on": "ubuntu-${{ matrix.version }}",
            "strategy": {"matrix": {"version": ["22.04", "24.04"]}},
        }), [["ubuntu-22.04"], ["ubuntu-24.04"]])

    def test_two_references_in_one_label_resolve_together(self):
        # Sustituir de una en una deja '${{ matrix.os }}-latest' a medias, que no
        # empieza por ubuntu: un fallo inventado sobre una matriz correcta.
        self.assertEqual(_runner_alternatives({
            "runs-on": "${{ matrix.os }}-${{ matrix.version }}",
            "strategy": {"matrix": {"os": ["ubuntu"], "version": ["latest", "22.04"]}},
        }), [["ubuntu-latest"], ["ubuntu-22.04"]])

    def test_a_combination_that_is_not_ubuntu_still_fails(self):
        self.assertIn(["windows-latest"], _runner_alternatives({
            "runs-on": "${{ matrix.os }}-${{ matrix.version }}",
            "strategy": {"matrix": {"os": ["ubuntu", "windows"], "version": ["latest"]}},
        }))

    def test_a_literal_prefix_does_not_disguise_a_windows_runner(self):
        errors = None
        with tempfile.TemporaryDirectory() as d:
            write(d, "w.yml", """\
name: Prefixed
on: [pull_request]
jobs:
  build:
    runs-on: ${{ matrix.flavour }}-latest
    timeout-minutes: 10
    strategy:
      matrix:
        flavour: [ubuntu, windows]
    steps:
      - run: echo hi
""")
            errors = check_tree(d)
        self.assertEqual(len(errors), 1)
        self.assertIn("windows-latest", errors[0])

    def test_a_literal_label_beside_an_expression_is_kept(self):
        # [self-hosted, "${{ matrix.os }}"]: resolver la expresion no puede hacer
        # desaparecer la etiqueta que ya estaba escrita al lado.
        self.assertEqual(_runner_alternatives({
            "runs-on": ["self-hosted", "${{ matrix.os }}"],
            "strategy": {"matrix": {"os": ["ubuntu-latest"]}},
        }), [["self-hosted", "ubuntu-latest"]])


class NothingChecked(unittest.TestCase):
    """Las tres formas de decir OK sin haber mirado nada."""

    def test_an_empty_tree_is_flagged_rather_than_passing_vacuously(self):
        # Sin workflows el gate no comprueba nada. Decir OK ahi es afirmar que se
        # miro algo; si el directorio desaparece, el check tiene que notarlo.
        with tempfile.TemporaryDirectory() as d:
            self.assertIsNone(check_tree(d))

    def test_a_file_with_no_jobs_is_flagged(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, "w.yml", "name: Empty\non: [pull_request]\n")
            errors = check_tree(d)
        self.assertEqual(len(errors), 1)
        self.assertIn("no jobs", errors[0])

    def test_the_reported_count_is_the_files_actually_read(self):
        # main() contaba con el glob '*.y*ml' y check_tree lee '*.yml'/'*.yaml': un
        # '.yxml' entraba en el total sin haberse comprobado. Se comprueba sobre lo
        # que main() IMPRIME: mirar workflow_paths seria comprobar el arreglo contra
        # si mismo, y revertir main() al glob ancho seguiria pasando.
        with tempfile.TemporaryDirectory() as d:
            write(d, "w.yml", GOOD)
            write(d, "notes.yxml", "esto no es un workflow")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = main(d)
        self.assertEqual(code, 0)
        self.assertIn("1 workflow(s)", out.getvalue())
        self.assertNotIn("2 workflow(s)", out.getvalue())

    def test_main_refuses_a_directory_with_no_workflows(self):
        with tempfile.TemporaryDirectory() as d:
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(main(d), 2)


class TheRealWorkflows(unittest.TestCase):
    """El gate corriendo sobre este repo. Si esto falla, el repo esta mal, no el test."""

    def test_this_repo_passes(self):
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        errors = check_tree(os.path.join(root, ".github", "workflows"))
        self.assertEqual(errors, [], "\n".join(errors or []))


if __name__ == "__main__":
    unittest.main()
