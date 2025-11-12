from django.db import models

# Create your models here.
from django.db import models
from datos_personales.models import Persona
from django.core.validators import MinValueValidator

# =========================================================
# I. Modelos para las Opciones de Inserción Laboral
# =========================================================

class SituacionLaboralPrincipal(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Situación Laboral Principal")

    class Meta:
        verbose_name = "Situación Laboral Principal"
        verbose_name_plural = "Situaciones Laborales Principales"

    def __str__(self):
        return self.nombre

class OpcionSINO(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Opción Sí/No/Temporalmente No")

    class Meta:
        verbose_name = "Opción Sí/No"
        verbose_name_plural = "Opciones Sí/No"

    def __str__(self):
        return self.nombre

class EstadoCupoLaboral(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Estado Acompañamiento Cupo Laboral")

    class Meta:
        verbose_name = "Estado Cupo Laboral"
        verbose_name_plural = "Estados Cupo Laboral"

    def __str__(self):
        return self.nombre

class TipoAcompanamientoLaboral(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Tipo de Acompañamiento Laboral")

    class Meta:
        verbose_name = "Tipo de Acompañamiento Laboral"
        verbose_name_plural = "Tipos de Acompañamiento Laboral"

    def __str__(self):
        return self.nombre

class NivelEndeudamiento(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Nivel de Endeudamiento")

    class Meta:
        verbose_name = "Nivel de Endeudamiento"
        verbose_name_plural = "Niveles de Endeudamiento"

    def __str__(self):
        return self.nombre

# =========================================================
# II. Modelo Principal del Eje Laboral
# =========================================================

class AcompanamientoLaboral(models.Model):
    """
    Modelo que registra la Inserción Laboral y Autonomía Económica de la persona.
    """
    # RELACIÓN PRINCIPAL
    persona = models.OneToOneField(
        Persona,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name="Persona Acompañada",
        help_text="Un registro laboral por cada persona."
    )

    # ------------------ Situación Laboral ------------------

    situacion_laboral_principal = models.ForeignKey(
        SituacionLaboralPrincipal,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name="Situación Laboral Principal",
    )

    ingreso_economico_promedio = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Ingreso Económico Promedio Mensual ($)",
        validators=[MinValueValidator(0)],
    )

    antiguedad_laboral_meses = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Antigüedad en la Situación Laboral (Meses)",
        help_text="Mide la estabilidad de la fuente de ingresos.",
        validators=[MinValueValidator(0)],
    )

    # ------------------ Búsqueda de Empleo ------------------

    interes_empleo_formal = models.ForeignKey(
        OpcionSINO,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='interes_formal',
        verbose_name="Interés en Empleo Formal",
    )

    posee_cv = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="CV (Currículum Vitae)",
        help_text="Opciones (Sí/No, ¿De quién/Qué?)"
    )

    acompanamiento_cupo_laboral = models.ForeignKey(
        EstadoCupoLaboral,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name="Acompañamiento para Cupo Laboral",
        help_text="Seguimiento específico de la política pública."
    )

    tipo_acompanamiento_laboral = models.ManyToManyField(
        TipoAcompanamientoLaboral,
        blank=True,
        verbose_name="Tipo de Acompañamiento Laboral",
        help_text="Selección Múltiple (Armado de CV, Simulación de entrevista, etc.)",
    )

    acceso_a_prestaciones = models.TextField(
        blank=True,
        verbose_name="Acceso a Prestaciones/Ayudas",
        help_text="Listado (Ej: Potenciar Trabajo, Pensiones No Contributivas, otros subsidios)",
    )

    # ------------------ Deudas/Gestión ------------------

    nivel_endeudamiento = models.ForeignKey(
        NivelEndeudamiento,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name="Nivel de Endeudamiento",
    )

    dependencia_economica = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Dependencia Económica",
        help_text="Opciones (Sí/No, ¿De quién/Qué?). Mide el grado de autonomía."
    )

    class Meta:
        verbose_name = "Acompañamiento - Laboral y Economía"
        verbose_name_plural = "Acompañamiento - Inserción Laboral y Autonomía Económica"

    def __str__(self):
        return f"Laboral/Económico de {self.persona.nombre_autopercebido}"