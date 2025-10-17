from django.db import models
from django.db.models import Sum, Count
from datetime import datetime, timedelta


class PagoManager(models.Manager):
    """
    Manager personalizado para el modelo Pago.
    """
    
    def pagos_del_mes(self, mes=None, anio=None):
        """
        Obtiene todos los pagos de un mes específico.
        Si no se especifica mes/año, usa el mes actual.
        """
        if mes is None:
            mes = datetime.now().month
        if anio is None:
            anio = datetime.now().year
            
        return self.filter(
            fecha_pago__month=mes,
            fecha_pago__year=anio
        )
    
    def pagos_completados(self):
        """
        Obtiene todos los pagos completados.
        """
        return self.filter(estado=2)  # 2 = Completado
    
    def pagos_pendientes(self):
        """
        Obtiene todos los pagos pendientes.
        """
        return self.filter(estado=1)  # 1 = Pendiente
    
    def total_recaudado(self, fecha_inicio=None, fecha_fin=None):
        """
        Calcula el total recaudado en un período de tiempo.
        """
        queryset = self.pagos_completados()
        
        if fecha_inicio:
            queryset = queryset.filter(fecha_pago__gte=fecha_inicio)
        if fecha_fin:
            queryset = queryset.filter(fecha_pago__lte=fecha_fin)
            
        resultado = queryset.aggregate(total=Sum('monto'))
        return resultado['total'] or 0
    
    def pagos_por_metodo(self):
        """
        Agrupa los pagos por método de pago.
        """
        return self.pagos_completados().values('metodo_pago').annotate(
            cantidad=Count('id'),
            total=Sum('monto')
        )
