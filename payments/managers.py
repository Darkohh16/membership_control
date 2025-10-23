from django.db import models


class PagoManager(models.Manager):
    """
    Manager personalizado para el modelo Pago.
    Funciones básicas para gestión de pagos.
    """
    
    def pagos_completados(self):
        """
        Obtiene todos los pagos con estado completado.
        """
        return self.filter(estado=2)  # 2 = Completado
    
    def pagos_pendientes(self):
        """
        Obtiene todos los pagos con estado pendiente.
        """
        return self.filter(estado=1)  # 1 = Pendiente
