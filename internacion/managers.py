from django.db import models
from django.db.models import Count, Q
from django.utils.timezone import make_aware, datetime

class InternacionManager(models.Manager):
    
    def por_fecha_internacion(self, fecha):
        """
        Devuelve internaciones realizadas en una fecha específica.
        Acepta objetos date o string en formato YYYY-MM-DD.
        """
        if isinstance(fecha, str):
            try:
                fecha = datetime.strptime(fecha, "%Y-%m-%d").date()
            except ValueError:
                return self.none()
        return self.filter(fecha_internacion__date=fecha)

    def por_usuario(self, usuario):
        """
        Devuelve internaciones realizadas por un usuario.
        Acepta objeto User o string (username).
        """
        if hasattr(usuario, "pk"):  # si es un objeto User
            return self.filter(usuario=usuario)
        else:  # si es un nombre de usuario
            return self.filter(usuario__username=usuario)
        

    def fecha_rango(self, desde, hasta):
        """
        Devuelve internaciones realizadas entre dos fechas (inclusive).
        Acepta strings 'YYYY-MM-DD' o objetos date/datetime.
        """
        from datetime import datetime

        # Convertir strings a fechas si hace falta
        if isinstance(desde, str):
            desde = datetime.strptime(desde, "%Y-%m-%d").date()
        if isinstance(hasta, str):
            hasta = datetime.strptime(hasta, "%Y-%m-%d").date()

        return self.filter(fecha_internacion__range=(desde, hasta))

    def cantidad_internaciones(self):
        """Devuelve la cantidad total de internaciones."""
        return self.count()
    

    def internacion_motivo_internacion(
        self,
        fecha_desde=None,
        fecha_hasta=None,
        tipo_internacion_id=None,
        grupo_etario_id=None,
        sede_id=None,
    ):
        filtros = Q(estado=True)

        if fecha_desde and fecha_hasta:
            # OJO: en el modelo aparece fecha_internacion / fecha_alta.
            # Usá el campo correcto (acá dejo fecha_internacion como ejemplo).
            filtros &= Q(fecha_internacion__range=(fecha_desde, fecha_hasta))

        if tipo_internacion_id:
            filtros &= Q(tipo_internacion_id=tipo_internacion_id)

        # grupo_etario está en Expediente (relación vía expediente_institucion -> expediente)
        if grupo_etario_id:
            filtros &= Q(expediente_institucion__expediente__grupo_etario_id=grupo_etario_id)

        # sede está en Expediente (según tu comentario)
        if sede_id:
            filtros &= Q(expediente_institucion__expediente__sede_id=sede_id)

        qs = (
            self.get_queryset()
            .filter(filtros)
            .values("motivo_internacion__id", "motivo_internacion__motivo_internacion")
            .annotate(total=Count("id"))
            .order_by("motivo_internacion__motivo_internacion")
        )

        total_general = self.get_queryset().filter(filtros).count()

        return {"total_general": total_general, "detalle": qs}