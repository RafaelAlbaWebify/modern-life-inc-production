# MLI_EP003 — Producción de formato largo

Título provisional: **Why Being Helpful Is Making You Overwhelmed**.

Guion de 1.680 palabras. 48 imágenes seleccionadas para un montaje de integración, generadas directamente en el chat; una corrección localizada. Estimación de duración alrededor de 9:25 al ritmo de EP002, pendiente de medir con la nueva voz. No se ha renderizado un vídeo final ni aprobado la publicación.

## Continuar

1. Abre VoiceStudio y ejecuta `GENERAR_VOZ_EP003.ps1`. Conserva su carpeta predeterminada en Descargas: `MLI_EP003_AUDIO_V1`. El narrador es el mismo de EP002. Si ya ejecutaste el script facilitado en el chat, no necesitas repetirlo: reutiliza esa carpeta.
2. Ejecuta `TERMINAR_EP003.ps1` desde esta carpeta extraída. Importará los WAV que correspondan exactamente a este guion, reconstruirá `accepted_images` a partir de las selecciones verificadas y ejecutará montaje, alineación real nueva, Soft Karaoke y QC. Usa el entorno WhisperX existente en `Downloads\MLI_WHISPERX_ENV`. Si está en otro lugar, pasa su Python mediante `-AlignmentPython`.
3. El MP4 final y los informes aparecerán en `renders\MLI_EP003_RENDER_...`. Revisa el vídeo completo y comparte el MP4 y los informes de tiempos.

Los scripts PowerShell de este paquete se han revisado en código; todavía no se han ejecutado en Windows. Los módulos canónicos Python/FFmpeg proceden de la receta de EP002. La importación y revisión de estas 48 imágenes sí se ejecutaron aquí. Una ejecución local es necesaria para medir voz y acabado en tu equipo.

La carpeta incluye una copia de cada imagen importada (también SC31 anterior para auditoría), referencias, guion, prompts, hashes, decisiones de revisión y tiempos. Las copias `accepted_images` se reconstruyen para evitar duplicar imágenes en el ZIP. No uses alineación de EP002: las palabras y los tiempos son nuevos.

La publicación requiere visionado y escucha completos. Un PASS técnico no equivale a aprobación editorial.
