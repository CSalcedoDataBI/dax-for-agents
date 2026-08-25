#!/usr/bin/env python3
"""Tests del guardia de credenciales. Ejecutar: python -m unittest discover -s scripts -t scripts

Ningun secreto de verdad aparece aqui, ni siquiera de juguete: los tokens de prueba se
componen en tiempo de ejecucion (`"ghp_" + "a" * 36`) para que el propio archivo no
contenga nada con forma de credencial. Asi el guardia no necesita una excepcion para sus
propias pruebas, que es la clase de excepcion que despues tapa una fuga real.
"""
import hashlib
import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from check_no_credentials import (find_in_text, load_digests,  # noqa: E402
                                  scan_history, scan_tree)

PAT_CLASICO = "ghp_" + "a1B2" * 9                     # 4 + 36
PAT_FINO = "github_pat_" + "b" * 22 + "_" + "c" * 59
CLAVE_AWS = "AKIA" + "Q7ZK3MN4PX8VWY2C"               # 4 + 16
SECRETO_AAD = "Zq7" + "8Q~" + "k3Lm9pQr2sTu5vWx8yZa1bCd4eFg7hJk"
CABECERA_PEM = "-----BEGIN " + "RSA PRIVATE KEY" + "-----"
CADENA_CONEXION = "Server=x;User Id=y;Pass" + "word=Tr0ub4dor3xyz;"


class FindInText(unittest.TestCase):

    def hits(self, texto, digests=frozenset()):
        return list(find_in_text(texto, digests))

    def test_texto_limpio_no_reporta_nada(self):
        self.assertEqual(self.hits("una nota sobre DAX\nsin nada dentro\n"), [])

    def test_encuentra_un_pat_clasico_de_github(self):
        h = self.hits(f"token = {PAT_CLASICO}\n")
        self.assertEqual([x["line"] for x in h], [1])
        self.assertIn("GitHub", h[0]["label"])

    def test_encuentra_un_pat_de_grano_fino(self):
        self.assertEqual(len(self.hits(f"GH_TOKEN={PAT_FINO}\n")), 1)

    def test_encuentra_una_clave_de_acceso_de_aws(self):
        self.assertEqual(len(self.hits(f"aws_access_key_id = {CLAVE_AWS}\n")), 1)

    def test_encuentra_un_secreto_de_cliente_de_azure(self):
        self.assertEqual(len(self.hits(f"PAC_CLIENT_SECRET: {SECRETO_AAD}\n")), 1)

    def test_encuentra_una_clave_privada_pem(self):
        self.assertEqual(len(self.hits(CABECERA_PEM + "\nMIIE\n")), 1)

    def test_encuentra_una_contrasena_en_cadena_de_conexion(self):
        self.assertEqual(len(self.hits(CADENA_CONEXION + "\n")), 1)

    def test_el_valor_nunca_se_imprime(self):
        # El informe va a CI y a la consola. Reproducir el secreto para avisar de que hay
        # un secreto lo copia a un sitio mas. Se dice donde esta y cuanto mide, nada mas.
        h = self.hits(f"token = {PAT_CLASICO}\n")[0]
        self.assertNotIn(PAT_CLASICO, h["text"])
        self.assertNotIn(PAT_CLASICO[4:20], h["text"])
        self.assertIn("REDACTADO", h["text"])
        self.assertIn(str(len(PAT_CLASICO)), h["text"])

    def test_los_marcadores_de_ejemplo_no_cuentan(self):
        # La documentacion tiene que poder ensenar la forma de una cadena de conexion.
        for linea in ("Password=<TU_CLAVE>",
                      "Password=${PGPASSWORD}",
                      "password=YOUR_PASSWORD_HERE",
                      "password=xxxxxxxx",
                      "Password=***"):
            self.assertEqual(self.hits(linea + "\n"), [], linea)

    def test_un_valor_por_digest_se_encuentra_aunque_no_tenga_forma_de_secreto(self):
        # Un GUID de inquilino no se distingue de cualquier otro GUID por su forma. La
        # unica manera de vigilarlo sin escribirlo en un repositorio que sera publico es
        # guardar su huella.
        valor = "e0c1a2b3-4d5e-6f70-8192-a3b4c5d6e7f8"
        d = {hashlib.sha256(valor.encode()).hexdigest()}
        h = self.hits(f"tenant = {valor}\n", d)
        self.assertEqual(len(h), 1)
        self.assertIn("huella", h[0]["label"])
        self.assertNotIn(valor, h[0]["text"])

    def test_un_guid_que_no_esta_en_la_lista_no_cuenta(self):
        valor = "11111111-2222-3333-4444-555555555555"
        d = {hashlib.sha256(b"otra-cosa").hexdigest()}
        self.assertEqual(self.hits(f"id = {valor}\n", d), [])

    def test_el_digest_no_distingue_mayusculas(self):
        valor = "AABBCCDD-1122-3344-5566-778899AABBCC"
        d = {hashlib.sha256(valor.lower().encode()).hexdigest()}
        self.assertEqual(len(self.hits(f"id = {valor}\n", d)), 1)


class Ficheros(unittest.TestCase):

    def setUp(self):
        self.dir = tempfile.mkdtemp()

    def write(self, rel, body):
        path = os.path.join(self.dir, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(body)

    def git(self, *args):
        subprocess.run(("git", "-C", self.dir) + args, check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def test_el_arbol_limpio_no_reporta_nada(self):
        self.write("README.md", "# limpio\n")
        self.assertEqual(scan_tree(self.dir, frozenset()), [])

    def test_reporta_el_fichero_y_la_linea(self):
        self.write("ci/deploy.sh", f"set -e\nexport TOKEN={PAT_CLASICO}\n")
        h = scan_tree(self.dir, frozenset())
        self.assertEqual(len(h), 1)
        self.assertEqual(h[0]["line"], 2)
        self.assertTrue(h[0]["file"].endswith("deploy.sh"))

    def test_los_binarios_no_rompen_el_barrido(self):
        with open(os.path.join(self.dir, "icon.png"), "wb") as f:
            f.write(b"\x89PNG\r\n\x1a\n\xff\xfe\x00\x01")
        self.assertEqual(scan_tree(self.dir, frozenset()), [])

    def test_un_secreto_en_el_mensaje_del_commit_se_encuentra(self):
        # Mismo agujero que tenian las rutas, y aqui pesa mas: un token pegado
        # en un mensaje no se arregla borrandolo, se ROTA. Un mensaje no es un blob ni
        # tiene ruta, asi que recorrer blobs no lo veia.
        for a in (("init", "-q"), ("config", "user.email", "t@e.com"),
                  ("config", "user.name", "T")):
            self.git(*a)
        self.write("README.md", "limpio\n")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", f"probando con {PAT_CLASICO}")
        self.assertEqual(scan_tree(self.dir, frozenset()), [])
        h = scan_history(self.dir, frozenset())
        self.assertEqual(len(h), 1)
        self.assertTrue(h[0]["path"].startswith("(mensaje del commit"))
        # El informe nunca reproduce lo que encuentra, tampoco aqui.
        self.assertNotIn(PAT_CLASICO, h[0]["text"])

    def test_un_secreto_borrado_del_arbol_sigue_en_la_historia(self):
        for a in (("init", "-q"), ("config", "user.email", "t@e.com"),
                  ("config", "user.name", "T")):
            self.git(*a)
        self.write("ci/deploy.sh", f"export TOKEN={PAT_CLASICO}\n")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "mete el token")
        os.remove(os.path.join(self.dir, "ci", "deploy.sh"))
        self.git("commit", "-q", "-am", "lo quita")
        self.assertEqual(scan_tree(self.dir, frozenset()), [])
        h = scan_history(self.dir, frozenset())
        self.assertEqual(len(h), 1)
        self.assertEqual(h[0]["path"], "ci/deploy.sh")
        self.assertNotIn(PAT_CLASICO, h[0]["text"])


class Digests(unittest.TestCase):

    def test_lee_hex_y_salta_comentarios_y_lineas_en_blanco(self):
        d = tempfile.mkdtemp()
        p = os.path.join(d, "digests.txt")
        with open(p, "w", encoding="utf-8") as f:
            f.write("# un comentario\n\n" + "ab" * 32 + "\n" + "CD" * 32 + "\n")
        self.assertEqual(load_digests(p), {"ab" * 32, "cd" * 32})

    def test_una_linea_que_no_es_un_digest_es_un_error(self):
        # Pegar el secreto en vez de su huella es el error que este fichero existe para
        # impedir. Tiene que doler de inmediato, no pasar en silencio.
        d = tempfile.mkdtemp()
        p = os.path.join(d, "digests.txt")
        with open(p, "w", encoding="utf-8") as f:
            f.write("11111111-2222-3333-4444-555555555555\n")
        with self.assertRaises(ValueError):
            load_digests(p)


if __name__ == "__main__":
    unittest.main()
