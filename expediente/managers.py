from django.db import models
from django.db.models import Count, Q
from django.utils.timezone import make_aware, datetime

class ExpedienteManager(models.Manager):
    
    def activos(self):
        """Devuelve los expedientes activos (estado=True)."""
        return self.filter(estado=True)

    def por_fecha_creacion(self, fecha):
        """
        Devuelve expedientes creados en una fecha específica.
        Acepta objetos date o string en formato YYYY-MM-DD.
        """
        if isinstance(fecha, str):
            try:
                fecha = datetime.strptime(fecha, "%Y-%m-%d").date()
            except ValueError:
                return self.none()
        return self.filter(fecha_creacion__date=fecha)

    def por_usuario(self, usuario):
        """
        Devuelve expedientes creados por un usuario.
        Acepta objeto User o string (username).
        """
        if hasattr(usuario, "pk"):  # si es un objeto User
            return self.filter(user=usuario)
        else:  # si es un nombre de usuario
            return self.filter(user__username=usuario)
        

    def fecha_rango(self, desde, hasta):
        """
        Devuelve expedientes creados entre dos fechas (inclusive).
        Acepta strings 'YYYY-MM-DD' o objetos date/datetime.
        """
        from datetime import datetime

        # Convertir strings a fechas si hace falta
        if isinstance(desde, str):
            desde = datetime.strptime(desde, "%Y-%m-%d").date()
        if isinstance(hasta, str):
            hasta = datetime.strptime(hasta, "%Y-%m-%d").date()

        return self.filter(fecha_creacion__range=(desde, hasta))

    def cantidad_expedientes(self):
        """Devuelve la cantidad total de expedientes."""
        return self.count()
    
    def estadisticas_por_sede(self, sede):
        """
        Devuelve expedientes asociados a una sede específica.
        Acepta objeto Sede o string (nombre de la sede).
        """
        if hasattr(sede, "pk"):  # si es un objeto Sede
            return self.filter(sede=sede).aggregate(Count('id'))
        
    def con_relaciones(self):
        """
        Devuelve expedientes con personas e instituciones
        correctamente prefetcheadas para listados/reportes.
        """
        return (
            self.get_queryset()
            .prefetch_related(
                'expedientepersona_expediente__persona',
                'expedientepersona_expediente__rol',
                'expedienteinstitucion_expediente__institucion',
                'expedienteinstitucion_expediente__rol',
            )
        )
    
    def resumen_por_intervencion(
        self,
        fecha_desde=None,
        fecha_hasta=None,
        medio_ingreso_id=None,
        grupo_etario_id=None
    ):
        filtros = Q(estado=True)

        if fecha_desde and fecha_hasta:
            filtros &= Q(fecha_creacion__range=(fecha_desde, fecha_hasta))

        if medio_ingreso_id:
            filtros &= Q(medio_ingreso_id=medio_ingreso_id)

        if grupo_etario_id:
            filtros &= Q(grupo_etario_id=grupo_etario_id)

        queryset = (
            self.get_queryset()
            .filter(filtros)
            .values(
                'resumen_intervencion__id',
                'resumen_intervencion__resumen_intervencion'  # ajustar si el campo se llama distinto
            )
            .annotate(total=Count('id'))
            .order_by('resumen_intervencion__resumen_intervencion')
        )

        total_general = self.get_queryset().filter(filtros).count()

        return {
            "total_general": total_general,
            "detalle": queryset
        }