# Criptomonedas desde cero
## Manual de referencia para principiantes y base de conocimiento para agentes de IA

**Versión:** 1.0 — octubre de 2026
**Idioma:** español (Latinoamérica, con foco en Chile cuando aplica)
**Nivel:** de cero absoluto a intermedio

### Aviso general

Las criptomonedas son activos de alto riesgo y alta volatilidad. Su precio puede caer 50%, 70% o más en meses. Muchos proyectos han ido a cero. Exchanges grandes han quebrado con el dinero de sus clientes. Nada de lo escrito aquí es asesoría financiera, legal ni tributaria.

---

## Índice

**Parte I — Fundamentos**
1. El dinero y el problema que las criptomonedas intentan resolver
2. Qué es una blockchain y cómo funciona
3. Criptografía básica sin matemáticas
4. Bitcoin a fondo
5. Ethereum y los contratos inteligentes
6. Mecanismos de consenso: Proof of Work, Proof of Stake y otros

**Parte II — El ecosistema**
7. El mapa de las criptomonedas: categorías y principales redes
8. Stablecoins
9. Finanzas descentralizadas (DeFi)
10. NFTs y tokenización de activos reales
11. Escalabilidad, Layer 2 y puentes entre cadenas

**Parte III — La práctica**
12. Billeteras (wallets): tipos y cómo elegir
13. La frase semilla: el concepto más importante del manual
14. Exchanges: centralizados y descentralizados
15. Tu primera compra, paso a paso
16. Enviar y recibir: direcciones, redes y comisiones
17. Seguridad operativa
18. Estafas y fraudes: catálogo y cómo detectarlos

**Parte IV — Invertir con criterio**
19. Psicología del inversor y gestión de riesgo
20. Estrategias: DCA, holding, trading y sus trampas
21. Cómo analizar un proyecto: fundamentos y tokenomics
22. Análisis técnico básico
23. Análisis on-chain
24. Ciclos de mercado e historia de las grandes caídas

**Parte V — Marco legal y tributario**
25. Regulación en el mundo
26. Impuestos: principios generales y el caso de Chile

**Parte VI — Hacia dónde va esto**
27. Tendencias: ETFs, tokenización, CBDCs, IA y cripto

**Parte VII — Referencia**
28. Glosario
29. Preguntas frecuentes
30. Checklists y plantillas
31. Recursos para seguir aprendiendo

**Anexos**
- A. Casos prácticos resueltos
- B. Guía de respuestas para el agente
- C. Cronología resumida del ecosistema

---

# PARTE I — FUNDAMENTOS

---

# Capítulo 1. El dinero y el problema que las criptomonedas intentan resolver

## 1.1 Por qué empezar por el dinero

Mucha gente entra al mundo cripto por el precio: escuchó que Bitcoin subió, que un conocido ganó plata, que "hay que estar". Ese es el peor punto de partida, porque deja a la persona sin forma de distinguir un proyecto serio de una estafa. Para entender las criptomonedas primero hay que entender qué es el dinero y qué problemas tiene el sistema actual. Recién ahí se entiende qué intenta resolver Bitcoin, qué resuelve de verdad y qué no.

## 1.2 Las tres funciones del dinero

Los economistas coinciden en que el dinero cumple tres funciones:

1. **Medio de intercambio.** Sirve para comprar y vender cosas sin tener que hacer trueque. Sin dinero, un panadero que quiere zapatos tiene que encontrar a un zapatero que quiera pan, justo en ese momento.
2. **Unidad de cuenta.** Sirve para medir el valor de las cosas. Decimos que un café vale 3.000 pesos y un auto 15 millones. Eso permite comparar.
3. **Reserva de valor.** Sirve para guardar poder de compra en el tiempo. Si hoy ahorro, quiero poder comprar algo parecido en cinco años.

Un buen dinero cumple las tres. Ninguna criptomoneda las cumple todas de forma perfecta hoy, y eso es importante decirlo desde el inicio. Bitcoin funciona razonablemente como reserva de valor a largo plazo para quienes lo ven así, pero es demasiado volátil para ser buena unidad de cuenta. Las stablecoins (monedas estables atadas al dólar) funcionan bien como medio de intercambio, pero su valor depende de un emisor centralizado.

## 1.3 Las propiedades de un buen dinero

Además de las funciones, el dinero tiene propiedades deseables:

| Propiedad | Qué significa | Oro | Peso/dólar | Bitcoin |
|---|---|---|---|---|
| Escasez | No se puede crear de la nada | Alta | Baja (el banco central emite) | Muy alta (máximo 21 millones) |
| Divisibilidad | Se puede partir en unidades pequeñas | Media | Alta | Muy alta (8 decimales) |
| Portabilidad | Fácil de transportar | Baja | Alta (digital) | Muy alta |
| Durabilidad | No se deteriora | Muy alta | Media (billetes) / Alta (digital) | Alta mientras la red funcione |
| Fungibilidad | Una unidad es igual a otra | Alta | Alta | Media (las monedas tienen historial rastreable) |
| Verificabilidad | Fácil comprobar que es auténtico | Media | Alta | Muy alta (matemática) |
| Aceptación | Mucha gente lo recibe | Media | Muy alta | Baja |

La tabla muestra algo honesto: Bitcoin destaca en escasez, portabilidad y verificabilidad, pero pierde en aceptación y estabilidad.

## 1.4 Breve historia del dinero

- **Trueque.** Funciona en comunidades pequeñas. Escala mal.
- **Dinero mercancía.** Sal, conchas, ganado, metales. El valor está en el objeto mismo.
- **Monedas metálicas.** Oro y plata acuñados. El estado garantiza peso y pureza.
- **Papel respaldado.** Un billete era un recibo canjeable por oro guardado en un banco.
- **Dinero fiduciario (fiat).** Desde 1971, cuando Estados Unidos terminó la convertibilidad del dólar en oro, el dinero de casi todos los países no está respaldado por nada físico. Vale porque el Estado lo declara de curso legal, porque se exige para pagar impuestos y porque la gente confía en que otros lo aceptarán.
- **Dinero digital bancario.** Hoy la mayor parte del dinero no existe como billetes, sino como registros en bases de datos de bancos. Cuando haces una transferencia, ningún billete se mueve: se modifican dos registros.

Ese último punto es clave. **El dinero moderno ya es digital.** Lo que cambia con las criptomonedas no es que el dinero sea digital, sino **quién lleva el registro**.

## 1.5 El problema del doble gasto

Un archivo digital se puede copiar. Si te mando una foto, yo sigo teniéndola. Si el dinero fuera un simple archivo, podría "gastar" el mismo archivo dos veces. Esto se llama **problema del doble gasto**.

Hasta 2008, la única solución práctica era tener un **intermediario de confianza**: un banco, una procesadora de tarjetas, PayPal. Ese intermediario lleva el registro oficial y verifica que no gastes lo que no tienes.

Funciona, pero tiene costos:

- **Hay que confiar en el intermediario.** Puede quebrar, congelar tu cuenta, equivocarse o ser hackeado.
- **Puede censurar.** Puede negarse a procesar un pago por razones políticas, comerciales o de cumplimiento.
- **Cobra comisiones** y fija horarios (piensa en transferencias internacionales que demoran días).
- **Excluye.** Según el Banco Mundial, cientos de millones de adultos en el mundo no tienen cuenta bancaria **[VERIFICAR cifra actual]**.

## 1.6 La propuesta de Bitcoin

En octubre de 2008, alguien con el seudónimo **Satoshi Nakamoto** publicó un documento de nueve páginas: *"Bitcoin: A Peer-to-Peer Electronic Cash System"* (Bitcoin: un sistema de efectivo electrónico de persona a persona). La idea central: **resolver el doble gasto sin intermediario**, haciendo que miles de computadoras independientes mantengan una copia del mismo registro y se pongan de acuerdo sobre su contenido mediante reglas matemáticas y económicas.

El contexto importa. El documento salió en plena crisis financiera de 2008, cuando los bancos rescatados con dinero público eran el tema del día. En el primer bloque de Bitcoin (el "bloque génesis", minado el 3 de enero de 2009), Satoshi incluyó un titular del diario británico *The Times* sobre un segundo rescate bancario. Se interpreta como una declaración de intenciones.

Nadie sabe quién es Satoshi. Dejó de comunicarse públicamente en 2011. Se estima que controla alrededor de un millón de bitcoins que nunca se han movido.

## 1.7 Qué resuelven las criptomonedas y qué no

**Lo que sí resuelven (o intentan):**

- Transferir valor entre personas sin pedir permiso a nadie.
- Tener un activo cuya oferta total es conocida y no puede ser alterada por un gobierno o empresa (en el caso de Bitcoin).
- Custodiar tu propio dinero sin depender de un banco.
- Mover valor a través de fronteras las 24 horas, todos los días.
- Crear aplicaciones financieras programables (préstamos, intercambios) que funcionan con código en vez de oficinas.

**Lo que no resuelven, o empeoran:**

- **Volatilidad.** El precio sube y baja con violencia. Mala unidad de cuenta.
- **Responsabilidad total.** Si pierdes tu clave, nadie te ayuda. No hay "olvidé mi contraseña".
- **Irreversibilidad.** Si te estafan, no hay contracargo.
- **Estafas.** El ecosistema está lleno de fraudes que aprovechan la ignorancia técnica.
- **Complejidad.** El uso seguro requiere conocimientos que la mayoría de la gente no tiene.
- **Concentración.** Aunque la tecnología es descentralizada, gran parte del uso real pasa por unos pocos exchanges centralizados.

## 1.8 Criptomoneda, token, criptoactivo: aclarando palabras

- **Criptomoneda:** la moneda nativa de una blockchain. BTC en Bitcoin, ETH en Ethereum, SOL en Solana. Se usa para pagar comisiones de la red.
- **Token:** un activo creado *encima* de una blockchain existente, usando contratos inteligentes. USDC es un token que vive en Ethereum (y otras redes). No tiene blockchain propia.
- **Criptoactivo / activo digital:** término paraguas que usan reguladores para todo lo anterior.
- **Altcoin:** cualquier criptomoneda que no sea Bitcoin.
- **Shitcoin / memecoin:** términos informales para tokens sin utilidad real, muchas veces creados como broma o para especular.

En la conversación diaria se usan como sinónimos, y no pasa nada. Pero cuando se habla de regulación o impuestos, la diferencia puede importar.

## 1.9 Ideas clave del capítulo

- El dinero moderno ya es digital; la novedad de cripto es **quién lleva el registro**.
- Bitcoin resolvió el doble gasto sin intermediario por primera vez.
- Las criptomonedas cambian "confiar en un banco" por "confiar en matemática + responsabilidad personal total".
- Ninguna cripto cumple hoy todas las funciones del dinero de forma perfecta.

---

# Capítulo 2. Qué es una blockchain y cómo funciona

## 2.1 La definición corta

Una **blockchain** (cadena de bloques) es un **registro compartido de transacciones**, copiado en miles de computadoras, que se actualiza agregando "bloques" de transacciones nuevas, y donde cada bloque está matemáticamente encadenado al anterior, de modo que alterar el pasado es prácticamente imposible.

## 2.2 La analogía del cuaderno compartido

Imagina un barrio donde nadie confía en un banco. Deciden llevar un cuaderno con todas las deudas y pagos. Pero si una sola persona guarda el cuaderno, puede hacer trampa. Entonces:

1. **Todos tienen una copia del cuaderno.**
2. Cuando alguien paga, lo anuncia a todo el barrio: "Ana le paga 5 a Bruno".
3. Cada cierto tiempo, alguien junta los anuncios recientes en una página nueva.
4. Antes de agregar la página, todos verifican que Ana efectivamente tenía 5 para pagar.
5. Cada página nueva incluye un "sello" que depende del contenido de la página anterior. Si alguien cambia una página vieja, el sello deja de cuadrar y todos lo notan.
6. Para que nadie escriba páginas falsas a voluntad, escribir una página cuesta algo (trabajo, o dinero puesto en garantía).

Eso es una blockchain. Las "páginas" son los bloques. El "sello" es un hash. El "costo de escribir" es el mecanismo de consenso.

## 2.3 Los componentes

### Transacciones
Una transacción es una instrucción firmada: "mueve X unidades desde esta dirección a esta otra". La firma prueba que quien la envía controla los fondos (ver capítulo 3).

### Bloques
Un bloque es un paquete de transacciones más un encabezado. El encabezado contiene, entre otras cosas:
- El **hash del bloque anterior** (esto es lo que forma la "cadena").
- Una marca de tiempo.
- Un resumen de todas las transacciones del bloque (raíz de Merkle).
- En Bitcoin, un número llamado **nonce** que usan los mineros.

### Nodos
Un **nodo** es una computadora que ejecuta el software de la red y guarda una copia de la blockchain. Los nodos:
- Reciben transacciones y las retransmiten.
- Verifican que cada transacción y cada bloque cumplan las reglas.
- Rechazan lo que no cumpla.

Cualquier persona puede correr un nodo de Bitcoin en una computadora común. Eso es lo que lo hace difícil de controlar: no hay un servidor central que apagar.

### Mempool
Es la "sala de espera" de transacciones que fueron anunciadas pero todavía no están en un bloque. Cuando la red está congestionada, la mempool crece y las comisiones suben.

### Consenso
Las reglas que determinan **quién escribe el próximo bloque** y **cuál es la versión válida** de la cadena si hay desacuerdo. Se detalla en el capítulo 6.

## 2.4 Cómo viaja una transacción, paso a paso

Ejemplo: Ana envía 0,01 BTC a Bruno.

1. Ana abre su billetera y escribe la dirección de Bruno y el monto.
2. La billetera arma la transacción y la **firma** con la clave privada de Ana. La clave nunca sale de la billetera.
3. La transacción se envía a uno o varios nodos.
4. Los nodos verifican: ¿la firma es válida? ¿Ana tiene esos fondos? ¿no los gastó ya? Si todo cuadra, la pasan a otros nodos. En segundos, miles de nodos la conocen.
5. La transacción espera en la mempool.
6. Un minero (o validador) la incluye en un bloque candidato, normalmente priorizando las que pagan más comisión.
7. El bloque se agrega a la cadena. La transacción tiene **1 confirmación**.
8. Cada bloque nuevo encima suma una confirmación más. En Bitcoin, 6 confirmaciones (≈ 1 hora) se consideran prácticamente irreversibles para montos grandes.

## 2.5 Por qué es tan difícil alterar el pasado

Cada bloque contiene el hash del anterior. Un hash es como una huella digital del contenido: si cambias una coma, el hash cambia completamente.

Si alguien modifica una transacción en el bloque 100:
- El hash del bloque 100 cambia.
- El bloque 101, que guardaba el hash viejo del 100, queda inválido.
- Tendría que rehacer el 101, el 102, y todos los siguientes.
- Y tendría que hacerlo **más rápido que todo el resto de la red junta**, que sigue agregando bloques.

En Bitcoin, rehacer bloques requiere una cantidad enorme de energía y equipos. Por eso decimos que la blockchain es **inmutable en la práctica**, no en teoría absoluta.

## 2.6 Propiedades que importan

- **Descentralización:** no hay un dueño único. Varía mucho según la red.
- **Inmutabilidad:** lo escrito no se borra.
- **Transparencia:** en la mayoría de blockchains públicas, cualquiera puede ver todas las transacciones. Esto es importante: **Bitcoin no es anónimo, es seudónimo**. Las direcciones no llevan tu nombre, pero si alguien vincula una dirección contigo (por ejemplo, porque compraste en un exchange con verificación de identidad), puede rastrear el historial.
- **Sin permiso (permissionless):** cualquiera puede usarla sin pedir autorización.
- **Resistencia a la censura:** es difícil impedir que una transacción válida se procese.

## 2.7 Blockchains públicas vs. privadas

| | Pública | Privada / permisionada |
|---|---|---|
| Quién puede participar | Cualquiera | Solo invitados |
| Ejemplos | Bitcoin, Ethereum, Solana | Hyperledger Fabric, redes corporativas |
| Token nativo | Sí, normalmente | Muchas veces no |
| Uso típico | Dinero, DeFi, aplicaciones abiertas | Trazabilidad, consorcios empresariales |

Muchos proyectos corporativos de "blockchain" entre 2016 y 2020 eran en realidad bases de datos compartidas que no necesitaban blockchain. Una pregunta útil para evaluar cualquier propuesta: **¿hay varias partes que no confían entre sí y necesitan un registro común sin un administrador central?** Si la respuesta es no, probablemente una base de datos normal es mejor.

## 2.8 El trilema de la blockchain

Vitalik Buterin (cofundador de Ethereum) popularizó la idea de que una blockchain tiene dificultad para lograr a la vez tres cosas:

1. **Seguridad**
2. **Descentralización**
3. **Escalabilidad** (muchas transacciones por segundo, baratas)

Bitcoin prioriza seguridad y descentralización, y sacrifica escalabilidad (unas 7 transacciones por segundo en la capa base). Otras redes, como Solana, procesan miles de transacciones por segundo, pero requieren nodos con hardware caro, lo que reduce cuántas personas pueden operarlos. Las soluciones de capa 2 (capítulo 11) intentan escapar del trilema.

## 2.9 Ideas clave del capítulo

- Una blockchain es un registro compartido, encadenado con hashes y mantenido por muchos nodos.
- Alterar el pasado requiere rehacer todos los bloques posteriores más rápido que el resto de la red.
- Las blockchains públicas son transparentes: Bitcoin es seudónimo, no anónimo.
- No todo problema necesita blockchain.

---

# Capítulo 3. Criptografía básica sin matemáticas

## 3.1 Por qué hay que entender esto

No necesitas saber matemáticas para usar criptomonedas. Pero sí necesitas entender **tres ideas**: hash, par de claves y firma digital. Casi todos los errores graves que comete un principiante (perder fondos, caer en estafas) vienen de no entender qué es una clave privada.

## 3.2 Funciones hash

Una función hash toma cualquier dato (una palabra, un libro, un video) y devuelve una "huella" de largo fijo. Bitcoin usa SHA-256, que devuelve 64 caracteres hexadecimales.

Propiedades:
- **Determinista:** el mismo dato siempre da el mismo hash.
- **Rápida de calcular.**
- **Irreversible:** con el hash no puedes reconstruir el dato original.
- **Efecto avalancha:** un cambio mínimo cambia el hash por completo.
- **Resistente a colisiones:** es prácticamente imposible encontrar dos datos distintos con el mismo hash.

Ejemplo ilustrativo (los valores son reales para SHA-256):
- "hola" → `b221d9dbb083a7f33428d7c2a3c3198ae925614d70210e28716ccaa7cd4ddb79`
- "Hola" → un hash completamente diferente.

**Usos en cripto:** encadenar bloques, minería, generar direcciones, verificar integridad.

## 3.3 Criptografía de clave pública (asimétrica)

Funciona con un **par de claves** matemáticamente relacionadas:

- **Clave privada:** un número secreto enorme. Es literalmente la propiedad de tus fondos. Quien la tiene, controla el dinero.
- **Clave pública:** se deriva de la privada. Se puede compartir sin riesgo.
- **Dirección:** una versión abreviada y codificada de la clave pública (pasada por hash). Es lo que compartes para recibir fondos.

La relación es de un solo sentido:

```
Clave privada  →  Clave pública  →  Dirección
   (secreta)        (pública)        (pública)
      ✗ no se puede ir hacia atrás ✗
```

### La analogía del buzón
- La **dirección** es la ranura del buzón: cualquiera puede meter cartas (enviarte dinero).
- La **clave privada** es la llave del buzón: solo quien la tiene puede sacar las cartas (gastar el dinero).

### Qué tan grande es una clave privada
Una clave privada de Bitcoin es un número entre 1 y aproximadamente 2^256. Eso es un número con 78 dígitos, comparable al número estimado de átomos en el universo observable. Adivinar una clave ajena por fuerza bruta es imposible con la tecnología actual. **Nadie va a "hackear" Bitcoin adivinando tu clave. Lo que sí pasa es que te engañen para que la entregues.**

## 3.4 Firmas digitales

Cuando envías cripto, tu billetera usa la clave privada para **firmar** la transacción. La firma:

- Prueba que quien envía tiene la clave privada, **sin revelar la clave**.
- Está atada al contenido exacto de la transacción: si alguien cambia el monto o el destino, la firma deja de ser válida.
- Cualquiera puede verificarla usando la clave pública.

Bitcoin usa los algoritmos ECDSA y, desde la actualización Taproot (2021), también firmas Schnorr.

## 3.5 Frase semilla: la clave privada en formato humano

Una clave privada en formato crudo se ve así: `E9873D79C6D87DC0FB6A5778633389F4453213303DA61F20BD67FC233AA33262`. Imposible de anotar sin errores.

Por eso existe el estándar **BIP-39**: representa la información de la que se derivan tus claves con **12 o 24 palabras** de una lista oficial de 2.048 palabras. Ejemplo (inventado, no usar):

`trigo lámpara océano ... (12 palabras)`

Detalles importantes:
- Con una sola frase semilla se pueden generar millones de claves y direcciones (estándar BIP-32/44, "billeteras jerárquicas deterministas").
- La lista oficial existe en varios idiomas, incluido español, pero **la mayoría de las billeteras usan la lista en inglés**. Lo más seguro es usar inglés porque es compatible con todo.
- La última palabra incluye un "checksum": no cualquier combinación de 12 palabras es válida.
- Se puede agregar una **passphrase** (palabra 13/25) opcional que actúa como contraseña extra.

Todo el capítulo 13 está dedicado a la frase semilla porque es el punto más crítico de la seguridad.

## 3.6 "Not your keys, not your coins"

La frase más repetida en el mundo cripto: **"si no son tus llaves, no son tus monedas"**.

Si tienes Bitcoin en un exchange, el exchange tiene las claves privadas. Tú tienes una promesa del exchange de que te debe esos bitcoins. Si el exchange quiebra, es hackeado o te congela la cuenta, tu "saldo" puede desaparecer. Esto pasó con Mt. Gox (2014), QuadrigaCX (2019), FTX (2022) y muchos otros.

Eso no significa que nunca debas usar un exchange. Significa que debes saber que **un saldo en exchange es un crédito contra una empresa, no propiedad directa de cripto**.

## 3.7 Computación cuántica: ¿una amenaza?

Una pregunta frecuente. Respuesta corta:
- Una computadora cuántica suficientemente potente podría, en teoría, derivar claves privadas a partir de claves públicas expuestas (algoritmo de Shor).
- Hoy no existe una máquina capaz de hacerlo a la escala necesaria **[VERIFICAR estado del arte]**.
- Las direcciones cuya clave pública nunca se ha revelado (porque nunca han enviado fondos) tienen una capa extra de protección por el hash.
- La comunidad de Bitcoin y Ethereum discute propuestas de firmas "post-cuánticas". Una migración así tomaría años y requeriría consenso.

Es un riesgo real a largo plazo, no una emergencia de hoy para el usuario común.

## 3.8 Ideas clave del capítulo

- **Quien tiene la clave privada, tiene el dinero.** No hay otra forma de propiedad.
- La frase semilla de 12/24 palabras es tu clave privada en formato humano.
- Nadie adivina claves por fuerza bruta. Los robos ocurren por engaño, malware o descuido.
- Un saldo en un exchange no es propiedad directa: es una deuda del exchange contigo.

---

# Capítulo 4. Bitcoin a fondo

## 4.1 Qué es Bitcoin

Bitcoin es dos cosas con el mismo nombre:
- **Bitcoin (con mayúscula):** la red, el protocolo, el software.
- **bitcoin o BTC (minúscula o ticker):** la unidad monetaria que circula en esa red.

Fue la primera criptomoneda, sigue siendo la de mayor capitalización de mercado y es la referencia de todo el sector. Cuando Bitcoin cae, casi todo cae.

## 4.2 Datos esenciales

| Característica | Valor |
|---|---|
| Lanzamiento | 3 de enero de 2009 |
| Creador | Satoshi Nakamoto (seudónimo) |
| Oferta máxima | 21.000.000 BTC |
| Unidad mínima | 1 satoshi (sat) = 0,00000001 BTC |
| Tiempo entre bloques | ~10 minutos en promedio |
| Consenso | Proof of Work (SHA-256) |
| Halving | Cada 210.000 bloques (~4 años) |
| Último halving | Abril de 2024 (recompensa: 3,125 BTC por bloque) |
| Próximo halving estimado | ~2028 **[VERIFICAR fecha]** |

## 4.3 La política monetaria fija

Este es el punto que más diferencia a Bitcoin de cualquier moneda estatal.

- Los bitcoins nuevos se crean solo como **recompensa a los mineros** por cada bloque.
- La recompensa empezó en 50 BTC por bloque y se **reduce a la mitad cada 210.000 bloques** (el "halving"):

| Período | Recompensa por bloque |
|---|---|
| 2009–2012 | 50 BTC |
| 2012–2016 | 25 BTC |
| 2016–2020 | 12,5 BTC |
| 2020–2024 | 6,25 BTC |
| 2024–2028 | 3,125 BTC |
| 2028–2032 | 1,5625 BTC |

- Alrededor del año 2140 se emitirá el último satoshi. A partir de ahí, los mineros solo cobrarán comisiones.
- Más del 90% de todos los bitcoins que existirán ya fueron emitidos.

¿Se puede cambiar el límite de 21 millones? Técnicamente es software, así que sí podría modificarse. En la práctica, requeriría que la gran mayoría de nodos, mineros, exchanges y usuarios aceptaran una versión nueva que diluye su propio patrimonio. Es socialmente casi imposible, y esa rigidez es justamente lo que la gente valora.

### Bitcoins perdidos
Se estima que entre 3 y 4 millones de BTC están perdidos para siempre (claves olvidadas, discos duros botados, fallecidos sin herencia) **[estimación, varía por fuente]**. La oferta efectiva es menor a 21 millones.

## 4.4 Minería

### Qué hacen los mineros
1. Juntan transacciones de la mempool en un bloque candidato.
2. Prueban miles de millones de valores para el *nonce* hasta encontrar uno que haga que el hash del bloque empiece con cierta cantidad de ceros (más técnicamente: que sea menor que un "objetivo").
3. El primero que lo encuentra transmite el bloque. Los nodos verifican (verificar es instantáneo, encontrar es carísimo) y lo aceptan.
4. El minero ganador cobra la recompensa del bloque más las comisiones.

### Ajuste de dificultad
Cada 2.016 bloques (~2 semanas), la red ajusta la dificultad para que los bloques sigan saliendo cada ~10 minutos, sin importar cuántos mineros se sumen o se vayan. Si entra más poder de cómputo, la dificultad sube.

### La industria hoy
- La minería se hace con máquinas especializadas llamadas **ASIC**. Minar con un computador personal ya no es rentable.
- Los mineros se agrupan en **pools** para recibir ingresos más estables.
- La rentabilidad depende del precio de BTC, el costo de electricidad y la eficiencia de los equipos.
- El consumo energético es alto y es una crítica frecuente. Los defensores responden que parte importante usa energía renovable o excedente que de otro modo se desperdiciaría. El debate sigue abierto.

## 4.5 El modelo UTXO

Bitcoin no lleva "saldos" como un banco. Lleva **salidas de transacciones no gastadas** (UTXO, por sus siglas en inglés).

Analogía: tu billetera física. No tienes "un saldo de 15.000 pesos", tienes un billete de 10.000 y uno de 5.000. Si pagas algo de 7.000, entregas el de 10.000 y recibes 3.000 de vuelto.

En Bitcoin:
- Si recibiste 0,5 BTC en una transacción y 0,3 BTC en otra, tienes dos UTXO.
- Para enviar 0,6 BTC, tu billetera usa ambas (0,8 total), envía 0,6 al destino, paga una comisión y se devuelve el resto a una **dirección de cambio** tuya.

Consecuencias prácticas:
- Tu billetera puede mostrar direcciones nuevas cada vez: es normal.
- Muchas UTXO pequeñas encarecen las transacciones futuras (más datos = más comisión).

## 4.6 Tipos de direcciones

| Prefijo | Tipo | Nota |
|---|---|---|
| `1...` | Legacy (P2PKH) | Las más antiguas. Comisiones más altas. |
| `3...` | P2SH | Usadas para multifirma y SegWit compatible. |
| `bc1q...` | SegWit nativo (Bech32) | Estándar actual, comisiones menores. |
| `bc1p...` | Taproot | Más reciente, más privacidad y eficiencia. |

Todas son compatibles entre sí para enviar y recibir.

## 4.7 Comisiones

- Se pagan en función del **tamaño en datos** de la transacción (en vbytes), no del monto enviado. Enviar 1.000 dólares o 1 millón de dólares puede costar lo mismo.
- Se miden en **sat/vB** (satoshis por byte virtual).
- Cuando hay congestión, sube el precio. Sitios como mempool.space muestran la tarifa recomendada en tiempo real.
- Si pagas muy poco, tu transacción puede quedar atascada horas o días.

## 4.8 Lightning Network

Bitcoin en su capa base es lento y caro para pagos pequeños. **Lightning** es una red de "capa 2" construida encima:

- Dos partes abren un **canal de pago** bloqueando BTC en una transacción en la blockchain.
- Dentro del canal pueden hacer miles de pagos instantáneos y casi gratis, sin tocar la blockchain.
- Los canales se conectan entre sí, formando una red: puedes pagar a alguien con quien no tienes canal directo.
- Al cerrar el canal, se registra el saldo final en la blockchain.

Usos: micropagos, propinas, pagos en comercios. Billeteras como Phoenix, Breez o Wallet of Satoshi **[VERIFICAR disponibilidad]** facilitan su uso. Algunos exchanges ya permiten retirar por Lightning.

Limitaciones: requiere que la billetera esté en línea para recibir (o usar servicios intermedios), y las billeteras más simples son custodiales.

## 4.9 Hitos de la historia de Bitcoin

- **2008:** publicación del whitepaper.
- **2009:** bloque génesis. Primera transacción: Satoshi envía 10 BTC a Hal Finney.
- **2010:** "Bitcoin Pizza Day". Laszlo Hanyecz paga 10.000 BTC por dos pizzas (22 de mayo). Primera compra documentada de un bien físico.
- **2011–2013:** Silk Road (mercado ilegal) usa BTC. Primera gran burbuja.
- **2014:** colapso de Mt. Gox, el mayor exchange de la época. Se pierden ~850.000 BTC.
- **2017:** "guerra del tamaño de bloque". Se activa SegWit. Nace Bitcoin Cash como bifurcación. Burbuja hasta casi 20.000 USD.
- **2020–2021:** empresas (MicroStrategy, Tesla) compran BTC. Máximo cercano a 69.000 USD.
- **2021:** El Salvador lo declara moneda de curso legal (luego, en 2025, flexibilizó esa obligación como parte de un acuerdo con el FMI). Activación de Taproot.
- **2022:** caída fuerte por colapsos de Terra/Luna, Celsius y FTX.
- **2024:** la SEC de EE.UU. aprueba **ETFs de Bitcoin al contado** (enero). Halving (abril). Supera los 100.000 USD en diciembre.
- **2025:** EE.UU. crea una reserva estratégica de bitcoin a partir de activos incautados; se aprueba la ley GENIUS sobre stablecoins (julio).
- **2026:** mercado con ETFs consolidados e institucionales relevantes; debate regulatorio en EE.UU. centrado en la ley CLARITY **[VERIFICAR estado]**.

## 4.10 Bifurcaciones (forks)

- **Soft fork:** cambio compatible hacia atrás. Los nodos viejos siguen funcionando. Ejemplos: SegWit, Taproot.
- **Hard fork:** cambio incompatible. Si una parte de la comunidad no lo adopta, la cadena se divide en dos. Ejemplo: Bitcoin Cash (2017), que se separó por querer bloques más grandes.

Cuando hay un hard fork, quienes tenían BTC antes de la división normalmente reciben la misma cantidad de la moneda nueva. Históricamente, las bifurcaciones han perdido valor frente a la cadena original.

## 4.11 Críticas frecuentes a Bitcoin (y respuestas habituales)

| Crítica | Respuesta de los defensores | Comentario |
|---|---|---|
| "No tiene valor intrínseco" | Ningún dinero lo tiene; vale por escasez y red | Debate filosófico abierto |
| "Consume mucha energía" | Incentiva renovables y estabiliza redes | Ambas partes tienen datos a favor |
| "Se usa para delitos" | El efectivo se usa más; la blockchain es rastreable | Los informes de análisis on-chain muestran que la actividad ilícita es una fracción pequeña del total [VERIFICAR cifras] |
| "Es demasiado volátil" | La volatilidad ha bajado con los años | Sigue siendo muy alta comparada con acciones |
| "Es lento" | Lightning resuelve pagos rápidos | Lightning tiene sus propias limitaciones |
| "Es una burbuja" | Ha sobrevivido varias caídas de 70-80% | Rendimiento pasado no garantiza nada |

## 4.12 Ideas clave del capítulo

- 21 millones máximo; el halving reduce la emisión cada ~4 años.
- La minería asegura la red; el ajuste de dificultad mantiene los bloques cada ~10 min.
- Las comisiones dependen del tamaño de la transacción, no del monto.
- Lightning permite pagos rápidos y baratos sobre Bitcoin.

---

# Capítulo 5. Ethereum y los contratos inteligentes

## 5.1 Qué es Ethereum

Si Bitcoin es "dinero digital", Ethereum es una **computadora mundial**: una blockchain donde, además de mover dinero, se pueden ejecutar programas. Fue propuesto por Vitalik Buterin en 2013 y lanzado en 2015.

Su moneda nativa es el **ether (ETH)**, que se usa para pagar el "gas" (las comisiones por ejecutar operaciones).

## 5.2 Contratos inteligentes

Un **contrato inteligente** (smart contract) es un programa que vive en la blockchain y se ejecuta automáticamente cuando se cumplen ciertas condiciones. No es "inteligente" ni es un "contrato" legal; es código.

Ejemplo simple:
> "Si alguien deposita 1 ETH en este contrato, enviarle 3.000 unidades de un token X."

Ejemplo más complejo:
> "Si alguien deposita ETH como garantía, prestarle hasta el 70% de su valor en stablecoins. Si el valor del ETH cae y la garantía baja del 80%, vender la garantía automáticamente para pagar el préstamo."

Propiedades:
- **Público:** cualquiera puede leer el código.
- **Inmutable por defecto:** una vez desplegado, no se puede cambiar (aunque hay patrones de "contratos actualizables" que lo permiten, lo cual implica confiar en quien controla esa actualización).
- **Determinista:** con los mismos datos, siempre da el mismo resultado.
- **Sin intermediario:** nadie puede impedir que se ejecute si se cumplen las condiciones.

**Riesgo principal:** si el código tiene un error, el error se ejecuta igual. Miles de millones de dólares se han perdido por bugs en contratos inteligentes.

## 5.3 La Ethereum Virtual Machine (EVM)

La EVM es el "motor" que ejecuta los contratos. Su importancia práctica: muchas otras blockchains copiaron la EVM para ser compatibles (BNB Chain, Polygon, Avalanche C-Chain, Arbitrum, Base, Optimism, etc.). Por eso:

- Una billetera como MetaMask funciona en todas ellas.
- **Tu dirección es la misma en todas las redes EVM** (empieza con `0x...`). Esto genera confusión: el mismo `0x...` puede tener saldos distintos en Ethereum, en Base y en Arbitrum.

## 5.4 Gas: las comisiones de Ethereum

- Cada operación cuesta una cantidad de **gas** (unidad de trabajo computacional). Una transferencia simple de ETH cuesta 21.000 gas; una operación DeFi compleja puede costar 200.000 o más.
- El **precio del gas** se mide en *gwei* (1 gwei = 0,000000001 ETH).
- Comisión total ≈ gas usado × precio del gas.
- Desde la actualización EIP-1559 (2021), cada transacción paga una **tarifa base** que se **quema** (se destruye) más una **propina** opcional al validador.
- Si la transacción falla (por ejemplo, por error del contrato), **igual pagas el gas consumido**.

En la red principal de Ethereum, las comisiones pueden ser altas en momentos de congestión. Por eso gran parte de la actividad migró a redes de capa 2 (capítulo 11), donde cuestan centavos.

## 5.5 Política monetaria de ETH

A diferencia de Bitcoin, **ETH no tiene un tope máximo fijo**.

- Se emite ETH nuevo como recompensa a los validadores.
- Se quema ETH con cada transacción (EIP-1559).
- Si la actividad es alta, se quema más de lo que se emite y la oferta baja ("deflacionario"). Si la actividad es baja, la oferta sube levemente.

En la práctica, desde 2022 la oferta total se ha mantenido relativamente estable **[VERIFICAR tendencia actual; con la migración a capa 2, la quema en capa 1 bajó]**.

## 5.6 The Merge: de Proof of Work a Proof of Stake

En septiembre de 2022, Ethereum cambió su mecanismo de consenso de minería (Proof of Work) a **Proof of Stake**. Se le llamó "The Merge". Efectos:
- El consumo energético bajó más de 99%.
- La emisión de ETH nuevo bajó cerca de 90%.
- Los mineros fueron reemplazados por **validadores**, que bloquean 32 ETH como garantía.

Cualquier persona puede participar del staking, directamente (con 32 ETH y un nodo propio) o mediante servicios de staking líquido o exchanges (ver capítulo 9).

## 5.7 Tokens en Ethereum: estándares

- **ERC-20:** tokens fungibles (todas las unidades son iguales). La mayoría de los tokens y stablecoins (USDC, USDT en su versión Ethereum, UNI, LINK) son ERC-20.
- **ERC-721:** tokens no fungibles (NFT). Cada uno es único.
- **ERC-1155:** permite ambos tipos en un solo contrato (muy usado en juegos).
- **ERC-4626:** estándar para "bóvedas" que generan rendimiento.

Crear un token ERC-20 toma minutos y cuesta muy poco. **Esto explica por qué hay millones de tokens y por qué la gran mayoría no vale nada.**

## 5.8 Aprobaciones (approvals): un riesgo que pocos conocen

Para que una aplicación (por ejemplo, un exchange descentralizado) pueda mover tus tokens ERC-20, primero debes **aprobarla**. Muchas aplicaciones piden aprobación "ilimitada" por comodidad.

Riesgo: si ese contrato es malicioso o es hackeado después, puede vaciar esos tokens de tu billetera **sin que firmes nada más**.

Buenas prácticas:
- Aprobar solo el monto necesario cuando la billetera lo permita.
- Revisar y revocar aprobaciones viejas periódicamente con herramientas como Revoke.cash o el revisor de aprobaciones de Etherscan.
- Desconfiar de cualquier sitio que pida aprobaciones o firmas que no entiendes.

## 5.9 Qué se ha construido sobre Ethereum

- **DeFi:** exchanges descentralizados (Uniswap), préstamos (Aave), stablecoins descentralizadas (DAI/USDS).
- **Stablecoins:** buena parte del USDC y USDT del mundo circula en Ethereum y sus capas 2.
- **NFTs:** arte digital, coleccionables, entradas.
- **DAOs:** organizaciones gobernadas por votación con tokens.
- **Tokenización:** fondos de bonos del Tesoro de EE.UU. tokenizados (como BUIDL de BlackRock), que usan Ethereum.
- **Identidad y nombres:** ENS (nombres tipo `carlos.eth`).

## 5.10 Ideas clave del capítulo

- Ethereum ejecuta programas (contratos inteligentes); ETH paga el gas.
- La compatibilidad EVM hace que tu dirección `0x...` sea la misma en muchas redes, con saldos distintos en cada una.
- Las transacciones fallidas igual cobran gas.
- Revisa y revoca aprobaciones de tokens: es una puerta de robo frecuente.

---

# Capítulo 6. Mecanismos de consenso

## 6.1 El problema que resuelven

En una red sin jefe, miles de computadoras deben ponerse de acuerdo sobre **qué transacciones son válidas y en qué orden ocurrieron**. Algunas de esas computadoras pueden fallar o mentir. El mecanismo de consenso es el conjunto de reglas que hace que la red llegue a un acuerdo de todos modos, y que hacer trampa sea más caro que jugar limpio.

Este problema se conoce en informática como el **problema de los generales bizantinos**.

## 6.2 Proof of Work (prueba de trabajo)

**Quién escribe el siguiente bloque:** el que primero resuelve un acertijo matemático que solo se puede resolver probando al azar (gastando electricidad).

**Por qué es seguro:** para reescribir la historia, un atacante necesitaría más del 50% del poder de cómputo total de la red ("ataque del 51%"). En Bitcoin, eso implica inversiones de miles de millones de dólares en equipos y energía, y si el ataque se nota, el precio de BTC caería, destruyendo el valor de la propia inversión del atacante.

**Ventajas:**
- Probado en batalla desde 2009.
- El costo de atacar es físico y externo (energía, hardware).
- Distribución inicial de monedas relativamente abierta (cualquiera podía minar).

**Desventajas:**
- Alto consumo energético.
- Tiende a concentrarse en grandes operaciones y pools.

**Redes que lo usan:** Bitcoin, Litecoin, Dogecoin, Monero, Bitcoin Cash.

## 6.3 Proof of Stake (prueba de participación)

**Quién escribe el siguiente bloque:** un validador elegido (con algo de azar) entre quienes han bloqueado ("stakeado") monedas como garantía. Más monedas bloqueadas, más probabilidad de ser elegido.

**Por qué es seguro:** si un validador intenta hacer trampa (por ejemplo, firmar dos versiones distintas de un bloque), la red le **destruye parte de su garantía**. Esto se llama **slashing**.

**Ventajas:**
- Consumo energético mínimo.
- Permite a cualquiera ganar rendimiento por asegurar la red.

**Desventajas:**
- "El rico se hace más rico": quien tiene más monedas gana más recompensas.
- Riesgo de concentración en grandes custodios (exchanges, servicios de staking líquido).
- Menos años de historia que PoW.

**Redes que lo usan:** Ethereum, Solana, Cardano, Avalanche, Polkadot, Tron, entre muchas otras.

## 6.4 Variantes y otros mecanismos

- **Delegated Proof of Stake (DPoS):** los poseedores votan por un número reducido de validadores. Más rápido, más centralizado. (EOS, Tron.)
- **Proof of History (Solana):** no es consenso en sí, sino un "reloj" criptográfico que ordena eventos y acelera el consenso PoS.
- **Proof of Authority:** validadores identificados y aprobados. Usado en redes privadas o de prueba.
- **Byzantine Fault Tolerance (BFT) y variantes (Tendermint/CometBFT):** finalidad inmediata; usado en el ecosistema Cosmos.

## 6.5 Finalidad

**Finalidad** es el momento en que una transacción ya no puede revertirse.

- **Probabilística (Bitcoin):** cada bloque nuevo hace más improbable la reversión. Nunca es 0%, pero tras 6 bloques es despreciable.
- **Económica / determinista (Ethereum PoS y otras):** tras cierto número de "épocas" (en Ethereum, ~13 minutos), revertir requeriría destruir una enorme cantidad de ETH en garantía.

Por eso los exchanges piden distintas cantidades de confirmaciones según la red antes de acreditar un depósito.

## 6.6 Ataques conocidos

- **Ataque del 51%:** controlar la mayoría del poder (PoW) o del stake (PoS) para reescribir transacciones recientes. Ha ocurrido en redes pequeñas como Ethereum Classic y Bitcoin Gold. Prácticamente inviable en Bitcoin o Ethereum por costo.
- **Ataque Sybil:** crear muchas identidades falsas. PoW y PoS lo resuelven porque el "voto" depende de recursos, no de identidades.
- **Censura por validadores:** validadores que se niegan a incluir ciertas transacciones (por ejemplo, por sanciones). Es un tema de debate en Ethereum.

## 6.7 Comparación rápida

| | Proof of Work | Proof of Stake |
|---|---|---|
| Recurso que se arriesga | Energía y hardware | Monedas bloqueadas |
| Castigo por trampa | Pérdida de energía invertida | Slashing (pérdida de garantía) |
| Consumo energético | Alto | Muy bajo |
| Quién participa | Mineros con ASIC | Validadores con stake |
| Rendimiento para el usuario común | No (salvo minar) | Sí, vía staking |
| Ejemplo | Bitcoin | Ethereum |

## 6.8 Ideas clave del capítulo

- El consenso decide quién escribe el siguiente bloque y hace que mentir salga caro.
- PoW arriesga energía; PoS arriesga capital.
- La seguridad de una red depende de cuánto costaría atacarla: las redes grandes son mucho más seguras que las pequeñas.


---

# PARTE II — EL ECOSISTEMA

---

# Capítulo 7. El mapa de las criptomonedas: categorías y principales redes

## 7.1 Por qué necesitas un mapa

Existen millones de tokens. Sitios como CoinMarketCap o CoinGecko listan decenas de miles. Sin un mapa mental, todo parece igual: logos, nombres raros, promesas de "revolucionar" algo. Este capítulo ordena el paisaje por **categorías** y presenta las redes más relevantes, explicando para qué sirven y cuáles son sus críticas.

**Advertencia para el agente:** las posiciones en el ranking por capitalización cambian constantemente. Las redes descritas aquí son relevantes por historia, uso o tamaño a octubre de 2026, pero cualquier dato de precio, capitalización o ranking es **[VERIFICAR]**.

## 7.2 Capitalización de mercado: la métrica básica

**Capitalización de mercado = precio × cantidad de unidades en circulación.**

Error frecuente de principiante: pensar que una moneda de 0,0001 dólares está "barata" y puede llegar a 1 dólar. Si esa moneda tiene 500 billones de unidades, llegar a 1 dólar implicaría una capitalización de 500 billones de dólares, varias veces todo el mercado cripto junto. **El precio unitario no dice nada; la capitalización sí.**

Otras métricas:
- **Oferta circulante:** unidades que hoy se pueden comprar y vender.
- **Oferta total:** unidades creadas, incluyendo las bloqueadas.
- **Oferta máxima:** el límite que alguna vez existirá (si lo hay).
- **FDV (Fully Diluted Valuation):** precio × oferta máxima. Muestra cuánto valdría el proyecto si todas las monedas futuras ya existieran. Si el FDV es muchas veces la capitalización actual, viene mucha dilución.

## 7.3 Categorías principales

### 1. Reserva de valor / dinero
Monedas pensadas principalmente como dinero o "oro digital".
- **Bitcoin (BTC):** la referencia.
- **Litecoin (LTC):** una de las primeras variantes de Bitcoin (2011), bloques más rápidos.
- **Bitcoin Cash (BCH):** bifurcación de 2017 con bloques más grandes.
- **Monero (XMR):** enfocada en privacidad (ver categoría 7).

### 2. Plataformas de contratos inteligentes (Layer 1)
Blockchains donde se construyen aplicaciones.
- **Ethereum (ETH):** la principal, con el ecosistema más grande de desarrolladores y DeFi.
- **Solana (SOL):** muy rápida y barata. Fuerte en trading, memecoins y pagos. Críticas: caídas de red en años anteriores, requisitos altos de hardware.
- **BNB Chain (BNB):** asociada al exchange Binance. Compatible con EVM. Crítica: centralización.
- **Cardano (ADA):** enfoque académico, revisado por pares. Crítica: adopción y ecosistema de aplicaciones más pequeños de lo prometido.
- **Avalanche (AVAX):** arquitectura de "subredes" personalizables.
- **Tron (TRX):** muy usada para transferir USDT por sus comisiones bajas, especialmente en Asia, África y Latinoamérica. Crítica: centralización.
- **Sui, Aptos:** redes nuevas basadas en el lenguaje Move, nacidas del proyecto cancelado Diem de Facebook.
- **TON (Toncoin):** vinculada a Telegram.

### 3. Capas 2 (Layer 2)
Redes que procesan transacciones fuera de la cadena principal y luego "liquidan" en ella. Se detallan en el capítulo 11.
- Sobre Ethereum: **Arbitrum (ARB), Optimism (OP), Base** (de Coinbase, sin token propio **[VERIFICAR]**), zkSync, Starknet, Linea, Scroll.
- Sobre Bitcoin: **Lightning Network**, y otras propuestas como Stacks o Liquid.

### 4. Stablecoins
Tokens que buscan mantener un valor estable, normalmente 1 dólar. Capítulo 8.
- **USDT (Tether), USDC (Circle), USDS/DAI (Sky/Maker), PYUSD (PayPal), USDe (Ethena)**, entre otras.

### 5. DeFi (finanzas descentralizadas)
Tokens de protocolos financieros. Capítulo 9.
- **Uniswap (UNI), Aave (AAVE), Lido (LDO), Maker/Sky (MKR/SKY), Curve (CRV), Hyperliquid (HYPE)**.

### 6. Infraestructura y oráculos
- **Chainlink (LINK):** el principal proveedor de oráculos (lleva datos del mundo real, como precios, a los contratos inteligentes).
- **The Graph (GRT):** indexación de datos de blockchains.
- **Filecoin (FIL), Arweave (AR):** almacenamiento descentralizado.

### 7. Privacidad
- **Monero (XMR):** transacciones privadas por defecto (oculta remitente, receptor y monto).
- **Zcash (ZEC):** privacidad opcional mediante pruebas de conocimiento cero.

Muchos exchanges regulados las han deslistado por presión regulatoria. En algunas jurisdicciones su uso está restringido **[VERIFICAR jurisdicción]**.

### 8. Interoperabilidad
Proyectos que conectan blockchains.
- **Polkadot (DOT), Cosmos (ATOM):** ecosistemas de cadenas interconectadas.

### 9. Memecoins
Tokens basados en bromas, mascotas o cultura de internet, sin utilidad declarada.
- **Dogecoin (DOGE):** la original (2013), nacida como broma.
- **Shiba Inu (SHIB), PEPE, BONK, WIF**, y miles más.

Realidad: algunas memecoins alcanzan capitalizaciones enormes, pero la gran mayoría pierde casi todo su valor. En plataformas de lanzamiento de memecoins (como pump.fun en Solana), se crean decenas de miles de tokens al día; estudios del propio ecosistema muestran que una fracción mínima sobrevive más de unas horas **[VERIFICAR]**. Es más parecido a un casino que a una inversión.

### 10. Exchange tokens
Tokens emitidos por exchanges: **BNB (Binance), OKB (OKX), CRO (Crypto.com)**. Su valor depende fuertemente de la salud de la empresa. FTT, el token de FTX, perdió casi todo su valor en días cuando FTX colapsó.

### 11. Gaming y metaverso
- **Axie Infinity (AXS), The Sandbox (SAND), Decentraland (MANA), Immutable (IMX)**.
Tuvieron un auge en 2021 y luego cayeron más del 90% en la mayoría de los casos.

### 12. IA y cripto
Proyectos que mezclan blockchain con inteligencia artificial: mercados de cómputo, agentes autónomos con billeteras, redes de datos.
- **Bittensor (TAO), Render (RENDER), Fetch.ai / ASI**, entre otros.
Categoría muy especulativa: muchos proyectos usan "IA" como etiqueta de marketing. Ver capítulo 27.

### 13. Tokenización de activos reales (RWA)
Bonos, fondos, inmuebles y otros activos representados como tokens. Capítulo 10.
- **Ondo (ONDO)**, fondos tokenizados de gestoras como BlackRock y Franklin Templeton.

## 7.4 Cómo leer este mapa con criterio

Preguntas para cualquier moneda nueva:

1. **¿En qué categoría cae?** Si no puedes ubicarla, probablemente el proyecto tampoco sabe qué es.
2. **¿Quién la usa y para qué, hoy?** No en el futuro prometido: hoy.
3. **¿Quién tiene la mayoría de las monedas?** (Capítulo 21.)
4. **¿Sobrevivió a un mercado bajista?** Un proyecto que pasó por 2018 o 2022 y sigue activo tiene más evidencia que uno nacido el mes pasado.
5. **¿Por qué necesita un token?** Muchos proyectos podrían funcionar sin token; el token existe para financiar a los fundadores.

## 7.5 Bitcoin dominance

La **dominancia de Bitcoin** es el porcentaje de la capitalización total del mercado cripto que corresponde a BTC. Se usa como termómetro:
- Dominancia alta: el dinero prefiere la "seguridad" relativa de BTC.
- Dominancia cayendo con mercado al alza: el dinero fluye a altcoins (la llamada "altseason").

Es un indicador útil para entender el ánimo del mercado, no una señal de compra o venta.

## 7.6 Ideas clave del capítulo

- El precio unitario no importa; importa la capitalización y la dilución futura (FDV).
- Ordena cualquier moneda por categoría antes de evaluarla.
- La enorme mayoría de tokens, en especial memecoins, termina valiendo casi nada.

---

# Capítulo 8. Stablecoins

## 8.1 Qué son y por qué importan

Una **stablecoin** es un token diseñado para mantener un precio estable, casi siempre **1 dólar estadounidense**. Combinan lo mejor del dólar (estabilidad) con lo mejor de cripto (transferencia 24/7, global, programable).

Son probablemente **el caso de uso de cripto con más adopción real**:
- Pagos y remesas internacionales.
- Protección contra la inflación en países como Argentina, Venezuela o Turquía.
- Base de casi todo el trading cripto (los pares de trading son "BTC/USDT", no "BTC/USD").
- Base de la mayoría de los protocolos DeFi.

El mercado total de stablecoins supera con holgura los 200.000 millones de dólares **[VERIFICAR cifra actual]**.

## 8.2 Tipos de stablecoins

### 1. Respaldadas por dinero fiat (centralizadas)
Una empresa recibe dólares, los guarda en bancos o bonos del Tesoro, y emite el mismo número de tokens. Si devuelves el token, te devuelve el dólar.

- **USDT (Tether):** la más grande y la más usada en mercados emergentes. Históricamente criticada por falta de auditorías completas y transparencia de reservas; publica "atestaciones" periódicas.
- **USDC (Circle):** segunda más grande, con foco en cumplimiento regulatorio en EE.UU. y Europa.
- **PYUSD (PayPal), FDUSD, USD1**, entre otras.

**Riesgos:**
- Dependes de que el emisor realmente tenga las reservas.
- El emisor **puede congelar** tokens en cualquier dirección (lo hacen por orden judicial o sanciones).
- Riesgo bancario: en marzo de 2023, USDC perdió temporalmente su paridad (bajó a ~0,87 USD) porque Circle tenía parte de sus reservas en Silicon Valley Bank, que quebró. Se recuperó cuando el gobierno de EE.UU. garantizó los depósitos.

### 2. Respaldadas por cripto (sobrecolateralizadas)
Se crean depositando más valor en cripto del que se emite. Por ejemplo, depositas 150 USD en ETH para generar 100 en stablecoins. Si el valor del ETH cae demasiado, el sistema liquida la garantía automáticamente.

- **DAI / USDS (Sky, antes MakerDAO):** la principal de este tipo. Hoy parte importante de su respaldo son también activos reales y USDC, lo que reduce su descentralización.

**Riesgos:** caídas violentas del colateral, fallas del oráculo, errores en contratos.

### 3. Sintéticas / delta-neutral
Mantienen la paridad combinando cripto con posiciones cortas en derivados.
- **USDe (Ethena):** usa ETH/BTC en staking más posiciones cortas en futuros perpetuos. Genera rendimiento alto cuando las tasas de financiamiento son positivas.

**Riesgos:** si las tasas de financiamiento se vuelven negativas por mucho tiempo, o si un exchange donde están las posiciones falla.

### 4. Algorítmicas (sin colateral real)
Intentan mantener la paridad solo con incentivos y un segundo token que se crea o destruye.
- **UST (TerraUSD):** el caso más famoso de fracaso. En mayo de 2022 perdió la paridad, entró en una "espiral de la muerte" con su token hermano LUNA, y destruyó unos **40.000 millones de dólares** en días. Arrastró a fondos y prestamistas (Celsius, Three Arrows Capital) y fue uno de los detonantes del mercado bajista de 2022.

**Lección para el agente:** cualquier stablecoin que prometa rendimientos altos sin explicar con claridad de dónde vienen merece máxima desconfianza. Anchor Protocol pagaba ~20% anual en UST antes del colapso.

## 8.3 La paridad (peg) y cómo se mantiene

Una stablecoin respaldada en fiat mantiene el precio por **arbitraje**:
- Si se vende a 0,99, los arbitrajistas la compran y la canjean con el emisor por 1,00. La demanda sube el precio.
- Si se vende a 1,01, los arbitrajistas depositan 1 dólar con el emisor, reciben un token nuevo y lo venden a 1,01. La oferta baja el precio.

Esto funciona mientras el mercado confíe en que el emisor canjea. Si la confianza se rompe, se pierde la paridad ("depeg").

## 8.4 Una misma stablecoin, muchas redes

USDT y USDC existen en muchas blockchains: Ethereum, Tron, Solana, Arbitrum, Base, Polygon, Avalanche, etc. **Son el mismo activo emitido en redes distintas, pero no son intercambiables de forma automática entre redes.**

Error clásico: retirar USDT por la red Tron (TRC-20) a una dirección que solo acepta la red Ethereum (ERC-20). Dependiendo del caso, los fondos pueden perderse o requerir un proceso de recuperación largo y no garantizado. Ver capítulo 16.

## 8.5 Regulación de stablecoins

- **Estados Unidos:** la **ley GENIUS**, firmada en julio de 2025, creó el primer marco federal para stablecoins de pago: exige respaldo 1:1 con activos líquidos (efectivo, bonos del Tesoro de corto plazo), auditorías y licencias. La implementación reglamentaria se ha extendido durante 2026 **[VERIFICAR detalles de entrada en vigor]**.
- **Unión Europea:** bajo **MiCA**, las stablecoins se clasifican como "e-money tokens" (EMT) o "asset-referenced tokens" (ART). Los emisores necesitan autorización. Por esto, varios exchanges europeos limitaron USDT, que no tenía autorización MiCA **[VERIFICAR estado actual]**.
- **Latinoamérica:** en general, no hay marcos específicos completos; se aplican reglas generales de cripto, cambiarias y antilavado.

## 8.6 Stablecoins en monedas distintas al dólar

Existen stablecoins en euros (EURC, EURS), y algunos proyectos en monedas latinoamericanas (por ejemplo, tokens en pesos mexicanos, reales brasileños o pesos argentinos emitidos por empresas locales). Tienen mucho menos liquidez que las de dólar. **[VERIFICAR opciones disponibles en cada país]**.

## 8.7 Usos prácticos para una persona en Latinoamérica

- **Ahorro en dólares** cuando el acceso a dólares bancarios es limitado o caro.
- **Recibir pagos del extranjero** (freelancers que trabajan para clientes en EE.UU. o Europa).
- **Remesas familiares** con comisiones menores que los servicios tradicionales, siempre que el receptor tenga cómo convertir a moneda local.
- **"Estacionar" valor** entre operaciones de inversión sin salir del ecosistema cripto.

Recordatorio: "estable" no significa "sin riesgo". El riesgo cambia de volatilidad a **riesgo de emisor, de plataforma y regulatorio**.

## 8.8 Ideas clave del capítulo

- Las stablecoins son el uso con más adopción real de cripto.
- Las respaldadas en fiat dependen de la confianza en el emisor, que además puede congelar fondos.
- Las algorítmicas sin colateral real han fracasado de forma catastrófica (UST/Terra).
- Siempre verifica la red (Tron, Ethereum, Solana…) al enviar o recibir stablecoins.

---

# Capítulo 9. Finanzas descentralizadas (DeFi)

## 9.1 Qué es DeFi

**DeFi** (Decentralized Finance) es el conjunto de servicios financieros que funcionan con contratos inteligentes en vez de instituciones: intercambiar, prestar, pedir prestado, generar rendimiento, operar derivados. Cualquiera con una billetera puede usarlos, sin cuenta, sin aprobación y a cualquier hora.

La métrica más usada para medir su tamaño es el **TVL (Total Value Locked)**: el valor total depositado en los protocolos. Se consulta en DefiLlama **[VERIFICAR cifra actual]**.

## 9.2 Exchanges descentralizados (DEX) y AMMs

### Cómo funciona un exchange tradicional
Tiene un **libro de órdenes**: compradores ponen precios a los que quieren comprar, vendedores a los que quieren vender, y el sistema los cruza.

### Cómo funciona un AMM
Un **Automated Market Maker** (creador de mercado automatizado) reemplaza el libro de órdenes por **pools de liquidez**:

1. Personas (proveedores de liquidez, o LPs) depositan dos tokens en un pool, por ejemplo ETH y USDC, en igual valor.
2. Quien quiere cambiar ETH por USDC deposita ETH en el pool y retira USDC.
3. El precio se ajusta automáticamente según una fórmula. La más clásica (Uniswap v2) es **x × y = k**: el producto de las cantidades de ambos tokens se mantiene constante.
4. Cada intercambio paga una comisión (por ejemplo, 0,3%) que va a los LPs.

**Ejemplos:** Uniswap (Ethereum y capas 2), Raydium y Jupiter (agregador) en Solana, PancakeSwap (BNB Chain), Curve (especializado en stablecoins).

### Conceptos clave en un DEX
- **Slippage (deslizamiento):** diferencia entre el precio esperado y el obtenido, por el tamaño de tu operación o por movimientos del mercado. Se configura una tolerancia máxima (por ejemplo, 0,5%).
- **Price impact:** cuánto mueve tu propia operación el precio del pool. En pools pequeños, una compra mediana puede mover el precio 10% o más.
- **MEV / sandwich attacks:** bots que ven tu transacción pendiente, compran justo antes y venden justo después, quedándose con la diferencia. Protección: usar RPCs privados o agregadores con protección MEV, y no poner slippage alto.
- **Agregadores:** herramientas como 1inch, Jupiter o CoW Swap buscan el mejor precio entre varios DEX.

### Pérdida impermanente
Si eres proveedor de liquidez y el precio de un token cambia mucho respecto al otro, terminas con menos valor que si simplemente hubieras guardado los dos tokens. Se llama "impermanente" porque desaparece si el precio vuelve al punto inicial, pero si retiras con el precio cambiado, la pérdida se vuelve real. Las comisiones cobradas pueden compensarla o no.

## 9.3 Préstamos descentralizados

**Protocolos:** Aave, Compound, Morpho, Spark, Kamino (Solana).

Cómo funciona:
1. **Prestar (suplir):** depositas, por ejemplo, USDC. Ganas un interés variable pagado por quienes piden prestado.
2. **Pedir prestado:** depositas un colateral (por ejemplo, ETH) y puedes pedir prestado otro activo hasta cierto porcentaje del valor del colateral (por ejemplo, 75%).
3. **Factor de salud (health factor):** indicador de cuán cerca estás de ser liquidado. Si baja de 1, te liquidan.
4. **Liquidación:** si el valor del colateral cae, cualquiera puede pagar parte de tu deuda y quedarse con parte de tu colateral con descuento. Pierdes una penalidad.

¿Para qué pedir prestado contra tu propia cripto? Para obtener liquidez sin vender (y sin realizar una ganancia tributable, según la jurisdicción) o para apalancarse. Lo segundo es la causa de muchas liquidaciones masivas en caídas.

**Sobrecolateralización:** en DeFi no hay historial crediticio, así que todo préstamo exige más colateral que lo prestado.

## 9.4 Staking

**Staking** es bloquear monedas de una red Proof of Stake para ayudar a asegurarla, a cambio de recompensas.

Formas de hacerlo:
| Forma | Cómo | Ventaja | Riesgo |
|---|---|---|---|
| Solo staking | Corres tu propio validador (en Ethereum, 32 ETH) | Máxima independencia | Técnico; slashing si fallas |
| Delegación nativa | Delegas a un validador sin entregar custodia (común en Solana, Cardano, Cosmos) | Simple, mantienes tus claves | Validador malo = menos rendimiento; períodos de desbloqueo |
| Staking líquido | Depositas en un protocolo (Lido, Rocket Pool, Jito) y recibes un token que representa tu posición (stETH, rETH, JitoSOL) | Puedes usar ese token en DeFi | Riesgo de contrato; el token puede cotizar bajo su valor |
| Staking en exchange | El exchange hace todo | Muy simple | Riesgo de custodia; el exchange se queda un porcentaje |

Rendimientos típicos: varían por red y momento, en general de un dígito anual en redes grandes **[VERIFICAR tasas actuales]**. **Desconfía de cualquier rendimiento de staking de dos dígitos altos en redes poco conocidas: suele pagarse con inflación del propio token, que diluye su precio.**

### Restaking
Protocolos como EigenLayer permiten "re-usar" ETH ya stakeado para asegurar otros servicios, a cambio de rendimiento extra. Suma rendimiento y suma capas de riesgo (más reglas de slashing, más contratos).

## 9.5 Yield farming y rendimientos

**Yield farming** es mover capital entre protocolos para capturar el mayor rendimiento, muchas veces pagado en tokens del propio protocolo.

Regla fundamental: **todo rendimiento tiene una fuente**. Pregunta siempre de dónde sale.

| Fuente legítima del rendimiento | Ejemplo |
|---|---|
| Intereses pagados por quienes piden prestado | Aave |
| Comisiones de intercambio | Proveer liquidez en Uniswap |
| Recompensas de consenso | Staking de ETH |
| Intereses de bonos del Tesoro tokenizados | Fondos RWA |
| Tasas de financiamiento de derivados | Ethena |

| Fuente dudosa o insostenible | Señal |
|---|---|
| Emisión del propio token del protocolo | El APY baja a medida que el token pierde valor |
| Depósitos de nuevos usuarios | Esquema Ponzi |
| "Trading con IA" o "arbitraje secreto" | Casi siempre fraude |

## 9.6 Derivados descentralizados

- **Futuros perpetuos en DEX:** Hyperliquid, dYdX, GMX, Jupiter Perps. Permiten operar con apalancamiento sin exchange centralizado.
- **Opciones:** Derive (antes Lyra), entre otros.

Para principiantes: **no**. El apalancamiento es la forma más rápida de perder todo el capital (capítulo 19).

## 9.7 Gobernanza y DAOs

Muchos protocolos DeFi tienen un **token de gobernanza** que permite votar cambios (comisiones, nuevos activos, uso de la tesorería). Una **DAO** (organización autónoma descentralizada) es la comunidad que vota.

Realidad: la participación suele ser baja y los votos se concentran en pocas billeteras (fondos de capital de riesgo, fundadores). "Descentralizado" muchas veces es aspiracional.

## 9.8 Riesgos de DeFi (lista que el agente debe recordar)

1. **Riesgo de contrato inteligente:** bugs explotables. Ha habido hackeos de cientos de millones de dólares.
2. **Riesgo de oráculo:** si el precio que recibe el contrato es manipulado, se pueden drenar fondos.
3. **Riesgo de gobernanza:** un atacante compra suficientes tokens de voto y aprueba un cambio malicioso.
4. **Riesgo de admin keys:** si el equipo puede actualizar contratos, puede (por error, coacción o mala fe) mover fondos.
5. **Rug pull:** el equipo retira la liquidez y desaparece. Muy común en tokens nuevos.
6. **Riesgo de depeg:** stablecoins o tokens de staking líquido que pierden su paridad.
7. **Riesgo de liquidación:** por volatilidad o por fallas de red en el peor momento.
8. **Riesgo de puentes:** capítulo 11.
9. **Riesgo de interfaz (frontend):** sitios web falsos o hackeados que imitan al protocolo real.
10. **Complejidad acumulada ("lego financiero"):** un protocolo usa a otro que usa a otro. Si uno falla, el efecto se propaga.

## 9.9 Cómo empezar en DeFi de forma prudente

1. Domina primero billeteras, envíos y seguridad (Parte III).
2. Empieza con montos que puedas perder por completo.
3. Usa protocolos con años de historia, auditorías múltiples y TVL alto.
4. Prefiere redes de capa 2 o de comisiones bajas para practicar.
5. Accede a los protocolos escribiendo la URL o desde un marcador guardado, **nunca desde anuncios en buscadores** (son una vía común de phishing).
6. Revisa y revoca aprobaciones periódicamente.
7. Lleva registro de todas las operaciones para efectos tributarios.

## 9.10 Ideas clave del capítulo

- DeFi reemplaza instituciones por contratos: más acceso, más responsabilidad.
- Todo rendimiento tiene una fuente; si no la entiendes, el producto eres tú.
- Los riesgos se acumulan cuando los protocolos se apilan.

---

# Capítulo 10. NFTs y tokenización de activos reales

## 10.1 Qué es un NFT

Un **NFT (token no fungible)** es un token único e irrepetible en una blockchain. A diferencia de un bitcoin (todos iguales), cada NFT tiene un identificador propio.

Lo que un NFT **es**: un registro en la blockchain que dice "la dirección X es dueña del token #1234 de la colección Y".

Lo que un NFT **normalmente no es**:
- No es la imagen en sí. La imagen suele estar guardada en otro lugar (IPFS, Arweave o un servidor común) y el token solo apunta a ella.
- No es necesariamente un derecho de autor. Comprar un NFT de una imagen no te da, por defecto, derechos de reproducción comercial, salvo que la licencia lo diga.

## 10.2 Breve historia

- **2017:** CryptoPunks y CryptoKitties (que congestionaron Ethereum).
- **2021:** auge masivo. Una obra del artista Beeple se vende en Christie's por 69 millones de dólares. Colecciones como Bored Ape Yacht Club alcanzan precios de cientos de miles de dólares por pieza.
- **2022–2023:** colapso. Volúmenes y precios caen más de 90% en la mayoría de colecciones.
- **Hoy:** mercado mucho más pequeño, con nichos activos (arte generativo, coleccionables con comunidad, juegos, entradas y membresías).

## 10.3 Usos que van más allá del arte

- **Entradas y membresías:** acceso a eventos o comunidades.
- **Certificados y credenciales:** diplomas, certificaciones verificables.
- **Objetos de juegos:** ítems que el jugador realmente controla.
- **Nombres de dominio:** ENS (`.eth`), Unstoppable Domains.
- **Posiciones financieras:** en Uniswap v3/v4, las posiciones de liquidez son NFTs.
- **Representación de activos físicos:** relojes, vinos, obras guardadas en custodia.

## 10.4 Riesgos de los NFTs

- **Iliquidez:** puede que nadie quiera comprar tu NFT a ningún precio.
- **Wash trading:** volúmenes inflados artificialmente por vendedores que se compran a sí mismos.
- **Dependencia del enlace:** si el servidor donde está la imagen desaparece, tu NFT apunta a nada.
- **Estafas de "mint" falsos** y airdrops de NFTs maliciosos que al interactuar piden aprobaciones que vacían la billetera.
- **Regalías:** muchos mercados dejaron de obligar el pago de regalías a creadores.

**Regla práctica:** si te llega un NFT que no pediste, **no interactúes con él**. No lo vendas, no visites el enlace que trae.

## 10.5 Tokenización de activos reales (RWA)

**RWA (Real World Assets)** es representar activos del mundo tradicional como tokens: bonos, fondos monetarios, acciones, inmuebles, facturas, materias primas.

Por qué importa:
- **Liquidación 24/7** y casi instantánea.
- **Fraccionamiento:** comprar una parte pequeña de un activo caro.
- **Programabilidad:** usar un bono tokenizado como colateral en DeFi.
- **Acceso global** (dentro de los límites regulatorios).

Ejemplos relevantes:
- **Fondos monetarios / bonos del Tesoro de EE.UU. tokenizados:** BUIDL (BlackRock), BENJI (Franklin Templeton), productos de Ondo. Es el segmento más grande de RWA **[VERIFICAR cifras]**.
- **Oro tokenizado:** PAXG, XAUT.
- **Crédito privado:** plataformas como Centrifuge o Maple.
- **Acciones tokenizadas:** varios exchanges y plataformas ofrecen representaciones de acciones estadounidenses para usuarios fuera de EE.UU. **[VERIFICAR disponibilidad y estructura legal; muchas veces son derivados, no la acción real]**.

### Lo que hay que entender de la tokenización
Un token que representa un activo real **solo vale lo que valga el compromiso legal de quien custodia el activo real**. La blockchain garantiza el registro del token, no la existencia del bono o del edificio. Por eso, en RWA:
- Importa quién es el emisor y bajo qué ley opera.
- Suele haber KYC (verificación de identidad) y listas blancas de direcciones.
- Muchos productos solo están disponibles para inversionistas calificados o fuera de ciertas jurisdicciones.

## 10.6 Ideas clave del capítulo

- Un NFT es un registro de propiedad de un identificador único, no la obra en sí.
- El mercado de NFTs especulativos colapsó; los usos funcionales siguen.
- La tokenización de activos reales es una de las tendencias más serias del sector, pero su confianza depende del emisor y del marco legal, no de la blockchain.

---

# Capítulo 11. Escalabilidad, Layer 2 y puentes entre cadenas

## 11.1 El problema

Las blockchains descentralizadas son lentas y caras porque cada nodo procesa cada transacción. Ethereum en su capa base procesa del orden de 15–30 transacciones por segundo; Visa puede procesar miles. Si todo el mundo quisiera usar Ethereum directamente, las comisiones serían prohibitivas.

Dos caminos de solución:
1. **Escalar la capa 1:** bloques más grandes, hardware más potente (camino de Solana). Más rápido, pero menos nodos pueden participar.
2. **Escalar por capas:** mantener la capa 1 segura y descentralizada, y procesar la mayoría de las transacciones en una **capa 2** que luego se "ancla" a la capa 1 (camino de Ethereum y Bitcoin).

## 11.2 Rollups: la capa 2 dominante en Ethereum

Un **rollup** ejecuta transacciones fuera de Ethereum, las agrupa en lotes y publica un resumen comprimido en Ethereum. Así, miles de transacciones comparten el costo de una sola publicación.

### Optimistic rollups
- Asumen que las transacciones son válidas ("optimistas").
- Cualquiera puede presentar una "prueba de fraude" durante un período de desafío (típicamente 7 días).
- Consecuencia práctica: **retirar fondos de forma nativa hacia Ethereum demora ~7 días**. (Existen puentes de terceros que lo hacen rápido cobrando una comisión.)
- Ejemplos: **Arbitrum, Optimism, Base**.

### ZK rollups (de conocimiento cero)
- Publican una **prueba matemática** (prueba de validez) de que todas las transacciones del lote son correctas.
- Retiros más rápidos, una vez generada y verificada la prueba.
- Tecnológicamente más complejos.
- Ejemplos: **zkSync, Starknet, Linea, Scroll, Polygon zkEVM**.

### Comisiones
Desde la actualización **Dencun** de Ethereum (marzo de 2024), que introdujo los "blobs" (espacio de datos más barato para rollups), las comisiones en capas 2 bajaron drásticamente: hoy una transacción típica cuesta centavos de dólar o menos **[VERIFICAR]**. Actualizaciones posteriores (como Pectra en 2025) siguieron ampliando la capacidad.

### Matices de seguridad
No todas las capas 2 son igual de seguras. Algunas todavía tienen:
- Un **secuenciador centralizado** (una sola empresa ordena las transacciones).
- **Contratos actualizables** controlados por un consejo o multifirma.
- Pruebas de fraude aún no plenamente activas.

El sitio **L2BEAT** clasifica cada capa 2 por "etapas" de madurez de seguridad (Stage 0, 1, 2). Es la referencia para evaluarlas.

## 11.3 Sidechains

Una **sidechain** es una blockchain independiente, con su propio consenso, conectada a otra por un puente. A diferencia de un rollup, **no hereda la seguridad de la cadena principal**. Ejemplo histórico: Polygon PoS (que funcionaba como sidechain de Ethereum).

## 11.4 Capa 2 en Bitcoin

- **Lightning Network:** canales de pago (capítulo 4).
- **Liquid:** sidechain federada (administrada por un grupo de empresas), usada para transferencias rápidas entre exchanges y emisión de activos.
- **Stacks y otras:** buscan llevar contratos inteligentes al ecosistema Bitcoin.
- Hay propuestas más recientes de rollups sobre Bitcoin, aún en etapas tempranas **[VERIFICAR]**.

## 11.5 Puentes (bridges)

Un **puente** permite mover activos entre blockchains distintas. Como cada blockchain no "ve" a las otras, el mecanismo típico es:

1. Bloqueas tus tokens en un contrato en la cadena A.
2. El puente emite una versión "envuelta" (wrapped) equivalente en la cadena B.
3. Para volver, quemas la versión envuelta en B y se desbloquean los originales en A.

Ejemplo: **WBTC** es bitcoin "envuelto" para usarse en Ethereum. Su valor depende de que el custodio realmente tenga los BTC bloqueados.

### Por qué los puentes son peligrosos
Los puentes concentran enormes cantidades de fondos bloqueados en un solo lugar: son el blanco favorito de los hackers. Algunos de los mayores robos de la historia cripto fueron a puentes:
- **Ronin Bridge (Axie Infinity), 2022:** ~600 millones de dólares, atribuido al grupo Lazarus de Corea del Norte.
- **Wormhole, 2022:** ~320 millones.
- **Nomad, 2022:** ~190 millones.

### Recomendaciones
- Usa puentes oficiales o con mucho historial.
- Para mover stablecoins como USDC, prefiere mecanismos nativos del emisor (Circle tiene su propio protocolo de transferencia entre cadenas, CCTP) en vez de versiones envueltas.
- Muchas veces lo más simple y seguro para un principiante es **usar un exchange centralizado como puente**: depositar en una red y retirar en otra (verificando que el exchange soporte ambas).
- Nunca dejes grandes montos en tokens envueltos de puentes poco conocidos.

## 11.6 Abstracción de cuentas y la experiencia de usuario

Una tendencia importante: hacer que usar cripto se sienta como usar una app normal.
- **Abstracción de cuentas (ERC-4337, EIP-7702):** billeteras que funcionan como contratos inteligentes y permiten recuperar acceso con métodos sociales, pagar comisiones en stablecoins, poner límites de gasto, etc.
- **Passkeys:** iniciar sesión con huella o FaceID en vez de frase semilla, en algunas billeteras.
- **Intents y cadenas abstraídas:** el usuario dice "quiero cambiar X por Y" y el sistema decide por qué redes y puentes pasar.

Esto reduce errores, pero cada solución agrega supuestos de confianza nuevos que conviene entender.

## 11.7 Ideas clave del capítulo

- Ethereum escala con rollups; Bitcoin con Lightning y otras capas.
- No todas las capas 2 son igual de seguras: revisa L2BEAT.
- Los puentes son el punto más hackeado del ecosistema.
- Para principiantes, un exchange confiable suele ser el "puente" más simple.


---

# PARTE III — LA PRÁCTICA

---

# Capítulo 12. Billeteras (wallets): tipos y cómo elegir

## 12.1 Qué es realmente una billetera

Una billetera cripto **no guarda criptomonedas**. Las monedas siempre están en la blockchain. La billetera guarda (o te da acceso a) las **claves privadas** que permiten moverlas, y te muestra el saldo leyendo la blockchain.

Por eso, si pierdes tu teléfono pero tienes tu frase semilla, no perdiste nada: instalas la billetera en otro dispositivo, ingresas la frase y aparecen tus fondos. Y por eso, si alguien obtiene tu frase semilla, puede vaciar tus fondos desde cualquier parte del mundo aunque tú tengas el teléfono en la mano.

## 12.2 La gran división: custodial vs. no custodial

| | Custodial | No custodial (autocustodia) |
|---|---|---|
| Quién tiene las claves | Una empresa (exchange, app) | Tú |
| Si olvidas la contraseña | Recuperas con soporte | Solo con tu frase semilla |
| Si la empresa quiebra | Puedes perder todo | No te afecta |
| Si te hackean la cuenta | Depende de la seguridad de la empresa y la tuya | Depende 100% de ti |
| Facilidad | Alta | Media |
| Ejemplos | Saldo en Binance, Coinbase, Buda, Bitso | MetaMask, Phantom, Ledger, Trezor, Sparrow |

No hay una opción "correcta" para todos. Hay una regla útil:

> **Montos pequeños para operar: custodial puede estar bien. Ahorro de largo plazo o montos importantes: autocustodia con billetera de hardware.**

## 12.3 Billeteras calientes (hot) vs. frías (cold)

- **Caliente:** las claves están en un dispositivo conectado a internet (app en el teléfono, extensión del navegador). Cómoda, más expuesta a malware y phishing.
- **Fría:** las claves se generan y quedan en un dispositivo que nunca se conecta directamente a internet (billetera de hardware, computador aislado). Más segura, menos cómoda.

## 12.4 Tipos de billeteras no custodiales

### Billeteras móviles
Apps en el teléfono. Buenas para el día a día y montos pequeños.
- Bitcoin: BlueWallet, Phoenix (Lightning), Muun, Blockstream App (antes Green) **[VERIFICAR disponibilidad y estado de cada app]**.
- Multicadena: Trust Wallet, Exodus, Coinbase Wallet (no confundir con la app del exchange Coinbase).
- Solana: Phantom, Solflare.

### Extensiones de navegador
Para interactuar con aplicaciones DeFi y NFTs.
- **MetaMask** (redes EVM), **Rabby** (EVM, con buenas alertas de seguridad), **Phantom** (Solana y otras).
- Mayor exposición a sitios de phishing: cada firma que apruebas puede ser peligrosa.

### Billeteras de escritorio
- **Sparrow, Electrum** (Bitcoin, para usuarios más avanzados).
- **Exodus** (multicadena, amigable).

### Billeteras de hardware
Dispositivos físicos que generan y guardan las claves offline. Para firmar una transacción, el computador o teléfono prepara la transacción, el dispositivo la firma internamente, y la clave nunca sale.
- **Ledger** (Nano S Plus, Nano X, Flex, Stax), **Trezor** (Safe 3, Safe 5, Model One), **Coldcard** (solo Bitcoin, avanzado), **BitBox02**, **Keystone**, **Foundation Passport** **[VERIFICAR modelos vigentes]**.

Puntos a saber:
- **Cómpralas solo en la tienda oficial del fabricante o distribuidores autorizados.** Hay casos documentados de dispositivos manipulados vendidos en marketplaces.
- Un dispositivo legítimo **nunca viene con una frase semilla ya escrita**. Si viene una tarjeta con 24 palabras impresas, es una estafa: no lo uses.
- **Verifica siempre en la pantalla del dispositivo** la dirección y el monto antes de confirmar. La pantalla del dispositivo es la única que no puede ser manipulada por malware del computador.
- Si pierdes o se rompe el dispositivo, recuperas todo con la frase semilla en otro dispositivo (incluso de otra marca, si es compatible con BIP-39).

### Billeteras de papel (no recomendadas)
Imprimir claves en papel era común en 2013–2017. Hoy no se recomienda: son fáciles de usar mal (reutilización de direcciones, impresoras comprometidas).

### Billeteras multifirma (multisig)
Requieren **varias claves para mover fondos**, por ejemplo 2 de 3. Si pierdes una clave, las otras dos siguen permitiendo acceso; si roban una, el ladrón no puede mover nada.
- Bitcoin: Sparrow, Nunchuk, Casa, Unchained.
- Ethereum: **Safe** (antes Gnosis Safe), el estándar para tesorerías de empresas y DAOs.
- Recomendada para montos grandes o empresas. Requiere más conocimiento.

### Billeteras de contrato inteligente / con recuperación social
Nuevas billeteras basadas en abstracción de cuentas permiten recuperar acceso con "guardianes" (personas o dispositivos de confianza) en vez de una frase semilla única. Mejoran la experiencia, pero hay que entender bien quiénes son los guardianes y qué pasa si la empresa detrás desaparece.

## 12.5 Cómo elegir: árbol de decisión simple

1. **¿Vas a invertir menos de lo que te dolería perder (por ejemplo, unos cientos de dólares) y solo comprar y mantener?**
   → Puedes empezar en un exchange regulado y confiable. Activa todas las medidas de seguridad (capítulo 17).

2. **¿Quieres aprender autocustodia con poco riesgo?**
   → Instala una billetera móvil reconocida, anota la frase semilla en papel, envía un monto pequeño y practica enviar y recibir.

3. **¿Tu monto en cripto ya es significativo para ti (por ejemplo, más de un mes de sueldo)?**
   → Billetera de hardware comprada en la tienda oficial.

4. **¿Montos muy grandes, empresa o herencia?**
   → Multifirma, con plan de herencia documentado. Considerar asesoría especializada.

5. **¿Quieres usar DeFi o NFTs?**
   → Billetera de navegador (Rabby/MetaMask/Phantom), idealmente **conectada a una billetera de hardware**, y una billetera separada "de batalla" con poco saldo para interactuar con sitios nuevos.

## 12.6 Buenas prácticas con varias billeteras

Un esquema que usan muchos usuarios con experiencia:

| Billetera | Propósito | Saldo |
|---|---|---|
| Bóveda (hardware o multisig) | Ahorro de largo plazo, casi nunca se mueve | La mayor parte |
| Operativa (hardware + extensión) | DeFi en protocolos conocidos | Moderado |
| Desechable ("burner") | Probar sitios nuevos, reclamar airdrops, mints | Mínimo |
| Exchange | Comprar/vender, entrada y salida a moneda local | Lo necesario para operar |

## 12.7 Errores comunes con billeteras

- Descargar una billetera desde un enlace de anuncio o de un mensaje, en vez de la tienda oficial o el sitio verificado. Hay apps falsas que copian el nombre y logo.
- Guardar la frase semilla en una foto, en notas del teléfono, en el correo o en la nube.
- No probar la recuperación antes de depositar montos grandes.
- Confundir la app de un exchange (custodial) con la billetera del mismo nombre (no custodial).
- No respaldar la passphrase opcional, si se usó.
- Instalar extensiones de navegador desconocidas que pueden leer lo que haces en otras pestañas.

## 12.8 Ideas clave del capítulo

- La billetera guarda claves, no monedas.
- Custodial = confías en una empresa. No custodial = confías en ti.
- Para montos importantes: billetera de hardware comprada en la tienda oficial.
- Separa billeteras por propósito.

---

# Capítulo 13. La frase semilla: el concepto más importante del manual

## 13.1 Por qué un capítulo entero

Si el lector olvida todo el resto del manual pero recuerda este capítulo, ya está mejor protegido que la mayoría de los usuarios. **La mayor parte de las pérdidas de cripto en usuarios comunes no viene de hackeos sofisticados, sino de frases semilla perdidas, mal guardadas o entregadas a un estafador.**

## 13.2 Qué es

La **frase semilla** (seed phrase, recovery phrase, frase de recuperación, mnemónico) es una lista de 12 o 24 palabras que genera **todas** las claves privadas de una billetera no custodial.

- **Quien tiene la frase, tiene el dinero.** No necesita tu teléfono, tu contraseña ni tu huella.
- **Si pierdes la frase y pierdes el dispositivo, pierdes el dinero.** Nadie puede recuperarlo. No hay soporte técnico que ayude.

## 13.3 Las reglas de oro

1. **Nunca la escribas en nada conectado a internet.** Ni foto, ni captura de pantalla, ni notas del teléfono, ni correo, ni WhatsApp a ti mismo, ni Google Drive, ni iCloud, ni gestor de contraseñas en la nube (este último es debatible para usuarios avanzados, pero para principiantes: no).
2. **Nunca la compartas con nadie.** Ningún soporte técnico, exchange, fabricante de billeteras, "experto en recuperación", amigo ni familiar que te "ayude" la necesita jamás. **Quien te la pide, te está robando.**
3. **Nunca la ingreses en un sitio web.** La única vez que se ingresa es para restaurar en una billetera que tú descargaste de una fuente oficial, o en el propio dispositivo de hardware.
4. **Anótala a mano, en papel o metal, en el orden exacto y con la ortografía exacta.**
5. **Verifica que la anotaste bien** (muchas billeteras te piden confirmar algunas palabras; algunas permiten un "dry run" de recuperación).
6. **Guárdala en un lugar seguro contra robo, fuego y agua.**
7. **Piensa en quién la encontrará si te pasa algo** (sección 13.7).

## 13.4 Cómo guardarla físicamente

| Método | Ventajas | Desventajas |
|---|---|---|
| Papel en sobre | Gratis, inmediato | Fuego, agua, deterioro, fácil de tirar por error |
| Papel plastificado | Algo más durable | Sigue siendo vulnerable a fuego |
| Placa de acero/titanio (estampada o con letras) | Resiste fuego e inundación | Costo; hay que comprar marcas confiables |
| Dividida en lugares | Reduce riesgo de robo total | Si se pierde una parte, problema (no dividir de forma ingenua) |

Sobre dividir la frase: **no la partas por la mitad en dos lugares** (eso reduce mucho la seguridad, porque cada mitad facilita adivinar el resto). Si necesitas distribuir el riesgo, usa soluciones diseñadas para eso: multifirma o el esquema **SLIP-39 / Shamir** (que tienen algunos dispositivos Trezor), donde se generan varias partes y se necesita un mínimo para recuperar (por ejemplo, 2 de 3).

## 13.5 La passphrase (palabra 13 o 25)

Muchas billeteras permiten agregar una **passphrase** opcional. Con la misma frase semilla y distinta passphrase se generan billeteras completamente distintas.

Ventajas:
- Si alguien encuentra tus 24 palabras, sin la passphrase no accede a los fondos.
- Permite tener una billetera "señuelo" con poco saldo (sin passphrase) y la real oculta.

Riesgos:
- **Si olvidas la passphrase, pierdes los fondos.** No hay forma de recuperarla.
- Debe respaldarse en un lugar **distinto** de la frase semilla.

Recomendación: para principiantes, primero domina el manejo de la frase semilla. Agrega passphrase solo cuando entiendas bien el respaldo.

## 13.6 Las estafas que buscan tu frase semilla

El agente debe reconocer estos patrones y alertar de inmediato:

- **Falso soporte técnico:** publicaste una duda en un grupo o en redes, y alguien te escribe por mensaje privado: "Soy del soporte de MetaMask/Ledger/Binance, para resolver tu problema necesito validar tu billetera". **El soporte real nunca escribe primero por mensaje privado y nunca pide la frase.**
- **Sitios de "validación" o "sincronización" de billeteras:** te piden ingresar la frase para "sincronizar", "rectificar", "migrar" o "desbloquear" fondos.
- **Correos o cartas físicas falsas de fabricantes:** después de filtraciones de datos de clientes de fabricantes de hardware, hubo campañas de correos y hasta cartas por correo postal con dispositivos falsos o pidiendo "actualizar" la frase.
- **Apps falsas** que imitan billeteras reales y envían la frase al atacante.
- **Formularios de "airdrop" o "recompensas"** que piden la frase para reclamar.
- **"Recuperadores de fondos"** que prometen recuperar tu dinero estafado si les das acceso.

Respuesta estándar que el agente debe dar: **"Nadie legítimo necesita tu frase semilla. Si ya la compartiste, considera que tus fondos están en riesgo: crea una billetera nueva con una frase nueva y mueve todo de inmediato."**

## 13.7 Herencia: el tema que nadie quiere tocar

Si mueres o quedas incapacitado y nadie sabe cómo acceder a tu cripto, esos fondos se pierden para siempre. Se estima que una parte relevante de los bitcoins perdidos corresponde a esto.

Plan mínimo:
1. **Un documento de instrucciones** (sin la frase): qué activos tienes, en qué billeteras/exchanges, dónde está el respaldo, y a quién acudir.
2. **Acceso físico controlado:** caja de seguridad, notario, o una persona de confianza que sepa dónde está todo pero no tenga todo por sí sola.
3. **Para exchanges:** tus herederos podrán reclamar con procesos legales (certificado de defunción, posesión efectiva, etc.). Deja registro de qué exchanges usas.
4. **Para montos grandes:** multifirma con un servicio de herencia, o asesoría legal especializada.
5. **Revisa el plan** cuando cambien tus billeteras.

## 13.8 Qué hacer si crees que tu frase está comprometida

1. No esperes. Los ladrones usan bots que vacían billeteras en segundos.
2. Crea una **billetera nueva** con una **frase nueva** (en un dispositivo limpio).
3. Mueve todos los fondos a la billetera nueva.
4. Revoca aprobaciones de la billetera vieja si aún queda algo.
5. Nunca vuelvas a usar la frase comprometida.

Si los fondos ya fueron robados: ver capítulo 18 (sección "Qué hacer si te estafaron").

## 13.9 Ideas clave del capítulo

- La frase semilla es el dinero. Quien la tiene, lo controla.
- Solo en papel o metal, nunca digital, nunca compartida.
- Todo el que la pide es un estafador.
- Planifica la herencia.

---

# Capítulo 14. Exchanges: centralizados y descentralizados

## 14.1 Qué es un exchange

Un **exchange** es una plataforma para comprar, vender e intercambiar criptomonedas. Es, para la mayoría de las personas, la **puerta de entrada y salida** entre el dinero tradicional (pesos, dólares) y cripto. A esa función se le llama **on-ramp** (entrada) y **off-ramp** (salida).

## 14.2 Exchanges centralizados (CEX)

Empresas que operan como intermediarios. Tú depositas dinero, ellos custodian tus fondos y llevan un libro de órdenes interno.

**Exchanges internacionales con presencia en Latinoamérica [VERIFICAR disponibilidad, licencias y servicios en cada país]:**
- **Binance:** el mayor por volumen. Amplia oferta. Ha tenido problemas regulatorios importantes (en 2023 llegó a un acuerdo con autoridades de EE.UU. por violaciones de normas antilavado).
- **Coinbase:** empresa listada en bolsa en EE.UU., foco regulatorio.
- **Kraken, OKX, Bybit, Bitget, KuCoin, Crypto.com**, entre otros.

**Exchanges regionales/locales (ejemplos) [VERIFICAR]:**
- **Chile:** Buda.com, CryptoMKT, Orionx; además operan exchanges internacionales y regionales.
- **México:** Bitso.
- **Argentina:** Lemon, Belo, Ripio, Buenbit.
- **Brasil:** Mercado Bitcoin, Foxbit; también Mercado Pago ofrece cripto.
- **Colombia, Perú y otros:** Bitso, Binance P2P y operadores locales.

### Ventajas de un CEX
- Fácil de usar.
- Depósitos y retiros en moneda local (transferencia bancaria).
- Liquidez alta.
- Soporte al cliente (variable en calidad).
- Recuperación de cuenta si olvidas la contraseña.

### Desventajas y riesgos
- **Custodia:** no son tus claves.
- **Riesgo de quiebra o fraude:** FTX (2022) usó fondos de clientes para apuestas propias y quebró, dejando a millones de usuarios con fondos atrapados durante años.
- **Congelamiento de cuentas:** por revisiones de cumplimiento, a veces sin explicación clara.
- **Hackeos:** han sido hackeados exchanges grandes. En febrero de 2025, Bybit sufrió el mayor robo de la historia cripto (~1.500 millones de dólares en ETH), atribuido a Corea del Norte; el exchange cubrió las pérdidas de clientes.
- **Riesgo regulatorio:** un exchange puede dejar de operar en tu país.

### Cómo evaluar un CEX
1. **¿Está registrado o licenciado en tu país o en jurisdicciones serias?** (En Chile, revisar registro ante la CMF bajo la Ley Fintec; en la UE, el registro MiCA de ESMA.)
2. **¿Publica prueba de reservas (Proof of Reserves)?** Muestra que tiene los activos de clientes. Ojo: sin incluir pasivos, es una prueba incompleta.
3. **¿Cuánto tiempo lleva operando?** ¿Ha sobrevivido mercados bajistas?
4. **¿Qué historial de hackeos tiene y cómo respondió?**
5. **¿Qué medidas de seguridad ofrece?** (2FA con app, llaves físicas, listas blancas de retiro.)
6. **¿Cómo son las comisiones** de depósito, trading y retiro?
7. **¿Qué dicen los usuarios del soporte?**

## 14.3 Tipos de operaciones en un CEX

### "Comprar/Vender" simple (conversión instantánea)
Botón grande de comprar. Fácil, pero **normalmente con spread o comisión más alta**, que a veces no se muestra explícitamente.

### Spot trading (mercado al contado)
Operar en el libro de órdenes. Más barato, un poco más complejo.
- **Orden de mercado (market):** compra/vende ya, al mejor precio disponible. Paga comisión de "taker" (más alta).
- **Orden límite (limit):** fijas el precio. Se ejecuta solo si el mercado llega ahí. Suele pagar comisión de "maker" (más baja).
- **Stop-loss:** orden que se activa si el precio cae a cierto nivel, para limitar pérdidas.
- **Libro de órdenes:** lista de compradores (bids) y vendedores (asks). La diferencia entre el mejor bid y el mejor ask es el **spread**.

### P2P (persona a persona)
El exchange conecta compradores y vendedores que se pagan directamente (por transferencia bancaria u otros medios), mientras el exchange retiene la cripto en garantía ("escrow").
- Útil en países con controles cambiarios o pocos on-ramps.
- **Riesgos:** fraude con transferencias revertidas, pagos de terceros (cuentas de "mulas" que pueden involucrarte en lavado de dinero), estafas fuera de la plataforma. Reglas: opera solo dentro de la plataforma, con contrapartes con historial alto, y nunca liberes cripto antes de confirmar el pago **en tu banco**, no en una captura de pantalla.

### Productos con riesgo alto (no recomendados para principiantes)
- **Margin trading:** operar con dinero prestado.
- **Futuros y perpetuos:** contratos con apalancamiento de hasta 100x o más.
- **Productos "Earn" o de rendimiento:** prestar tus fondos al exchange para que te pague interés. Antes de 2022, Celsius, BlockFi y Voyager ofrecían esto y quebraron. Lee siempre de dónde sale el rendimiento y si los fondos quedan segregados.
- **Copy trading:** copiar las operaciones de otros. Los rankings de "traders exitosos" tienen sesgo de supervivencia.

## 14.4 KYC y AML

- **KYC (Know Your Customer):** verificación de identidad. Te pedirán documento, selfie, a veces comprobante de domicilio y origen de fondos.
- **AML (Anti-Money Laundering):** reglas antilavado. Los exchanges monitorean transacciones y pueden pedir explicaciones.
- **Travel Rule:** norma del GAFI/FATF que exige que los proveedores compartan información de remitente y receptor en transferencias. Por eso algunos exchanges te preguntan, al retirar, si la dirección de destino es tuya o de otro exchange.

Implicancia: **todo lo que compras en un exchange con KYC queda vinculado a tu identidad**, y en muchos países el exchange reporta información al servicio de impuestos.

## 14.5 Exchanges descentralizados (DEX)

Revisados en el capítulo 9. Resumen:
- Operas directamente desde tu billetera, sin cuenta.
- No hay KYC (en la mayoría).
- No puedes depositar pesos: necesitas ya tener cripto.
- Cualquiera puede crear un par de trading, **incluidos tokens fraudulentos con el mismo nombre que uno legítimo**. Verifica siempre la **dirección del contrato** del token en fuentes oficiales.

## 14.6 CEX vs DEX: cuándo cada uno

| Necesidad | Mejor opción |
|---|---|
| Convertir pesos a cripto por primera vez | CEX local o regional regulado |
| Comprar BTC o ETH para mantener | CEX y luego retirar a tu billetera |
| Acceder a tokens de DeFi que no están en exchanges | DEX (con mucho cuidado) |
| Vender cripto y recibir pesos en tu banco | CEX |
| Privacidad respecto a terceros | DEX (pero la blockchain sigue siendo pública) |
| Máxima simplicidad | CEX |

## 14.7 Otras vías de acceso

- **Fintechs y bancos digitales** que ofrecen compra de cripto dentro de su app (custodial, normalmente sin opción de retirar a tu billetera, o con limitaciones) **[VERIFICAR por país]**.
- **ETFs de cripto:** fondos cotizados en bolsa que replican el precio de BTC, ETH u otras. Se compran con una cuenta de corredora como cualquier acción. Ventajas: regulación del mercado de valores, sin manejo de claves. Desventajas: comisión anual de administración, solo operan en horario bursátil, no puedes usar la cripto. Desde Latinoamérica se accede vía corredoras con acceso a mercados de EE.UU. o mediante productos locales que repliquen esos ETFs **[VERIFICAR opciones]**.
- **Cajeros (ATMs) de Bitcoin:** existen en algunas ciudades. Comisiones muy altas y usados frecuentemente en estafas (víctimas a quienes se les indica depositar efectivo).

## 14.8 Ideas clave del capítulo

- El exchange es la puerta de entrada y salida; no debería ser tu bóveda de largo plazo.
- Evalúa licencias, historial y prueba de reservas.
- Usa órdenes límite en el modo spot para pagar menos.
- En P2P, confirma pagos en tu banco, nunca por captura de pantalla.
- En un DEX, verifica el contrato del token.

---

# Capítulo 15. Tu primera compra, paso a paso

## 15.1 Antes de comprar: cinco preguntas

1. **¿Por qué quiero comprar?** "Porque sube" no es una razón; es la que lleva a comprar caro. Razones mejores: aprender, diversificar una parte pequeña del patrimonio con tesis de largo plazo, necesidad de usar stablecoins.
2. **¿Cuánto puedo perder sin que afecte mi vida?** Esa es la cantidad máxima. Ni un peso más.
3. **¿Tengo fondo de emergencia y deudas caras bajo control?** Si tienes deudas de tarjeta de crédito al 30–50% anual, pagarlas es una "inversión" con rendimiento garantizado mejor que cualquier cripto.
4. **¿Cuánto tiempo pienso mantenerlo?** Si necesitas ese dinero en 6 meses, no debería estar en un activo que puede caer 50%.
5. **¿Qué haré si cae 50%?** Si la respuesta honesta es "vender en pánico", la cantidad es demasiado grande.

## 15.2 Paso 1: Elegir el exchange

Con los criterios del capítulo 14. Para una primera compra, conviene un exchange con:
- Operación legal y registro en tu país.
- Depósito por transferencia bancaria en moneda local.
- Buena reputación de soporte.

## 15.3 Paso 2: Crear la cuenta de forma segura

1. **Entra escribiendo la URL** o desde la app oficial de la tienda de aplicaciones. No desde anuncios ni enlaces de mensajes.
2. Usa un **correo electrónico dedicado** si es posible, con contraseña única y 2FA.
3. Crea una **contraseña larga y única** (usa un gestor de contraseñas).
4. Completa el **KYC** con tus datos reales.
5. **Activa la autenticación de dos factores (2FA)** con una app autenticadora (Google Authenticator, Authy, Aegis, etc.) o una llave física (YubiKey). **Evita el SMS** como segundo factor si hay alternativa: es vulnerable a "SIM swapping" (robo de tu número telefónico).
6. Respalda los códigos de recuperación del 2FA en papel.
7. Activa, si existen: **código anti-phishing** (el exchange incluye un código que tú defines en sus correos reales), **lista blanca de direcciones de retiro**, y **bloqueo de retiros** tras cambios de seguridad.

## 15.4 Paso 3: Depositar moneda local

- Normalmente por transferencia bancaria desde una cuenta **a tu nombre**. Transferencias de terceros suelen ser rechazadas.
- Revisa comisiones de depósito y tiempos.
- Empieza con un monto pequeño para probar el flujo completo.

## 15.5 Paso 4: Comprar

Dos formas:
- **Botón "Comprar":** fácil, pero revisa el precio final que te dan comparado con el precio del mercado. La diferencia es tu costo real.
- **Spot con orden límite:** pones el precio al que quieres comprar. Suele ser más barato.

Ejemplo práctico: quieres comprar BTC con 100.000 pesos.
1. Ve a la sección de trading BTC/CLP (o el par en tu moneda).
2. Elige "Límite".
3. Mira el mejor precio de venta (ask). Pon tu precio de compra igual o levemente más bajo.
4. Ingresa el monto en pesos.
5. Revisa la comisión estimada.
6. Confirma.

**Anota:** fecha, cantidad comprada, precio, comisión. Lo necesitarás para impuestos (capítulo 26). Muchos exchanges permiten descargar este historial, pero es bueno tener tu propio registro.

## 15.6 Paso 5: Decidir dónde guardarlo

- Si el monto es pequeño y estás aprendiendo: puede quedar en el exchange mientras te familiarizas.
- Si quieres practicar autocustodia o el monto es relevante: retira a tu billetera (Paso 6).

## 15.7 Paso 6: Primer retiro a tu propia billetera

1. Configura tu billetera no custodial y respalda la frase semilla (capítulo 13).
2. En la billetera, pulsa **"Recibir"** y copia la dirección (o escanea el QR).
3. En el exchange, ve a **"Retirar"**, elige la moneda y **la red correcta** (capítulo 16).
4. **Pega la dirección y verifica los primeros y últimos 4–6 caracteres.** Existe malware que cambia la dirección del portapapeles por la del atacante.
5. **Primero envía un monto pequeño de prueba.**
6. Espera a que llegue y aparezca en tu billetera.
7. Luego envía el resto.

Las comisiones de retiro pueden ser fijas (por ejemplo, una cantidad de BTC independiente del monto). Por eso, retirar muchas veces montos chicos sale caro.

## 15.8 Paso 7: Probar la recuperación (opcional pero muy recomendable)

Con montos pequeños, borra la billetera del teléfono (o usa otro dispositivo), restaura con la frase semilla y comprueba que aparecen los fondos. Ahora sabes que tu respaldo funciona.

## 15.9 Cómo vender y volver a pesos

1. Si la cripto está en tu billetera, envíala al exchange (depositar → elegir moneda y red → copiar la dirección del exchange → enviar desde tu billetera).
2. Espera las confirmaciones necesarias.
3. Vende (botón o spot).
4. Retira los pesos a tu cuenta bancaria a tu nombre.
5. Registra la operación para impuestos.

## 15.10 Errores de primera compra más comunes

- Comprar en un pico de euforia mediática.
- Comprar una moneda "barata" por precio unitario.
- Usar el botón de compra rápida sin ver el spread.
- No activar 2FA.
- Enviar por la red equivocada.
- No hacer un envío de prueba.
- Revisar el precio cada 10 minutos y operar por impulso.

## 15.11 Ideas clave del capítulo

- Decide cuánto puedes perder antes de comprar.
- Asegura la cuenta antes de depositar.
- Orden límite > botón de compra rápida, en costo.
- Envío de prueba siempre. Registra todo para impuestos.

---

# Capítulo 16. Enviar y recibir: direcciones, redes y comisiones

## 16.1 Por qué los envíos generan tantas pérdidas

Una transferencia bancaria a una cuenta inexistente rebota. Una transferencia cripto a una dirección equivocada, por una red equivocada, **normalmente no tiene vuelta atrás**. Este capítulo es corto en conceptos y largo en precauciones.

## 16.2 Anatomía de un envío

Para enviar cripto necesitas tres datos:
1. **El activo:** BTC, ETH, USDC, SOL…
2. **La red:** Bitcoin, Ethereum, Tron, Solana, Arbitrum, Base, BNB Chain…
3. **La dirección de destino.**

Y a veces un cuarto:
4. **Memo / tag / destination tag:** algunas redes (XRP, Stellar, Cosmos, TON, EOS) y muchos exchanges usan una sola dirección para todos sus clientes y te identifican con un número o texto adicional. **Si el exchange te da un memo, es obligatorio incluirlo.** Si no lo incluyes, los fondos llegan al exchange pero no a tu cuenta, y recuperarlos requiere un trámite con soporte que puede tardar o no resolverse.

## 16.3 Cómo se ven las direcciones en las redes más comunes

| Red | Formato típico | Ejemplo de inicio |
|---|---|---|
| Bitcoin | 26–62 caracteres | `bc1q...`, `bc1p...`, `1...`, `3...` |
| Ethereum y redes EVM (Arbitrum, Base, Optimism, Polygon, BNB Chain, Avalanche C) | 42 caracteres | `0x...` |
| Solana | 32–44 caracteres base58 | letras y números, sin `0x` |
| Tron | 34 caracteres | `T...` |
| XRP | | `r...` + destination tag |
| Litecoin | | `ltc1...`, `L...`, `M...` |
| Dogecoin | | `D...` |
| TON | | `UQ...` / `EQ...` + memo en exchanges |

**El peligro de las redes EVM:** una dirección `0x...` es válida en Ethereum, Arbitrum, Base, BNB Chain, Polygon, etc. Si envías USDC por Arbitrum a una dirección de exchange que solo monitorea Ethereum, la transacción se completa en la blockchain, pero el exchange no lo acredita. A veces se puede recuperar (si el exchange controla esa dirección en la otra red y acepta hacerlo), a veces no.

**Regla para el agente:** ante cualquier consulta de envío, preguntar o recordar: **¿la plataforma de destino acepta ese activo en esa red específica?**

## 16.4 Checklist antes de enviar

1. ¿El activo es correcto?
2. ¿La red de origen es **exactamente** la que acepta el destino?
3. ¿La dirección es correcta? (Verifica inicio y final; mejor aún, verifícala completa en la pantalla de la billetera de hardware.)
4. ¿Hace falta memo/tag?
5. ¿El monto, descontada la comisión, supera el mínimo de depósito del destino? (Algunos exchanges no acreditan depósitos bajo cierto mínimo.)
6. ¿Hice un envío de prueba si es la primera vez a esa dirección?
7. ¿Tengo saldo de la moneda nativa para pagar el gas? (Para enviar USDC en Ethereum necesitas ETH; en Solana necesitas SOL; en Tron necesitas TRX o "energía".)

## 16.5 El problema del gas en otra moneda

Situación clásica: alguien tiene 500 USDT en la red Tron y no puede enviarlos porque no tiene TRX para la comisión. O tiene USDC en Ethereum sin ETH.

Soluciones:
- Comprar una pequeña cantidad de la moneda nativa y enviarla a esa billetera.
- Algunas billeteras nuevas permiten pagar comisiones con la propia stablecoin (abstracción de cuentas).
- Planificar: siempre mantener un pequeño saldo de la moneda nativa en cada red que uses.

## 16.6 Comisiones por red (orientativo)

| Red | Costo típico de una transferencia | Velocidad |
|---|---|---|
| Bitcoin (capa base) | Muy variable: de centavos a varios dólares en congestión | ~10 min por confirmación |
| Lightning | Fracciones de centavo | Segundos |
| Ethereum (capa base) | Variable; puede ser bajo en calma, alto en congestión | ~12 s por bloque |
| Capas 2 de Ethereum | Centavos o menos | Segundos |
| Solana | Fracciones de centavo | Segundos |
| Tron | Bajo, pero depende de energía/ancho de banda | Segundos |

**[VERIFICAR: las comisiones cambian con la congestión y las actualizaciones de red.]**

Además de la comisión de red, **los exchanges cobran su propia comisión de retiro**, que puede ser mayor que la de la red.

## 16.7 Transacción atascada

En Bitcoin, si pagaste comisión muy baja, la transacción puede quedar pendiente. Opciones:
- **RBF (Replace-By-Fee):** reenviar la misma transacción con comisión más alta, si tu billetera lo habilitó.
- **CPFP (Child-Pays-For-Parent):** el receptor gasta el monto pendiente con comisión alta, incentivando a los mineros a incluir ambas.
- Esperar: si la congestión baja, se confirmará; si no, eventualmente puede ser descartada de la mempool y los fondos "vuelven" (nunca salieron).

En Ethereum y EVM, una transacción pendiente bloquea las siguientes (por el "nonce"). Las billeteras permiten "acelerar" o "cancelar" enviando otra con el mismo nonce y mayor comisión.

## 16.8 Exploradores de bloques

Un **explorador de bloques** es un sitio web que muestra el contenido de la blockchain. Sirve para comprobar si una transacción se envió, cuántas confirmaciones tiene y a qué dirección llegó.

- Bitcoin: mempool.space, blockstream.info
- Ethereum: etherscan.io
- Arbitrum: arbiscan.io; Base: basescan.org
- Solana: solscan.io, explorer.solana.com
- Tron: tronscan.org

Cada transacción tiene un identificador único (**TXID** o **hash de transacción**). Es lo que pide el soporte de un exchange cuando reclamas un depósito.

## 16.9 Envenenamiento de direcciones (address poisoning)

Estafa muy extendida:
1. El atacante ve en la blockchain que enviaste fondos a una dirección (por ejemplo, `0x1234...abcd`).
2. Genera una dirección que empieza y termina igual (`0x1234...abcd`) pero con el medio distinto.
3. Te envía una transacción de valor cero o ínfimo desde esa dirección, para que aparezca en tu historial.
4. La próxima vez, copias "la dirección de siempre" desde tu historial... y copias la del atacante.

Protección:
- **No copies direcciones desde el historial de transacciones.**
- Usa la libreta de direcciones guardada de tu billetera o la lista blanca del exchange.
- Verifica la dirección **completa**, no solo inicio y fin, cuando el monto es importante.

## 16.10 Ideas clave del capítulo

- Activo + red + dirección (+ memo) deben coincidir con lo que acepta el destino.
- Una dirección `0x` sirve en muchas redes: elige la correcta.
- Necesitas moneda nativa para pagar gas.
- No copies direcciones desde el historial (address poisoning).
- Envío de prueba siempre que sea la primera vez.


---

# Capítulo 17. Seguridad operativa

## 17.1 El modelo de amenazas

Antes de elegir medidas, hay que saber **de qué te proteges**. Para un usuario común, las amenazas reales, en orden aproximado de frecuencia, son:

1. **Ingeniería social y phishing** (te engañan para que entregues acceso o firmes algo).
2. **Errores propios** (red equivocada, frase perdida, dirección mal copiada).
3. **Malware** en tu computador o teléfono.
4. **Robo de cuentas** (correo, número telefónico, exchange).
5. **Fallas o fraude de un custodio** (exchange que quiebra).
6. **Robo físico o coerción** (rara pero real para personas que exhiben su patrimonio).
7. **Hackeos de contratos o protocolos** (si usas DeFi).

Casi nunca es "alguien hackeó Bitcoin". Casi siempre es una de las primeras cuatro.

## 17.2 Higiene digital básica

### Correo electrónico
Tu correo es la llave maestra: con él se resetean contraseñas de exchanges.
- Contraseña única y larga.
- 2FA con app o llave física.
- Considera un correo exclusivo para cripto que no publiques en ningún lado.
- Revisa reglas de reenvío y filtros: un atacante con acceso temporal puede crear una regla que reenvíe tus correos de exchange.

### Número telefónico y SIM swapping
El **SIM swapping** consiste en que un atacante convence (o soborna) a tu operadora para trasladar tu número a una SIM suya. Con eso recibe tus SMS de verificación.
- No uses SMS como 2FA si hay alternativa.
- Pide a tu operadora una clave o bloqueo adicional para cambios de SIM, si lo ofrece.
- No publiques tu número asociado a tu identidad cripto.

### Contraseñas
- Un **gestor de contraseñas** reconocido (Bitwarden, 1Password, KeePassXC, entre otros).
- Contraseña única para cada servicio.
- Nunca reutilices la contraseña del exchange.

### 2FA: jerarquía de seguridad
1. **Llave física (FIDO2/WebAuthn, como YubiKey):** la más resistente a phishing.
2. **Passkeys**, donde estén disponibles.
3. **App autenticadora (TOTP).**
4. **SMS:** el más débil.

### Dispositivos
- Sistema operativo y apps actualizados.
- No instales software pirata (es una fuente clásica de malware que roba billeteras).
- Desconfía de extensiones de navegador que no necesitas.
- Considera un dispositivo o perfil de navegador dedicado solo a cripto.
- No conectes tu billetera a sitios en Wi-Fi públicas sin protección.

## 17.3 Seguridad específica en exchanges

- **Lista blanca de direcciones de retiro** (whitelist): solo permite retirar a direcciones que registraste previamente, con un período de espera para agregar nuevas. Si alguien entra a tu cuenta, no puede retirar a su dirección de inmediato.
- **Código anti-phishing:** el exchange incluye una palabra secreta en sus correos reales.
- **Bloqueo de retiros por 24–48 horas** tras cambios de contraseña o 2FA.
- **Revisión de sesiones y dispositivos activos.**
- **Claves API:** si las creas (por ejemplo, para herramientas de impuestos), dales solo permiso de lectura, nunca de retiro.

## 17.4 Seguridad al firmar transacciones (DeFi y Web3)

Cuando conectas tu billetera a un sitio, este puede pedirte:

1. **Conexión:** solo comparte tu dirección. Bajo riesgo en sí.
2. **Firma de mensaje (sign):** puede ser inofensiva (iniciar sesión) o peligrosa. Las firmas tipo **"Permit"** o **"Permit2"** pueden autorizar a alguien a mover tus tokens sin una transacción adicional. Muchos robos ocurren con firmas que el usuario creyó inofensivas.
3. **Aprobación (approve):** autoriza a un contrato a mover tus tokens.
4. **Transacción:** mueve fondos directamente.

Reglas:
- **Lee lo que firmas.** Usa billeteras que simulen y expliquen la transacción (Rabby, y extensiones de seguridad como Pocket Universe, Wallet Guard o similares **[VERIFICAR disponibilidad]**).
- **Si no entiendes qué estás firmando, no lo firmes.**
- Desconfía de "setApprovalForAll" (da acceso a toda una colección de NFTs) y de firmas "Permit" en sitios desconocidos.
- Usa una billetera desechable para sitios nuevos.
- Revisa y revoca aprobaciones (Revoke.cash).

## 17.5 Phishing: cómo se ve hoy

- **Anuncios patrocinados en buscadores** que imitan exchanges o protocolos (el primer resultado puede ser falso).
- **Dominios casi idénticos:** `uniswap.org` vs. `uníswap.org` o `uniswap-app.org`.
- **Cuentas de redes sociales hackeadas** de proyectos legítimos, que publican un enlace a un "airdrop".
- **Respuestas falsas** en hilos de X/Twitter, Discord y Telegram que suplantan cuentas oficiales.
- **Correos que imitan a exchanges** avisando de "actividad sospechosa".
- **Llamadas telefónicas** de supuestos agentes de exchanges o bancos (en 2024–2025 hubo campañas grandes de suplantación de soporte de Coinbase).
- **Deepfakes de video** de figuras conocidas promocionando "regalos" de cripto.

Regla: **entra siempre por marcadores guardados o escribiendo la URL**. Nunca por enlaces recibidos.

## 17.6 Privacidad y seguridad física

- **No publiques cuánto tienes.** Las capturas de saldos y "ganancias" en redes sociales atraen estafadores y, en casos extremos, delincuentes. Hay casos documentados de secuestros y robos violentos dirigidos a poseedores de cripto ("ataques de llave inglesa").
- Ten cuidado con lo que revelas en eventos y grupos.
- Las filtraciones de datos de exchanges y fabricantes de billeteras han expuesto direcciones físicas de clientes. Considera recibir tu billetera de hardware en una dirección distinta a tu domicilio si te preocupa.
- Una passphrase con billetera señuelo (capítulo 13) puede servir ante coerción.

## 17.7 Rutina de seguridad trimestral

Cada tres meses:
1. Revisa que tus respaldos de frase semilla sigan en su lugar y legibles.
2. Revoca aprobaciones de tokens que ya no uses.
3. Revisa sesiones activas en exchanges y en tu correo.
4. Actualiza firmware de billeteras de hardware (solo desde la app oficial).
5. Revisa que tu plan de herencia siga vigente.
6. Exporta el historial de operaciones del trimestre (para impuestos).

## 17.8 Ideas clave del capítulo

- La amenaza principal es el engaño, no el hackeo sofisticado.
- Asegura correo y número telefónico: son llaves maestras.
- 2FA con llave física o app, nunca SMS si hay alternativa.
- Lee lo que firmas. Si no lo entiendes, no lo firmes.
- No exhibas tu patrimonio.

---

# Capítulo 18. Estafas y fraudes: catálogo y cómo detectarlos

## 18.1 La regla que resume todo

> **Si te prometen ganancias garantizadas, altas y sin riesgo, es una estafa. Siempre.**

En cripto, como en finanzas tradicionales, el rendimiento alto viene con riesgo alto. Nadie regala dinero. Nadie "duplica tus bitcoins".

## 18.2 Señales de alerta universales

El agente debe identificar estas señales y nombrarlas explícitamente al usuario:

1. **Rendimientos garantizados** ("2% diario", "duplica en 30 días").
2. **Urgencia** ("solo por hoy", "quedan 10 cupos").
3. **Contacto no solicitado** (te escriben primero por redes, WhatsApp, Telegram, apps de citas).
4. **Pedido de frase semilla, clave privada o acceso remoto.**
5. **Pedido de pagar para retirar** ("debes pagar un impuesto/comisión de liberación antes de retirar tus ganancias").
6. **Secreto o exclusividad** ("no le cuentes a tu banco", "es una oportunidad privada").
7. **Plataformas desconocidas** que solo se encuentran por el enlace que te dio la persona.
8. **Celebridades o "expertos"** que regalan cripto.
9. **Ganancias espectaculares que solo se ven en la pantalla** de la plataforma, sin poder retirarlas.
10. **Presión emocional:** romance, culpa, miedo, amistad repentina.

## 18.3 Catálogo de estafas

### Esquemas Ponzi y piramidales
Pagan "rendimientos" a los primeros participantes con el dinero de los nuevos. Colapsan cuando entran menos personas.
- Casos históricos: **BitConnect** (2016–2018), **OneCoin** (estafa de ~4.000 millones de dólares que ni siquiera tenía blockchain), **PlusToken**.
- En Latinoamérica han existido múltiples esquemas que prometían rendimientos fijos mensuales por "trading" o "minería" **[el agente puede mencionar que existen casos locales sin nombrar sin verificar]**.
- Señal: rendimiento fijo, bonos por traer gente, "planes" de inversión.

### Pig butchering ("carnicería de cerdos")
Estafa de larga duración, frecuentemente operada por redes criminales organizadas:
1. Contacto "casual" (mensaje equivocado, app de citas, LinkedIn).
2. Semanas de conversación amistosa o romántica.
3. La persona menciona que gana dinero con cripto y ofrece "enseñarte".
4. Te lleva a una plataforma falsa que muestra ganancias ficticias.
5. Te deja retirar un poco al principio para generar confianza.
6. Te anima a invertir más, incluso pedir préstamos.
7. Cuando intentas retirar todo, aparecen "impuestos" o "comisiones" que debes pagar primero.
8. Desaparecen.

Es una de las estafas que más dinero mueve en el mundo según reportes del FBI **[VERIFICAR cifras actuales del FBI IC3]**. Si un usuario describe algo parecido, el agente debe decirlo con claridad.

### Falsos regalos (giveaways)
"Envía 1 ETH y te devolvemos 2". Suelen usar videos falsos o en vivo hackeados de figuras conocidas.

### Rug pulls
El equipo de un token o proyecto retira la liquidez o vende todo y desaparece. Muy común en memecoins y tokens nuevos de DEX.
Variante: **soft rug**, el equipo abandona lentamente el proyecto tras vender.

### Honeypots
Tokens programados para que puedas comprar pero **no vender**. Ves cómo "sube" tu inversión pero nunca puedes salir. Herramientas como Token Sniffer o Honeypot.is ayudan a detectarlos **[VERIFICAR]**, pero no son infalibles.

### Pump and dump
Grupos coordinados (Telegram, Discord) inflan el precio de un token poco líquido y venden a los que llegan tarde. Los "organizadores" compran antes de anunciar.

### Airdrops falsos y tokens no solicitados
Aparece un token o NFT en tu billetera con un enlace a un sitio para "reclamar" o "vender". El sitio te pide firmar una aprobación que vacía tu billetera.

### Phishing y drainers
Sitios falsos que imitan protocolos o exchanges. Existen "kits de drainer" que se venden como servicio a criminales.

### Falso soporte técnico
Visto en el capítulo 13. Nunca entregues frase semilla ni instales software de acceso remoto (AnyDesk, TeamViewer) por indicación de un "soporte".

### Recuperadores de fondos (recovery scams)
Después de una estafa, aparecen "hackers éticos", "abogados" o "agencias" que prometen recuperar tu dinero a cambio de un pago adelantado. **Es una segunda estafa sobre la misma víctima.** Las víctimas a menudo están en listas que se venden entre estafadores.

### Minería en la nube falsa
"Alquila poder de minado y recibe BTC diario". La mayoría son Ponzi.

### Bots de trading con IA "garantizados"
Prometen rendimientos fijos gracias a un algoritmo secreto o inteligencia artificial. Si un bot ganara de forma consistente, sus creadores no necesitarían tu dinero.

### Préstamos con cripto falsos
Te ofrecen un préstamo en pesos si primero envías cripto como "garantía" o "comisión".

### ICO / preventas falsas
Proyectos que venden tokens antes de lanzarse y desaparecen con el dinero.

### Estafas en P2P
Pagos falsos (capturas editadas), transferencias que se revierten, uso de cuentas de terceros. Siempre confirma en tu banco.

### Estafas de cajeros Bitcoin
Alguien (supuesto banco, policía, servicio de impuestos o familiar en apuros) indica a la víctima que deposite efectivo en un cajero de Bitcoin a una dirección QR que envía. Afecta mucho a adultos mayores.

### Extorsión ("sextorsión" con cripto)
Correos que dicen tener videos comprometedores y exigen pago en BTC. Casi siempre son mentira y se envían de forma masiva.

### Empleos falsos
Ofertas de trabajo que piden "depositar cripto para desbloquear tareas" o comisiones.

### Malware de portapapeles
Cambia la dirección que copias por la del atacante. Verifica siempre la dirección pegada.

## 18.4 Cómo verificar un proyecto o plataforma antes de invertir

1. ¿Está registrada ante el regulador financiero de tu país? (En Chile, CMF; en México, CNBV; en Argentina, CNV; en Colombia, SFC; en Perú, SBS/SMV; en España, CNMV/Banco de España; en la UE, registro de ESMA.) Los reguladores publican también **listas de alertas** de entidades no autorizadas.
2. ¿Hay información pública verificable sobre el equipo?
3. ¿Hay reportes negativos? Busca "[nombre] + estafa / scam / fraude / reviews".
4. ¿Puedes retirar fondos sin condiciones extrañas?
5. ¿El dominio web es reciente? (Herramientas de WHOIS muestran la fecha de registro.)
6. ¿El rendimiento prometido tiene una fuente explicable?

## 18.5 Qué hacer si te estafaron

Pasos que el agente puede guiar:

1. **Deja de enviar dinero.** Ningún pago adicional "liberará" tus fondos.
2. **Corta el contacto** con el estafador.
3. **Asegura lo que queda:** si comprometiste tu frase semilla, mueve fondos a una billetera nueva; cambia contraseñas; revoca aprobaciones.
4. **Documenta todo:** capturas de conversaciones, direcciones de billetera, TXIDs, sitios web, montos, fechas.
5. **Reporta:**
   - Al exchange desde el cual enviaste los fondos y, si conoces el exchange de destino, a ese también (pueden congelar fondos si actúan rápido).
   - A la policía (en Chile: PDI, Brigada Investigadora del Cibercrimen, o denuncia en Fiscalía) **[VERIFICAR canal vigente]**.
   - Al regulador financiero, si la plataforma se presentaba como empresa.
   - En EE.UU., el FBI recibe denuncias internacionales en ic3.gov.
6. **Si un emisor de stablecoins es parte de la ruta** (USDT, USDC), a veces pueden congelar fondos a pedido de autoridades.
7. **No caigas en recuperadores de fondos.**
8. **Habla con alguien.** Las estafas, especialmente las románticas, tienen un impacto emocional fuerte. Buscar apoyo de personas cercanas o profesional es parte de la recuperación.

Expectativa realista: la recuperación de fondos es poco frecuente, pero el reporte rápido aumenta las probabilidades y ayuda a detener a los estafadores.

## 18.6 Ideas clave del capítulo

- Rendimiento garantizado = estafa.
- Contacto no solicitado + cripto = máxima sospecha.
- Pagar para retirar = estafa.
- Los "recuperadores de fondos" son una segunda estafa.

---

# PARTE IV — INVERTIR CON CRITERIO

**Nota para el agente:** esta parte es educativa. Explica conceptos, herramientas y riesgos. No recomiendes activos específicos, montos ni momentos de compra o venta. Si el usuario pide "¿compro X?", responde explicando cómo podría evaluarlo, qué riesgos tiene y qué preguntas hacerse.

---

# Capítulo 19. Psicología del inversor y gestión de riesgo

## 19.1 Por qué empezar por la cabeza y no por los gráficos

La mayoría de las pérdidas en cripto no vienen de no saber leer un gráfico. Vienen de **decisiones emocionales**: comprar por euforia, vender por pánico, apostar más para recuperar, usar apalancamiento. Los mercados cripto, abiertos 24/7 y con movimientos de 10% en un día, amplifican todos los sesgos humanos.

## 19.2 Los sesgos más dañinos

- **FOMO (fear of missing out):** miedo a quedarse fuera. Lleva a comprar después de grandes subidas, justo cuando el riesgo es mayor.
- **FUD (fear, uncertainty, doubt):** miedo e incertidumbre. Lleva a vender en caídas, muchas veces en el peor momento.
- **Aversión a la pérdida:** una pérdida duele aproximadamente el doble de lo que alegra una ganancia del mismo tamaño. Lleva a mantener posiciones perdedoras "hasta que vuelvan" y vender las ganadoras demasiado pronto.
- **Sesgo de confirmación:** buscar solo información que confirma lo que ya crees. En cripto, las comunidades de cada token son cámaras de eco.
- **Exceso de confianza:** después de algunas ganancias en mercado alcista, creer que es habilidad y no contexto.
- **Falacia del costo hundido:** "ya perdí mucho, no puedo vender ahora".
- **Anclaje:** fijarse en un precio pasado ("antes valía 4 dólares, a 0,50 está barato").
- **Comportamiento de manada:** "todos están comprando".
- **Sesgo de supervivencia:** ves a quienes ganaron con una memecoin, no a los miles que perdieron.

## 19.3 Gestión de riesgo: las reglas que más importan

### 1. Tamaño de la posición
La decisión más importante no es **qué** comprar, sino **cuánto**. Una forma común de pensarlo:
- Define qué porcentaje de tu patrimonio total puedes tener en cripto sin que una caída de 80% cambie tu vida. Para muchas personas que empiezan, ese número es bajo **[esto es un principio general, no una recomendación personal]**.
- Dentro de cripto, cuanto más especulativo el activo, menor la porción.

### 2. Diversificación (con matices)
En cripto, la correlación entre activos es alta: cuando BTC cae fuerte, casi todo cae más. Tener 20 altcoins no es diversificar; es multiplicar riesgo. La diversificación real es entre clases de activos (efectivo, renta fija, acciones, inmuebles, cripto).

### 3. Nunca invertir dinero prestado
Préstamos de consumo, tarjetas de crédito, avances en efectivo: la combinación de deuda con interés alto y activo volátil es la receta para una ruina financiera.

### 4. Evitar el apalancamiento
- Con apalancamiento 10x, una caída de 10% te liquida.
- Con 50x, una caída de 2%.
- En cripto, caídas de 10% en horas son normales. Los exchanges ganan enormes sumas con las liquidaciones de usuarios minoristas.
- Estudios de reguladores europeos sobre productos apalancados (CFDs) muestran que la mayoría de las cuentas minoristas pierde dinero; las propias plataformas deben advertirlo **[VERIFICAR porcentajes vigentes]**.

### 5. Plan escrito antes de comprar
Responde por escrito:
- ¿Por qué compro esto? (Tesis.)
- ¿Qué tendría que pasar para que mi tesis esté equivocada? (Invalidación.)
- ¿Cuánto tiempo pienso mantenerlo?
- ¿Tomaré ganancias en algún punto? ¿Cómo?
- ¿Qué haré si cae 30%, 50%, 80%?

Un plan escrito en calma vale más que mil decisiones tomadas mirando la pantalla.

### 6. Reducir la exposición a la pantalla
- Desactiva notificaciones de precio.
- Define cuándo revisarás tu portafolio (por ejemplo, una vez por semana o por mes).
- Evita grupos de Telegram/Discord que generan urgencia constante.

### 7. Tomar ganancias
Muchas personas vieron sus inversiones multiplicarse en mercados alcistas y luego volver al punto de partida (o peor) porque nunca vendieron nada. Estrategias simples:
- Vender porcentajes fijos a medida que el valor sube (por ejemplo, recuperar el capital inicial cuando la posición se duplica).
- **Rebalancear:** si cripto pasó de ser 5% a 15% de tu patrimonio, vender una parte para volver al 5%.

## 19.4 Señales de que la relación con el mercado no está sana

El agente debe estar atento a estas señales en la conversación y, si aparecen, priorizar el bienestar del usuario sobre la pregunta técnica:
- Revisar precios de forma compulsiva, también de noche.
- Usar dinero destinado a gastos básicos, arriendo o deudas.
- Pedir préstamos para invertir o para "recuperar".
- Ocultar pérdidas a la pareja o familia.
- Sentir ansiedad, insomnio o irritabilidad asociados al mercado.
- Aumentar el riesgo después de perder.

Estas conductas se parecen mucho a la ludopatía. Es razonable sugerir pausar, hablar con alguien de confianza y, si corresponde, buscar apoyo profesional.

## 19.5 Ideas clave del capítulo

- Cuánto inviertes importa más que en qué inviertes.
- Sin deuda, sin apalancamiento, con plan escrito.
- La diversificación entre altcoins no reduce mucho el riesgo.
- Toma ganancias y rebalancea.

---

# Capítulo 20. Estrategias: DCA, holding, trading y sus trampas

## 20.1 Panorama

Las estrategias se pueden ordenar por cuánto tiempo, conocimiento y estrés exigen:

| Estrategia | Tiempo requerido | Conocimiento | Riesgo de errores emocionales |
|---|---|---|---|
| DCA + mantener | Bajo | Bajo | Bajo |
| Holding con rebalanceo | Bajo | Medio | Bajo-medio |
| Swing trading | Medio | Alto | Alto |
| Day trading | Alto | Muy alto | Muy alto |
| Trading apalancado | Alto | Muy alto | Extremo |

## 20.2 DCA (Dollar-Cost Averaging / promedio de costo)

**Qué es:** invertir un monto fijo a intervalos regulares (por ejemplo, el mismo monto cada mes), sin importar el precio.

**Por qué funciona para muchas personas:**
- Elimina la necesidad de "adivinar el momento".
- Compras más unidades cuando el precio está bajo y menos cuando está alto.
- Reduce el arrepentimiento y la carga emocional.
- Se puede automatizar en muchos exchanges.

**Ejemplo ilustrativo** (números inventados para mostrar el mecanismo):
| Mes | Monto invertido | Precio | Unidades compradas |
|---|---|---|---|
| 1 | 100 | 50 | 2,00 |
| 2 | 100 | 25 | 4,00 |
| 3 | 100 | 40 | 2,50 |
| 4 | 100 | 50 | 2,00 |
| **Total** | **400** | | **10,50** |

Precio promedio pagado: 400 / 10,5 ≈ **38,1**, menor que el precio promedio simple de los cuatro meses (41,25).

**Limitaciones:**
- No evita pérdidas si el activo cae a largo plazo. DCA en un proyecto que va a cero es perder de a poco.
- Con montos muy pequeños, las comisiones pueden pesar mucho (busca opciones de compra recurrente con comisión baja).
- En un mercado que sube de forma sostenida, invertir todo al inicio habría rendido más (pero eso solo se sabe después).

**Para qué activos tiene más sentido:** los que tienen una tesis de largo plazo creíble y alta probabilidad de seguir existiendo. Aplicarlo a memecoins o tokens nuevos es mucho más riesgoso.

## 20.3 HODL (holding de largo plazo)

"HODL" nació de un error de tipeo en un foro en 2013 ("I AM HODLING") y se volvió filosofía: comprar y mantener durante años, ignorando la volatilidad.

**A favor:** históricamente, quienes mantuvieron BTC por ciclos completos de 4 años obtuvieron rendimientos altos (rendimiento pasado no garantiza el futuro).
**En contra:** funciona solo si el activo sobrevive. Muchas altcoins del top 20 de 2017 hoy valen una fracción mínima o desaparecieron.
**Clave:** HODL sin plan de toma de ganancias ni rebalanceo puede significar ver subir y bajar todo sin capturar nada.

## 20.4 Rebalanceo

Definir una proporción objetivo (por ejemplo, X% en cripto dentro del patrimonio total, o dentro de cripto Y% en BTC y Z% en ETH) y ajustarla cada cierto tiempo o cuando se desvíe mucho.
- Fuerza a vender caro y comprar barato de forma disciplinada.
- Ojo con los impuestos: cada venta puede generar un evento tributable.

## 20.5 Trading activo

### Lo que nadie te dice en los cursos de trading
- **La mayoría de los traders minoristas pierde dinero.** Los datos de reguladores sobre productos apalancados y numerosos estudios académicos sobre day trading muestran lo mismo **[VERIFICAR estudios específicos]**.
- Compites contra fondos con algoritmos, información más rápida y comisiones menores.
- Las comisiones y el spread se acumulan: con muchas operaciones, aunque aciertes más de lo que fallas, puedes perder.
- **Los vendedores de cursos de trading** muchas veces ganan más vendiendo cursos que operando.
- El trading activo genera muchos eventos tributables y registros complejos.

### Si igual alguien quiere hacerlo
Principios mínimos:
- Solo con una porción pequeña, separada del ahorro.
- Sin apalancamiento hasta tener historial demostrable de rentabilidad (meses, con registro honesto).
- Siempre con **stop-loss** definido antes de entrar.
- Arriesgar un porcentaje pequeño del capital de trading por operación (muchos usan 1–2%).
- Llevar un **diario de trading**: por qué entraste, por qué saliste, qué sentías.
- Practicar primero en modo demo (muchos exchanges lo ofrecen).

## 20.6 Futuros perpetuos y apalancamiento: explicación para entender el riesgo

- Un **futuro perpetuo** es un contrato que sigue el precio de un activo sin fecha de vencimiento.
- La **tasa de financiamiento (funding rate)** es un pago periódico entre posiciones largas y cortas para mantener el precio del contrato cerca del precio real. Si muchos apuestan al alza, los "largos" pagan a los "cortos".
- **Liquidación:** si el precio va en tu contra lo suficiente para consumir tu margen, el exchange cierra tu posición y pierdes el margen.
- **Cascadas de liquidación:** cuando el precio cae, se liquidan largos, lo que genera ventas forzadas, que bajan más el precio y liquidan más largos. Por eso las caídas en cripto son tan violentas.

El agente debe explicar esto cuando se pregunte por apalancamiento, y dejar claro que **no es apropiado para principiantes**.

## 20.7 Ingresos pasivos: staking, préstamos, liquidez

Ver capítulo 9. Resumen:
- Staking en redes grandes: rendimiento moderado, con riesgos de custodia y técnicos.
- Prestar stablecoins en protocolos establecidos: rendimiento variable, riesgo de contrato.
- Proveer liquidez: comisiones vs. pérdida impermanente.
- Productos "Earn" de exchanges: riesgo de contraparte.

**Para efectos tributarios**, muchos de estos ingresos pueden considerarse renta al momento de recibirse **[VERIFICAR según jurisdicción; ver capítulo 26]**.

## 20.8 Airdrops y "farming de airdrops"

Algunos proyectos regalan tokens a usuarios tempranos (airdrops). Ejemplos famosos: Uniswap (2020), Arbitrum (2023), Jupiter (2024). Esto creó una práctica de usar protocolos nuevos con la esperanza de recibir airdrops futuros.

Riesgos: interactuar con muchos contratos nuevos (riesgo de seguridad), sitios falsos de "claim", tiempo y comisiones gastados sin garantía, y criterios cada vez más estrictos contra cuentas múltiples ("sybil").

## 20.9 Ideas clave del capítulo

- DCA + mantener + rebalancear es la estrategia de menor estrés para la mayoría.
- El trading activo es, estadísticamente, una forma de perder dinero para la mayoría de minoristas.
- El apalancamiento convierte la volatilidad normal en liquidaciones.

---

# Capítulo 21. Cómo analizar un proyecto: fundamentos y tokenomics

## 21.1 Objetivo

Dar al lector (y al agente) un **marco de preguntas** para evaluar cualquier criptomoneda o token. No hay fórmula de valoración aceptada como en acciones (no hay flujos de caja en la mayoría de los casos), pero sí hay señales de calidad y señales de alarma.

## 21.2 Las ocho preguntas fundamentales

### 1. ¿Qué problema resuelve y para quién?
- ¿Es un problema real? ¿Quién lo paga hoy?
- ¿Necesita blockchain para resolverse?
- ¿Necesita un token propio?

### 2. ¿Se usa hoy?
Métricas de uso real:
- Usuarios o direcciones activas (cuidado: una persona puede tener mil direcciones).
- Volumen de transacciones.
- **Ingresos del protocolo** (comisiones que pagan los usuarios). Herramientas: Token Terminal, DefiLlama (sección "Fees" y "Revenue").
- TVL (para DeFi).
- Desarrolladores activos (GitHub, informes de Electric Capital).

### 3. ¿Quién está detrás?
- ¿Equipo identificado y con trayectoria?
- ¿Inversionistas de capital de riesgo? (Pueden dar respaldo, pero también suelen tener tokens baratos que venderán.)
- ¿Fundación, empresa o comunidad anónima?

### 4. ¿Cuál es la tokenomics? (Sección 21.3.)

### 5. ¿Qué tan descentralizado es?
- ¿Cuántos validadores/nodos? ¿Quién los controla?
- ¿El equipo puede cambiar los contratos o congelar fondos?
- ¿Cómo se toman las decisiones?

### 6. ¿Cuál es su historial de seguridad?
- Auditorías (¿de quién? ¿cuántas?).
- Hackeos previos y cómo respondieron.
- Programas de recompensas por bugs (bug bounty).

### 7. ¿Quién compite con él?
- ¿Tiene ventajas sostenibles (efectos de red, liquidez, desarrolladores)?
- ¿Qué pasa si un competidor ofrece lo mismo más barato?

### 8. ¿Cuáles son los riesgos regulatorios?
- ¿Podría considerarse un valor (security)?
- ¿Depende de un país o empresa específica?

## 21.3 Tokenomics: la economía del token

### Oferta
- **Oferta máxima:** ¿existe un tope?
- **Inflación anual:** ¿cuántos tokens nuevos se emiten por año? Una inflación del 10% anual significa que tu porción del total se diluye si no participas del staking.
- **Mecanismos de quema:** ¿se destruyen tokens con el uso?

### Distribución inicial
¿Quién recibió los tokens al principio?
| Destinatario | Señal |
|---|---|
| Equipo y asesores | Normal en cierta medida; preocupante si es una porción muy grande |
| Inversionistas privados (VC) | Compraron muy barato; tendrán incentivo a vender |
| Tesorería / fundación | ¿Quién controla su uso? |
| Comunidad / airdrop | Más distribución, aunque muchos venden de inmediato |
| Venta pública | Precio que pagó el público |

### Calendario de desbloqueo (vesting)
Los tokens de equipo e inversionistas suelen estar bloqueados y se liberan en el tiempo. **Los grandes desbloqueos suelen presionar el precio a la baja.** Herramientas como Token Unlocks / Tokenomist muestran calendarios **[VERIFICAR nombres actuales]**.

### "Low float, high FDV"
Patrón que se volvió común desde 2023: se lanza un token con poca oferta circulante (por ejemplo, 10% del total) y una valoración total enorme. Al principio el precio puede subir porque hay poca oferta, pero a medida que se desbloquea el 90% restante, la presión vendedora es constante. Muchos lanzamientos de este tipo perdieron gran parte de su valor en el primer año.

### Utilidad del token (value accrual)
¿Por qué alguien necesitaría tener el token?
- **Pagar comisiones** (ETH, SOL).
- **Staking para seguridad de la red.**
- **Gobernanza** (débil por sí sola: votar rara vez genera demanda sostenida).
- **Participación en ingresos** (el protocolo usa ingresos para recomprar tokens o distribuir a stakers).
- **Colateral** en otros protocolos.
- **Acceso** a un servicio.

Si la única utilidad es "gobernanza" y "especulación", el valor depende casi completamente del sentimiento.

## 21.4 Red flags (señales de alarma)

- Equipo anónimo **y** tokens concentrados en pocas billeteras.
- Whitepaper vago, lleno de palabras de moda (IA, metaverso, quantum) sin explicación técnica.
- Rendimientos o precios futuros prometidos.
- Comunidad que ataca cualquier pregunta crítica.
- Código cerrado o no auditado.
- Liquidez no bloqueada (en tokens de DEX).
- Funciones de "mint" o "blacklist" en manos de una sola dirección.
- Marketing muy fuerte vía influencers pagados.
- Listado solo en exchanges desconocidos.
- Hoja de ruta que siempre se atrasa sin explicación.

## 21.5 Green flags (señales positivas)

- Producto funcionando con usuarios reales y que pagan comisiones.
- Código abierto y múltiples auditorías.
- Varios años de operación, incluyendo al menos un mercado bajista.
- Distribución amplia de tokens.
- Transparencia en tesorería y desbloqueos.
- Desarrollo activo constante.
- Ecosistema de terceros construyendo encima.

## 21.6 Herramientas útiles

| Herramienta | Para qué |
|---|---|
| CoinGecko / CoinMarketCap | Precios, capitalización, oferta, exchanges |
| DefiLlama | TVL, comisiones, ingresos, stablecoins, rendimientos |
| Token Terminal | Métricas financieras de protocolos |
| L2BEAT | Seguridad y actividad de capas 2 |
| Etherscan / Solscan | Contratos, titulares de tokens, transacciones |
| Messari | Investigación y perfiles de proyectos |
| GitHub | Actividad de desarrollo |
| Sitio oficial y documentación | Fuente primaria (verifica la URL) |

**[VERIFICAR: herramientas y su modelo gratuito/pago pueden cambiar.]**

## 21.7 Plantilla de evaluación rápida

```
Proyecto: ____________   Ticker: ______   Red: ______
Categoría: ____________
Problema que resuelve: ________________________________
¿Se usa hoy? (métrica + fuente): ______________________
Ingresos del protocolo (últimos 30 días): _____________
Capitalización: ______   FDV: ______   % circulante: ___
Próximos desbloqueos relevantes: ______________________
Top 10 billeteras (% de oferta): ______________________
Equipo: ______________   Inversionistas: ______________
Auditorías: ___________   Hackeos previos: ___________
¿El equipo puede pausar/actualizar/congelar? __________
Competidores: _________________________________________
Riesgo regulatorio: ___________________________________
Mi tesis: _____________________________________________
¿Qué la invalidaría?: _________________________________
Red flags detectadas: _________________________________
```

## 21.8 Ideas clave del capítulo

- Pregunta qué problema resuelve, si se usa hoy y por qué necesita token.
- La tokenomics (dilución, desbloqueos, concentración) puede hundir un buen proyecto.
- "Low float, high FDV" es un patrón de riesgo.
- Ingresos reales del protocolo son una de las mejores señales de uso.


---

# Capítulo 22. Análisis técnico básico

## 22.1 Qué es y qué no es

El **análisis técnico (AT)** estudia gráficos de precio y volumen para identificar patrones y probabilidades. Parte de la idea de que el precio refleja la psicología colectiva y que ciertos comportamientos se repiten.

**Lo que no es:** una bola de cristal. El AT habla de probabilidades, no de certezas. Su utilidad real para un principiante es más **gestión de riesgo** (dónde poner un stop-loss, cuándo no comprar en plena euforia) que predicción.

La evidencia académica sobre la rentabilidad sostenida del AT en mercados tradicionales es mixta, y en cripto, con manipulación y baja liquidez en muchos activos, las señales son aún menos fiables.

## 22.2 Gráficos de velas (candlesticks)

Cada **vela** representa un período (1 minuto, 1 hora, 1 día, 1 semana):
- **Cuerpo:** entre el precio de apertura y el de cierre.
- **Mechas (sombras):** el máximo y el mínimo del período.
- **Color:** verde (o blanco) si cerró más alto que abrió; rojo (o negro) si cerró más bajo.

```
     |      <- máximo
   ┌─┴─┐
   │   │    <- cuerpo (apertura a cierre)
   └─┬─┘
     |      <- mínimo
```

**Temporalidades:** para una visión de inversión, conviene mirar gráficos diarios, semanales y mensuales. Las temporalidades cortas (minutos) son mayormente ruido.

**Escala logarítmica:** para activos que han multiplicado su precio muchas veces (como BTC), la escala logarítmica muestra mejor los movimientos porcentuales. Un movimiento de 1.000 a 2.000 se ve igual que uno de 50.000 a 100.000.

## 22.3 Tendencias

- **Tendencia alcista:** máximos y mínimos cada vez más altos.
- **Tendencia bajista:** máximos y mínimos cada vez más bajos.
- **Lateral (rango):** el precio se mueve entre dos niveles sin dirección clara.

"La tendencia es tu amiga" es uno de los principios más repetidos: es más probable que una tendencia continúe a que se revierta en un momento cualquiera.

## 22.4 Soportes y resistencias

- **Soporte:** nivel de precio donde históricamente aparece demanda (compradores) y el precio deja de caer.
- **Resistencia:** nivel donde aparece oferta (vendedores) y el precio deja de subir.
- Cuando una resistencia se rompe con fuerza, a menudo se convierte en soporte, y viceversa.
- Los **números redondos** (por ejemplo, 100.000 USD en BTC) actúan como soportes y resistencias psicológicas.

## 22.5 Indicadores más usados

### Medias móviles (MA / EMA)
Promedio del precio en los últimos N períodos.
- **Media de 200 días (MA200):** referencia clásica de tendencia de largo plazo. Precio sobre la MA200 se interpreta como contexto alcista.
- **Media de 50 días:** tendencia de mediano plazo.
- **Cruce dorado (golden cross):** la MA50 cruza hacia arriba la MA200. **Cruce de la muerte (death cross):** lo contrario. Son señales retrasadas y con muchos falsos positivos.
- En Bitcoin, se usa también la **media de 200 semanas**, que históricamente marcó zonas cercanas a mínimos de ciclo (lo que no garantiza que siga pasando).

### RSI (Relative Strength Index)
Oscilador entre 0 y 100 que mide la velocidad de los movimientos recientes.
- Sobre 70: "sobrecomprado".
- Bajo 30: "sobrevendido".
- En tendencias fuertes, puede quedarse en sobrecompra o sobreventa por mucho tiempo.
- **Divergencias:** precio hace un nuevo máximo pero el RSI no; puede indicar pérdida de fuerza.

### MACD
Diferencia entre dos medias exponenciales, con una línea de señal. Sirve para ver cambios de impulso. Cruces del MACD sobre su línea de señal se interpretan como señales alcistas, y viceversa.

### Volumen
Cantidad negociada. Un movimiento con volumen alto es más significativo que uno con volumen bajo. Ojo: el volumen reportado por algunos exchanges ha estado inflado artificialmente.

### Bandas de Bollinger
Banda alrededor de una media que se ensancha con la volatilidad. Bandas muy estrechas suelen preceder movimientos fuertes (en cualquier dirección).

### Retrocesos de Fibonacci
Niveles (23,6%, 38,2%, 50%, 61,8%, 78,6%) donde, según la teoría, el precio tiende a reaccionar tras un movimiento. Muy populares; su base es más psicológica (muchos los miran) que matemática.

## 22.6 Patrones gráficos comunes

- **Doble techo / doble suelo:** el precio prueba dos veces un nivel y falla; posible reversión.
- **Hombro-cabeza-hombro:** patrón de reversión bajista (invertido, alcista).
- **Triángulos, banderas y cuñas:** patrones de continuación o reversión según su forma.

Los patrones son subjetivos: dos analistas ven cosas distintas en el mismo gráfico.

## 22.7 Indicadores específicos de cripto

- **Funding rate** de futuros perpetuos: tasas muy positivas indican muchas posiciones apalancadas al alza (riesgo de cascada si el precio cae).
- **Interés abierto (open interest):** volumen total de contratos de futuros abiertos. Interés abierto subiendo rápido con precio subiendo indica apalancamiento creciente.
- **Mapas de liquidación:** muestran niveles donde se concentrarían liquidaciones.
- **Índice de miedo y codicia (Fear & Greed Index):** combina varias métricas en un número de 0 a 100. Extremos de miedo han coincidido a veces con buenas zonas de compra de largo plazo; extremos de codicia, con zonas de riesgo. No es una señal mecánica.

## 22.8 Uso razonable del AT para un principiante

1. Mirar el gráfico semanal para entender el contexto (¿estamos en tendencia alcista, bajista, lateral?).
2. Evitar comprar grandes montos tras subidas verticales con RSI extremo y euforia en redes.
3. Si se hace trading, definir stop-loss en niveles técnicos lógicos.
4. No usar más de 2–3 indicadores (más indicadores no da más certeza; da más confusión).
5. Recordar que noticias inesperadas (hackeos, regulación, macroeconomía) rompen cualquier patrón.

Herramienta más usada para gráficos: **TradingView** (versión gratuita suficiente para aprender).

## 22.9 Ideas clave del capítulo

- El AT da probabilidades, no certezas.
- Úsalo más para gestionar riesgo que para predecir.
- Temporalidades largas, pocos indicadores, escala logarítmica.
- En cripto, mira también funding rate e interés abierto.

---

# Capítulo 23. Análisis on-chain

## 23.1 Qué es

Como las blockchains públicas registran todo, se pueden analizar los datos directamente: cuántas direcciones están activas, cuánto tiempo llevan los inversionistas sin vender, cuánta cripto entra y sale de exchanges, qué hacen las "ballenas" (grandes poseedores). Esto se llama **análisis on-chain**, y es una herramienta propia de cripto que no existe en acciones.

## 23.2 Métricas clave (principalmente de Bitcoin)

### Flujos de exchanges
- **Entradas netas a exchanges:** más cripto llegando a exchanges puede indicar intención de vender.
- **Salidas netas:** más cripto saliendo hacia autocustodia suele interpretarse como intención de mantener.
- **Reservas en exchanges:** total de BTC en exchanges conocidos. Una tendencia a la baja sostenida se interpreta como acumulación.

### Comportamiento por antigüedad
- **Holders de largo plazo (LTH):** monedas que no se han movido en más de ~155 días. Si estos empiezan a vender fuerte, suele coincidir con fases tardías de mercados alcistas.
- **Holders de corto plazo (STH):** compradores recientes, más reactivos.
- **HODL waves:** visualización de cuánta oferta lleva cuánto tiempo sin moverse.

### Valoración on-chain
- **Realized price (precio realizado):** precio promedio al que se movió por última vez cada moneda. Aproxima el "costo base" promedio de la red.
- **MVRV (Market Value to Realized Value):** capitalización de mercado / capitalización realizada. Valores muy altos históricamente coincidieron con techos; cercanos o bajo 1, con suelos.
- **SOPR (Spent Output Profit Ratio):** indica si las monedas que se mueven lo hacen con ganancia o pérdida.
- **NUPL (Net Unrealized Profit/Loss):** proporción de la red en ganancia o pérdida no realizada.

### Actividad de la red
- Direcciones activas, número de transacciones, comisiones pagadas.
- **Hashrate:** poder de cómputo de minería (seguridad de la red).

### Stablecoins
- **Oferta de stablecoins y su crecimiento:** más stablecoins en el ecosistema se interpreta como "pólvora seca" disponible para comprar.
- **Flujos de stablecoins a exchanges.**

### Ballenas
- Billeteras con grandes montos. Servicios como Whale Alert publican movimientos grandes.
- Cuidado: muchas "ballenas" son en realidad billeteras de exchanges o custodios que mueven fondos de clientes.

## 23.3 Herramientas

| Herramienta | Enfoque |
|---|---|
| Glassnode | Métricas on-chain de Bitcoin y Ethereum (mayormente de pago) |
| CryptoQuant | Flujos de exchanges, métricas de mineros y derivados |
| Dune Analytics | Paneles creados por la comunidad con consultas SQL sobre datos de muchas redes |
| Nansen, Arkham | Etiquetado de billeteras (qué dirección pertenece a qué entidad) |
| DefiLlama | DeFi, stablecoins, flujos entre cadenas |
| mempool.space | Estado de la red Bitcoin, comisiones |

**[VERIFICAR modelos de precio y disponibilidad.]**

## 23.4 Límites del análisis on-chain

- Las métricas funcionaron en ciclos pasados, pero el mercado cambió: los **ETFs** y custodios institucionales mantienen enormes cantidades de BTC en pocas direcciones, distorsionando métricas como "reservas en exchanges" o "comportamiento de ballenas".
- El etiquetado de billeteras es imperfecto.
- Mucha actividad ocurre fuera de la cadena (en exchanges, en Lightning, en capas 2).
- Como el AT, son probabilidades basadas en historia, no leyes.

## 23.5 Privacidad: el reverso del análisis on-chain

Las mismas herramientas que permiten analizar el mercado permiten **rastrear personas**. Empresas como Chainalysis, Elliptic y TRM Labs trabajan con gobiernos y exchanges para seguir fondos. Implicancias para el usuario:
- Si una dirección está vinculada a tu identidad (por KYC), tu historial puede reconstruirse.
- Recibir fondos que pasaron por direcciones vinculadas a delitos (incluso sin saberlo) puede hacer que un exchange congele tu cuenta y pida explicaciones.
- Los "mezcladores" (mixers) han sido sancionados en algunas jurisdicciones; usarlos puede generar problemas con exchanges y autoridades **[VERIFICAR situación legal por país]**.

## 23.6 Ideas clave del capítulo

- La blockchain permite medir el comportamiento de inversionistas de forma directa.
- Flujos de exchanges, holders de largo plazo, MVRV y stablecoins son métricas de referencia.
- Los ETFs y custodios cambiaron la lectura de muchas métricas históricas.
- Transparencia significa también rastreabilidad.

---

# Capítulo 24. Ciclos de mercado e historia de las grandes caídas

## 24.1 Los ciclos de cuatro años

Bitcoin ha mostrado, hasta ahora, un patrón aproximado de ciclos de ~4 años vinculados al halving:

1. **Halving:** la emisión de nuevos BTC se reduce a la mitad.
2. **12–18 meses después:** fuerte subida, nuevos máximos históricos, euforia, entrada masiva de minoristas, auge de altcoins.
3. **Techo y caída:** el precio cae entre 70% y 85% desde el máximo.
4. **Mercado bajista (bear market):** 1 a 2 años de precios bajos, desinterés, quiebras de empresas.
5. **Acumulación:** lateralidad, construcción, preparación del siguiente ciclo.

| Ciclo | Máximo aproximado | Caída posterior aproximada |
|---|---|---|
| 2013 | ~1.100 USD | ~85% |
| 2017 | ~20.000 USD | ~84% |
| 2021 | ~69.000 USD | ~77% |
| 2024–2025 | sobre 100.000 USD | **[VERIFICAR evolución posterior]** |

**Advertencia importante:** muchos analistas creen que los ciclos se están **suavizando** o cambiando, porque:
- El halving afecta cada vez menos la oferta (la emisión ya es pequeña frente al total).
- La entrada de ETFs, empresas e instituciones cambia la estructura del mercado.
- La macroeconomía (tasas de interés, liquidez global) tiene cada vez más peso.

El agente no debe presentar el ciclo de cuatro años como una ley. Es un patrón histórico con pocas repeticiones (apenas tres o cuatro observaciones).

## 24.2 Fases del sentimiento

Un esquema clásico de la psicología de mercado:

**Esperanza → Optimismo → Creencia → Entusiasmo → Euforia (techo) → Complacencia → Ansiedad → Negación → Pánico → Capitulación → Ira → Depresión (suelo) → Incredulidad → Esperanza…**

Señales típicas de euforia: familiares sin experiencia preguntando qué comprar, celebridades lanzando tokens, publicidad masiva de exchanges (estadios, Super Bowl), promesas de que "esta vez es diferente".

Señales típicas de suelo: medios declarando "la muerte de Bitcoin" (hay sitios que contabilizan cientos de estos obituarios), quiebras de empresas cripto, desinterés total.

## 24.3 Altseason

En las fases finales de algunos mercados alcistas, el capital rota de Bitcoin a Ethereum y luego a altcoins cada vez más especulativas. Las altcoins pueden subir mucho más que BTC... y luego caer 90% o más. En el ciclo 2024–2025, la "altseason" amplia fue más débil que en ciclos previos, con mucho capital concentrado en BTC vía ETFs **[VERIFICAR evolución]**.

## 24.4 Historia de las grandes caídas y quiebras (lecciones)

### Mt. Gox (2014)
- El mayor exchange del mundo (llegó a procesar la mayoría de las transacciones de BTC).
- Pérdida de ~850.000 BTC por hackeos y mala gestión durante años.
- Los acreedores empezaron a recibir pagos parciales recién una década después.
- **Lección:** el riesgo de custodia es real.

### The DAO (2016)
- Fondo de inversión descentralizado en Ethereum, hackeado por un bug (se drenó un tercio de sus fondos).
- Ethereum hizo un hard fork para revertir el robo. Quienes se opusieron siguieron en la cadena original: **Ethereum Classic**.
- **Lección:** el código tiene bugs; "inmutable" depende del consenso social.

### Burbuja ICO (2017–2018)
- Miles de proyectos recaudaron dinero vendiendo tokens con solo un whitepaper.
- La mayoría fracasó o eran fraudes.
- **Lección:** recaudar dinero no es tener un producto.

### Marzo de 2020 ("Jueves Negro")
- Con la pandemia, BTC cayó ~50% en un día.
- Liquidaciones masivas en DeFi.
- **Lección:** en crisis de liquidez global, cripto cae junto con todo lo demás.

### Terra/Luna (mayo de 2022)
- Stablecoin algorítmica UST pierde la paridad; LUNA cae de ~80 USD a prácticamente cero en días.
- ~40.000 millones de dólares destruidos.
- Contagio: Three Arrows Capital (fondo), Celsius y Voyager (prestamistas) quiebran.
- **Lección:** rendimientos "estables" de 20% eran insostenibles; los riesgos estaban interconectados.

### FTX (noviembre de 2022)
- Uno de los exchanges más grandes y "respetables", con patrocinios de estadios y celebridades.
- Se reveló que usaba fondos de clientes para financiar su fondo hermano (Alameda Research).
- Colapso en días. Su fundador, Sam Bankman-Fried, fue condenado por fraude a 25 años de prisión.
- **Lección:** la reputación y el marketing no son garantía. "Not your keys, not your coins".

### Colapsos bancarios (marzo de 2023)
- Quiebras de Silvergate, Silicon Valley Bank y Signature, bancos ligados al sector cripto.
- USDC pierde la paridad temporalmente.
- **Lección:** cripto y banca tradicional están conectados.

### Hackeo de Bybit (febrero de 2025)
- ~1.500 millones de dólares robados, el mayor robo de la historia cripto, atribuido a Lazarus (Corea del Norte), mediante la manipulación de la interfaz de firma de una billetera multifirma.
- El exchange cubrió a los clientes.
- **Lección:** incluso la multifirma puede ser vulnerada si se compromete lo que el firmante ve.

### Caídas por desapalancamiento
- Episodios recurrentes donde el precio cae 10–20% en horas, liquidando miles de millones en posiciones apalancadas. Se repiten en cada ciclo **[VERIFICAR eventos recientes de 2025–2026]**.

## 24.5 Qué enseñan todas estas historias

1. **Las caídas de 70–80% no son excepciones; son parte del activo.**
2. **El riesgo de contraparte** (exchanges, prestamistas) ha causado más pérdidas a usuarios comunes que la volatilidad de BTC.
3. **Los rendimientos altos esconden riesgos ocultos.**
4. **El apalancamiento convierte caídas normales en ruina.**
5. **Sobrevivir es más importante que maximizar.** Quienes no usaron apalancamiento, mantuvieron autocustodia y no se sobreexpusieron pudieron atravesar los ciclos.

## 24.6 Factores macroeconómicos

Desde 2020, cripto se comporta en gran parte como un **activo de riesgo** sensible a:
- **Tasas de interés:** tasas altas suelen afectar negativamente; tasas en baja, positivamente.
- **Liquidez global** (expansión o contracción del balance de bancos centrales).
- **Fortaleza del dólar.**
- **Correlación con acciones tecnológicas** (Nasdaq), especialmente en crisis.
- **Flujos de ETFs** y compras de empresas (tesorerías corporativas de BTC).

## 24.7 Ideas clave del capítulo

- Los ciclos de ~4 años son un patrón histórico, no una ley.
- Las mayores pérdidas de usuarios vinieron de quiebras de custodios y de apalancamiento.
- Euforia generalizada es una señal de riesgo, no de oportunidad.
- La macroeconomía pesa cada vez más.

---

# PARTE V — MARCO LEGAL Y TRIBUTARIO

**Nota para el agente:** esta parte cambia con frecuencia. Todo dato legal o tributario debe tratarse como **[VERIFICAR]**. La información está actualizada con lo disponible hasta octubre de 2026. Recomienda siempre confirmar con un contador o abogado, y con las fuentes oficiales del regulador y del servicio de impuestos.

---

# Capítulo 25. Regulación en el mundo

## 25.1 Por qué importa la regulación al usuario común

La regulación define:
- Qué exchanges pueden operar en tu país.
- Qué protección tienes si un exchange quiebra.
- Qué información se reporta a las autoridades.
- Qué productos puedes comprar (ETFs, staking, derivados).
- Cómo tributan tus operaciones.

## 25.2 Conceptos regulatorios clave

- **VASP / CASP / PSAV:** proveedor de servicios de activos virtuales (exchanges, custodios). Distintos nombres según la jurisdicción.
- **¿Valor (security) o mercancía (commodity)?** Debate central en EE.UU. Si un token se considera valor, aplica la regulación del mercado de valores (más exigente).
- **GAFI/FATF:** organismo internacional contra el lavado de dinero. Sus recomendaciones (incluida la Travel Rule) son adoptadas por la mayoría de los países.
- **CARF (Crypto-Asset Reporting Framework):** marco de la OCDE para que los países intercambien información tributaria sobre operaciones cripto de sus residentes, similar a lo que ya existe para cuentas bancarias. Muchos países se comprometieron a implementarlo con intercambios a partir de 2027 **[VERIFICAR adhesión de cada país]**.

## 25.3 Estados Unidos

- **ETFs:** la SEC aprobó ETFs de Bitcoin al contado (enero de 2024) y de Ethereum (mayo/julio de 2024). Posteriormente se lanzaron productos sobre otras criptomonedas como Solana y XRP **[VERIFICAR lista actual]**.
- **Stablecoins:** la **ley GENIUS** (julio de 2025) establece el marco federal para stablecoins de pago.
- **Estructura de mercado:** la **ley CLARITY** (Digital Asset Market Clarity Act) busca definir qué tokens son valores y cuáles mercancías, y repartir supervisión entre SEC y CFTC. Fue aprobada por la Cámara de Representantes en julio de 2025, pero a fines de agosto de 2026 **seguía sin convertirse en ley**, pendiente en el Senado **[VERIFICAR estado actual]**.
- **Cambio de enfoque regulatorio:** desde 2025, la SEC y la CFTC han adoptado una postura más favorable al sector, cerrando varios casos contra empresas cripto y trabajando en reglas específicas **[VERIFICAR]**.
- **Reserva estratégica:** en 2025 se creó por orden ejecutiva una reserva estratégica de bitcoin con activos incautados.
- **Impuestos:** el IRS trata la cripto como propiedad; ventas, permutas y gastos generan ganancias o pérdidas de capital. Los exchanges reportan con el formulario 1099-DA desde operaciones de 2025 **[VERIFICAR]**.

## 25.4 Unión Europea: MiCA

El **Reglamento MiCA (Markets in Crypto-Assets)** es el marco integral de la UE:
- Exige que los proveedores de servicios (CASP) obtengan autorización en un país miembro, válida para toda la UE ("pasaporte").
- Regula emisores de stablecoins (EMT y ART) con requisitos de reservas.
- Establece obligaciones de transparencia (whitepapers), conducta y protección al cliente.
- Las reglas para stablecoins aplicaron desde junio de 2024 y las de proveedores desde el 30 de diciembre de 2024.
- **El período de transición terminó el 1 de julio de 2026:** desde esa fecha, cualquier proveedor sin licencia CASP ya no puede atender a clientes de la UE.
- ESMA mantiene un registro público de proveedores autorizados, que es la referencia para verificar un exchange en Europa.
- Para el usuario: si vives en la UE, verifica que tu exchange esté en el registro.

## 25.5 Latinoamérica

**[Todo lo de esta sección: VERIFICAR estado actual]**

### Chile
- **Ley Fintec (Ley 21.521, 2023):** incorporó a los proveedores de servicios financieros basados en tecnología, incluyendo plataformas de intercambio y custodia de activos virtuales, bajo supervisión de la **Comisión para el Mercado Financiero (CMF)**. Exige inscripción en un registro, y requisitos de gobierno corporativo, gestión de riesgos y capital, según el servicio.
- La cripto no es moneda de curso legal.
- Fuentes de prensa especializada describen el mercado chileno en 2026 como más maduro institucionalmente, por la combinación de Ley Fintec, fiscalización del SII y supervisión de la CMF.
- **Recomendación práctica:** verificar en el sitio de la CMF que la plataforma esté registrada.

### México
- La **Ley Fintech (2018)** regula a instituciones de tecnología financiera. Las entidades financieras tradicionales tienen restricciones fuertes para ofrecer cripto a clientes. Los activos virtuales son actividad vulnerable bajo la ley antilavado.

### Argentina
- Alta adopción por inflación y controles cambiarios.
- Registro de **Proveedores de Servicios de Activos Virtuales (PSAV)** ante la CNV, con requisitos reforzados desde 2025.
- Hubo un régimen de "blanqueo" que incluyó cripto en 2024.

### Brasil
- **Ley 14.478 (2022)** sobre activos virtuales; el **Banco Central de Brasil** es el regulador de proveedores de servicios, con normas publicadas en 2025 **[VERIFICAR entrada en vigor]**.
- Mercado grande, con ETFs de cripto en la bolsa brasileña (B3).

### El Salvador
- Primer país en declarar BTC moneda de curso legal (2021). En 2025, en el marco de un acuerdo con el FMI, modificó la ley para que su aceptación sea voluntaria. El gobierno mantiene compras de BTC **[VERIFICAR]**.

### Colombia, Perú y otros
- Registros de proveedores ante supervisores financieros o unidades antilavado, con distintos grados de avance. Sandbox regulatorios en algunos casos.

## 25.6 Otras jurisdicciones relevantes

- **Reino Unido:** régimen de registro antilavado ante la FCA y avance hacia un régimen completo de activos cripto.
- **Emiratos Árabes Unidos (Dubái):** regulador específico (VARA). Hub de empresas cripto.
- **Singapur, Hong Kong:** licencias específicas, con restricciones a minoristas.
- **China:** prohibición de exchanges y minería desde 2021 (aunque persiste actividad informal). Hong Kong tiene régimen propio.

## 25.7 Qué significa la regulación para el usuario

- **Más protección:** segregación de fondos, requisitos de capital, auditorías.
- **Menos privacidad:** KYC, Travel Rule, reportes tributarios (y en el futuro, intercambio internacional vía CARF).
- **Menos productos disponibles** en algunos países (restricciones a derivados, staking o ciertos tokens).
- **Más acceso institucional** (ETFs, bancos ofreciendo custodia).

## 25.8 Ideas clave del capítulo

- Verifica siempre si tu exchange está registrado ante el regulador local.
- EE.UU. ya tiene ley de stablecoins; la ley de estructura de mercado (CLARITY) seguía pendiente a fines de agosto de 2026.
- En la UE, desde el 1 de julio de 2026 solo pueden operar proveedores con licencia MiCA.
- En Chile, la Ley Fintec pone a los exchanges bajo la CMF.
- El intercambio internacional de información tributaria cripto (CARF) viene en camino.

---

# Capítulo 26. Impuestos: principios generales y el caso de Chile

**Aviso:** este capítulo no es asesoría tributaria. Las reglas cambian y dependen de la situación personal. Confirma con un contador y con el servicio de impuestos de tu país.

## 26.1 Principios que aplican en casi todos los países

La mayoría de los sistemas tributarios trata las criptomonedas como **activos o bienes** (no como moneda). De ahí se derivan reglas comunes:

### Eventos que generalmente NO tributan
- **Comprar** cripto con moneda local.
- **Mantener** cripto (no hay impuesto por tenencia en la mayoría de los países, aunque en algunos puede contar para impuestos al patrimonio).
- **Mover** cripto entre billeteras propias.

### Eventos que generalmente SÍ pueden tributar
- **Vender** cripto por moneda local con ganancia.
- **Permutar** una cripto por otra (por ejemplo, BTC por ETH). En muchos países se considera una venta seguida de una compra. **Esto sorprende a muchos usuarios.**
- **Pagar** bienes o servicios con cripto.
- **Recibir** cripto como sueldo, honorarios o pago comercial.
- **Recibir** recompensas de staking, intereses, airdrops o minería (según la jurisdicción, al momento de recibirlas o al venderlas).

### Cálculo básico de la ganancia
**Ganancia = Precio de venta − Costo de adquisición (incluyendo comisiones)**

Cuando compraste en varias fechas y precios, hay que definir qué unidades vendiste. Métodos comunes: **FIFO** (primero en entrar, primero en salir), **costo promedio**, u otros, según lo que permita cada país.

### Pérdidas
En muchos países, las pérdidas por venta de cripto pueden compensar ganancias del mismo tipo, con reglas específicas.

## 26.2 El registro: la clave de todo

Sin registros, calcular impuestos es casi imposible. Para cada operación anota:
- Fecha y hora.
- Tipo (compra, venta, permuta, recepción, envío, staking…).
- Activo y cantidad.
- Precio en moneda local al momento.
- Comisión pagada.
- Plataforma o billetera.
- TXID (si es on-chain).

Herramientas que ayudan: Koinly, CoinTracking, CoinLedger, Accointing, entre otras **[VERIFICAR soporte para cada país]**. Importan historiales de exchanges (por archivo o conexión API de solo lectura) y direcciones de billeteras.

## 26.3 El caso de Chile (orientativo)

**[Todo este apartado: VERIFICAR con el SII y un contador. Situación con información disponible a octubre de 2026.]**

### Calificación
- El **SII** considera las criptomonedas como **bienes incorporales / activos digitales**, no como moneda ni como valores.

### Compra y tenencia
- La adquisición y la simple tenencia **no** están gravadas con impuestos.

### Venta con ganancia
- La ganancia de capital obtenida al vender sí tributa dentro del **Impuesto a la Renta**.
- Para personas naturales, la ganancia se incorpora a la base del **Impuesto Global Complementario**, cuya tasa es progresiva según el tramo de ingresos del contribuyente (desde exento hasta la tasa marginal máxima) **[VERIFICAR tramos vigentes]**.
- Se distingue, en la práctica tributaria, entre operaciones **habituales** y **no habituales (esporádicas)**, lo que puede cambiar el tratamiento. Algunos sitios mencionan que el SII no ha fijado un criterio numérico cerrado para definir habitualidad; esto es un punto a revisar con un contador.
- La ganancia se declara en el **Formulario 22** en la Operación Renta de cada abril, por las operaciones del año comercial anterior.

### IVA
- La venta de criptomonedas como tal, en general, no se ha considerado afecta a IVA para personas naturales **[VERIFICAR; puede cambiar para empresas o servicios asociados]**.

### Staking, intereses y otros ingresos
- Fuentes secundarias indican que las recompensas de staking y similares se consideran renta. No hay un criterio oficial detallado ampliamente difundido para todos los casos; **confirmar con un contador**.

### Reporte de exchanges al SII
- Fuentes de 2026 indican que exchanges con sede en Chile (por ejemplo, Buda, CryptoMKT y Orionx) **informan operaciones de sus usuarios al SII**, en línea con nuevas obligaciones de información de la ley de cumplimiento tributario (Ley 21.713, de 2024) **[VERIFICAR alcance exacto de la obligación]**.
- Las operaciones en exchanges extranjeros o en billeteras propias igualmente deben declararse si generan renta; que no se informen automáticamente no las exime.
- Con la futura implementación del estándar CARF de la OCDE, se espera mayor intercambio de información entre países **[VERIFICAR compromiso de Chile y fechas]**.

### Tipo de cambio
- Para operaciones en dólares o stablecoins, se debe convertir a pesos usando el tipo de cambio correspondiente (consultar el criterio del SII, por ejemplo, dólar observado del día o promedios mensuales) **[VERIFICAR]**.

### Empresas
- Las empresas que tienen o reciben cripto tienen reglas contables y tributarias propias (reconocimiento de activos, tributación de la renta, posibles efectos en IVA según la actividad). Requiere asesoría profesional.

### Recomendaciones prácticas para un contribuyente en Chile
1. Descarga cada año el historial completo de cada exchange.
2. Calcula ganancias y pérdidas por cada venta o permuta en pesos chilenos.
3. Consulta a un contador antes de la Operación Renta si operaste mucho, si usaste DeFi o staking, o si recibiste pagos en cripto.
4. Guarda la documentación por los plazos de prescripción que establece la ley.

## 26.4 Otros países (muy resumido) [VERIFICAR TODO]

| País | Idea general |
|---|---|
| EE.UU. | Propiedad; ganancias de capital de corto o largo plazo según tenencia (más o menos de 1 año); reporte 1099-DA |
| España | Ganancias patrimoniales en la base del ahorro; declaración informativa de cripto en el extranjero (modelo 721) |
| México | Ganancias por enajenación de activos virtuales; reglas aún con zonas grises |
| Argentina | Impuesto a las ganancias sobre resultados; tratamiento específico según origen |
| Colombia | Activos intangibles; ganancia ocasional o renta según el caso |
| Brasil | Ganancias de capital con exención para ventas mensuales bajo cierto monto; declaración mensual a la Receita Federal sobre operaciones en el extranjero o en exchanges sin reporte |

## 26.5 Errores tributarios frecuentes

- Creer que las permutas cripto-cripto no tributan.
- Creer que si el dinero no se retira al banco, no hay que declarar.
- No guardar el costo de adquisición (y tener que pagar sobre el total de la venta).
- Olvidar exchanges cerrados o quebrados (pedir el historial a tiempo).
- No declarar ingresos de staking o airdrops donde corresponde.
- Asumir que los fondos en billeteras propias son invisibles: la blockchain es pública y el rastreo es posible.

## 26.6 Ideas clave del capítulo

- Comprar y mantener normalmente no tributa; vender, permutar y recibir ingresos sí.
- Registra cada operación con fecha, precio y comisión.
- En Chile, la ganancia tributa en el impuesto a la renta y se declara en el F22; los exchanges locales informan al SII.
- Ante dudas: contador.


---

# PARTE VI — HACIA DÓNDE VA ESTO

---

# Capítulo 27. Tendencias: ETFs, tokenización, CBDCs, IA y cripto

**Nota para el agente:** este capítulo describe tendencias a octubre de 2026. Es el más propenso a quedar desactualizado. Trata cada afirmación sobre el estado actual como **[VERIFICAR]** y distingue siempre entre lo que ya existe y lo que se promete.

## 27.1 La institucionalización

El cambio más grande del sector entre 2024 y 2026 no fue tecnológico, fue de **quién participa**.

### ETFs de cripto
- Los ETFs de Bitcoin al contado en EE.UU. (aprobados en enero de 2024) se convirtieron en uno de los lanzamientos de ETF más exitosos de la historia por flujo de entrada.
- Gestoras como BlackRock, Fidelity y otras acumularon cientos de miles de BTC en nombre de sus clientes **[VERIFICAR cifras]**.
- Siguieron ETFs de Ethereum (2024) y luego productos sobre otras criptomonedas.
- Efecto práctico: personas que nunca abrirían una cuenta en un exchange ahora pueden tener exposición a BTC desde su cuenta de inversión tradicional o su fondo de pensiones.

### Tesorerías corporativas
- Siguiendo el modelo de MicroStrategy (renombrada Strategy), decenas de empresas cotizadas empezaron a comprar BTC (y en algunos casos ETH, SOL u otras) como activo de tesorería, muchas veces financiándose con deuda o emisión de acciones.
- **Riesgo a entender:** estas empresas amplifican el ciclo. En subidas, compran más; en caídas prolongadas, algunas podrían verse obligadas a vender o enfrentar problemas financieros **[VERIFICAR situación actual]**.

### Bancos y custodia
- Bancos grandes empezaron a ofrecer custodia de cripto, trading para clientes privados y servicios con stablecoins, en la medida que la regulación lo permite.

### Qué significa para el usuario común
- Más liquidez y más estabilidad relativa en BTC (no ausencia de volatilidad).
- Mayor correlación con mercados tradicionales.
- Más formas reguladas de acceso.
- La narrativa "contra el sistema" convive ahora con el sistema financiero comprando el mismo activo.

## 27.2 Stablecoins como infraestructura de pagos

- Con la ley GENIUS en EE.UU. y MiCA en Europa, las stablecoins pasaron de ser una herramienta de traders a ser **infraestructura de pagos**.
- Empresas de pagos tradicionales (Visa, Mastercard, Stripe, PayPal) integraron liquidación con stablecoins en distintos grados **[VERIFICAR]**.
- Bancos y fintechs exploran emitir sus propias stablecoins.
- Para Latinoamérica, las stablecoins compiten directamente con las remesas tradicionales y con el acceso a dólares.

**Pregunta abierta:** ¿cuánto de este crecimiento se queda con Tether y Circle, y cuánto se fragmenta entre stablecoins bancarias? Afecta qué stablecoin será más líquida en cada país.

## 27.3 Tokenización de activos reales

Ver capítulo 10. La tendencia:
- Fondos de bonos del Tesoro tokenizados crecieron con fuerza y se usan como colateral dentro de cripto.
- Exchanges y bolsas tradicionales exploran acciones tokenizadas y operación 24/7.
- Gestoras grandes hablan abiertamente de tokenizar "todos los activos" a largo plazo.

**Lectura prudente:** la tokenización es probable que crezca, pero beneficiará en gran parte a instituciones existentes. No implica que cualquier token de "RWA" sea una buena inversión.

## 27.4 Monedas digitales de bancos centrales (CBDC)

Una **CBDC** es dinero digital emitido directamente por un banco central. **No es una criptomoneda** en el sentido de Bitcoin: es centralizada, emitida por el Estado y sin límite de oferta.

Estado general **[VERIFICAR]**:
- **China:** e-CNY en piloto amplio.
- **Unión Europea:** el euro digital en fase de preparación.
- **Brasil:** proyecto Drex, que fue redefiniendo su alcance.
- **Chile:** el Banco Central de Chile ha estudiado un peso digital y publicado informes; no hay una CBDC minorista lanzada **[VERIFICAR]**.
- **Estados Unidos:** la administración actual se ha opuesto a una CBDC minorista.

Debate central: eficiencia y modernización de pagos versus privacidad y control estatal sobre el dinero.

## 27.5 IA y cripto

Una convergencia que genera tanto interés como ruido.

### Lo que tiene sentido
- **Agentes de IA con billeteras:** programas autónomos que necesitan pagar por servicios (datos, cómputo, APIs) pueden usar stablecoins en redes rápidas. Existen protocolos de pago entre máquinas (por ejemplo, propuestas basadas en el código HTTP 402 "Payment Required") **[VERIFICAR estado]**.
- **Mercados de cómputo descentralizado:** alquilar GPUs de muchos proveedores.
- **Verificación de contenido:** usar firmas criptográficas para probar el origen de imágenes, videos o documentos ante el auge de deepfakes.
- **Prueba de humanidad:** sistemas para demostrar que una cuenta es de una persona real.

### Lo que hay que mirar con escepticismo
- Tokens que agregan "AI" al nombre sin producto.
- "Bots de trading con IA" que garantizan rendimientos (capítulo 18: estafa).
- Agentes que "gestionan tu portafolio" de forma autónoma con tus claves: riesgo enorme si el agente es manipulado o se equivoca.

### Implicancia para un agente como el que usa este documento
Un agente de IA que asesora sobre cripto **no debe** tener acceso a claves privadas, ni ejecutar transacciones sin confirmación explícita, ni recomendar inversiones específicas. Su rol es explicar, verificar y advertir.

## 27.6 Mejoras técnicas en curso

- **Ethereum:** hoja de ruta centrada en escalar capas 2 y la capa base, mejorar la experiencia de usuario (abstracción de cuentas) y simplificar la ejecución de nodos.
- **Bitcoin:** debates sobre nuevas funciones (covenants, mejoras para capas 2), uso del espacio de bloques (inscripciones/Ordinals) y preparación para la computación cuántica.
- **Solana:** mejoras de rendimiento y nuevos clientes de validador para reducir el riesgo de caídas.
- **Interoperabilidad:** protocolos que buscan que el usuario no tenga que saber en qué red está.
- **Privacidad:** tecnologías de conocimiento cero (ZK) que permiten demostrar algo (por ejemplo, ser mayor de edad o tener fondos suficientes) sin revelar todos los datos.

## 27.7 Riesgos sistémicos a vigilar

- **Concentración:** pocos custodios (ETFs, exchanges) controlan una parte creciente de la oferta.
- **Riesgo regulatorio:** cambios políticos pueden revertir el entorno favorable.
- **Apalancamiento oculto** en tesorerías corporativas y productos estructurados.
- **Stablecoins como punto único de falla** del ecosistema.
- **Hackeos de Estados-nación** (Corea del Norte se atribuye la mayor parte del valor robado en varios años recientes).
- **Computación cuántica** a largo plazo.

## 27.8 Ideas clave del capítulo

- La gran tendencia es la institucionalización: ETFs, tesorerías, bancos.
- Las stablecoins se están volviendo infraestructura de pagos.
- La tokenización de activos reales crece, sobre todo en manos de instituciones.
- CBDC no es cripto: es dinero estatal digital.
- IA + cripto tiene usos razonables y mucho marketing vacío.


---

# PARTE VII — REFERENCIA

---

# Capítulo 28. Glosario

Términos ordenados alfabéticamente. Cada definición está pensada para entenderse sin leer el resto del manual. Entre paréntesis, el capítulo donde se profundiza.

### A

**2FA (autenticación de dos factores):** segundo paso de verificación además de la contraseña (código de una app, llave física o SMS). (Cap. 17)

**51%, ataque del:** cuando un actor controla la mayoría del poder de minado o del stake de una red y puede reescribir transacciones recientes. (Cap. 6)

**Abstracción de cuentas:** billeteras que funcionan como contratos inteligentes, permitiendo recuperación social, límites de gasto y pago de comisiones en otros tokens. Estándares ERC-4337 y EIP-7702. (Cap. 11)

**Address poisoning (envenenamiento de direcciones):** estafa que deja en tu historial una dirección parecida a una que usas, para que la copies por error. (Cap. 16)

**Airdrop:** distribución gratuita de tokens a ciertas direcciones. Puede ser legítimo o un vector de estafa. (Cap. 20)

**Altcoin:** cualquier criptomoneda distinta de Bitcoin. (Cap. 1)

**AML (Anti-Money Laundering):** normas contra el lavado de dinero. (Cap. 14)

**AMM (Automated Market Maker):** mecanismo de los exchanges descentralizados que usa pools de liquidez y una fórmula en vez de un libro de órdenes. (Cap. 9)

**Análisis on-chain:** estudio de los datos de la blockchain para entender el comportamiento del mercado. (Cap. 23)

**Análisis técnico (AT):** estudio de gráficos de precio y volumen. (Cap. 22)

**APR / APY:** tasa anual sin capitalizar (APR) y con capitalización (APY). El APY siempre se ve más alto.

**Aprobación (approve):** permiso que das a un contrato inteligente para mover tus tokens. Riesgoso si es ilimitado o a un contrato malicioso. (Cap. 5)

**ASIC:** máquina especializada en minar con un algoritmo específico (por ejemplo, SHA-256 para Bitcoin). (Cap. 4)

**Auditoría (de contratos):** revisión del código de un contrato inteligente por expertos externos. Reduce, no elimina, el riesgo. (Cap. 21)

### B

**Ballena (whale):** dirección o entidad con una cantidad muy grande de un activo. (Cap. 23)

**Bear market (mercado bajista):** período prolongado de caída de precios. (Cap. 24)

**BIP (Bitcoin Improvement Proposal):** propuesta formal de mejora de Bitcoin. BIP-39 define las frases semilla. (Cap. 3)

**Billetera (wallet):** software o dispositivo que guarda tus claves y te permite firmar transacciones. No guarda monedas. (Cap. 12)

**Billetera caliente (hot wallet):** billetera conectada a internet. (Cap. 12)

**Billetera de hardware:** dispositivo físico que guarda claves privadas offline. (Cap. 12)

**Billetera fría (cold wallet):** billetera cuyas claves nunca tocan internet. (Cap. 12)

**Bitcoin dominance:** porcentaje del mercado cripto total que representa BTC. (Cap. 7)

**Bloque:** paquete de transacciones agregado a la blockchain. (Cap. 2)

**Bloque génesis:** primer bloque de una blockchain. En Bitcoin, minado el 3 de enero de 2009. (Cap. 1)

**Blockchain:** registro compartido de transacciones encadenadas por hashes y mantenido por muchos nodos. (Cap. 2)

**Bull market (mercado alcista):** período prolongado de subida de precios. (Cap. 24)

**Burn (quema):** destrucción permanente de tokens enviándolos a una dirección inaccesible o mediante reglas del protocolo. (Cap. 5)

### C

**CARF:** marco de la OCDE para intercambio internacional de información tributaria sobre criptoactivos. (Cap. 25)

**CASP:** proveedor de servicios de criptoactivos bajo MiCA (UE). (Cap. 25)

**CBDC:** moneda digital emitida por un banco central. No es una criptomoneda descentralizada. (Cap. 27)

**CEX:** exchange centralizado. (Cap. 14)

**Capitalización de mercado (market cap):** precio × oferta circulante. (Cap. 7)

**Clave privada:** número secreto que controla los fondos de una dirección. Quien la tiene, tiene el dinero. (Cap. 3)

**Clave pública:** derivada de la clave privada; se puede compartir. (Cap. 3)

**CMF:** Comisión para el Mercado Financiero de Chile; supervisa a los proveedores bajo la Ley Fintec. (Cap. 25)

**Colateral:** activo depositado como garantía de un préstamo. (Cap. 9)

**Confirmación:** cada bloque agregado después del bloque que contiene tu transacción. (Cap. 2)

**Consenso:** reglas por las cuales la red se pone de acuerdo sobre el estado de la blockchain. (Cap. 6)

**Contrato inteligente (smart contract):** programa que se ejecuta en la blockchain. (Cap. 5)

**Custodial:** servicio donde un tercero guarda tus claves. (Cap. 12)

### D

**DAO:** organización autónoma descentralizada, gobernada por votos de poseedores de tokens. (Cap. 9)

**DCA (Dollar-Cost Averaging):** invertir montos fijos a intervalos regulares. (Cap. 20)

**DeFi:** finanzas descentralizadas; servicios financieros mediante contratos inteligentes. (Cap. 9)

**Depeg:** pérdida de la paridad de una stablecoin o token vinculado. (Cap. 8)

**DEX:** exchange descentralizado. (Cap. 9)

**Dirección:** identificador público para recibir fondos, derivado de la clave pública. (Cap. 3)

**Doble gasto:** problema de gastar el mismo dinero digital dos veces; Bitcoin lo resolvió sin intermediario. (Cap. 1)

**Drainer:** software malicioso o sitio que vacía billeteras mediante firmas engañosas. (Cap. 18)

### E

**ERC-20 / ERC-721 / ERC-1155:** estándares de tokens en Ethereum (fungibles, NFT, mixtos). (Cap. 5)

**ETF:** fondo cotizado en bolsa. Los ETFs de Bitcoin al contado permiten exposición a BTC desde una cuenta de corredora. (Cap. 14, 27)

**EVM:** máquina virtual de Ethereum; muchas redes son compatibles. (Cap. 5)

**Exchange:** plataforma para comprar, vender e intercambiar cripto. (Cap. 14)

**Explorador de bloques:** sitio web para ver transacciones y direcciones de una blockchain. (Cap. 16)

### F

**FDV (Fully Diluted Valuation):** precio × oferta máxima. (Cap. 7, 21)

**Fiat:** dinero emitido por un Estado (peso, dólar, euro). (Cap. 1)

**Finalidad:** momento en que una transacción ya no puede revertirse. (Cap. 6)

**FOMO / FUD:** miedo a quedarse fuera / miedo, incertidumbre y duda. (Cap. 19)

**Fork (bifurcación):** cambio en las reglas de una blockchain. Soft fork (compatible) o hard fork (incompatible). (Cap. 4)

**Frase semilla (seed phrase):** 12 o 24 palabras que generan todas las claves de una billetera. (Cap. 13)

**Funding rate:** pago periódico entre posiciones largas y cortas en futuros perpetuos. (Cap. 20)

**Fungible:** intercambiable uno por uno (un BTC es igual a otro). (Cap. 1)

### G

**Gas:** unidad que mide el trabajo computacional en Ethereum; se paga en ETH. (Cap. 5)

**Gwei:** unidad pequeña de ETH (0,000000001 ETH), usada para el precio del gas. (Cap. 5)

### H

**Halving:** reducción a la mitad de la recompensa por bloque en Bitcoin, cada 210.000 bloques. (Cap. 4)

**Hash:** huella digital de largo fijo de un dato. (Cap. 3)

**Hashrate:** poder de cómputo total dedicado a minar una red PoW. (Cap. 23)

**HODL:** mantener a largo plazo. (Cap. 20)

**Honeypot:** token que se puede comprar pero no vender. (Cap. 18)

### I

**ICO:** oferta inicial de monedas; venta de tokens antes del lanzamiento. (Cap. 24)

**Impermanent loss (pérdida impermanente):** pérdida relativa de un proveedor de liquidez por cambios de precio. (Cap. 9)

**Interés abierto (open interest):** total de contratos de futuros abiertos. (Cap. 22)

### K

**KYC (Know Your Customer):** verificación de identidad en exchanges. (Cap. 14)

### L

**Layer 1 (capa 1):** blockchain base (Bitcoin, Ethereum, Solana). (Cap. 7)

**Layer 2 (capa 2):** red que procesa transacciones fuera de la capa 1 y se ancla a ella. (Cap. 11)

**Ley Fintec:** Ley 21.521 de Chile, que regula a proveedores de servicios financieros tecnológicos, incluidos los de activos virtuales. (Cap. 25)

**Lightning Network:** red de canales de pago sobre Bitcoin para pagos rápidos y baratos. (Cap. 4)

**Liquidación:** cierre forzado de una posición apalancada o préstamo cuando el colateral no alcanza. (Cap. 9, 20)

**Liquidez:** facilidad para comprar o vender sin mover mucho el precio.

**Liquid staking:** staking que entrega un token negociable que representa la posición (stETH, rETH, JitoSOL). (Cap. 9)

### M

**Market cap:** ver capitalización de mercado.

**Memecoin:** token basado en humor o cultura de internet, sin utilidad declarada. (Cap. 7)

**Mempool:** sala de espera de transacciones no confirmadas. (Cap. 2)

**MEV:** valor que validadores o bots extraen reordenando transacciones (por ejemplo, ataques sándwich). (Cap. 9)

**MiCA:** reglamento de criptoactivos de la Unión Europea. (Cap. 25)

**Minería:** proceso de crear bloques en redes Proof of Work. (Cap. 4)

**Multifirma (multisig):** billetera que requiere varias firmas para mover fondos. (Cap. 12)

**MVRV:** relación entre capitalización de mercado y capitalización realizada. (Cap. 23)

### N

**NFT:** token no fungible; cada unidad es única. (Cap. 10)

**Nodo:** computadora que ejecuta el software de una blockchain y verifica las reglas. (Cap. 2)

**Nonce:** número usado una vez; en Bitcoin, valor que los mineros varían; en Ethereum, contador de transacciones de una dirección. (Cap. 4, 16)

**No custodial:** tú controlas tus claves. (Cap. 12)

### O

**Oráculo:** servicio que lleva datos externos (como precios) a contratos inteligentes. (Cap. 7)

**Orden límite / de mercado:** orden a un precio fijado / al mejor precio disponible. (Cap. 14)

### P

**P2P:** intercambio directo entre personas, normalmente con escrow de una plataforma. (Cap. 14)

**Passphrase:** palabra adicional opcional a la frase semilla que genera una billetera distinta. (Cap. 13)

**Permit / Permit2:** firmas que autorizan el gasto de tokens sin transacción separada; vector de robo frecuente. (Cap. 17)

**Phishing:** suplantación para robar credenciales o firmas. (Cap. 17)

**Pig butchering:** estafa de larga duración con vínculo emocional e inversión falsa. (Cap. 18)

**Pool de liquidez:** reserva de tokens en un contrato que permite intercambios en un DEX. (Cap. 9)

**Ponzi:** esquema que paga a los primeros con dinero de los nuevos. (Cap. 18)

**Proof of Reserves:** prueba de que un exchange tiene los activos de sus clientes. (Cap. 14)

**Proof of Stake (PoS):** consenso basado en monedas bloqueadas como garantía. (Cap. 6)

**Proof of Work (PoW):** consenso basado en gasto computacional. (Cap. 6)

**Puente (bridge):** mecanismo para mover activos entre blockchains. (Cap. 11)

### R

**Rebalanceo:** volver a una proporción objetivo entre activos. (Cap. 20)

**Restaking:** reutilizar activos en staking para asegurar servicios adicionales. (Cap. 9)

**Rollup:** capa 2 que agrupa transacciones y publica datos en la capa 1 (optimistic o ZK). (Cap. 11)

**RSI:** indicador técnico de impulso entre 0 y 100. (Cap. 22)

**Rug pull:** el equipo de un proyecto retira la liquidez o fondos y desaparece. (Cap. 18)

**RWA (Real World Assets):** activos del mundo real tokenizados. (Cap. 10)

### S

**Satoshi (sat):** unidad mínima de Bitcoin (0,00000001 BTC). (Cap. 4)

**Seudónimo:** identidad no vinculada directamente a un nombre real, pero rastreable. Bitcoin es seudónimo, no anónimo. (Cap. 2)

**SII:** Servicio de Impuestos Internos de Chile. (Cap. 26)

**SIM swapping:** robo de tu número telefónico para interceptar SMS. (Cap. 17)

**Slashing:** penalización que destruye parte del stake de un validador que actúa mal. (Cap. 6)

**Slippage:** diferencia entre el precio esperado y el ejecutado. (Cap. 9)

**Spot:** mercado al contado, sin apalancamiento. (Cap. 14)

**Spread:** diferencia entre el mejor precio de compra y de venta. (Cap. 14)

**Stablecoin:** token diseñado para mantener un valor estable (normalmente 1 USD). (Cap. 8)

**Staking:** bloquear monedas para asegurar una red PoS a cambio de recompensas. (Cap. 9)

**Stop-loss:** orden para vender automáticamente si el precio cae a un nivel. (Cap. 14, 20)

### T

**Testnet:** red de prueba sin valor real.

**Token:** activo creado sobre una blockchain existente. (Cap. 1)

**Tokenomics:** economía de un token: oferta, distribución, emisión, utilidad. (Cap. 21)

**Travel Rule:** norma que exige compartir datos de remitente y receptor entre proveedores. (Cap. 14)

**TVL (Total Value Locked):** valor total depositado en protocolos DeFi. (Cap. 9)

**TXID:** identificador único de una transacción. (Cap. 16)

### U

**UTXO:** salida de transacción no gastada; forma en que Bitcoin registra fondos. (Cap. 4)

### V

**Validador:** participante que propone y verifica bloques en una red PoS. (Cap. 6)

**VASP / PSAV:** proveedor de servicios de activos virtuales. (Cap. 25)

**Vesting:** calendario de liberación de tokens bloqueados. (Cap. 21)

### W

**Whitepaper:** documento técnico que describe un proyecto. (Cap. 1)

**Wrapped token:** versión "envuelta" de un activo en otra red (por ejemplo, WBTC). (Cap. 11)

### Y

**Yield farming:** mover capital entre protocolos para capturar rendimientos. (Cap. 9)

### Z

**ZK (Zero-Knowledge, conocimiento cero):** técnica criptográfica para probar algo sin revelar los datos subyacentes. (Cap. 11, 27)

---

# Capítulo 29. Preguntas frecuentes

Respuestas cortas y directas, pensadas para que un agente pueda usarlas como base. Cada respuesta indica el capítulo donde profundizar.

## Básicas

**¿Qué es Bitcoin en una frase?**
Dinero digital con oferta máxima de 21 millones, que se transfiere entre personas sin banco, registrado en una blockchain mantenida por miles de computadoras. (Cap. 4)

**¿Quién controla Bitcoin?**
Nadie en particular. Las reglas las aplican miles de nodos independientes. Cambiarlas requiere un consenso amplio entre usuarios, mineros, desarrolladores y empresas. (Cap. 2, 4)

**¿Bitcoin es anónimo?**
No. Es seudónimo: las transacciones son públicas y pueden vincularse a personas, especialmente si compraste en un exchange con verificación de identidad. (Cap. 2, 23)

**¿Puedo comprar menos de un bitcoin?**
Sí. Se puede comprar cualquier fracción, hasta 0,00000001 BTC (un satoshi). (Cap. 4)

**¿Cuál es la diferencia entre Bitcoin y Ethereum?**
Bitcoin se enfoca en ser dinero con política monetaria fija. Ethereum es una plataforma para ejecutar programas (contratos inteligentes), y su moneda ETH paga el uso de esa plataforma. (Cap. 4, 5)

**¿Qué es una stablecoin?**
Un token que busca valer siempre lo mismo, casi siempre 1 dólar, normalmente respaldado por reservas en dólares de un emisor. (Cap. 8)

**¿Qué es la blockchain?**
Un registro de transacciones compartido por muchas computadoras, donde cada bloque está encadenado al anterior para que sea prácticamente imposible modificar el pasado. (Cap. 2)

## Comprar y guardar

**¿Dónde compro cripto por primera vez?**
En un exchange regulado en tu país, que permita depositar moneda local por transferencia bancaria. En Chile, verifica que esté registrado en la CMF. (Cap. 14, 15)

**¿Es seguro dejar mi cripto en un exchange?**
Es cómodo, pero implica confiar en la empresa. Exchanges grandes han quebrado o sido hackeados. Para montos pequeños puede ser aceptable; para montos importantes, considera autocustodia. (Cap. 3, 12, 14)

**¿Qué billetera me recomiendas?**
Depende del monto y uso. Para aprender: una billetera móvil reconocida. Para ahorro importante: billetera de hardware comprada en la tienda oficial del fabricante. Para empresas o montos muy grandes: multifirma. (Cap. 12)

**¿Qué es la frase semilla y dónde la guardo?**
Son 12 o 24 palabras que controlan todos tus fondos. Se anotan a mano en papel o metal, se guardan en un lugar seguro y nunca se digitalizan ni se comparten. (Cap. 13)

**Perdí mi teléfono, ¿perdí mis cripto?**
Si tienes tu frase semilla, no: instala la billetera en otro dispositivo y restaura. Si no la tienes y la billetera era no custodial, lamentablemente probablemente sí. (Cap. 13)

**Alguien de soporte me pidió mi frase semilla, ¿se la doy?**
No. Ningún soporte legítimo la pide jamás. Es una estafa. Si ya la diste, crea una billetera nueva y mueve tus fondos de inmediato. (Cap. 13, 18)

**¿Qué pasa si muero? ¿Mi familia puede recuperar mi cripto?**
Solo si dejaste instrucciones y acceso al respaldo, o si los fondos están en un exchange y tus herederos hacen el trámite legal. Planifícalo. (Cap. 13)

## Envíos

**Envié cripto por la red equivocada, ¿la recupero?**
Depende. Si enviaste a un exchange, contacta a su soporte con el TXID; a veces pueden recuperarla. Si enviaste a una dirección inexistente o de un tercero, probablemente no. (Cap. 16)

**¿Por qué no puedo enviar mis USDT?**
Probablemente te falta la moneda nativa de la red para pagar la comisión (TRX en Tron, ETH en Ethereum, SOL en Solana). (Cap. 16)

**Olvidé poner el memo/tag, ¿qué hago?**
Contacta al soporte del exchange de destino con el TXID y la información de tu cuenta. Suelen poder acreditar los fondos, aunque puede tardar. (Cap. 16)

**¿Cuánto demora una transferencia?**
Bitcoin: unos 10 minutos por confirmación, y los exchanges piden varias. Redes como Solana o capas 2 de Ethereum: segundos. Lightning: instantáneo. (Cap. 16)

**¿Por qué la comisión es tan alta?**
En Bitcoin y Ethereum, la comisión depende de la congestión de la red y del tamaño de la transacción, no del monto. Además, los exchanges suman su propia comisión de retiro. (Cap. 4, 5, 16)

## Inversión

**¿Debería comprar Bitcoin ahora?**
No puedo decirte qué comprar ni cuándo. Puedo ayudarte a pensar: cuánto podrías perder sin afectar tu vida, cuál es tu horizonte de tiempo, y si entiendes los riesgos. Muchas personas usan compras periódicas (DCA) para no depender del momento. (Cap. 15, 19, 20)

**¿Cuánto debería invertir en cripto?**
Solo lo que puedas perder por completo sin que cambie tu vida, después de tener fondo de emergencia y deudas caras controladas. El porcentaje exacto depende de tu situación; un asesor financiero puede ayudarte. (Cap. 19)

**Una moneda cuesta 0,0001 dólares, ¿puede llegar a 1 dólar?**
Mira la capitalización, no el precio unitario. Si tiene billones de unidades, llegar a 1 dólar implicaría un valor total imposible. (Cap. 7)

**¿Qué es mejor, Bitcoin o altcoins?**
Son riesgos distintos. Bitcoin tiene más historia y liquidez. Las altcoins pueden subir más y caer más; la mayoría ha perdido casi todo su valor a largo plazo. (Cap. 7, 24)

**¿El staking es dinero gratis?**
No. Es una recompensa por asegurar una red, con riesgos: de custodia, de contrato, de liquidez y de que el precio del token caiga más que lo que ganas. (Cap. 9)

**¿Me conviene operar con apalancamiento?**
Para un principiante, no. Con 10x, una caída de 10% te liquida, y en cripto eso pasa en horas. La mayoría de los minoristas que operan apalancados pierde dinero. (Cap. 19, 20)

**¿Qué es el halving y sube el precio?**
Es la reducción a la mitad de la emisión de Bitcoin cada ~4 años. Históricamente coincidió con ciclos alcistas, pero con pocas observaciones y en un mercado que cambió mucho. No es garantía. (Cap. 4, 24)

**Perdí mucho dinero, ¿cómo lo recupero rápido?**
Intentar recuperar rápido suele llevar a perder más (más riesgo, más apalancamiento). Lo primero es parar, revisar tu situación financiera y hablar con alguien de confianza. Si la pérdida afecta tus gastos básicos o tu salud, busca apoyo. (Cap. 19)

## Estafas

**Me ofrecen 3% diario garantizado, ¿es real?**
No. Es una estafa (probablemente un esquema Ponzi). (Cap. 18)

**Conocí a alguien en línea que me enseña a invertir en cripto y gano mucho en su plataforma, pero me piden pagar impuestos para retirar. ¿Qué hago?**
Es casi seguro una estafa de tipo "pig butchering". No envíes más dinero, corta el contacto, documenta todo y denuncia. (Cap. 18)

**Apareció un token en mi billetera que no compré, ¿lo vendo?**
No interactúes con él ni visites su sitio. Suele ser un señuelo para que firmes algo que vacía tu billetera. (Cap. 10, 18)

**Una empresa me ofrece recuperar mis fondos estafados, ¿es confiable?**
Casi siempre es una segunda estafa. Denuncia a la policía y al exchange; no pagues adelantado a "recuperadores". (Cap. 18)

**¿Cómo sé si un exchange es legítimo?**
Verifica registro ante el regulador de tu país, historial, prueba de reservas, opiniones independientes y que puedas retirar sin condiciones extrañas. (Cap. 14, 18)

## Impuestos y legal

**¿Tengo que pagar impuestos por tener cripto?**
En la mayoría de los países, incluido Chile, la simple tenencia no tributa. Sí tributa la ganancia al vender o permutar. (Cap. 26)

**¿Cambiar BTC por ETH paga impuestos?**
En muchos países sí, porque se considera una venta. Confirma la regla en tu país con un contador. (Cap. 26)

**¿Cómo declaro cripto en Chile?**
Las ganancias se declaran en el Formulario 22 en la Operación Renta de abril, como parte del impuesto a la renta. Los exchanges locales informan al SII. Si operaste mucho, usaste DeFi o recibiste staking, consulta a un contador. (Cap. 26)

**¿Es legal la cripto en Chile?**
Sí. No es moneda de curso legal, pero su compra, venta y tenencia son legales; los exchanges están bajo la Ley Fintec y la supervisión de la CMF. (Cap. 25)

**Si uso una billetera propia, ¿el SII se entera?**
La obligación de declarar existe igual. Además, la blockchain es pública y los vínculos con tu identidad (por ejemplo, vía exchanges) permiten rastrear. (Cap. 23, 26)

## Técnicas

**¿Qué es una capa 2?**
Una red que procesa transacciones fuera de la cadena principal (por ejemplo, Ethereum) y publica resúmenes en ella, logrando comisiones mucho más bajas. (Cap. 11)

**¿Por qué mi dirección de MetaMask es la misma en varias redes?**
Porque muchas redes son compatibles con Ethereum (EVM) y usan el mismo formato de dirección. Pero los saldos son distintos en cada red. (Cap. 5, 16)

**¿Pueden hackear Bitcoin?**
La red en sí nunca ha sido hackeada en su funcionamiento esencial. Lo que se hackea son exchanges, billeteras mal protegidas y usuarios engañados. (Cap. 3, 17)

**¿Las computadoras cuánticas van a romper Bitcoin?**
Es un riesgo de largo plazo que la comunidad estudia. Hoy no existen máquinas capaces de hacerlo, y hay propuestas de migración a firmas resistentes. (Cap. 3)

---

# Capítulo 30. Checklists y plantillas

## 30.1 Checklist antes de invertir por primera vez

- [ ] Tengo fondo de emergencia.
- [ ] No tengo deudas caras sin controlar.
- [ ] Definí el monto máximo que puedo perder sin afectar mi vida.
- [ ] Entiendo qué es una clave privada y una frase semilla.
- [ ] Sé que el precio puede caer 50–80%.
- [ ] Elegí un exchange registrado ante el regulador local.
- [ ] Escribí por qué compro y qué haré si cae.

## 30.2 Checklist de seguridad de cuenta en exchange

- [ ] Entré escribiendo la URL o desde la app oficial.
- [ ] Contraseña única y larga, en un gestor de contraseñas.
- [ ] 2FA con app o llave física (no SMS).
- [ ] Códigos de recuperación del 2FA respaldados en papel.
- [ ] Código anti-phishing activado.
- [ ] Lista blanca de direcciones de retiro activada.
- [ ] Correo asociado con 2FA propio.
- [ ] Revisé sesiones y dispositivos activos.

## 30.3 Checklist de configuración de billetera no custodial

- [ ] Descargué la billetera desde la fuente oficial.
- [ ] (Hardware) Lo compré en la tienda oficial y no venía con frase escrita.
- [ ] Anoté la frase semilla a mano, en orden y sin errores.
- [ ] No tomé foto ni la guardé digitalmente.
- [ ] Guardé el respaldo en un lugar protegido de robo, fuego y agua.
- [ ] Hice una prueba de recuperación con montos pequeños.
- [ ] Si uso passphrase, la respaldé en un lugar distinto.
- [ ] Documenté instrucciones de herencia (sin la frase).

## 30.4 Checklist antes de enviar cripto

- [ ] Activo correcto.
- [ ] Red correcta, aceptada por el destino.
- [ ] Dirección verificada (no copiada del historial).
- [ ] Memo/tag incluido si se requiere.
- [ ] Monto supera el mínimo de depósito del destino.
- [ ] Tengo moneda nativa para el gas.
- [ ] Envío de prueba si es la primera vez.

## 30.5 Checklist antes de conectar la billetera a un sitio nuevo

- [ ] Llegué al sitio por URL verificada o marcador, no por anuncio o mensaje.
- [ ] Uso una billetera desechable con poco saldo.
- [ ] Entiendo cada firma o aprobación que me pide.
- [ ] La billetera o extensión de seguridad no muestra alertas.
- [ ] Después, revoco aprobaciones que no necesito.

## 30.6 Checklist de detección de estafa

Si alguna respuesta es "sí", detente:
- [ ] ¿Me prometen rendimiento garantizado?
- [ ] ¿Me contactaron sin que yo lo pidiera?
- [ ] ¿Me piden frase semilla, clave privada o acceso remoto?
- [ ] ¿Me piden pagar para poder retirar?
- [ ] ¿Hay urgencia o secreto?
- [ ] ¿La plataforma solo la conozco por un enlace que me dieron?
- [ ] ¿Hay una relación personal o romántica reciente involucrada?

## 30.7 Plantilla de plan de inversión personal

```
Fecha: __________
Objetivo (por qué invierto en cripto): __________________________
Horizonte de tiempo: ____________
Monto máximo total en cripto: ____________ (equivale a ___% de mi patrimonio)
Activos y proporción objetivo:
  - ________: ___%
  - ________: ___%
Método de compra: [ ] Única  [ ] DCA cada ______ por ______
Dónde guardaré: [ ] Exchange ______  [ ] Billetera ______
Rebalanceo: cada ______ o si la proporción se desvía más de ___%
Toma de ganancias: ______________________________________________
Si cae 50%, haré: _______________________________________________
Si cae 80%, haré: _______________________________________________
Qué me haría salir completamente: _______________________________
Revisión de este plan: cada ______
```

## 30.8 Plantilla de registro de operaciones (para impuestos)

| Fecha y hora | Tipo | Activo | Cantidad | Precio unitario (moneda local) | Total | Comisión | Plataforma / billetera | TXID | Notas |
|---|---|---|---|---|---|---|---|---|---|
| | Compra / Venta / Permuta / Envío / Recepción / Staking | | | | | | | | |

## 30.9 Plantilla de documento de herencia (sin datos secretos)

```
Documento de instrucciones de activos digitales
Fecha de última actualización: __________

1. Resumen
   Tengo criptoactivos en: [exchanges] [billeteras propias]

2. Exchanges
   - Nombre: ______ / Correo asociado: ______ / Notas: ______

3. Billeteras propias
   - Tipo (hardware, móvil, multifirma): ______
   - Dónde está el dispositivo: ______
   - Dónde está el respaldo de la frase semilla: ______ (NO escribir la frase aquí)
   - ¿Usa passphrase? Sí/No. Dónde está su respaldo: ______

4. Personas de confianza
   - Nombre y contacto de quien puede ayudar técnicamente: ______
   - Abogado / notario: ______

5. Pasos sugeridos
   - Contactar a ______ antes de mover nada.
   - No compartir la frase semilla con nadie que la pida por mensaje.
```

## 30.10 Rutina de mantenimiento

| Frecuencia | Tarea |
|---|---|
| Cada operación | Registrar fecha, precio, comisión |
| Mensual | Revisar saldos y comparar con el plan |
| Trimestral | Revisar respaldos, revocar aprobaciones, revisar sesiones, actualizar firmware |
| Anual | Exportar historiales, preparar declaración de impuestos, actualizar plan de herencia |

---

# Capítulo 31. Recursos para seguir aprendiendo

**[VERIFICAR: los recursos pueden cambiar o desaparecer. Antes de recomendar un sitio, el agente debe confirmar que sigue activo y que la URL es la oficial.]**

## 31.1 Documentos fundacionales
- **Whitepaper de Bitcoin** (Satoshi Nakamoto, 2008): bitcoin.org/bitcoin.pdf. Nueve páginas; vale la pena leerlo.
- **Whitepaper de Ethereum** (Vitalik Buterin, 2013) y documentación oficial en ethereum.org (disponible en español).

## 31.2 Libros recomendados (generales)
- *Mastering Bitcoin* — Andreas M. Antonopoulos y David Harding (técnico, gratuito en línea en inglés).
- *Mastering Ethereum* — Andreas M. Antonopoulos y Gavin Wood (técnico).
- *The Bitcoin Standard* — Saifedean Ammous (visión económica pro-Bitcoin; leer con espíritu crítico).
- *Number Go Up* — Zeke Faux (periodismo crítico sobre estafas y excesos del sector).
- *Going Infinite* — Michael Lewis (sobre Sam Bankman-Fried y FTX).
- *The Psychology of Money* — Morgan Housel (no es de cripto, pero sí de decisiones financieras).

## 31.3 Datos y herramientas
| Uso | Recurso |
|---|---|
| Precios y datos de mercado | CoinGecko, CoinMarketCap |
| DeFi y stablecoins | DefiLlama |
| Seguridad de capas 2 | L2BEAT |
| Comisiones y estado de Bitcoin | mempool.space |
| Exploradores | Etherscan, Solscan, Tronscan, mempool.space |
| Gráficos | TradingView |
| Revocar aprobaciones | Revoke.cash |
| Análisis on-chain | Glassnode, CryptoQuant, Dune |
| Seguimiento de hackeos | rekt.news, informes de Chainalysis y similares |

## 31.4 Fuentes oficiales y reguladores
- **Chile:** CMF (cmfchile.cl) — registro Fintec y alertas; SII (sii.cl) — orientación tributaria.
- **Unión Europea:** ESMA — registro de proveedores MiCA.
- **EE.UU.:** SEC, CFTC; FBI IC3 (ic3.gov) para denunciar fraudes.
- **Internacional:** GAFI/FATF (estándares antilavado); OCDE (CARF).

## 31.5 Comunidades y medios
- Medios especializados en español e inglés (verificar fuentes y separar noticias de opinión patrocinada).
- Comunidades locales (por ejemplo, asociaciones de Bitcoin en cada país) que organizan encuentros y educación.
- **Precaución:** grupos de Telegram, Discord y redes sociales están llenos de estafadores y promotores pagados. Nadie legítimo te escribirá primero para "ayudarte".

## 31.6 Cómo seguir aprendiendo de forma segura
1. Practica con montos mínimos o en redes de prueba (testnets).
2. Prefiere fuentes primarias (documentación oficial, código, informes de reguladores) sobre influencers.
3. Busca siempre la opinión contraria antes de decidir.
4. Desconfía de cualquier curso que prometa ganancias.
5. Revisa este manual periódicamente: lo conceptual se mantiene, lo marcado [VERIFICAR] cambia.

---



---

# Anexo A. Casos prácticos resueltos

Situaciones reales típicas, con el razonamiento paso a paso. Sirven al lector para practicar y al agente como ejemplos de cómo responder.

## Caso 1. Primer ahorro en Bitcoin con sueldo en pesos

**Situación:** Daniela, 32 años, trabaja en Santiago, tiene fondo de emergencia de 4 meses y ninguna deuda de consumo. Quiere empezar a comprar Bitcoin "para el largo plazo" y no sabe cuánto ni cómo.

**Razonamiento:**
1. Cumple las condiciones previas: fondo de emergencia y sin deudas caras.
2. Definir monto: el criterio no es "cuánto podría ganar", sino "cuánto podría perder sin que le cambie la vida". Ella decide un monto mensual que, si se perdiera completo durante años, no afectaría sus metas.
3. Método: compra periódica (DCA) el mismo día de cada mes, en un exchange registrado en la CMF, usando orden límite o la función de compra recurrente si tiene comisión razonable.
4. Custodia: los primeros meses en el exchange con 2FA por app y lista blanca de retiro. Cuando el acumulado supere un umbral que ella define (por ejemplo, el equivalente a un sueldo), compra una billetera de hardware en la tienda oficial y retira, primero con envío de prueba.
5. Registro: descarga el historial cada año para el Formulario 22 (comprar y mantener no tributa; vender sí).

**Lo que el agente no debe hacer:** decirle "invierte X%" ni "es buen momento". Sí puede explicar el método, los riesgos y las preguntas.

## Caso 2. Retiro de USDT por la red equivocada

**Situación:** Matías retiró 300 USDT desde un exchange internacional eligiendo la red BNB Smart Chain (BEP-20), pero la dirección que pegó era de depósito de USDT en la red Tron de su exchange local. El retiro aparece "completado", pero no llega.

**Razonamiento:**
1. Una dirección de Tron empieza con `T`; una de BNB Chain con `0x`. Si el exchange de origen aceptó el retiro, probablemente la dirección **no** era de Tron, o eligió otra dirección. Primero, revisar el TXID en el explorador (bscscan.com) y ver a qué dirección llegó.
2. Si los fondos llegaron a una dirección `0x` del exchange de destino que no soporta BNB Chain para USDT, hay que abrir un ticket en el exchange de destino con TXID, monto, red y captura. Algunos exchanges recuperan fondos enviados por red no soportada, a veces con cargo.
3. Si la dirección no pertenece a nadie conocido, los fondos probablemente se perdieron.
4. Prevención: verificar que la red de retiro coincida con la red de depósito indicada por el destino; envío de prueba.

## Caso 3. "Soporte de MetaMask" por Telegram

**Situación:** Carla preguntó en un grupo de Telegram por qué no veía sus tokens. Minutos después, "MetaMask Support" le escribió por privado y le envió un enlace para "sincronizar la billetera" ingresando su frase de 12 palabras. Ya la ingresó.

**Respuesta correcta:**
1. Es una estafa. MetaMask no tiene soporte por Telegram ni pide la frase.
2. Urgente: crear una billetera nueva (frase nueva, idealmente en otro dispositivo) y mover **todo** lo que quede, empezando por lo de mayor valor. Los atacantes usan bots que vacían billeteras en segundos; puede que ya no quede nada.
3. Si se robaron fondos: documentar direcciones y TXIDs, reportar a la plataforma donde se hizo el grupo, denunciar.
4. Sobre los tokens que no veía: lo más común es que estaban en otra red o había que "importar" el token por su dirección de contrato. Explicarlo una vez asegurado lo urgente.

## Caso 4. Inversión "romántica"

**Situación:** Un hombre de 58 años cuenta que conoció a una mujer por una app de idiomas hace dos meses. Ella le enseñó a invertir en una plataforma de cripto donde su saldo pasó de 5.000 a 38.000 dólares. Al querer retirar, le piden pagar un "impuesto de liberación" de 6.000 dólares. Pregunta si es normal pagar impuestos antes de retirar.

**Respuesta correcta:**
1. Decirlo con claridad y respeto: esto coincide con una estafa conocida como "pig butchering". Ninguna plataforma legítima cobra impuestos por adelantado para liberar retiros.
2. El saldo de 38.000 es casi seguro ficticio: es un número en una pantalla.
3. No pagar nada más. Cortar contacto. Documentar todo (chats, nombre de la plataforma, direcciones donde envió dinero, TXIDs).
4. Denunciar a la policía y al exchange desde el que envió los fondos.
5. Advertir que pronto pueden aparecer "recuperadores de fondos": también son estafa.
6. Reconocer el impacto emocional: la relación probablemente también era falsa, y eso duele. Sugerir hablar con alguien de confianza.

## Caso 5. Compra de una memecoin recomendada por un influencer

**Situación:** Una usuaria quiere comprar un token nuevo en Solana que un influencer anunció "antes de que haga 100x". Pide ayuda para comprarlo en un DEX.

**Razonamiento del agente:**
1. Puede explicar cómo funciona una compra en un DEX (billetera Phantom, SOL para comisiones, agregador, slippage).
2. Debe advertir con claridad: tokens recién lanzados y promovidos por influencers tienen altísima probabilidad de ser pump and dump o rug pull. Muchos influencers cobran por promocionar o compraron antes.
3. Recomendaciones de seguridad: verificar la dirección del contrato en fuentes oficiales (hay copias falsas con el mismo nombre), revisar concentración de titulares y liquidez, usar una billetera desechable, invertir solo lo que esté dispuesta a perder al 100%.
4. No le dice "no lo hagas" de forma paternalista, pero sí deja claro el riesgo real.

## Caso 6. Venta con ganancia y declaración en Chile

**Situación:** Durante el año, Jorge compró 0,1 BTC en tres fechas por un total de 5.000.000 de pesos (incluyendo comisiones) y vendió 0,05 BTC por 3.200.000 pesos. Pregunta cuánto debe declarar.

**Razonamiento (ilustrativo, no asesoría):**
1. Necesita determinar el costo de los 0,05 BTC vendidos. Con costo promedio: 5.000.000 / 0,1 = 50.000.000 CLP por BTC; costo de 0,05 = 2.500.000.
2. Ganancia aproximada: 3.200.000 − 2.500.000 − comisión de venta = algo menos de 700.000 pesos.
3. Esa ganancia se incorpora a su base imponible del impuesto a la renta y se declara en el F22 de abril siguiente. La tasa efectiva depende de sus otros ingresos (Impuesto Global Complementario).
4. El método de costeo (promedio, FIFO) y si su actividad se considera habitual deben confirmarse con un contador o con orientación del SII **[VERIFICAR]**.
5. Los 0,05 BTC que conserva no tributan mientras no los venda.

## Caso 7. ¿ETF o Bitcoin directo?

**Situación:** Un profesional con cuenta en una corredora con acceso a EE.UU. pregunta si es mejor comprar un ETF de Bitcoin o BTC en un exchange.

**Comparación:**

| | ETF de Bitcoin | BTC directo |
|---|---|---|
| Custodia | Gestora y custodio regulados | Exchange o autocustodia |
| Manejo de claves | No | Sí (si hay autocustodia) |
| Costos | Comisión anual de administración + corretaje | Comisiones de compra/retiro |
| Horario | Horario bursátil | 24/7 |
| Uso de la cripto | No (no puedes enviarla) | Sí |
| Tributación | Según reglas de valores extranjeros **[VERIFICAR]** | Según reglas de criptoactivos |
| Herencia | Como cualquier inversión de corredora | Requiere planificación específica |

**Conclusión explicable:** el ETF es más simple y familiar para quien ya invierte en bolsa y no quiere manejar claves; el BTC directo da control total y uso real, pero exige responsabilidad en seguridad. El agente presenta ambos lados y no elige por el usuario.

## Caso 8. Préstamo en DeFi contra ETH

**Situación:** Un usuario depositó ETH en Aave y pidió prestado USDC hasta el máximo permitido para comprar más ETH. El precio de ETH cae 15%.

**Explicación:**
1. Al pedir prestado al máximo, su factor de salud estaba cerca de 1. Con una caída de 15%, probablemente bajó de 1 y fue liquidado parcialmente: alguien pagó parte de su deuda y se quedó con parte de su ETH con descuento.
2. Además, como usó el préstamo para comprar más ETH, estaba apalancado: la caída le afectó doble.
3. Lección: si se pide prestado en DeFi, mantener un factor de salud holgado (muchos usuarios prudentes no bajan de 2), vigilarlo y tener un plan para agregar colateral o pagar deuda.

---

# Anexo B. Guía de respuestas para el agente

Escenarios frecuentes y la estructura recomendada de respuesta. El objetivo es que el agente sea útil, directo y seguro.

## B.1 Principios de estilo
- **Respuesta directa primero**, luego el contexto.
- **Lenguaje simple**, explicando cada término técnico la primera vez.
- **Advertencias concretas**, no genéricas: en vez de "invierte con cuidado", decir "si usas apalancamiento 10x, una caída de 10% te liquida".
- **Sin asesoría personalizada de inversión**: explicar, comparar, hacer preguntas.
- **Señalar lo que puede estar desactualizado** ([VERIFICAR]).

## B.2 Plantillas de respuesta

### "¿Qué cripto compro?"
1. Aclarar que no puede recomendar activos específicos.
2. Ofrecer el marco: monto que puede perder, horizonte, conocimiento del activo.
3. Explicar diferencias de riesgo entre categorías (BTC, ETH, stablecoins, altcoins, memecoins).
4. Ofrecer ayuda para evaluar un proyecto concreto con la plantilla del capítulo 21.

### "Me pidieron mi frase semilla / ya la di"
1. Alerta clara: es estafa.
2. Acción inmediata: billetera nueva, mover fondos.
3. Pasos de denuncia y documentación.
4. Advertencia sobre recuperadores de fondos.

### "Envié a la dirección/red equivocada"
1. Pedir (o indicar que reúna) TXID, red usada, dirección de destino, plataforma de destino.
2. Revisar en el explorador.
3. Si el destino es un exchange: ticket a soporte con los datos.
4. Expectativa realista.
5. Prevención para la próxima vez.

### "¿Es esto una estafa?"
1. Comparar con las señales del capítulo 18.
2. Si hay señales claras, decirlo sin rodeos.
3. Sugerir verificación en el regulador.
4. Si la persona ya envió dinero: pasos de la sección 18.5.

### "¿Cómo pago impuestos por mis cripto?"
1. Principios generales (qué tributa y qué no).
2. Caso del país del usuario, marcado como [VERIFICAR].
3. Recomendación de registro y de contador.

### "Perdí mucho dinero"
1. Reconocer la situación sin juzgar.
2. Evaluar si hay riesgo inmediato (deudas, gastos básicos, angustia).
3. Desaconsejar intentar "recuperar rápido".
4. Sugerir pausa, revisión del plan financiero, apoyo de personas cercanas o profesional si hay señales de malestar serio.

### "Explícame X" (concepto)
1. Definición en una frase.
2. Analogía cotidiana.
3. Cómo funciona en la práctica.
4. Riesgos o errores comunes asociados.
5. Referencia al capítulo para profundizar.

## B.3 Lo que el agente nunca debe hacer
- Pedir, almacenar o repetir frases semilla, claves privadas, contraseñas o códigos 2FA.
- Asegurar que un precio subirá o bajará.
- Recomendar montos o momentos de compra/venta para un usuario específico.
- Recomendar apalancamiento a principiantes.
- Recomendar plataformas no verificadas o "recuperadores de fondos".
- Dar por vigente una regla legal o tributaria sin advertir que debe confirmarse.
- Ayudar a evadir controles antilavado, sanciones o impuestos.

## B.4 Señales que obligan a cambiar el enfoque de la respuesta
| Señal en el mensaje del usuario | Cambio de enfoque |
|---|---|
| Menciona préstamos o tarjeta para invertir | Advertir riesgo financiero antes de responder lo técnico |
| Describe contacto desconocido + plataforma + "impuesto para retirar" | Tratar como estafa probable |
| Expresa desesperación, insomnio, ocultamiento a familia | Priorizar bienestar; sugerir pausa y apoyo |
| Comparte frase semilla o clave en el chat | Indicar que está comprometida y que debe mover fondos |
| Pide garantías de ganancia | Explicar que no existen |
| Parece ser menor de edad | Mantener contenido educativo general, recordar que los exchanges exigen mayoría de edad |

---

# Anexo C. Cronología resumida del ecosistema

| Año | Hito |
|---|---|
| 2008 | Whitepaper de Bitcoin |
| 2009 | Bloque génesis de Bitcoin |
| 2010 | Primera compra con BTC (pizzas) |
| 2011 | Litecoin; Satoshi deja de comunicarse |
| 2013 | Primera gran burbuja; propuesta de Ethereum; nace Dogecoin |
| 2014 | Quiebra de Mt. Gox; lanzamiento de Tether |
| 2015 | Lanzamiento de Ethereum |
| 2016 | Hackeo de The DAO; nace Ethereum Classic |
| 2017 | Burbuja ICO; SegWit; Bitcoin Cash; BTC cerca de 20.000 USD |
| 2018 | Mercado bajista prolongado |
| 2020 | "Jueves Negro" (marzo); "verano DeFi"; empresas compran BTC |
| 2021 | Auge de NFTs; El Salvador adopta BTC; Taproot; máximo ~69.000 USD; China prohíbe minería |
| 2022 | Colapso Terra/Luna; quiebras de Celsius, 3AC, Voyager; The Merge de Ethereum; quiebra de FTX |
| 2023 | Crisis bancaria (SVB); USDC pierde paridad temporalmente; Ley Fintec en Chile; aprobación de MiCA |
| 2024 | ETFs de BTC y ETH al contado en EE.UU.; halving; Dencun; BTC supera 100.000 USD; MiCA aplica a proveedores |
| 2025 | Hackeo de Bybit; ley GENIUS de stablecoins en EE.UU.; reserva estratégica de BTC en EE.UU.; la Cámara aprueba la ley CLARITY |
| 2026 | Fin del período de transición de MiCA (1 de julio); la ley CLARITY sigue pendiente en el Senado de EE.UU. a fines de agosto **[VERIFICAR]** |

---

## Cierre

Las criptomonedas combinan una idea tecnológica brillante (dinero y contratos sin intermediario) con un mercado lleno de especulación, fraude y riesgo. Ambas cosas son ciertas a la vez.

Si hay que resumir este manual en cinco reglas:

1. **Quien tiene la clave privada tiene el dinero.** Protege tu frase semilla como si fuera todo tu patrimonio, porque lo es.
2. **Nadie legítimo te pide tu frase semilla ni te garantiza ganancias.**
3. **Invierte solo lo que puedas perder por completo.** Sin deuda, sin apalancamiento.
4. **Verifica siempre: red, dirección, sitio, regulador.** Un error no tiene vuelta atrás.
5. **Registra todo y declara.** Los impuestos y la regulación ya alcanzaron a cripto.

*Fin del manual — versión 1.0, octubre de 2026.*
