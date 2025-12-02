# Generador Automático de Reportes ESAR – Versión 1

Este script fue desarrollado para resolver un problema operativo real dentro de un proyecto de telecomunicaciones:  
**la necesidad de generar más de 2,000 reportes ESAR en una sola semana con un equipo de apenas 3 personas.**

Antes de la automatización, cada integrante debía producir alrededor de **100 reportes ESAR diarios**, lo que generaba:

- Fatiga operativa  
- Errores humanos al copiar y pegar datos  
- Retrasos en entregables  
- Riesgo de incumplimiento con el cliente  

Este proyecto eliminó prácticamente todo el trabajo manual, permitiendo producir reportes de manera masiva, rápida y sin errores.

---

## 🚀 Objetivo del proyecto

Automatizar la generación de documentos ESAR basados en una plantilla estándar de Excel, completando cada reporte con los datos correspondientes (PO Number, PO Line, Site Name, Item Description, QTY, etc.).

El resultado:  
**un proceso que antes tomaba horas-hombre ahora se completa en minutos.**

---

## 🧩 ¿Qué hace el script?

1. Carga una **tabla de datos en Excel** con cientos o miles de registros.  
2. Abre una **plantilla de ESAR** previamente formateada.  
3. Por cada fila del dataset:
   - Inserta los valores en las celdas correctas  
   - Genera un archivo ESAR independiente  
   - Lo guarda con un nombre estándar (`ESAR__<PO_NUMBER>.xlsx`)  
4. Repite el proceso hasta completar todos los registros.  
5. Imprime en consola la confirmación de cada archivo generado.

---

## 📊 Impacto logrado

Gracias a la automatización:

- El equipo dejó de hacer trabajo manual repetitivo.  
- Se redujeron prácticamente a **0 los errores por copia y pegado**.  
- La producción pasó de **100 ESAR por persona/día** a **miles en minutos**.  
- Se logró cumplir con una entrega crítica al cliente sin retrabajos.  
- Se liberó tiempo para tareas estratégicas y análisis del proyecto.  

Este script se convirtió en una herramienta clave para el área de reporting y apoyo técnico.

---

## 🛠️ Tecnologías utilizadas

- **Python**  
- **Pandas** para lectura de datos  
- **OpenPyXL** para manipulación de la plantilla ESAR  
- **OS Path** para rutas dinámicas y nombrado de archivos  
- **Excel como fuente y destino final**

---

## 🗂️ Estructura del flujo

1. `pd.read_excel()` carga los datos.  
2. `openpyxl.load_workbook()` abre la plantilla.  
3. Las celdas clave se actualizan:
   - L11 → PO Number  
   - C26 → PO Line  
   - D26 → Site Name  
   - F26 → Item Description  
   - J26 → QTY  
   - G33 → PO Number 2  
4. Se guarda el archivo en la carpeta correspondiente.

---

## 📦 Salida generada

Se produce un ESAR por cada registro del dataset en la ruta configurada:

