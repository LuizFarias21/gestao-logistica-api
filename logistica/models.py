from django.db import models

class Entrega(models.Model):
    motorista = models.ForeignKey(
        'frota.Motorista',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    destino = models.CharField(max_length=255)  
    status = models.CharField(max_length=30)
