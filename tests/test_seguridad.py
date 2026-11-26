"""Pruebas de seguridad: bloqueo de acciones y filtro de secretos.

La prueba clave de este archivo es determinista a propósito. En el flujo real,
cuando se pide "registra una compra", el modelo suele negarse por su cuenta y
entonces *parece* que el sistema bloqueó la acción, cuando en realidad el
modelo simplemente no la pidió. Esa evidencia no vale: un modelo distinto, un
cambio de prompt o una inyección podrían hacer que sí la pida.

Aquí se fuerza la situación incómoda con un modelo falso que emite el
`tool_call` de escritura. Lo que se verifica es que el nodo ReAct intercepta
**antes de ejecutar**, sin depender del criterio del modelo.
"""

import unittest
from unittest.mock import patch

from langchain_core.messages import AIMessage

from nodes.herramienta import herramienta
from nodes.juez import MENSAJE_SEGURO, _tiene_contenido_prohibido
from tools.herramientas import PORTAFOLIO_PATH


class ModeloQuePideEscribir:
    """Modelo falso: pide la herramienta de escritura y luego responde."""

    def __init__(self) -> None:
        self.llamadas = 0
        self.herramientas_vinculadas: list[str] = []

    def bind_tools(self, tools):  # noqa: ANN001 - imita la API de LangChain
        self.herramientas_vinculadas = [t.name for t in tools]
        return self

    def invoke(self, mensajes):  # noqa: ANN001
        self.llamadas += 1
        if self.llamadas == 1:
            return AIMessage(content="", tool_calls=[{
                "name": "registrar_compra_simulada",
                "args": {"cripto": "bitcoin", "cantidad": 1, "precio_usd": 40000},
                "id": "call-escritura",
            }])
        return AIMessage(content="Compra registrada.")


class BloqueoDeAccionesTest(unittest.TestCase):
    def setUp(self) -> None:
        # El portafolio se guarda y se restaura: la prueba no debe ensuciar
        # datos del usuario ni crear el archivo si no existía.
        self._existia = PORTAFOLIO_PATH.exists()
        self._contenido = PORTAFOLIO_PATH.read_text(encoding="utf-8") if self._existia else None

    def tearDown(self) -> None:
        if self._existia:
            PORTAFOLIO_PATH.write_text(self._contenido, encoding="utf-8")
        elif PORTAFOLIO_PATH.exists():
            PORTAFOLIO_PATH.unlink()

    def test_bloquea_escritura_antes_de_ejecutar(self):
        """Con `permitir_escritura=False` la tool no se ejecuta y queda en traza."""
        modelo = ModeloQuePideEscribir()
        with patch("nodes.herramienta.get_llm", return_value=modelo):
            salida = herramienta({"user_input": "Registra una compra de 1 BTC a 40000 USD.",
                                  "permitir_escritura": False})

        self.assertIn("accion_bloqueada", salida["trace"])
        self.assertIn("no autorizada", salida["borrador"].lower())
        # El modelo nunca llegó a ver la herramienta de escritura entre sus opciones.
        self.assertNotIn("registrar_compra_simulada", modelo.herramientas_vinculadas)
        # Y, sobre todo, no hubo efecto en disco.
        self.assertFalse(PORTAFOLIO_PATH.exists() and self._contenido is None,
                         "la acción bloqueada no debe crear el portafolio")

    def test_con_permiso_la_herramienta_se_vincula(self):
        """Control negativo: con escritura permitida la tool sí se ofrece."""
        modelo = ModeloQuePideEscribir()
        with patch("nodes.herramienta.get_llm", return_value=modelo):
            herramienta({"user_input": "Registra una compra de práctica.",
                         "permitir_escritura": True})
        self.assertIn("registrar_compra_simulada", modelo.herramientas_vinculadas)


class FiltroDeSecretosTest(unittest.TestCase):
    def test_bloquea_claves_de_google(self):
        self.assertTrue(_tiene_contenido_prohibido("la clave es AIza" + "x" * 30))

    def test_bloquea_nombres_de_variables(self):
        self.assertTrue(_tiene_contenido_prohibido("configura GOOGLE_API_KEY en el .env"))

    def test_no_bloquea_texto_normal(self):
        self.assertFalse(_tiene_contenido_prohibido("Una billetera guarda tus llaves privadas."))

    def test_mensaje_seguro_no_filtra(self):
        self.assertNotIn("AIza", MENSAJE_SEGURO)


if __name__ == "__main__":
    unittest.main()
