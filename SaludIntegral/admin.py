from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import (
    EstadoSalud, AccesoSistema, TipoTerapia, BarreraSalud, 
    AcompanamientoSalud
)

# ------------------ Registro de Opciones de Salud ------------------

@admin.register(EstadoSalud)
class EstadoSaludAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')

@admin.register(AccesoSistema)
class AccesoSistemaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')

@admin.register(TipoTerapia)
class TipoTerapiaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')

@admin.register(BarreraSalud)
class BarreraSaludAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')

# ------------------ Registro del Modelo Salud Principal ------------------

@admin.register(AcompanamientoSalud)
class AcompanamientoSaludAdmin(admin.ModelAdmin):
    list_display = (
        'persona_link', 
        'estado_salud_general', 
        'acceso_sistema_salud', 
        'requiere_terapia'
    )
    search_fields = (
        'persona__nombre_autopercebido', 
        'medicacion_cronica',
        'consumo_sustancias'
    )
    autocomplete_fields = ['persona']
    filter_horizontal = ('barreras_salud',)
    list_filter = ('estado_salud_general', 'acceso_sistema_salud', 'requiere_terapia')

    # Campo de solo lectura para mostrar el nombre de la persona en la lista
    def persona_link(self, obj):
        return obj.persona.nombre_autopercebido
    persona_link.short_description = "Persona"

    fieldsets = (
        ('I. Salud General y Acceso', {
            'fields': (
                'persona',
                ('estado_salud_general', 'acceso_sistema_salud'),
                'medicacion_cronica',
            ),
        }),
        ('II. Bienestar Psicosocial', {
            'fields': (
                ('requiere_terapia', 'tipo_terapia_actual'),
                'consumo_sustancias',
                'barreras_salud',
                'notas_bienestar',
            ),
        }),
    )