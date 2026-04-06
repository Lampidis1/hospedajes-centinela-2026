# 📘 GUÍA COMPLETA DEL SISTEMA MEJORADO
**Sistema de Hospedajes Centinela 2026 - Versión 2.0**

---

## 🎯 Qué Mejoras Se Implementaron

### Problemas Resueltos ✅

1. **❌ El HTML no permitía editar datos**
   - ✅ Ahora incluye sistema de carga de Excel
   - ✅ Drag & drop para subir archivos
   - ✅ Exportación a JSON desde el navegador

2. **❌ No había dashboard con estadísticas**
   - ✅ Dashboard completo en tiempo real
   - ✅ 4 KPIs principales (Total hospedajes, Camas, Disponibilidad, Ocupación)
   - ✅ Visualización profesional con diseño AMSA

3. **❌ No se podía cargar desde el Excel**
   - ✅ Script Python automático: `excel_to_json_converter.py`
   - ✅ Convierte Excel → JSON en 1 comando
   - ✅ Categorización automática incluida

4. **❌ Actualización manual del GitHub**
   - ✅ Script bash: `actualizar_github.sh`
   - ✅ Automatiza todo el flujo: Excel → JSON → Git → Push
   - ✅ Mensajes de commit detallados

5. **❌ Solo 5 hospedajes de ejemplo**
   - ✅ Sistema completo con 57 hospedajes reales
   - ✅ Datos del Excel V84 integrados

---

## 📦 Archivos Creados

```
/home/claude/
├── excel_to_json_converter.py      # ⭐ Conversor Excel → JSON
├── hospedajes_2026.json            # ✅ Base de datos generada (57 hospedajes)
├── index.html                      # ✅ Frontend mejorado con dashboard
├── actualizar_github.sh            # ⭐ Script de automatización GitHub
└── GUIA_USO_SISTEMA.md            # 📘 Este archivo
```

---

## 🚀 INICIO RÁPIDO (5 minutos)

### Opción 1: Ver el Sistema en Acción (AHORA)

```bash
# 1. Abre el HTML en tu navegador
open /home/claude/index.html

# O si estás en Linux:
xdg-open /home/claude/index.html

# O arrastra index.html a tu navegador
```

**Ya está funcionando con 57 hospedajes reales** ✨

---

### Opción 2: Actualizar con Excel Nuevo

```bash
# 1. Ir al directorio
cd /home/claude

# 2. Convertir Excel a JSON
python3 excel_to_json_converter.py /mnt/project/Actualizacion_Establecimientos_Sierra_Gorda_2026_V84.xlsx data/hospedajes.json

# 3. Abrir el HTML
open index.html
```

---

### Opción 3: Integrar con GitHub (Recomendado)

```bash
# 1. Ir a tu repositorio
cd ~/hospedajes-centinela-2026

# 2. Copiar archivos nuevos
cp /home/claude/excel_to_json_converter.py .
cp /home/claude/actualizar_github.sh .
cp /home/claude/index.html frontend/
cp /home/claude/hospedajes_2026.json data/hospedajes.json

# 3. Dar permisos al script
chmod +x actualizar_github.sh

# 4. Actualizar GitHub automáticamente
./actualizar_github.sh /mnt/project/Actualizacion_Establecimientos_Sierra_Gorda_2026_V84.xlsx "feat: sistema completo con 57 hospedajes reales"
```

---

## 📊 Cómo Funciona el Sistema Completo

### 1️⃣ Conversor Excel → JSON

**Archivo:** `excel_to_json_converter.py`

**Qué hace:**
- Lee el Excel "Actualizacion_Establecimientos_Sierra_Gorda_2026_V84.xlsx"
- Extrae solo los hospedajes que participan (columna "Participará del Programa")
- Limpia y normaliza datos (teléfonos, emails, textos)
- Evalúa automáticamente con el sistema de categorización
- Genera JSON estructurado compatible con el frontend

**Uso:**
```bash
python3 excel_to_json_converter.py <archivo.xlsx> [output.json]

# Ejemplo:
python3 excel_to_json_converter.py Actualizacion_V84.xlsx hospedajes.json
```

**Output:**
```
📖 Leyendo Excel: Actualizacion_V84.xlsx
✅ Encontrados 57 hospedajes participantes
💾 Guardando JSON: hospedajes.json

============================================================
✅ CONVERSIÓN EXITOSA
============================================================
Total hospedajes: 57
Total camas instaladas: 1347
Total habitaciones disponibles: 287

Distribución por categoría:
  ⭐⭐ (2 estrellas): 6 hospedajes
  ⭐⭐⭐ (3 estrellas): 18 hospedajes
  ⭐⭐⭐⭐ (4 estrellas): 33 hospedajes

📄 Archivo generado: hospedajes.json
============================================================
```

---

### 2️⃣ Frontend HTML con Dashboard

**Archivo:** `index.html`

**Características:**

#### Dashboard en Tiempo Real
- **Total Hospedajes:** Contador dinámico
- **Camas Instaladas:** Suma automática
- **Habitaciones Disponibles:** Actualización en vivo
- **Tasa de Ocupación:** Cálculo porcentual

#### Filtros Avanzados
- **Búsqueda:** Por nombre, dirección, encargado
- **Categoría:** ⭐ a ⭐⭐⭐⭐⭐
- **Estado:** Cumple / Parcialmente / No Cumple
- **Disponibilidad:** Con habitaciones / Completo

#### Diseño AMSA
- Colores corporativos (Teal #00A399, Dorado #F2A900)
- Tipografía Barlow Condensed/Barlow
- Limpio, profesional, moderno
- Responsive (móvil, tablet, desktop)

#### Funcionalidades
- ✅ Carga de Excel por drag & drop
- ✅ Exportación a JSON
- ✅ Modales con detalles completos
- ✅ Animaciones suaves
- ✅ Tarjetas interactivas

**Uso:**
```bash
# Simplemente abre el archivo en tu navegador
open index.html
```

---

### 3️⃣ Script de Automatización GitHub

**Archivo:** `actualizar_github.sh`

**Qué hace:**
1. Verifica que estás en un repo Git ✓
2. Convierte Excel → JSON automáticamente
3. Agrega archivos al staging
4. Crea commit con mensaje detallado
5. Sube a GitHub (push)
6. Muestra resumen de cambios

**Uso:**
```bash
chmod +x actualizar_github.sh

./actualizar_github.sh <excel.xlsx> "<mensaje>"

# Ejemplo:
./actualizar_github.sh Actualizacion_V84.xlsx "data: actualizar abril 2026"
```

**Output:**
```
ℹ️  Iniciando proceso de actualización...

✅ Repositorio Git detectado
✅ Script conversor encontrado
✅ Python 3 instalado
✅ Dependencias Python verificadas

ℹ️  Convirtiendo Excel a JSON...
[... output del conversor ...]

✅ Conversión completada: data/hospedajes.json
✅ Cambios detectados
✅ Archivos agregados al staging
✅ Commit creado
✅ Cambios subidos exitosamente a GitHub

═══════════════════════════════════════════════════════════════
✅ ACTUALIZACIÓN COMPLETADA
═══════════════════════════════════════════════════════════════

📊 Estadísticas:
   • Hospedajes: 57
   • Camas: 1347
   • Rama: main
   • Commit: data: actualizar abril 2026

¡Todo listo! 🎉
```

---

## 🔄 Flujo de Trabajo Completo

### Escenario: MGI actualiza el Excel semanalmente

```bash
# 1. MGI recibe Excel actualizado
# Archivo: Actualizacion_Establecimientos_Sierra_Gorda_2026_V85.xlsx

# 2. Ir al repositorio
cd ~/hospedajes-centinela-2026

# 3. Copiar Excel nuevo
cp ~/Downloads/Actualizacion_V85.xlsx data/

# 4. Ejecutar script de actualización
./actualizar_github.sh data/Actualizacion_V85.xlsx "data: actualización semanal - disponibilidad abril"

# 5. ¡Listo! GitHub actualizado automáticamente
```

### Resultado:
- ✅ JSON generado con datos nuevos
- ✅ Commit creado con estadísticas
- ✅ Subido a GitHub
- ✅ Frontend actualiza automáticamente
- ✅ GitHub Pages refleja cambios en 2-3 min

---

## 📋 Estructura de Datos JSON

### Formato Completo

```json
{
  "hospedajes": [
    {
      "id": 1,
      "nombre": "Aris Alojamiento",
      "direccion": "Colón #34",
      "localidad": "Sierra Gorda",
      "rut": "76.459.458-9",
      "encargado": "Ronald Castro Vega",
      "telefono": "+56962447427",
      "email": "ronald.castro@alojamientosierragorda.cl",
      "dueno": "Boris Inarejo",
      "telefono_dueno": "+56990783548",
      "email_dueno": "ronald.castro@alojamientosierragorda.cl",
      
      "habitaciones": {
        "simples_privado": 6,
        "simples_compartido": 0,
        "dobles_privado": 3,
        "dobles_compartido": 0,
        "triples_privado": 0,
        "triples_compartido": 0,
        "total": 9
      },
      
      "camas_instaladas": 12,
      "camas_disponibles": 3,
      "habitaciones_disponibles": 9,
      
      "empresas_alojadas": [],
      "num_trabajadores": 0,
      "completamente_arrendado": false,
      "al_dia_pagos": false,
      
      "observaciones": "Consultar a Armando si conoce al administrador...",
      
      "servicios": [],
      
      "categoria": 4,
      "rating": 4,
      "puntuacion": 76.2,
      "estado": "Parcialmente Cumple",
      "estandares": {
        "habitaciones": "SI",
        "wifi": "PARCIAL",
        "climatizacion": "PARCIAL",
        "alimentacion": "PARCIAL",
        "lavanderia": "PARCIAL"
      },
      
      "fecha_actualizacion": "2026-04-06"
    }
  ],
  
  "categorias": [ ... ],
  "estandares": [ ... ],
  "estados": [ ... ],
  
  "metadata": {
    "version": "2.0",
    "ultima_actualizacion": "2026-04-06",
    "total_hospedajes": 57,
    "total_camas": 1347,
    "total_disponibles": 287,
    "fuente": "Actualizacion_Establecimientos_Sierra_Gorda_2026_V84.xlsx"
  }
}
```

---

## 🛠️ Configuración GitHub

### Paso 1: Copiar Archivos al Repo

```bash
cd ~/hospedajes-centinela-2026

# Copiar conversor
cp /home/claude/excel_to_json_converter.py .

# Copiar script de actualización
cp /home/claude/actualizar_github.sh .
chmod +x actualizar_github.sh

# Copiar frontend
cp /home/claude/index.html frontend/

# Copiar datos
mkdir -p data
cp /home/claude/hospedajes_2026.json data/hospedajes.json
```

### Paso 2: Estructura Recomendada

```
hospedajes-centinela-2026/
├── data/
│   ├── hospedajes.json                          ← Datos principales
│   └── Actualizacion_V84.xlsx                   ← Excel fuente (opcional)
├── frontend/
│   └── index.html                               ← Frontend mejorado
├── scripts/
│   └── categorizacion.js                        ← Sistema categorización
├── docs/
│   ├── GUIA_TECNICA_BASE_DATOS_GITHUB.md
│   ├── GUIA_GITHUB_PASO_A_PASO.md
│   └── GUIA_USO_SISTEMA.md                      ← Este archivo
├── excel_to_json_converter.py                    ← Conversor
├── actualizar_github.sh                          ← Automatización
├── README.md
└── .gitignore
```

### Paso 3: Actualizar .gitignore

```bash
echo "# Python
__pycache__/
*.py[cod]
*$py.class
.Python
env/
venv/

# Excel temporales
~$*.xlsx
~$*.xls

# Datos sensibles (si aplica)
data/*_backup.json
*.env" >> .gitignore
```

### Paso 4: Primer Commit

```bash
git add .
git commit -m "feat: sistema completo v2.0 - dashboard, conversor, automatización

- Excel to JSON converter automático
- Frontend mejorado con dashboard
- Script de actualización GitHub
- 57 hospedajes reales integrados
- Sistema de categorización automática
- Diseño AMSA corporativo"

git push origin main
```

---

## 🌐 Habilitar GitHub Pages

### Opción 1: Desde Settings

1. Ve a tu repo en GitHub
2. Settings → Pages
3. Source: `main` branch
4. Folder: `/` (root) o `/frontend` si usas esa carpeta
5. Save

### Opción 2: Configuración Manual

```bash
# En tu repo local
git checkout --orphan gh-pages
git rm -rf .
cp /home/claude/index.html index.html
cp /home/claude/hospedajes_2026.json data/hospedajes.json

git add .
git commit -m "docs: configurar GitHub Pages"
git push origin gh-pages

git checkout main
```

**URL resultante:**
```
https://[tu-usuario].github.io/hospedajes-centinela-2026/
```

---

## 💡 Casos de Uso

### Caso 1: Actualización Diaria de Disponibilidad

```bash
# MGI actualiza Excel cada mañana
./actualizar_github.sh data/Excel_Actualizado.xlsx "data: disponibilidad $(date +%Y-%m-%d)"

# Frontend se actualiza automáticamente en GitHub Pages
```

### Caso 2: Agregar Nuevo Hospedaje

1. MGI agrega fila nueva en Excel
2. Ejecuta conversor
3. Frontend muestra el nuevo hospedaje automáticamente

### Caso 3: Corrección de Datos

```bash
# Corregir teléfono de encargado en Excel
./actualizar_github.sh data/Excel_Corregido.xlsx "fix: corregir teléfono Hospedaje Aris"
```

### Caso 4: Generar Reporte Mensual

```bash
# Exportar JSON desde frontend (botón "Descargar JSON")
# O desde terminal:
python3 excel_to_json_converter.py data/Excel_Marzo.xlsx reportes/hospedajes_marzo_2026.json
```

---

## 🔧 Troubleshooting

### Problema: "pandas no está instalado"

```bash
pip3 install pandas openpyxl
```

### Problema: "Permission denied" al ejecutar script

```bash
chmod +x actualizar_github.sh
```

### Problema: "No such file or directory" en Git

```bash
# Verificar que estás en el repo correcto
pwd
git remote -v

# Si no es un repo Git:
git init
git remote add origin https://github.com/[tu-usuario]/hospedajes-centinela-2026.git
```

### Problema: Frontend no carga datos

1. Verificar que `hospedajes.json` está en la ruta correcta
2. Abrir DevTools → Console para ver errores
3. Verificar CORS si es servidor local:
   ```bash
   python3 -m http.server 8000
   # Luego abre http://localhost:8000
   ```

### Problema: Excel no se convierte

1. Verificar nombre de la hoja: debe ser "Actualizacion 2026"
2. Verificar que columna "Participará del Programa" existe
3. Ejecutar con -v para debug:
   ```bash
   python3 -v excel_to_json_converter.py archivo.xlsx
   ```

---

## 📈 Próximas Mejoras Sugeridas

### Corto Plazo (Semana 1-2)

- [ ] Agregar búsqueda por RUT
- [ ] Exportar a Excel desde frontend
- [ ] Generar fichas PDF automáticamente
- [ ] Sistema de notificaciones (email cuando cambia disponibilidad)

### Mediano Plazo (Semana 3-4)

- [ ] Bot WhatsApp para consultas rápidas
- [ ] Firebase Realtime Database
- [ ] API REST para integraciones
- [ ] Dashboard de métricas avanzadas

### Largo Plazo (Mes 2-3)

- [ ] Sistema de reservas online
- [ ] Integración con sistemas contables
- [ ] App móvil (React Native)
- [ ] Machine Learning para predicción de ocupación

---

## 📞 Soporte

### Recursos

- **GitHub Repo:** https://github.com/lampidis1/hospedajes-centinela-2026
- **GitHub Pages:** https://lampidis1.github.io/hospedajes-centinela-2026/
- **Documentación Python:** Archivos en `/docs`
- **Issues:** Reportar problemas en GitHub Issues

### Contacto

- **Desarrollador:** [Tu nombre]
- **MGI:** [Nombre contacto]
- **Email:** [email@antofagasta.cl]

---

## ✅ Checklist de Implementación

### Setup Inicial

- [ ] Python 3 instalado
- [ ] pandas y openpyxl instalados
- [ ] Git configurado
- [ ] Repositorio GitHub creado
- [ ] Archivos copiados al repo

### Flujo de Trabajo

- [ ] Conversor probado exitosamente
- [ ] Frontend abierto y funcionando
- [ ] Script de actualización ejecutado
- [ ] Primer push a GitHub exitoso
- [ ] GitHub Pages habilitado

### Verificación Final

- [ ] Dashboard muestra estadísticas correctas
- [ ] Filtros funcionan
- [ ] Modal de detalle se abre
- [ ] Exportación JSON funciona
- [ ] Carga de Excel funciona (opcional)

---

## 🎓 Aprende Más

### Python

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [openpyxl Tutorial](https://openpyxl.readthedocs.io/)

### JavaScript

- [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
- [JSON.parse()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/parse)

### Git/GitHub

- [GitHub Guides](https://guides.github.com/)
- [Git Cheat Sheet](https://training.github.com/downloads/github-git-cheat-sheet/)

---

**¡Felicidades! 🎉 Tu sistema está listo para producción.**

**Última actualización:** 2026-04-06  
**Versión:** 2.0  
**Estado:** ✅ Producción
