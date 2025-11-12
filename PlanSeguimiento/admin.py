from django.contrib import admin
from .models import (
    TipoIntervencion, NivelRiesgo, MotivoCierre, 
    PlanIntervencion, RegistroSeguimiento
)

# ------------------ Inline para los Registros de Seguimiento ------------------

class RegistroSeguimientoInline(admin.TabularInline):
    model = RegistroSeguimiento
    extra = 1 
    fields = (
        'fecha_contacto', 
        'tipo_intervencion', 
        'resumen_avances_obstaculos', 
        'nivel_riesgo_actual'
    )
    autocomplete_fields = ['tipo_intervencion', 'nivel_riesgo_actual'] 
    ordering = ('-fecha_contacto',)


# ------------------ Registro de Opciones (Solución E040) ------------------

@admin.register(TipoIntervencion)
class TipoIntervencionAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',) # CORREGIDO

@admin.register(NivelRiesgo)
class NivelRiesgoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',) # CORREGIDO

@admin.register(MotivoCierre)
class MotivoCierreAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)


# ------------------ Registro del Modelo Plan de Intervención ------------------

@admin.register(PlanIntervencion)
class PlanIntervencionAdmin(admin.ModelAdmin):
    list_display = ('persona_link', 'objetivo_general_caso_extracto', 'fecha_cierre', 'motivo_cierre')
    search_fields = ('persona__nombre_autopercebido', 'objetivo_general_caso')
    autocomplete_fields = ['persona', 'motivo_cierre']
    inlines = [RegistroSeguimientoInline] 

    def persona_link(self, obj):
        return obj.persona.nombre_autopercebido
    persona_link.short_description = "Persona"
    
    def objetivo_general_caso_extracto(self, obj):
        return f"{obj.objetivo_general_caso[:50]}..."
    objetivo_general_caso_extracto.short_description = "Objetivo General"

    fieldsets = (
        ('I. Planificación y Objetivo General', {
            'fields': (
                'persona',
                'objetivo_general_caso',
            ),
        }),
        ('II. Cierre de Caso', {
            'fields': (
                ('fecha_cierre', 'motivo_cierre'),
                'evaluacion_final_resultados',
            ),
        }),
    )

# ------------------ Registro Individual de Seguimiento (Solución E037) ------------------

@admin.register(RegistroSeguimiento)
class RegistroSeguimientoAdmin(admin.ModelAdmin):
    list_display = ('fecha_contacto', 'plan_intervencion', 'tipo_intervencion', 'nivel_riesgo_actual')
    search_fields = ('plan_intervencion__persona__nombre_autopercebido', 'resumen_avances_obstaculos')
    list_filter = ('tipo_intervencion', 'nivel_riesgo_actual', 'fecha_contacto')
    
    # CORRECCIÓN E037: Usamos plan_intervencion en lugar de la persona eliminada.
    autocomplete_fields = ['plan_intervencion', 'tipo_intervencion', 'nivel_riesgo_actual']