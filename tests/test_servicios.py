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
