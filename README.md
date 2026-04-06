# 🏨 Sistema de Hospedajes - Centinela 2026

**Plataforma integral para la gestión de hospedajes en Sierra Gorda**

![Versión](https://img.shields.io/badge/Versión-2.0-blue)
![Estado](https://img.shields.io/badge/Estado-Producción-green)

---

## 🚀 Inicio Rápido

### Ver el Sistema en Vivo
👉 **[Abrir Dashboard](https://lampidis1.github.io/hospedajes-centinela-2026/index.html)**

---

## 📊 Estadísticas Actuales

- **Total Hospedajes:** 57
- **Camas Instaladas:** 1,347
- **Habitaciones Disponibles:** 287
- **Tasa Ocupación:** ~79%

---

## ✨ Características v2.0

- ✅ Dashboard interactivo con 4 KPIs en tiempo real
- ✅ Filtros avanzados (búsqueda, categoría, estado, disponibilidad)
- ✅ Sistema de categorización automática (⭐ a ⭐⭐⭐⭐⭐)
- ✅ Diseño AMSA corporativo (Teal, Dorado, Barlow)
- ✅ Modales detallados con información completa
- ✅ Conversor automático Excel → JSON
- ✅ Script de actualización GitHub automatizado
- ✅ 100% responsive (móvil, tablet, desktop)

---

## 📁 Estructura del Proyecto

hospedajes-centinela-2026/
├── data/
│   └── hospedajes.json              # Base de datos (57 hospedajes)
├── docs/
│   ├── GUIA_USO_SISTEMA.md         # Documentación completa
│   ├── RESUMEN_EJECUTIVO.md        # Resumen ejecutivo
│   └── INSTALACION_SIMPLE.md       # Guía de instalación
├── scripts/
│   └── categorizacion.js            # Sistema de categorización
├── index.html                       # Frontend con dashboard
├── excel_to_json_converter.py       # Conversor Excel → JSON
└── actualizar_github.sh             # Automatización GitHub

---

## 🔄 Actualizar Datos

### Opción 1: Automática (Terminal)
```bash
./actualizar_github.sh Excel_Nuevo.xlsx "mensaje del commit"
```

### Opción 2: Manual (GitHub Web)
1. Convertir Excel → JSON: `python3 excel_to_json_converter.py Excel.xlsx`
2. Subir `hospedajes.json` a la carpeta `data/`

---

## 📖 Documentación

- **[Guía de Uso Completa](docs/GUIA_USO_SISTEMA.md)** - 16 páginas
- **[Resumen Ejecutivo](docs/RESUMEN_EJECUTIVO.md)** - Overview rápido
- **[Guía de Instalación](docs/INSTALACION_SIMPLE.md)** - 3 opciones de setup

---

## 🌐 GitHub Pages

Sitio publicado en:
**https://lampidis1.github.io/hospedajes-centinela-2026/index.html**

---

## 🎨 Diseño

Cumple con el Manual de Marca AMSA:
- Colores: Teal (#00A399), Dorado (#F2A900)
- Tipografía: Barlow Condensed, Barlow
- Layout: Limpio, profesional, moderno

---

## 📈 Distribución de Hospedajes

| Categoría | Cantidad | % |
|-----------|----------|---|
| ⭐⭐ Aceptable | 6 | 10.5% |
| ⭐⭐⭐ Bueno | 18 | 31.6% |
| ⭐⭐⭐⭐ Muy Bueno | 33 | 57.9% |

---

## 🔧 Tecnologías

- **Frontend:** HTML5, CSS3, JavaScript Vanilla
- **Base de Datos:** JSON (GitHub)
- **Automatización:** Python 3, Bash
- **Deploy:** GitHub Pages

---

**Última actualización:** 2026-04-06  
**Versión:** 2.0  
**Desarrollado por:** Equipo Centinela 2026
