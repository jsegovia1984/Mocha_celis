from django.db import models
# Asegúrate de que 'datos_personales' está en INSTALLED_APPS
from datos_personales.models import Persona 

# =========================================================
# I. Modelos para las Opciones de Planificación y Cierre
# =========================================================

class TipoIntervencion(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Tipo de Intervención")

    class Meta:
        verbose_name = "Tipo de Intervención"
        verbose_name_plural = "Tipos de Intervención"

    def __str__(self):
        return self.nombre

class NivelRiesgo(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Nivel de Riesgo")

    class Meta:
        verbose_name = "Nivel de Riesgo"
        verbose_name_plural = "Niveles de Riesgo"

    def __str__(self):
        return self.nombre

class MotivoCierre(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Motivo de Cierre")

    class Meta:
        verbose_name = "Motivo de Cierre de Caso"
        verbose_name_plural = "Motivos de Cierre de Caso"

    def __str__(self):
        return self.nombre

# =========================================================
# II. Modelo Principal: Plan de Intervención (Registro 1:1)
# =========================================================

class PlanIntervencion(models.Model):
    """
    Define el objetivo general del caso y contiene la información del cierre.
    Relación 1:1 con Persona.
    """
    persona = models.OneToOneField(
        Persona,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name="Persona Acompañada",
    )
    
    # ------------------ Planificación ------------------

    objetivo_general_caso = models.TextField(
        verbose_name="Objetivo General del Caso (Meta a largo plazo)"
    )
    
    # ------------------ Cierre de Caso ------------------

    fecha_cierre = models.DateField(
        null=True, blank=True,
        verbose_name="Fecha de Cierre"
    )

    motivo_cierre = models.ForeignKey(
        MotivoCierre,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name="Motivo de Cierre"
    )

    evaluacion_final_resultados = models.TextField(
        blank=True,
        verbose_name="Evaluación Final de Resultados",
        help_text="Impacto de la intervención en la calidad de vida y derechos."
    )

    class Meta:
        verbose_name = "Plan de Intervención"
        verbose_name_plural = "Planes de Intervención y Cierre"

    def __str__(self):
        return f"Plan de {self.persona.nombre_autopercebido}"


# =========================================================
# III. Modelo de Seguimiento (Registro 1:N)
# =========================================================

class RegistroSeguimiento(models.Model):
    """
    Registra cada contacto o intervención realizada sobre un caso.
    Relación N:1 con PlanIntervencion (para usar como Inline).
    """
    # CORRECCIÓN CRÍTICA: Relación con el Plan, no con Persona
    plan_intervencion = models.ForeignKey(
        PlanIntervencion,
        on_delete=models.CASCADE,
        verbose_name="Plan de Intervención Asociado",
        related_name='registros_seguimiento'
    )

    fecha_contacto = models.DateField(
        verbose_name="Fecha del Contacto/Intervención"
    )

    tipo_intervencion = models.ForeignKey(
        TipoIntervencion,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name="Tipo de Intervención",
    )
    
    acciones_por_eje = models.TextField(
        blank=True,
        verbose_name="Acciones por Eje (Salud, Empleo, Documentación, Educación)",
        help_text="Listado de tareas y objetivos a corto/medio plazo.",
    )

    plazo_estimado_accion = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Plazo Estimado por Acción",
        help_text="Fecha o Indicación Temporal (Ej: 3 meses)."
    )

    resumen_avances_obstaculos = models.TextField(
        verbose_name="Resumen de Avances y Obstáculos",
        help_text="Registro narrativo breve y profesional."
    )

    nivel_riesgo_actual = models.ForeignKey(
        NivelRiesgo,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name="Nivel de Riesgo Actual del Caso",
    )

    derivaciones_realizadas = models.TextField(
        blank=True,
        verbose_name="Derivaciones Realizadas",
        help_text="Institución, Fecha y Contacto."
    )

    class Meta:
        verbose_name = "Registro de Seguimiento"
        verbose_name_plural = "Registros de Seguimiento"
        ordering = ['-fecha_contacto']

    def __str__(self):
        return f"Seguimiento {self.fecha_contacto} para {self.plan_intervencion.persona.nombre_autopercebido}"