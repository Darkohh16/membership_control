from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal

from payments.models import Pago
from payments.constants import METODOS_PAGO, ESTADOS_PAGO
from payments.helpers import validar_monto, calcular_descuento


User = get_user_model()


# Create your tests here.
class PagoModelTest(TestCase):
    """
    Tests para el modelo Pago.
    """
    
    def setUp(self):
        """
        Configuración inicial para los tests.
        """
        self.usuario = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            perfil=2
        )
        
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='adminpass123',
            first_name='Admin',
            last_name='User',
            perfil=1
        )
    
    def test_crear_pago(self):
        """
        Test para crear un pago correctamente.
        """
        pago = Pago.objects.create(
            usuario=self.usuario,
            monto=Decimal('100.00'),
            metodo_pago=METODOS_PAGO['Efectivo'],
            estado=ESTADOS_PAGO['Completado'],
            registrado_por=self.admin
        )
        
        self.assertIsNotNone(pago.numero_recibo)
        self.assertEqual(pago.usuario, self.usuario)
        self.assertEqual(pago.monto, Decimal('100.00'))
    
    def test_numero_recibo_unico(self):
        """
        Test para verificar que el número de recibo se genera automáticamente.
        """
        pago = Pago.objects.create(
            usuario=self.usuario,
            monto=Decimal('50.00'),
            metodo_pago=METODOS_PAGO['Tarjeta de Crédito']
        )
        
        self.assertTrue(pago.numero_recibo.startswith('REC-'))
    
    def test_validar_monto(self):
        """
        Test para la función de validación de monto.
        """
        self.assertTrue(validar_monto(100))
        self.assertFalse(validar_monto(0))
        self.assertFalse(validar_monto(-50))
    
    def test_calcular_descuento(self):
        """
        Test para la función de cálculo de descuento.
        """
        monto = 100
        descuento_10 = calcular_descuento(monto, 10)
        self.assertEqual(descuento_10, 90)
        
        sin_descuento = calcular_descuento(monto, 0)
        self.assertEqual(sin_descuento, 100)


class PagoManagerTest(TestCase):
    """
    Tests para el PagoManager.
    """
    
    def setUp(self):
        """
        Configuración inicial para los tests.
        """
        self.usuario = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            perfil=2
        )
        
        # Crear varios pagos de prueba
        Pago.objects.create(
            usuario=self.usuario,
            monto=Decimal('100.00'),
            metodo_pago=METODOS_PAGO['Efectivo'],
            estado=ESTADOS_PAGO['Completado']
        )
        
        Pago.objects.create(
            usuario=self.usuario,
            monto=Decimal('200.00'),
            metodo_pago=METODOS_PAGO['Tarjeta de Crédito'],
            estado=ESTADOS_PAGO['Completado']
        )
        
        Pago.objects.create(
            usuario=self.usuario,
            monto=Decimal('150.00'),
            metodo_pago=METODOS_PAGO['Efectivo'],
            estado=ESTADOS_PAGO['Pendiente']
        )
    
    def test_pagos_completados(self):
        """
        Test para obtener solo pagos completados.
        """
        pagos = Pago.objects.pagos_completados()
        self.assertEqual(pagos.count(), 2)
    
    def test_pagos_pendientes(self):
        """
        Test para obtener solo pagos pendientes.
        """
        pagos = Pago.objects.pagos_pendientes()
        self.assertEqual(pagos.count(), 1)
    
    def test_total_recaudado(self):
        """
        Test para calcular el total recaudado.
        """
        total = Pago.objects.total_recaudado()
        self.assertEqual(total, Decimal('300.00'))  # Solo suma los completados
