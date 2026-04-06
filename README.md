# 📘 GUÍA COMPLETA SISTEMA V3.0
**Sistema de Hospedajes Centinela 2026 - Gestión Integral**

---

## 🎯 NUEVAS FUNCIONALIDADES V3.0

### ✅ Implementado en esta Versión

1. **✏️ Edición en Tiempo Real**
   - Botón "Editar" en cada ficha
   - Modificar número de habitaciones por tipo
   - Activar/desactivar estándares (WiFi, AC, etc.)
   - Recálculo automático de categoría (estrellas)
   - Cálculo automático de camas según tipo habitación

2. **📊 Dashboard Mejorado**
   - Total de habitaciones reportadas
   - Habitaciones utilizadas por EECC CEN
   - Habitaciones utilizadas por otras empresas
   - Disponibilidad en tiempo real
   - Click en "Disponibles" filtra lista automáticamente

3. **💰 Sistema de Precios**
   - Precio por tipo de habitación en CLP
   - Simple/Doble/Triple con/sin baño privado
   - Editable desde cada ficha
   - Export able a Excel

4. **📋 Sistema de Contratos**
   - Agregar contratos desde la ficha
   - Dos tipos: EECC CEN o Otras Empresas
   - Para EECC CEN: empresa + trabajadores + habitaciones + tipo hab
   - Para Otras: solo habitaciones que usan
   - Resta automática de habitaciones disponibles
   - Visualización por color (dorado = EECC CEN)

5. **📱 Integración WhatsApp**
   - Botón para enviar WhatsApp individual
   - Mensaje predefinido con cuestionario
   - WhatsApp masivo (preparado para N8N)
   - Usa número telefónico de la base de datos

6. **💾 Actualización Automática**
   - Guardar cambios en JSON
   - Descarga automática para subir a GitHub
   - Export a Excel con toda la data mejorada

7. **🎨 UI Mejorada**
   - Fichas más compactas (4 por fila en PC)
   - Badge de disponibilidad en esquina superior
   - Tabs dentro del modal (Detalles/Editar/Contratos/Precios)
   - Diseño AMSA profesional

---

## 📦 ARCHIVOS GENERADOS

### 1. index_v3.html (48 KB)
Sistema completo con todas las funcionalidades

### 2. hospedajes_v3.json (59 KB)
Base de datos generada desde Base_de_datos_ordenada.xlsx
- 57 hospedajes
- 896 habitaciones totales
- 1,347 camas instaladas
- Estructura completa con contratos y precios

---

## 🚀 INSTALACIÓN

### Opción 1: Actualizar en GitHub (Recomendado)

```bash
# 1. Ir a tu repositorio
cd ~/hospedajes-centinela-2026

# 2. Copiar archivos
cp index_v3.html frontend/index.html
cp hospedajes_v3.json data/hospedajes.json

# 3. Commit y push
git add .
git commit -m "feat: sistema v3.0 - edición, contratos, precios, whatsapp

Nuevas funcionalidades:
- Edición en tiempo real de hospedajes
- Sistema de contratos (EECC CEN vs Otras)
- Gestión de precios por tipo de habitación
- Dashboard mejorado con métricas detalladas
- Integración WhatsApp individual y masivo
- UI compacta (4 fichas por fila)"

git push origin main
```

### Opción 2: Uso Local

```bash
# Simplemente abre index_v3.html en tu navegador
open index_v3.html
```

---

## 📱 CONFIGURACIÓN WHATSAPP + N8N

### Paso 1: Preparar N8N

1. **Instalar N8N**
   ```bash
   npm install n8n -g
   n8n
   # Abre: http://localhost:5678
   ```

2. **Crear Workflow "WhatsApp Masivo Hospedajes"**
   - Trigger: Webhook
   - Node 1: Leer JSON de hospedajes
   - Node 2: Loop por cada hospedaje
   - Node 3: Enviar WhatsApp (Twilio/WhatsApp Business API)
   - Node 4: Esperar respuesta
   - Node 5: Parsear respuesta y actualizar JSON

### Paso 2: Configurar Webhook

En el HTML, modificar función `enviarWhatsAppMasivo()`:

```javascript
async function enviarWhatsAppMasivo() {
    if (!confirm(`¿Enviar a ${hospedajesData.length} hospedajes?`)) return;
    
    // Enviar a N8N
    const response = await fetch('https://tu-n8n.com/webhook/whatsapp-masivo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            hospedajes: hospedajesData.map(h => ({
                id: h.id,
                nombre: h.nombre,
                encargado: h.encargado,
                telefono: h.telefono
            }))
        })
    });
    
    if (response.ok) {
        alert('✅ Mensajes enviados correctamente');
    }
}
```

### Paso 3: Template de Mensaje WhatsApp

```
Hola {{encargado}},

Actualización Hospedajes Centinela 2026
📋 {{nombre_hospedaje}}

Por favor responde las siguientes preguntas:

1️⃣ Habitaciones DISPONIBLES hoy: _____
2️⃣ ¿Tienes contrato con EECC Centinela? (Sí/No): _____
3️⃣ Si respondiste Sí:
   - Nombre empresa: _____
   - N° trabajadores: _____
   - Habitaciones usadas: _____
   - Tipo (Simple/Doble/Triple): _____

4️⃣ Otras empresas alojadas:
   - Nombre empresa: _____
   - Habitaciones usadas: _____

Gracias por tu colaboración!
```

### Paso 4: Parsear Respuestas en N8N

Workflow N8N para procesar respuestas:

```json
{
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "whatsapp-response"
      },
      "name": "Webhook Respuesta",
      "type": "n8n-nodes-base.webhook"
    },
    {
      "parameters": {
        "operation": "parseMessage"
      },
      "name": "Parsear Texto",
      "type": "n8n-nodes-base.function"
    },
    {
      "parameters": {
        "operation": "update",
        "updateFields": {
          "habitaciones_disponibles": "={{$json.disponibles}}",
          "contratos": "={{$json.contratos}}"
        }
      },
      "name": "Actualizar JSON",
      "type": "n8n-nodes-base.github"
    }
  ]
}
```

---

## 🎨 CÓMO USAR EL SISTEMA

### 1. Ver Dashboard

Al abrir el sistema verás:
- **Total Habitaciones:** 896 reportadas
- **EECC CEN:** 0 (se llenan con contratos)
- **Otras Empresas:** 0 (se llenan con contratos)
- **Disponibles:** 896 (se actualiza automáticamente)

### 2. Buscar y Filtrar

Usa los filtros superiores para:
- 🔍 Buscar por nombre/dirección
- ⭐ Filtrar por categoría (1 a 5 estrellas)
- 🏨 Filtrar por tipo de habitación
- 📊 Filtrar por disponibilidad

### 3. Ver Ficha de Hospedaje

Click en cualquier tarjeta para ver:
- **Tab Detalles:** Información general
- **Tab Editar:** Modificar habitaciones y estándares
- **Tab Contratos:** Agregar/eliminar contratos
- **Tab Precios:** Configurar precios por tipo

### 4. Editar Hospedaje

```
1. Click en tarjeta o botón "Editar"
2. Ir a tab "Editar"
3. Modificar:
   - Habitaciones simples/dobles/triples
   - Baño privado/compartido
   - Estándares (WiFi, AC, Alimentación, Lavandería)
4. Click "Guardar Cambios"
5. Categoría se recalcula automáticamente
```

### 5. Agregar Contrato

```
1. Abrir ficha de hospedaje
2. Tab "Contratos"
3. Click "+ Agregar Contrato"
4. Ingresar:
   - Nombre empresa
   - ¿Es EECC CEN? (Sí/No)
   - Si es EECC CEN: trabajadores + habitaciones + tipo
   - Si no: solo habitaciones usadas
5. Contrato aparece en la lista
6. Disponibilidad se actualiza automáticamente
```

### 6. Configurar Precios

```
1. Tab "Precios"
2. Ingresar precio CLP para cada tipo:
   - Simple Privado: $45,000
   - Simple Compartido: $35,000
   - Doble Privado: $55,000
   - etc.
3. Click "Guardar Precios"
```

### 7. Enviar WhatsApp

**Individual:**
```
1. Click botón 📱 en la tarjeta
2. Se abre WhatsApp Web
3. Mensaje predefinido aparece
4. Ajustar si necesario y enviar
```

**Masivo:**
```
1. Header → "📱 WhatsApp Masivo"
2. Confirmar envío
3. Si no tienes N8N: descarga Excel con números
4. Si tienes N8N: se envía automáticamente
```

### 8. Exportar Datos

```
1. Header → "📊 Exportar Excel"
2. Se genera Excel con 2 hojas:
   - Hoja 1: Hospedajes (todos los datos)
   - Hoja 2: Contratos (todos los contratos)
3. Excel se descarga automáticamente
```

### 9. Guardar en GitHub

```
1. Hacer todas las modificaciones necesarias
2. Header → "💾 Guardar en GitHub"
3. Se descarga JSON actualizado
4. Subir manualmente a GitHub:
   - Ir a: github.com/tu-repo/data/
   - Upload file → hospedajes_actualizado.json
   - Commit changes
```

---

## 📊 ESTRUCTURA DE DATOS

### Hospedaje Completo

```json
{
  "id": 1,
  "nombre": "Aris Alojamiento",
  "direccion": "Colón #34",
  "localidad": "Sierra Gorda",
  "rut": "76459458-9",
  "encargado": "Ronald Castro Vega",
  "telefono": "+56962447427",
  "email": "ronald.castro@alojamientosierragorda.cl",
  
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
  "categoria": 4,
  
  "estandares": {
    "habitaciones": "PARCIAL",
    "wifi": "SI",
    "climatizacion": "SI",
    "alimentacion": "PARCIAL",
    "lavanderia": "NO"
  },
  
  "contratos": [
    {
      "empresa": "Equans Chile",
      "tipo_cliente": "EECC_CEN",
      "num_trabajadores": 5,
      "habitaciones_usadas": 3,
      "tipo_habitacion": "doble",
      "fecha_inicio": "2026-04-01"
    },
    {
      "empresa": "Constructora XYZ",
      "tipo_cliente": "OTRA",
      "num_trabajadores": 0,
      "habitaciones_usadas": 2,
      "tipo_habitacion": "simple",
      "fecha_inicio": "2026-04-05"
    }
  ],
  
  "precios": {
    "simple_privado": 45000,
    "simple_compartido": 35000,
    "doble_privado": 55000,
    "doble_compartido": 45000,
    "triple_privado": 65000,
    "triple_compartido": 55000
  },
  
  "fecha_actualizacion": "2026-04-06"
}
```

---

## 🔄 FLUJO DE TRABAJO SEMANAL

### Lunes: Actualización de Disponibilidad

```
09:00 - MGI/Encargado abre sistema
09:15 - Click "📱 WhatsApp Masivo"
09:30 - Encargados reciben mensaje
10:00-12:00 - Encargados responden
12:00 - N8N procesa respuestas
12:30 - JSON se actualiza automáticamente
13:00 - Dashboard refleja nuevos datos
```

### Martes-Jueves: Gestión de Contratos

```
- Nuevos contratos: Tab "Contratos" → "+ Agregar"
- Contratos finalizados: "Eliminar"
- Actualización de trabajadores: Editar contrato existente
```

### Viernes: Exportación y Reportes

```
- Exportar Excel semanal
- Guardar en GitHub
- Revisar métricas en dashboard
- Generar reporte para gerencia
```

---

## 🛠️ PERSONALIZACIÓN

### Cambiar Mensaje WhatsApp

Editar en línea ~700 del HTML:

```javascript
const mensaje = encodeURIComponent(
    `TU MENSAJE PERSONALIZADO AQUÍ\n\n` +
    `1. Pregunta 1\n` +
    `2. Pregunta 2\n`
);
```

### Agregar Nuevo Campo

1. Modificar estructura JSON
2. Agregar campo en formulario (Tab Editar)
3. Actualizar función `guardarEdicion()`
4. Agregar a export Excel

### Cambiar Colores

Editar variables CSS (líneas 20-30):

```css
:root {
    --teal: #00A399;     /* Color principal */
    --gold: #F2A900;     /* Acentos */
    --dark: #1C2632;     /* Textos */
}
```

---

## 📈 MÉTRICAS Y REPORTES

### Dashboard Principal

```
Total Habitaciones: 896
├─ EECC CEN: 120 (13%)
├─ Otras Empresas: 350 (39%)
└─ Disponibles: 426 (48%)

Tasa Ocupación: 52%
Total Hospedajes: 57
```

### Reporte Semanal

Datos disponibles para exportar:
- Hospedajes activos
- Contratos por empresa
- Ocupación por tipo de habitación
- Precios promedio
- Disponibilidad por localidad

---

## 🔧 TROUBLESHOOTING

### Dashboard muestra "0" en todo

**Problema:** No hay contratos cargados  
**Solución:** Agregar contratos desde tab "Contratos" en cada hospedaje

### WhatsApp no abre

**Problema:** Número telefónico mal formateado  
**Solución:** Verificar que telefono tenga formato +569XXXXXXXX

### Exportar Excel no funciona

**Problema:** Librería XLSX no cargada  
**Solución:** Verificar conexión internet (CDN: cdnjs.cloudflare.com)

### Cambios no se guardan

**Problema:** Modal se cierra sin guardar  
**Solución:** Click en "Guardar Cambios" antes de cerrar

---

## 🎯 PRÓXIMAS MEJORAS (v4.0)

- [ ] Integración directa GitHub API (guardar sin descargar)
- [ ] Calendario de ocupación
- [ ] Historial de cambios
- [ ] Notificaciones automáticas
- [ ] App móvil (PWA)
- [ ] Dashboard de análisis avanzado
- [ ] Integración con sistemas contables

---

## 📞 SOPORTE

- **Documentación:** Este archivo
- **Issues:** GitHub Issues
- **Email:** soporte@centinela.cl

---

**Versión:** 3.0  
**Fecha:** 2026-04-06  
**Autor:** Equipo Centinela + Claude AI  
**Estado:** ✅ Producción
