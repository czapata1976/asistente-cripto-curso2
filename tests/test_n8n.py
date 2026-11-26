"""Pruebas del flujo de plan: la causa del fallo en Cloud Run.

En producción el agente respondía «No pude contactar al planificador. Intenta de
nuevo en unos minutos», que describe un fallo transitorio. En realidad faltaba
`N8N_WEBHOOK_URL` en el contenedor: no había nada que reintentar.

Estas pruebas fijan la distinción, para que el mensaje vuelva a ser exacto sin
depender de tener n8n levantado.
"""

import unittest
from unittest.mock import patch

from config import settings
from nodes.plan import PlanParams, plan_dca
from services.n8n_cliente import N8NInalcanzable, N8NNoConfigurado, pedir_plan


class ExtractorFalso:
    """Sustituye al LLM: devuelve siempre un plan válido."""

    def with_structured_output(self, modelo):  # noqa: ANN001 - imita LangChain
        return self

    def invoke(self, mensajes):  # noqa: ANN001
        return PlanParams(monto_usd=50, frecuencia="semanal", semanas=12, cripto="bitcoin")


class FlujoPlanTest(unittest.TestCase):
    def setUp(self) -> None:
        self._url = settings.n8n_webhook_url
        self._iam = settings.n8n_cloud_run_iam

    def tearDown(self) -> None:
        object.__setattr__(settings, "n8n_webhook_url", self._url)
        object.__setattr__(settings, "n8n_cloud_run_iam", self._iam)

    def _sin_url(self) -> None:
        object.__setattr__(settings, "n8n_webhook_url", "")
        object.__setattr__(settings, "n8n_cloud_run_iam", False)

    def test_sin_url_lanza_no_configurado(self):
        """Falta la variable: es un error de configuración, no de red."""
        self._sin_url()
        with self.assertRaises(N8NNoConfigurado):
            pedir_plan("encargo", {"monto_usd": 50})

    def test_url_inalcanzable_es_distinto_de_falta_de_configuracion(self):
        """Con URL pero sin servidor, el error es de conexión."""
        object.__setattr__(settings, "n8n_webhook_url", "http://127.0.0.1:9/webhook/a2a-plan")
        object.__setattr__(settings, "n8n_cloud_run_iam", False)
        with self.assertRaises(N8NInalcanzable):
            pedir_plan("encargo", {"monto_usd": 50})

    def test_el_nodo_no_promete_reintento_si_no_hay_planificador(self):
        """El mensaje al usuario debe decir que no está habilitado."""
        self._sin_url()
        with patch("nodes.plan.get_llm", return_value=ExtractorFalso()):
            salida = plan_dca({"user_input": "50 USD semanales durante 12 semanas"})

        self.assertIn("n8n_no_configurado", salida["trace"])
        self.assertEqual(salida["delegacion_n8n"]["estado"], "no_configurado")
        self.assertIn("no está habilitado", salida["borrador"])
        # Lo que no debe decir: que reintente, porque nunca funcionaría.
        self.assertNotIn("Intenta de nuevo", salida["borrador"])

    def test_el_estado_de_salud_publica_si_hay_planificador(self):
        """`/salud` debe permitir diagnosticar sin acceso a los logs."""
        from servidor import salud
        import asyncio

        self._sin_url()
        respuesta = asyncio.run(salud(None))
        import json

        datos = json.loads(respuesta.body)
        self.assertFalse(datos["especialistas"]["n8n_configurado"])

        object.__setattr__(settings, "n8n_webhook_url", "https://ejemplo/webhook/a2a-plan")
        datos = json.loads(asyncio.run(salud(None)).body)
        self.assertTrue(datos["especialistas"]["n8n_configurado"])


if __name__ == "__main__":
    unittest.main()
