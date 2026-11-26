"""Conteo de uso del LLM por solicitud (tokens y llamadas).

Se engancha como callback de LangChain en `graph.invoke(..., config={"callbacks":
[contador]})`. Así un solo objeto acumula las llamadas de *todos* los nodos que
participaron en esa solicitud —router, ReAct, juez, MCP, juez otra vez— sin
tener que tocar cada nodo.

Esto es lo que permite la ampliación de observabilidad: saber cuánto cuesta una
consulta y comparar el antes/después (con y sin juez) sobre las mismas entradas.

`usage_metadata` no está garantizado en todos los proveedores; cuando falta se
intenta `llm_output["token_usage"]` y, si tampoco está, se cuentan las llamadas
igual. Un 0 en tokens no significa "gratis": significa "no informado".
"""

from langchain_core.callbacks import BaseCallbackHandler


class ContadorUso(BaseCallbackHandler):
    """Acumula tokens de entrada/salida y número de llamadas al modelo."""

    def __init__(self) -> None:
        super().__init__()
        self.llamadas = 0
        self.tokens_entrada = 0
        self.tokens_salida = 0
        self.modelos: set[str] = set()
        self.errores: list[str] = []

    # -- Callbacks de LangChain -------------------------------------------

    def on_llm_end(self, response, **kwargs) -> None:  # noqa: ANN001 - firma de LangChain
        """Se dispara al terminar cada llamada al modelo."""
        self.llamadas += 1
        if self._desde_generaciones(response) or self._desde_llm_output(response):
            return

    def on_llm_error(self, error: BaseException, **kwargs) -> None:  # noqa: ANN001
        """Registra el tipo de fallo; el flujo decide qué hacer con él."""
        self.errores.append(type(error).__name__)

    # -- Extracción de uso -------------------------------------------------

    def _desde_generaciones(self, response) -> bool:  # noqa: ANN001
        encontrado = False
        for grupo in getattr(response, "generations", []) or []:
            for generacion in grupo:
                mensaje = getattr(generacion, "message", None)
                uso = getattr(mensaje, "usage_metadata", None)
                if not uso:
                    continue
                self.tokens_entrada += int(uso.get("input_tokens") or 0)
                self.tokens_salida += int(uso.get("output_tokens") or 0)
                encontrado = True
                modelo = getattr(mensaje, "response_metadata", {}).get("model_name")
                if modelo:
                    self.modelos.add(str(modelo))
        return encontrado

    def _desde_llm_output(self, response) -> bool:  # noqa: ANN001
        salida = getattr(response, "llm_output", None) or {}
        uso = salida.get("token_usage") or salida.get("usage_metadata") or {}
        if not uso:
            return False
        self.tokens_entrada += int(uso.get("prompt_tokens") or uso.get("input_tokens") or 0)
        self.tokens_salida += int(uso.get("completion_tokens") or uso.get("output_tokens") or 0)
        if salida.get("model_name"):
            self.modelos.add(str(salida["model_name"]))
        return True

    # -- Salida ------------------------------------------------------------

    def resumen(self) -> dict:
        """Diccionario listo para guardar en el registro de ejecuciones."""
        return {
            "llm_llamadas": self.llamadas,
            "tokens_entrada": self.tokens_entrada,
            "tokens_salida": self.tokens_salida,
            "tokens_total": self.tokens_entrada + self.tokens_salida,
            "modelos": sorted(self.modelos),
            "llm_errores": sorted(set(self.errores)),
        }
