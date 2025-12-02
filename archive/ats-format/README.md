# Generador Automático de CV en Word – Versión 1

Este proyecto genera un **Curriculum Vitae profesional en formato Word (.docx)** usando Python y la librería `python-docx`.  
El script construye toda la estructura del CV de manera programática: encabezados, secciones, párrafos, negritas, tamaños de fuente, formato compacto y contenido dinámico.

---

## 🚀 Objetivo del proyecto

Evitar la edición manual del CV y permitir una generación rápida, estandarizada y actualizable del documento.  
Con este enfoque, cualquier cambio en el CV puede automatizarse —solo se edita el código y se vuelve a ejecutar el script.

Permite:

- Crear CVs consistentes y profesionales.
- Mantener versiones actualizadas sin abrir Word.
- Generar múltiples plantillas o versiones del CV con cambios mínimos.

---

## 🛠️ Tecnologías utilizadas

- **Python**
- **python-docx** para creación y formateo del documento Word
- **docx.shared.Pt** para manejo de tamaños de fuente
- **Estructuración programática del contenido** (funciones, loops)

---

## 📄 ¿Qué hace este script?

1. **Crea un documento Word desde cero.**
2. **Define una función** para agregar párrafos compactos (fuente de 10 pt).
3. **Agrega automáticamente:**
   - Nombre y datos de contacto  
   - Resumen profesional  
   - Experiencia laboral  
   - Educación y certificaciones  
   - Habilidades técnicas  
   - Valor agregado profesional  

4. **Utiliza encabezados jerárquicos (H1, H2) para un CV limpio y estructurado.**
5. **Guarda el archivo final** en la ruta establecida por el usuario.

---

## 🧩 Estructura técnica principal

- `Document()` crea el archivo Word.
- `add_paragraph()` añade texto con formato compacto y opcionalmente en negrita.
- Encabezados generados con:
  ```python
  doc.add_heading('Texto', level=1)
