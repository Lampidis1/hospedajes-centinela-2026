#!/bin/bash
#
# Script de actualización automática del repositorio GitHub
# Sistema de Hospedajes Centinela 2026
#
# Uso:
#   ./actualizar_github.sh <archivo_excel.xlsx> "<mensaje_commit>"
#
# Ejemplo:
#   ./actualizar_github.sh Actualizacion_Establecimientos_Sierra_Gorda_2026_V84.xlsx "data: actualizar hospedajes abril 2026"

set -e  # Salir si hay error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funciones de utilidad
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Verificar argumentos
if [ $# -lt 1 ]; then
    echo "Uso: $0 <archivo_excel.xlsx> [mensaje_commit]"
    echo ""
    echo "Ejemplo:"
    echo "  $0 Actualizacion_Establecimientos_Sierra_Gorda_2026_V84.xlsx \"data: actualizar abril 2026\""
    exit 1
fi

EXCEL_FILE="$1"
COMMIT_MSG="${2:-data: actualizar base de datos de hospedajes}"

# Verificar que el archivo Excel existe
if [ ! -f "$EXCEL_FILE" ]; then
    log_error "Archivo no encontrado: $EXCEL_FILE"
    exit 1
fi

log_info "Iniciando proceso de actualización..."
echo ""

# 1. Verificar que estamos en un repositorio git
if [ ! -d ".git" ]; then
    log_error "Este directorio no es un repositorio Git"
    log_info "Ejecuta primero: git init"
    exit 1
fi

log_success "Repositorio Git detectado"

# 2. Verificar que existe el script conversor
if [ ! -f "excel_to_json_converter.py" ]; then
    log_error "No se encuentra excel_to_json_converter.py"
    log_info "Asegúrate de que el script esté en el directorio actual"
    exit 1
fi

log_success "Script conversor encontrado"

# 3. Verificar Python
if ! command -v python3 &> /dev/null; then
    log_error "Python 3 no está instalado"
    exit 1
fi

log_success "Python 3 instalado"

# 4. Verificar pandas
if ! python3 -c "import pandas" 2>/dev/null; then
    log_warning "pandas no está instalado"
    log_info "Instalando pandas..."
    pip3 install pandas openpyxl
fi

log_success "Dependencias Python verificadas"

# 5. Convertir Excel a JSON
log_info "Convirtiendo Excel a JSON..."
echo ""

python3 excel_to_json_converter.py "$EXCEL_FILE" data/hospedajes.json

if [ $? -ne 0 ]; then
    log_error "Error al convertir Excel a JSON"
    exit 1
fi

echo ""
log_success "Conversión completada: data/hospedajes.json"

# 6. Verificar cambios
log_info "Verificando cambios en el repositorio..."

git status --short

if [ -z "$(git status --porcelain)" ]; then
    log_warning "No hay cambios para commitear"
    exit 0
fi

log_success "Cambios detectados"

# 7. Agregar archivos al staging
log_info "Agregando archivos..."

git add data/hospedajes.json

# Si existe el Excel en el repo, también agregarlo
if [ -f "data/$(basename $EXCEL_FILE)" ]; then
    git add "data/$(basename $EXCEL_FILE)"
fi

log_success "Archivos agregados al staging"

# 8. Crear commit
log_info "Creando commit..."

# Generar mensaje detallado
FECHA=$(date +"%Y-%m-%d %H:%M")
TOTAL_HOSPEDAJES=$(python3 -c "import json; data=json.load(open('data/hospedajes.json')); print(data['metadata']['total_hospedajes'])")
TOTAL_CAMAS=$(python3 -c "import json; data=json.load(open('data/hospedajes.json')); print(data['metadata']['total_camas'])")

COMMIT_FULL="$COMMIT_MSG

- Total hospedajes: $TOTAL_HOSPEDAJES
- Total camas: $TOTAL_CAMAS
- Fecha actualización: $FECHA
- Fuente: $(basename $EXCEL_FILE)"

git commit -m "$COMMIT_FULL"

log_success "Commit creado"

# 9. Push a GitHub
log_info "Subiendo cambios a GitHub..."

# Detectar rama actual
BRANCH=$(git branch --show-current)

if [ -z "$BRANCH" ]; then
    BRANCH="main"
fi

log_info "Rama actual: $BRANCH"

# Intentar push
if git push origin "$BRANCH"; then
    log_success "Cambios subidos exitosamente a GitHub"
else
    log_error "Error al subir cambios a GitHub"
    log_info "Verifica tu configuración de Git:"
    log_info "  git remote -v"
    log_info "  git config user.name"
    log_info "  git config user.email"
    exit 1
fi

# 10. Resumen final
echo ""
echo "═══════════════════════════════════════════════════════════════"
log_success "ACTUALIZACIÓN COMPLETADA"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "📊 Estadísticas:"
echo "   • Hospedajes: $TOTAL_HOSPEDAJES"
echo "   • Camas: $TOTAL_CAMAS"
echo "   • Rama: $BRANCH"
echo "   • Commit: ${COMMIT_MSG:0:50}..."
echo ""
echo "🔗 Acciones sugeridas:"
echo "   1. Verifica en GitHub: https://github.com/[tu-usuario]/hospedajes-centinela-2026"
echo "   2. Actualiza GitHub Pages si está habilitado"
echo "   3. Verifica que el frontend cargue los datos correctamente"
echo ""
log_success "¡Todo listo! 🎉"
echo "═══════════════════════════════════════════════════════════════"
