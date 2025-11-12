from django.contrib import admin

# Register your models here.
from .models import (
    SituacionLaboralPrincipal, OpcionSINO, EstadoCupoLaboral, 
    TipoAcompanamientoLaboral, NivelEndeudamiento, AcompanamientoLaboral
)

# ------------------ Registro de Opciones Laborales ------------------

@admin.register(SituacionLaboralPrincipal)
class SituacionLaboralPrincipalAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')

@admin.register(OpcionSINO)
class OpcionSINOAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')

@admin.register(EstadoCupoLaboral)
class EstadoCupoLaboralAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')

@admin.register(TipoAcompanamientoLaboral)
class TipoAcompanamientoLaboralAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')

@admin.register(NivelEndeudamiento)
class NivelEndeudamientoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')

# ------------------ Registro del Modelo Laboral Principal ------------------

@admin.register(AcompanamientoLaboral)
class AcompanamientoLaboralAdmin(admin.ModelAdmin):
    list_display = (
        'persona_link', 
        'situacion_laboral_principal', 
        'ingreso_economico_promedio', 
        'nivel_endeudamiento'
    )
    search_fields = (
        'persona__nombre_autopercebido', 
        'dependencia_economica',
        'acceso_a_prestaciones'
    )
    autocomplete_fields = ['persona']
    filter_horizontal = ('tipo_acompanamiento_laboral',) # Para el ManyToMany
    list_filter = ('situacion_laboral_principal', 'nivel_endeudamiento')

    # Campo de solo lectura para mostrar el nombre de la persona en la lista
    def persona_link(self, obj):
        return obj.persona.nombre_autopercebido
    persona_link.short_description = "Persona"

    fieldsets = (
        ('I. Situación Laboral y Económica', {
            'fields': (
                'persona',
                'situacion_laboral_principal',
                ('ingreso_economico_promedio', 'antiguedad_laboral_meses'),
            ),
        }),
        ('II. Búsqueda de Empleo y Acompañamiento', {
            'fields': (
                ('interes_empleo_formal', 'posee_cv'),
                'acompanamiento_cupo_laboral',
                'tipo_acompanamiento_laboral',
                'acceso_a_prestaciones',
            ),
        }),
        ('III. Gestión Financiera', {
            'fields': (
                'nivel_endeudamiento',
                'dependencia_economica',
            ),
        }),
    )