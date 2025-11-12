from django.contrib import admin

# Register your models here.
# Acompanamiento/admin.py (Agregar las nuevas clases)

from django.contrib import admin

from .models import (
    TipoAcompanamiento, # <--- ¡Estos deben existir y estar bien escritos!
    NivelEscolaridad, EstadoBachilleratoMocha, BarreraEducativa, 
    EstadoCurso, AcompanamientoEducacion 
)


# ... (El registro de los modelos anteriores sigue aquí) ...

# ------------------ Registro de Nuevas Opciones de Educación ------------------

@admin.register(NivelEscolaridad)
class NivelEscolaridadAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')

@admin.register(EstadoBachilleratoMocha)
class EstadoBachilleratoMochaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')

@admin.register(BarreraEducativa)
class BarreraEducativaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')

@admin.register(EstadoCurso)
class EstadoCursoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')

# ------------------ Registro del Modelo de Educación ------------------

@admin.register(AcompanamientoEducacion)
class AcompanamientoEducacionAdmin(admin.ModelAdmin):
    list_display = (
        'persona_link', 
        'nivel_escolaridad_maximo', 
        'estado_bachillerato_mocha',
        'nombre_curso_actual',
    )
    search_fields = (
        'persona__nombre_autopercebido', 
        'nombre_curso_actual', 
        'institucion_curso'
    )
    autocomplete_fields = ['persona']
    filter_horizontal = ('barreras_educativas',) # Para el ManyToMany

    # Campo de solo lectura para mostrar el nombre de la persona en la lista
    def persona_link(self, obj):
        return obj.persona.nombre_autopercebido
    persona_link.short_description = "Persona"

    fieldsets = (
        ('I. Escolaridad Formal', {
            'fields': (
                'persona',
                'nivel_escolaridad_maximo',
                'estado_bachillerato_mocha',
                'barreras_educativas',
            ),
        }),
        ('II. Cursos y Capacitaciones', {
            'fields': (
                ('nombre_curso_actual', 'institucion_curso'),
                ('fecha_inicio_curso', 'estado_curso'),
            ),
        }),
        ('III. Planificación', {
            'fields': (
                'areas_interes_futuro',
            ),
        }),
    )