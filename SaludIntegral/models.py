from django.db import models

# Create your models here.
from django.db import models
# Importamos Persona desde la otra app, ya definida
from datos_personales.models import Persona 

# =========================================================
# I. Modelos para las Opciones de Salud
# =========================================================

class EstadoSalud(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Estado de Salud (Percibido)")

    class Meta:
        verbose_name = "Estado de Salud"
        verbose_name_plural = "Estados de Salud"

    def __str__(self):
        return self.nombre

class AccesoSistema(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Acceso al Sistema de Salud")

    class Meta:
        verbose_name = "Acceso a Sistema de Salud"
        verbose_name_plural = "Accesos a Sistema de Salud"

    def __str__(self):
        return self.nombre

class TipoTerapia(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Tipo de Acompañamiento Terapéutico")

    class Meta:
        verbose_name = "Tipo de Terapia"
        verbose_name_plural = "Tipos de Terapia"

    def __str__(self):
        return self.nombre

class BarreraSalud(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Barrera Sanitaria o Psicosocial")

    class Meta:
        verbose_name = "Barrera de Salud"
        verbose_name_plural = "Barreras de Salud"

    def __str__(self):
        return self.nombre

# =========================================================
# II. Modelo Principal del Eje Salud Integral
# =========================================================

class AcompanamientoSalud(models.Model):
    """
    Modelo que registra el estado de salud integral y bienestar psicosocial de la persona.
    """
    # RELACIÓN PRINCIPAL (Una persona tiene un solo registro de salud)
    persona = models.OneToOneField(
        Persona,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name="Persona Acompañada",
    )

    # ------------------ Salud General y Acceso ------------------

    estado_salud_general = models.ForeignKey(
        EstadoSalud,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name="Estado de Salud General (Percibido)",
    )

    acceso_sistema_salud = models.ForeignKey(
        AccesoSistema,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name="Acceso al Sistema de Salud",
        help_text="Ej: Público, Privado, Obras Sociales."
    )

    medicacion_cronica = models.TextField(
        blank=True,
        verbose_name="Medicación Crónica Actual",
        help_text="Listar medicamentos, dosis y diagnóstico asociado."
    )
    
    # ------------------ Bienestar Psicosocial ------------------

    requiere_terapia = models.BooleanField(
        default=False,
        verbose_name="Requiere Acompañamiento Psicológico/Psiquiátrico"
    )

    tipo_terapia_actual = models.ForeignKey(
        TipoTerapia,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name="Tipo de Terapia Actual (si aplica)",
    )
    
    consumo_sustancias = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Consumo de Sustancias/Tóxicos",
        help_text="Especificar tipo y frecuencia si la respuesta es Sí."
    )

    # ------------------ Barreras ------------------

    # Relación Muchos a Muchos para Barreras de Salud
    barreras_salud = models.ManyToManyField(
        BarreraSalud,
        blank=True,
        verbose_name="Barreras Sanitarias y Psicosociales",
        help_text="Identifica obstáculos para el acceso (Ej: Discriminación en consultorio, Falta de insumos)."
    )
    
    notas_bienestar = models.TextField(
        blank=True,
        verbose_name="Notas de Bienestar Psicosocial",
        help_text="Observaciones, red de apoyo, situaciones de crisis."
    )

    class Meta:
        verbose_name = "Acompañamiento - Salud"
        verbose_name_plural = "Acompañamiento - Salud Integral y Bienestar"

    def __str__(self):
        return f"Salud de {self.persona.nombre_autopercebido}"