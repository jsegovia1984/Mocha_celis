from django.db import models

# Create your models here.
from django.db import models
# Importamos Persona desde la otra app, ya definida
from datos_personales.models import Persona 



# Modelo que está causando el error
class TipoAcompanamiento(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Tipo de Acompañamiento")

    class Meta:
        verbose_name = "Tipo de Acompañamiento"
        verbose_name_plural = "Tipos de Acompañamiento"

    def __str__(self):
        return self.nombre
# =========================================================
# I. Modelos para las Opciones de Educación (Lookup Tables)
# =========================================================

class NivelEscolaridad(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nivel de Escolaridad")

    class Meta:
        verbose_name = "Nivel de Escolaridad"
        verbose_name_plural = "Niveles de Escolaridad"

    def __str__(self):
        return self.nombre

class EstadoBachilleratoMocha(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Estado en Bachillerato Mocha Celis")

    class Meta:
        verbose_name = "Estado Bachillerato Mocha Celis"
        verbose_name_plural = "Estados Bachillerato Mocha Celis"

    def __str__(self):
        return self.nombre

class BarreraEducativa(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Barrera Educativa")

    class Meta:
        verbose_name = "Barrera Educativa"
        verbose_name_plural = "Barreras Educativas"

    def __str__(self):
        return self.nombre

class EstadoCurso(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Estado del Curso/Capacitación")

    class Meta:
        verbose_name = "Estado del Curso"
        verbose_name_plural = "Estados del Curso"

    def __str__(self):
        return self.nombre

# =========================================================
# II. Modelo Específico de Acompañamiento: Educación
# =========================================================

class AcompanamientoEducacion(models.Model):
    """
    Modelo que registra el estado educativo y la formación profesional de la persona.
    """
    # RELACIÓN PRINCIPAL
    persona = models.OneToOneField(
        Persona,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name="Persona Acompañada",
        help_text="Un registro de educación por cada persona."
    )

    # ------------------ Escolaridad Formal ------------------

    nivel_escolaridad_maximo = models.ForeignKey(
        NivelEscolaridad,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name="Nivel Máximo Finalizado",
    )

    estado_bachillerato_mocha = models.ForeignKey(
        EstadoBachilleratoMocha,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name="Estado en el Bachillerato Mocha Celis",
        help_text="Mide la participación interna."
    )

    # RELACIÓN MUCHOS A MUCHOS para Barreras
    barreras_educativas = models.ManyToManyField(
        BarreraEducativa,
        blank=True,
        verbose_name="Barreras Educativas identificadas",
        help_text="Identifica obstáculos que impiden la finalización (Selección múltiple)."
    )

    # ------------------ Cursos y Capacitaciones ------------------

    nombre_curso_actual = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Nombre del Curso/Capacitación Actual",
        help_text="Ej: Panadería, Oficios Digitales, Asistente Administrativo."
    )

    institucion_curso = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Institución que dicta el curso",
        help_text="Permite registrar formaciones externas."
    )

    fecha_inicio_curso = models.DateField(
        blank=True,
        null=True,
        verbose_name="Fecha de Inicio del Curso"
    )

    estado_curso = models.ForeignKey(
        EstadoCurso,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name="Estado del Curso",
        help_text="Mide el éxito en la finalización."
    )
    
    # ------------------ Planificación Futura ------------------

    areas_interes_futuro = models.TextField(
        blank=True,
        verbose_name="Áreas de Interés Futuro",
        help_text="Para planificación de oferta formativa."
    )


    class Meta:
        verbose_name = "Acompañamiento - Educación"
        verbose_name_plural = "Acompañamiento - Educación y Formación"

    def __str__(self):
        return f"Educación de {self.persona.nombre_autopercebido}"