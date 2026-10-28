# Motor multifuente · contrato experimental v0.1

## Objetivo
Una búsqueda manual bajo demanda que consulta varias fuentes de empleo y entrega una lista consolidada, sin intervenir Career Radar.

## Arquitectura
- GitHub Pages es estático: la página no puede ocultar tokens ni saltarse restricciones CORS.
- APIs públicas de ATS por empresa: Ashby, Greenhouse, Lever. Requieren catálogo de boards reales y pruebas de disponibilidad.
- Fuentes públicas adicionales: analizar una por una sus APIs documentadas, CORS, límites y términos; no hacer scraping que eluda bloqueos.
- Agregadores/portales: LinkedIn, Indeed, HiringCafe, Weremoto, e-Talent, Computrabajo, Pandapé, HiringRoom, GlobalWork.ai. Estado inicial: NO INTEGRADO; mantener enlaces manuales hasta confirmar mecanismo legal y técnicamente viable.
- Google Jobs y Google site: solo complemento, no motor ATS.

## Contrato de salida por vacante
`id`, `source`, `company`, `title`, `location`, `remote_scope`, `original_url`, `published_at` (null si desconocida), `collected_at`, `status`, `eligibility_evidence`.
No confundir fecha de recopilación con publicación. No asumir que remoto admite Ecuador.

## Contrato de ejecución
1. Usuario pulsa Buscar una vez.
2. Ejecutar conectores compatibles de manera concurrente con timeout y errores independientes.
3. Normalizar y deduplicar por URL oficial o identificador.
4. Mostrar resultados con fuente y enlace original; mostrar por separado fallos y fuentes no integradas.
5. Nunca declarar cobertura total ni mostrar resultados ficticios.

## Pruebas y promoción
- Comprobar respuestas HTTP reales de cada proveedor, CORS desde navegador o backend seguro, y al menos un caso positivo y uno de error.
- Verificar filtros por familia y ubicación; indicar explícitamente los datos insuficientes.
- No publicar cambios a main hasta pruebas y revisión.
- No alterar ningún archivo de Career Office privado.
