from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import (
    IdentidadGenero, EstadoDNI, OpcionSINO, TipoVivienda, TenenciaVivienda,
    RiesgoResidencial, ViaIngreso, Persona,nacionalidad
)


# Personalizar los textos del sitio de administración
admin.site.site_header = 'ADMINISTRACIÓN MOCHA CELIS' # Encabezado principal
admin.site.site_title = 'Mocha Celis - Portal'        # Título de la pestaña (override)
admin.site.index_title = 'Ejes de Acompañamiento'     # Título en la página principal

# 1. Registro de Tablas de Opciones (Lookup Tables)
# Estas tablas son pequeñas y se gestionan bien con la configuración por defecto.

@admin.register(IdentidadGenero)
class IdentidadGeneroAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

@admin.register(EstadoDNI)
class EstadoDNIAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

@admin.register(OpcionSINO)
class OpcionSINOAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

@admin.register(TipoVivienda)
class TipoViviendaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

@admin.register(TenenciaVivienda)
class TenenciaViviendaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

@admin.register(RiesgoResidencial)
class RiesgoResidencialAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

@admin.register(ViaIngreso)
class ViaIngresoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)


@admin.register(nacionalidad)
class NacionalidadAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',) # Es vital para que la búsqueda/autocompletado funcione en el modelo Persona

# 2. Registro del Modelo Principal (Persona)
# Usamos fieldsets para agrupar los campos lógicamente.



@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = (
        'nombre_autopercebido', 
        'documento_identidad', 
        'identidad_genero', 
        'fecha_nacimiento', 
        'riesgo_residencial'
    )
    
    search_fields = ('nombre_autopercebido', 'documento_identidad', 'correo_electronico')
    
    list_filter = ('identidad_genero', 'estado_dni_rectificado', 'riesgo_residencial', 'via_ingreso')

    fieldsets = (
        ('I. Datos Personales', {
            'fields': (
                ('nombre_autopercebido', 'iniciales_dni'),
                ('documento_identidad', 'identidad_genero'),
                ('fecha_nacimiento', 'edad'),
                'nacionalidad',
            ),
        }),
        ('II. Documentación', {
            'fields': (
                ('estado_dni_rectificado', 'posee_cuit_cuil'),
            ),
        }),
        ('III. Contacto y Residencia', {
            'fields': (
                'direccion_actual_completa',
                ('tipo_vivienda', 'tenencia'),
                ('telefono', 'correo_electronico'),
                'riesgo_residencial',
            ),
        }),
        ('IV. Admisión al Caso', {
            'fields': (
                'fecha_inicio_caso',
                ('profesional_responsable', 'via_ingreso'),
            ),
        }),
    )