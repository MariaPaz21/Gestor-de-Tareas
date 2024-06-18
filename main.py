from models.tarea import Tarea, SessionLocal
import datetime
from datetime import date, timedelta
import csv
import argparse
from functools import wraps

def manejar_sesion(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session = SessionLocal()
        try:
            resultado = func(session, *args, **kwargs)
            session.commit()
            return resultado
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    return wrapper

# Funciones
@manejar_sesion
def agregar_tarea(session, descripcion, prioridad='media', fecha_vencimiento=None):
    nueva_tarea = Tarea(descripcion=descripcion, prioridad=prioridad, fecha_vencimiento=fecha_vencimiento)
    session.add(nueva_tarea)
    session.refresh(nueva_tarea)
    return nueva_tarea

@manejar_sesion
def completar_tarea(session, tarea_id):
    tarea = session.query(Tarea).get(tarea_id)
    if tarea:
        tarea.completada = True
        tarea.fecha_finalizacion = date.today()
        session.refresh(tarea)
    return tarea

@manejar_sesion
def eliminar_tarea(session, tarea_id):
    tarea = session.query(Tarea).get(tarea_id)
    if tarea:
        session.delete(tarea)
        return True
    return False

@manejar_sesion
def listar_tareas(session):
    return session.query(Tarea).all()

@manejar_sesion
def buscar_tareas(session, termino):
    return session.query(Tarea).filter(Tarea.descripcion.contains(termino)).all()

@manejar_sesion
def filtrar_tareas_por_prioridad(session, prioridad):
    return session.query(Tarea).filter(Tarea.prioridad == prioridad).all()

@manejar_sesion
def tareas_proximas_a_vencer(session, dias=7):
    fecha_limite = date.today() + timedelta(days=dias)
    return session.query(Tarea).filter(Tarea.fecha_vencimiento <= fecha_limite, Tarea.fecha_vencimiento >= date.today()).all()

@manejar_sesion
def exportar_tareas_a_csv(session, archivo_destino):
    tareas = session.query(Tarea).all()
    with open(archivo_destino, 'w', newline='') as csvfile:
        tarea_writer = csv.writer(csvfile)
        tarea_writer.writerow(['ID', 'Descripción', 'Completada', 'Fecha de Creación', 'Prioridad', 'Fecha de Vencimiento'])
        for tarea in tareas:
            tarea_writer.writerow([tarea.id, tarea.descripcion, tarea.completada, tarea.fecha_creacion, tarea.prioridad, tarea.fecha_vencimiento])

@manejar_sesion
def obtener_tareas_completadas(session, fecha_inicio=None, fecha_fin=None):
    query = session.query(Tarea).filter(Tarea.completada == True)
    if fecha_inicio:
        query = query.filter(Tarea.fecha_finalizacion >= fecha_inicio)
    if fecha_fin:
        query = query.filter(Tarea.fecha_finalizacion <= fecha_fin)
    return query.all()
# MAIN FN.
def main():
    parser = argparse.ArgumentParser(description="Gestor de Tareas")
    parser.add_argument('--agregar', type=str, help="Agregar una nueva tarea")
    parser.add_argument('--completar', type=int, help="Marcar una tarea como completada")
    parser.add_argument('--eliminar', type=int, help="Eliminar una tarea")
    parser.add_argument('--buscar', type=str, help="Buscar tareas por descripción")
    parser.add_argument('--listar', action='store_true', help="Listar todas las tareas")
    parser.add_argument('--prioridad', type=str, choices=['baja', 'media', 'alta'], help="Asignar prioridad a una tarea")
    parser.add_argument('--filtrar-por-prioridad', type=str, choices=['baja', 'media', 'alta'], help="Filtrar tareas por prioridad")
    parser.add_argument('--fecha-vencimiento', type=lambda s: datetime.strptime(s, '%Y-%m-%d').date(), help="Asignar fecha de vencimiento a una tarea (formato YYYY-MM-DD)")
    parser.add_argument('--mostrar-proximas', action='store_true', help="Mostrar tareas que están próximas a vencer")
    parser.add_argument('--exportar', type=str, help="Exportar tareas a un archivo CSV")
    parser.add_argument('--historial', action='store_true', help="Listar el historial de tareas completadas")
    parser.add_argument('--desde', type=lambda s: datetime.strptime(s, '%Y-%m-%d').date(), help="Filtrar tareas completadas desde una fecha")
    parser.add_argument('--hasta', type=lambda s: datetime.strptime(s, '%Y-%m-%d').date(), help="Filtrar tareas completadas hasta una fecha")
    args = parser.parse_args()

    if args.agregar:
        tarea = agregar_tarea(args.agregar, args.prioridad, args.fecha_vencimiento)
        print(f"Tarea agregada: {tarea}")
    elif args.completar:
        tarea = completar_tarea(args.completar)
        if tarea:
            print(f"Tarea completada: {tarea}")
        else:
            print("Tarea no encontrada")
    elif args.eliminar:
        if eliminar_tarea(args.eliminar):
            print("Tarea eliminada")
        else:
            print("Tarea no encontrada")
    elif args.buscar:
        tareas = buscar_tareas(args.buscar)
        print("Tareas encontradas:", tareas)
    elif args.listar:
        tareas = listar_tareas()
        print("Todas las tareas:", tareas)
    elif args.filtrar_por_prioridad:
        tareas = filtrar_tareas_por_prioridad(args.filtrar_por_prioridad)
        print(f"Tareas con prioridad {args.filtrar_por_prioridad}:", tareas)
    elif args.mostrar_proximas:
        tareas = tareas_proximas_a_vencer()
        print("Tareas con fecha de vencimiento cerca:", tareas)
    elif args.exportar:
        exportar_tareas_a_csv(args.exportar)
        print(f"Tareas exportadas a {args.exportar}")
    elif args.historial:
        tareas_completadas = obtener_tareas_completadas(args.desde, args.hasta)
        for tarea in tareas_completadas:
            print(f"{tarea.id}: {tarea.descripcion} / Completada el {tarea.fecha_finalizacion}")

if __name__ == "__main__":
    main()