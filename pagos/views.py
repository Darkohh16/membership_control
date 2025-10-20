from django.shortcuts import render, get_object_or_404
from .models import Socio, Pago

def historial_pagos(request, socio_id):
    socio = get_object_or_404(Socio, id=socio_id)
    pagos = socio.pagos.all().order_by('-fecha_pago')
    return render(request, 'pagos/historial_pagos.html', {
        'socio': socio,
        'pagos': pagos,
    })

