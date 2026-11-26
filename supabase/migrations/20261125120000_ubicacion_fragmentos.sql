-- Etiqueta de cita legible por fragmento.
--
-- Antes la ubicación se armaba en la consulta a partir de `fuente` + `pagina`,
-- lo que solo funcionaba para PDF. El corpus de este proyecto es un Markdown,
-- que no tiene páginas: la unidad de cita natural es la sección.
--
-- Con esta columna el cargador (`cargar_guia.py`) guarda la etiqueta ya
-- resuelta ("criptomonedas-desde-cero.md, §8 — Stablecoins") y la consulta la
-- usa tal cual. Se deja nullable para no romper índices cargados antes del
-- cambio: en ese caso la consulta cae al cálculo anterior.

alter table cripto.fragmentos
add column if not exists ubicacion text;