/**
 * SISTEMA DE CATEGORIZACIÓN AUTOMÁTICA DE HOSPEDAJES
 * Centinela 2026 - Sierra Gorda
 * 
 * Este script evalúa automáticamente los hospedajes basándose en los 5 estándares Centinela
 * y asigna una categoría de ⭐ a ⭐⭐⭐⭐⭐
 */

class CategorizadorHospedajes {
    constructor() {
        // Ponderación de criterios (suma = 100)
        this.pesos = {
            habitaciones: 20,      // Max 2 camas + Baño privado
            wifi: 15,              // WiFi buena señal
            televisión: 10,        // TV con canales
            climatización: 20,     // Aire acondicionado
            alimentación: 15,      // Desayuno/Cena/Colaciones
            lavandería: 10,        // Sistema de lavandería
            capacidad: 5,          // Número de camas
            precio: 5              // Rango de precios
        };

        // Criterios de evaluación por estándar
        this.criterios = {
            habitaciones: {
                si: 100,
                parcial: 50,
                no: 0
            },
            wifi: {
                si: 100,
                parcial: 50,
                no: 0
            },
            televisión: {
                si: 100,
                parcial: 50,
                no: 0
            },
            climatización: {
                si: 100,
                parcial: 50,
                no: 0
            },
            alimentación: {
                todo_dia: 100,      // Desayuno + Cena + Colaciones
                dos_servicios: 75,  // Desayuno + Cena O similar
                un_servicio: 50,    // Solo Desayuno O Cena O Colaciones
                no: 0
            },
            lavandería: {
                propio: 100,
                proveedor: 80,
                no: 0
            },
            capacidad: {
                muy_grande: 100,    // > 50 camas
                grande: 80,         // 20-50 camas
                mediano: 60,        // 10-20 camas
                pequeño: 40,        // 5-10 camas
                muy_pequeño: 20     // < 5 camas
            },
            precio: {
                economico: 100,     // < $40k por cama
                medio: 80,          // $40-60k
                moderado: 60,       // $60-80k
                premium: 40,        // > $80k
                no_disponible: 50   // Sin información
            }
        };
    }

    /**
     * Calcula la puntuación total de un hospedaje
     * @param {Object} hospedaje - Objeto con datos del hospedaje
     * @returns {Object} - {puntuacion: number, categoria: number, detalles: Object}
     */
    evaluar(hospedaje) {
        const puntuaciones = {};
        let puntuacionTotal = 0;

        // Evaluar cada criterio
        puntuaciones.habitaciones = this.evaluarHabitaciones(hospedaje);
        puntuaciones.wifi = this.evaluarWiFi(hospedaje);
        puntuaciones.televisión = this.evaluarTelevisión(hospedaje);
        puntuaciones.climatización = this.evaluarClimatización(hospedaje);
        puntuaciones.alimentación = this.evaluarAlimentación(hospedaje);
        puntuaciones.lavandería = this.evaluarLavandería(hospedaje);
        puntuaciones.capacidad = this.evaluarCapacidad(hospedaje);
        puntuaciones.precio = this.evaluarPrecio(hospedaje);

        // Calcular puntuación ponderada
        puntuacionTotal = 
            (puntuaciones.habitaciones * this.pesos.habitaciones +
            puntuaciones.wifi * this.pesos.wifi +
            puntuaciones.televisión * this.pesos.televisión +
            puntuaciones.climatización * this.pesos.climatización +
            puntuaciones.alimentación * this.pesos.alimentación +
            puntuaciones.lavandería * this.pesos.lavandería +
            puntuaciones.capacidad * this.pesos.capacidad +
            puntuaciones.precio * this.pesos.precio) / 100;

        // Convertir a categoría de estrellas (1-5)
        const categoria = this.puntuacionAEstrella(puntuacionTotal);

        // Determinar estado de cumplimiento
        const estado = this.determinarEstado(categoria, hospedaje);

        return {
            puntuacion: Math.round(puntuacionTotal),
            categoria: categoria,
            estado: estado,
            detalles: {
                puntuaciones: puntuaciones,
                puntacionTotal: Math.round(puntuacionTotal)
            }
        };
    }

    // ========== EVALUADORES INDIVIDUALES ==========

    evaluarHabitaciones(hospedaje) {
        const estandar = hospedaje.estandares?.habitaciones;
        return this.criterios.habitaciones[estandar?.toLowerCase()] ?? 0;
    }

    evaluarWiFi(hospedaje) {
        const estandar = hospedaje.estandares?.wifi;
        return this.criterios.wifi[estandar?.toLowerCase()] ?? 0;
    }

    evaluarTelevisión(hospedaje) {
        const estandar = hospedaje.estandares?.televisión;
        return this.criterios.televisión[estandar?.toLowerCase()] ?? 0;
    }

    evaluarClimatización(hospedaje) {
        const estandar = hospedaje.estandares?.climatización;
        return this.criterios.climatización[estandar?.toLowerCase()] ?? 0;
    }

    evaluarAlimentación(hospedaje) {
        const servicios = hospedaje.servicios || [];
        const tieneDesayuno = servicios.some(s => s.toLowerCase().includes('desayuno'));
        const tieneCena = servicios.some(s => s.toLowerCase().includes('cena'));
        const tieneColacion = servicios.some(s => s.toLowerCase().includes('colacion'));

        const serviciosCount = (tieneDesayuno ? 1 : 0) + (tieneCena ? 1 : 0) + (tieneColacion ? 1 : 0);

        if (serviciosCount === 3) return this.criterios.alimentación.todo_dia;
        if (serviciosCount === 2) return this.criterios.alimentación.dos_servicios;
        if (serviciosCount === 1) return this.criterios.alimentación.un_servicio;
        return this.criterios.alimentación.no;
    }

    evaluarLavandería(hospedaje) {
        const servicios = hospedaje.servicios || [];
        const tienePropio = servicios.some(s => s.toLowerCase().includes('lavandería propio') || s.toLowerCase().includes('lavandería (propia)'));
        const tieneProveedor = hospedaje.estandares?.lavandería?.toLowerCase() === 'si' || 
                             servicios.some(s => s.toLowerCase().includes('lavandería'));

        if (tienePropio) return this.criterios.lavandería.propio;
        if (tieneProveedor) return this.criterios.lavandería.proveedor;
        return this.criterios.lavandería.no;
    }

    evaluarCapacidad(hospedaje) {
        const camas = hospedaje.camas_instaladas || 0;

        if (camas > 50) return this.criterios.capacidad.muy_grande;
        if (camas >= 20) return this.criterios.capacidad.grande;
        if (camas >= 10) return this.criterios.capacidad.mediano;
        if (camas >= 5) return this.criterios.capacidad.pequeño;
        if (camas > 0) return this.criterios.capacidad.muy_pequeño;
        return 0;
    }

    evaluarPrecio(hospedaje) {
        const precio = hospedaje.precio_promedio || null;

        if (!precio) return this.criterios.precio.no_disponible;
        if (precio < 40000) return this.criterios.precio.economico;
        if (precio < 60000) return this.criterios.precio.medio;
        if (precio < 80000) return this.criterios.precio.moderado;
        return this.criterios.precio.premium;
    }

    /**
     * Convierte puntuación (0-100) a categoría de estrellas (1-5)
     */
    puntuacionAEstrella(puntuacion) {
        if (puntuacion >= 90) return 5;
        if (puntuacion >= 75) return 4;
        if (puntuacion >= 60) return 3;
        if (puntuacion >= 40) return 2;
        if (puntuacion >= 20) return 1;
        return 0;
    }

    /**
     * Determina el estado general de cumplimiento
     */
    determinarEstado(categoria, hospedaje) {
        const estandares = hospedaje.estandares || {};
        const cumplidos = Object.values(estandares).filter(e => e?.toLowerCase() === 'si').length;
        const total = Object.keys(estandares).length || 5;

        if (categoria >= 4) return 'Cumple Estándar';
        if (categoria >= 3 || cumplidos >= 3) return 'Parcialmente Cumple';
        return 'No Cumple';
    }

    /**
     * Obtiene una recomendación de mejoras basada en la evaluación
     */
    obtenerRecomendaciones(hospedaje) {
        const estandares = hospedaje.estandares || {};
        const recomendaciones = [];

        if (estandares.habitaciones?.toLowerCase() !== 'si') {
            recomendaciones.push({
                prioridad: 'ALTA',
                criterio: 'Habitaciones',
                descripcion: 'Ajustar a máximo 2 camas por habitación y garantizar baño privado',
                estimacion: '45 días'
            });
        }

        if (estandares.wifi?.toLowerCase() !== 'si') {
            recomendaciones.push({
                prioridad: 'MEDIA',
                criterio: 'WiFi',
                descripcion: 'Instalar WiFi de buena cobertura en todas las habitaciones',
                estimacion: '14 días'
            });
        }

        if (estandares.climatización?.toLowerCase() !== 'si') {
            recomendaciones.push({
                prioridad: 'ALTA',
                criterio: 'Climatización',
                descripcion: 'Instalar sistemas de aire acondicionado en habitaciones',
                estimacion: '30 días'
            });
        }

        const servicios = hospedaje.servicios || [];
        const serviciosAlimentacion = servicios.filter(s => 
            s.toLowerCase().includes('desayuno') || 
            s.toLowerCase().includes('cena') ||
            s.toLowerCase().includes('colacion')
        );

        if (serviciosAlimentacion.length < 2) {
            recomendaciones.push({
                prioridad: 'MEDIA',
                criterio: 'Alimentación',
                descripcion: 'Ofrecer al menos Desayuno y Cena diariamente',
                estimacion: '7 días'
            });
        }

        if (estandares.lavandería?.toLowerCase() !== 'si') {
            recomendaciones.push({
                prioridad: 'BAJA',
                criterio: 'Lavandería',
                descripcion: 'Establecer sistema de lavandería con proveedor local',
                estimacion: '14 días'
            });
        }

        return recomendaciones;
    }

    /**
     * Genera un reporte completo de categorización
     */
    generarReporte(hospedaje) {
        const evaluacion = this.evaluar(hospedaje);
        const recomendaciones = this.obtenerRecomendaciones(hospedaje);

        return {
            hospedaje: {
                id: hospedaje.id,
                nombre: hospedaje.nombre,
                direccion: hospedaje.direccion,
                encargado: hospedaje.encargado
            },
            evaluacion: {
                puntuacion: evaluacion.puntuacion,
                categoria: evaluacion.categoria,
                estado: evaluacion.estado,
                detalles: evaluacion.detalles
            },
            recomendaciones: recomendaciones,
            resumen: this.generarResumen(evaluacion, recomendaciones),
            fechaEvaluacion: new Date().toLocaleDateString('es-CL')
        };
    }

    /**
     * Genera un resumen textual de la evaluación
     */
    generarResumen(evaluacion, recomendaciones) {
        const estrella = '⭐'.repeat(evaluacion.categoria);
        const criticas = recomendaciones.filter(r => r.prioridad === 'ALTA');
        
        let resumen = `${estrella} - ${evaluacion.estado}. `;
        
        if (criticas.length > 0) {
            resumen += `Requiere ${criticas.length} mejora(s) crítica(s).`;
        } else if (recomendaciones.length > 0) {
            resumen += `Tiene ${recomendaciones.length} área(s) de mejora.`;
        } else {
            resumen += 'Cumple con todos los estándares.';
        }

        return resumen;
    }
}

// ========== EJEMPLO DE USO ==========

// Datos de prueba
const hospedajePrueba = {
    id: 1,
    nombre: "Aris Alojamiento",
    direccion: "Colón #34",
    encargado: "Juan Pérez",
    camas_instaladas: 12,
    precio_promedio: 45000,
    servicios: ["WiFi", "TV", "Desayuno", "AC"],
    estandares: {
        habitaciones: "SI",
        wifi: "SI",
        televisión: "SI",
        climatización: "SI",
        alimentación: "PARCIAL",
        lavandería: "NO"
    }
};

// Crear categorizador
const categorizador = new CategorizadorHospedajes();

// Evaluar hospedaje
const reporte = categorizador.generarReporte(hospedajePrueba);

console.log("========== REPORTE DE CATEGORIZACIÓN ==========");
console.log(JSON.stringify(reporte, null, 2));

// Exportar para uso en otros scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CategorizadorHospedajes;
}
