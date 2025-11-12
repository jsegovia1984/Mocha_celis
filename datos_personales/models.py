from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import MinValueValidator



class nacionalidad(models.Model):

    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nacionalidad")

    class Meta:
        verbose_name = "Nacionalidad"
        verbose_name_plural = "Nacionalidades"

    def __str__(self):
        return self.nombre


# =========================================================
# I. Modelos para las Opciones (Tablas de Lookup/Choices)
# =========================================================

class IdentidadGenero(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Identidad de Género")
    
    class Meta:
        verbose_name = "Identidad de Género"
        verbose_name_plural = "Identidades de Género"

    def __str__(self):
        return self.nombre

class EstadoDNI(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Estado DNI Rectificado")
    
    class Meta:
        verbose_name = "Estado DNI"
        verbose_name_plural = "Estados DNI"

    def __str__(self):
        return self.nombre

class OpcionSINO(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Opciones (CUIT)")
    
    class Meta:
        verbose_name = "Opción"
        verbose_name_plural = "Opciones (CUIT)"

    def __str__(self):
        return self.nombre

class TipoVivienda(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Tipo de Vivienda")
    
    class Meta:
        verbose_name = "Tipo de Vivienda"
        verbose_name_plural = "Tipos de Vivienda"

    def __str__(self):
        return self.nombre

class TenenciaVivienda(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Tenencia de la Vivienda")
    
    class Meta:
        verbose_name = "Tenencia de Vivienda"
        verbose_name_plural = "Tenencias de Vivienda"

    def __str__(self):
        return self.nombre

class RiesgoResidencial(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Nivel de Riesgo Residencial")
    
    class Meta:
        verbose_name = "Riesgo Residencial"
        verbose_name_plural = "Riesgos Residenciales"

    def __str__(self):
        return self.nombre

class ViaIngreso(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Vía de Ingreso del Caso")
    
    class Meta:
        verbose_name = "Vía de Ingreso"
        verbose_name_plural = "Vías de Ingreso"

    def __str__(self):
        return self.nombre

# =========================================================
# II. Modelo Principal de la Persona (Relaciona con I)
# =========================================================

class Persona(models.Model):
    """
    Modelo para gestionar la información de una persona, con campos de lookup relacionales.
    """

    # ------------------ Datos Personales ------------------

    nombre_autopercebido = models.CharField(
        max_length=255,
        verbose_name="Nombre Autopercebido",
        help_text="Campo prioritario y obligatorio."
    )

    iniciales_dni = models.CharField(
        max_length=100,
        null=True, blank=True,
        verbose_name="Iniciales (DNI/Partida)",
        help_text="Para trámites administrativos y archivo (si no tiene cambio registral)."
    )

    documento_identidad = models.CharField(
        max_length=50,
        unique=True,
        null=True, blank=True,
        verbose_name="Documento de Identidad (DNI/Pasaporte)",
    )

    # RELACIÓN: Identidad de Género (ForeignKey)
    identidad_genero = models.ForeignKey(
        IdentidadGenero,
        on_delete=models.SET_NULL, # Mantiene la persona si se elimina la opción
        null=True, blank=True,
        verbose_name="Identidad de Género",
    )

    fecha_nacimiento = models.DateField(
        null=True, blank=True,
        verbose_name="Fecha de Nacimiento",
    )

    edad = models.PositiveIntegerField(
        null=True, blank=True,
        verbose_name="Edad",
        validators=[MinValueValidator(0)]
    )

    nacionalidad = models.ForeignKey(
        nacionalidad,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name="Nacionalidad",
    )
    # ------------------ Documentación ------------------

    # RELACIÓN: Estado DNI Rectificado (ForeignKey)
    estado_dni_rectificado = models.ForeignKey(
        EstadoDNI,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name="Estado del DNI rectificado",
        help_text="Mide el acceso al derecho a la identidad."
    )

    # RELACIÓN: Posee CUIT/CUIL (ForeignKey - Usamos OpcionSINO)
    posee_cuit_cuil = models.ForeignKey(
        OpcionSINO,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='personas_cuit_cuil', # Se necesita un related_name para diferenciarlo de posee_cuit_cuil
        verbose_name="Posee CUIT/CUIL",
        help_text="Necesario para empleo y prestaciones sociales."
    )

    # ------------------ Contacto y Residencia ------------------

    direccion_actual_completa = models.TextField( # Usar TextField para direcciones largas
        null=True, blank=True,
        verbose_name="Dirección Actual Completa",
    )

    # RELACIÓN: Tipo de Vivienda (ForeignKey)
    tipo_vivienda = models.ForeignKey(
        TipoVivienda,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name="Tipo de Vivienda",
        help_text="Detallar formas de residencia precaria."
    )

    # RELACIÓN: Tenencia de la Vivienda (ForeignKey)
    tenencia = models.ForeignKey(
        TenenciaVivienda,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name="Tenencia",
    )

    telefono = models.CharField(
        max_length=50,
        null=True, blank=True,
        verbose_name="Teléfono",
    )

    correo_electronico = models.EmailField(
        max_length=254,
        null=True, blank=True,
        verbose_name="Correo Electrónico",
    )

    # RELACIÓN: Riesgo Residencial (ForeignKey)
    riesgo_residencial = models.ForeignKey(
        RiesgoResidencial,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name="Riesgo Residencial",
    )

    # ------------------ Admisión al Caso ------------------

    fecha_inicio_caso = models.DateField(
        null=True, blank=True,
        verbose_name="Fecha de Inicio del Caso",
    )

    profesional_responsable = models.CharField(
        max_length=255,
        null=True, blank=True,
        verbose_name="Profesional Responsable",
        help_text="Nombre del equipo Mocha Celis"
    )

    # RELACIÓN: Vía de Ingreso (ForeignKey)
    via_ingreso = models.ForeignKey(
        ViaIngreso,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name="Vía de Ingreso",
    )

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"

    def __str__(self):
        return self.nombre_autopercebido


# datos_personales/models.py (Nueva adición)

# ... (El resto de tus modelos de lookup: IdentidadGenero, EstadoDNI, etc.) ...