# Alternativas de Text-to-Speech

## Problema con Edge TTS

Microsoft Edge TTS estaba rechazando las solicitudes con error 403 debido a:
- Rate limiting (demasiadas solicitudes muy rapido)
- Bloqueos temporales por uso excesivo
- Problemas de autenticacion

## Solucion Implementada: gTTS (Google Text-to-Speech)

### Ventajas de gTTS:

1. **Completamente Gratis**: No requiere API keys ni registro
2. **Sin Rate Limiting Severo**: No tiene los mismos problemas que Edge TTS
3. **Buena Calidad**: Voces naturales en espanol
4. **Facil de Usar**: Integracion simple
5. **Sin Límites Estrictos**: Puede procesar textos largos dividiendolos automaticamente

### Limitaciones:

- Limite de ~5000 caracteres por solicitud (se maneja automaticamente dividiendo el texto)
- Requiere conexion a internet
- Velocidad ligeramente mas lenta que Edge TTS

## Como Usar

### Opcion 1: gTTS (Recomendado - Por Defecto)

```powershell
py audiobook_pipeline.py
```

O especificamente:

```powershell
py audiobook_pipeline.py --tts gtts
```

### Opcion 2: Edge TTS (Si quieres intentar de nuevo)

```powershell
py audiobook_pipeline.py --tts edge
```

## Instalacion

Las nuevas dependencias se instalan automaticamente con:

```powershell
py -m pip install -r requirements.txt
```

O usando el script:

```powershell
# Doble clic en install_dependencies.bat
```

## Comparacion

| Caracteristica | gTTS | Edge TTS |
|----------------|------|----------|
| Gratis | ✅ Si | ✅ Si |
| Rate Limiting | ⚠️ Minimo | ❌ Severo |
| Calidad | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Velocidad | ⚠️ Media | ⭐ Rapida |
| Requiere Internet | ✅ Si | ✅ Si |
| API Key | ❌ No | ❌ No |

## Otras Alternativas Consideradas

### pyttsx3 (Respaldo Local)
- **Ventaja**: Completamente local, sin internet
- **Desventaja**: Calidad variable segun el sistema operativo
- **Estado**: Disponible como opcion futura si se necesita

### Coqui TTS
- **Ventaja**: Open source, buena calidad
- **Desventaja**: Requiere mas configuracion y recursos
- **Estado**: Considerado para versiones futuras

### ElevenLabs
- **Ventaja**: Excelente calidad
- **Desventaja**: Plan gratuito muy limitado
- **Estado**: No implementado (requiere API key)

## Recomendacion

**Usa gTTS por defecto** - Es la mejor opcion balanceada entre:
- Facilidad de uso
- Calidad de voz
- Confiabilidad
- Sin problemas de rate limiting

Si gTTS falla, puedes intentar Edge TTS nuevamente, pero gTTS deberia funcionar sin problemas.



