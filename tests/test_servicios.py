import asyncio
from langchain_core.exceptions import ModelRateLimitError
import unittest
from unittest.mock import AsyncMock, patch

from langchain_core.messages import AIMessage
from starlette.testclient import TestClient

import servidor
import servidor_especialista


class ServiciosTest(unittest.TestCase):
    def test_chat_publica_el_login(self):
        self.assertEqual(TestClient(servidor.app).get("/app").status_code, 200)

    def test_especialista_devuelve_artefacto_a2a(self):
        cliente = TestClient(servidor_especialista.app)
        ruta = "/a2a/especialista_cripto"
        solicitud = {"jsonrpc": "2.0", "id": "prueba", "method": "message/send", "params": {
            "message": {"parts": [{"kind": "text", "text": "Stablecoin"}]}
        }}
        with patch.object(servidor_especialista.graph, "ainvoke", new_callable=AsyncMock) as invocar:
            invocar.return_value = {"messages": [AIMessage(content='{"estado":"sin_evidencia"}')]}
            resultado = cliente.post(ruta, json=solicitud).json()
            invocar.assert_awaited_once()
        self.assertEqual(resultado["id"], "prueba")
        self.assertEqual(resultado["result"]["status"]["state"], "completed")
        self.assertEqual(resultado["result"]["artifacts"][0]["parts"][0]["kind"], "text")


    def test_calculo_responde_ante_limite_de_gemini(self):
        pregunta = "Compré 0,5 BTC a USD 40000 y hoy cada BTC vale USD 50000. ¿Cuánto gané?"
        with patch.object(servidor.graph, "invoke", side_effect=ModelRateLimitError("429")):
            dato, status = asyncio.run(servidor.ejecutar_consulta(pregunta, []))
            invalido, status_invalido = asyncio.run(servidor.ejecutar_consulta("Otro mensaje", []))
        self.assertEqual(status, 200)
        self.assertIn("5,000.00", dato["respuesta"])
        self.assertIn("calculo_local", dato["traza"])
        self.assertEqual(status_invalido, 503)
        self.assertIn("Gemini", invalido["error"])
