
# Taller: Gestor de Tareas con ORM

## Descripción del Proyecto

**Gestor de Tareas:**

El Gestor de Tareas es una aplicación de gestión de tareas que permite a los usuarios organizar y seguir sus actividades pendientes. Los usuarios pueden agregar nuevas tareas, marcar tareas como completadas, eliminar tareas y ver todas las tareas tanto pendientes como completadas. La aplicación utiliza un ORM (Object-Relational Mapping) para interactuar con la base de datos, lo que facilita la gestión de las tareas de manera eficiente y estructurada.

## Requerimientos y Funcionalidades del Proyecto

1. **Agregar Nueva Tarea:**
   - Permitir a los usuarios agregar una nueva tarea proporcionando una descripción.
   - Asignar automáticamente una fecha de creación a cada tarea.

2. **Listar Todas las Tareas:**
   - Mostrar una lista de todas las tareas, tanto pendientes como completadas.
   - Permitir la opción de filtrar y mostrar solo las tareas pendientes o solo las completadas.

3. **Marcar Tarea como Completada:**
   - Permitir a los usuarios marcar una tarea como completada.
   - Actualizar el estado de la tarea en la base de datos.

4. **Eliminar Tarea:**
   - Permitir a los usuarios eliminar una tarea específica.
   - Eliminar la tarea de la base de datos.

5. **Buscar Tareas:**
   - Permitir a los usuarios buscar tareas por descripción.
   - Mostrar las tareas que coincidan con los términos de búsqueda.

6. **Actualizar Descripción de Tarea:**
   - Permitir a los usuarios actualizar la descripción de una tarea existente.

7. **Interfaz de Usuario:**
   - Proveer una interfaz de línea de comandos (CLI) para interactuar con la aplicación.
   - Proveer mensajes de retroalimentación claros y concisos para cada acción realizada por el usuario.

8. **Persistencia de Datos:**
   - Utilizar un ORM (SQLAlchemy o peewee) para gestionar la persistencia de datos en una base de datos SQLite.



# Taller: Gestor de Tareas con ORM - Parte 1

## Inicio del Proyecto y Configuración

En esta primera parte, configuraremos el entorno de desarrollo e iniciaremos el proyecto. Vamos a crear un entorno virtual, instalar las dependencias necesarias, y configurar la estructura inicial del proyecto.

### Paso 1: Crear el Entorno de Desarrollo

1. **Crear un Entorno Virtual:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

2. **Instalar las Dependencias:**

   ```bash
   pip install sqlalchemy sqlite3
   ```

### Paso 2: Configurar la Estructura Inicial del Proyecto

1. **Crear la Estructura de Directorios:**

   ```bash
   mkdir gestor_tareas
   cd gestor_tareas
   mkdir models
   touch main.py
   touch models/tarea.py
   ```

2. **Configurar el ORM (SQLAlchemy):**

   **Archivo `models/tarea.py`:**

   ```python
   from sqlalchemy import Column, Integer, String, Boolean, DateTime, create_engine
   from sqlalchemy.ext.declarative import declarative_base
   from sqlalchemy.orm import sessionmaker
   from datetime import datetime

   Base = declarative_base()

   class Tarea(Base):
       __tablename__ = 'tareas'
       id = Column(Integer, primary_key=True)
       descripcion = Column(String, nullable=False)
       completada = Column(Boolean, default=False)
       fecha_creacion = Column(DateTime, default=datetime.utcnow)

       def __repr__(self):
           return f"<Tarea(id={self.id}, descripcion='{self.descripcion}', completada={self.completada})>"

   DATABASE_URL = "sqlite:///tareas.db"
   engine = create_engine(DATABASE_URL)
   SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
   Base.metadata.create_all(bind=engine)
   ```

3. **Crear la Configuración Inicial del Proyecto:**

   **Archivo `main.py`:**

   ```python
   from models.tarea import Tarea, SessionLocal

   def agregar_tarea(descripcion):
       session = SessionLocal()
       nueva_tarea = Tarea(descripcion=descripcion)
       session.add(nueva_tarea)
       session.commit()
       session.refresh(nueva_tarea)
       session.close()
       return nueva_tarea

   if __name__ == "__main__":
       tarea = agregar_tarea("Mi primera tarea")
       print(tarea)
   ```

4. **Probar la Configuración Inicial:**

   Ejecuta el archivo `main.py` para asegurarte de que todo está configurado correctamente:

   ```bash
   python main.py
   ```

   Deberías ver una salida similar a:

   ```
   <Tarea(id=1, descripcion='Mi primera tarea', completada=False)>
   ```

# Taller: Gestor de Tareas con ORM - Parte 2

## Agregar, Listar y Marcar Tareas como Completadas

En esta parte, implementaremos las funcionalidades para agregar nuevas tareas, listar todas las tareas y marcar tareas como completadas.

### Paso 1: Agregar Tareas

**Archivo `main.py` (Continuación):**

```python
def listar_tareas():
    session = SessionLocal()
    tareas = session.query(Tarea).all()
    session.close()
    return tareas

def completar_tarea(tarea_id):
    session = SessionLocal()
    tarea = session.query(Tarea).filter(Tarea.id == tarea_id).first()
    if tarea:
        tarea.completada = True
        session.commit()
        session.refresh(tarea)
    session.close()
    return tarea

if __name__ == "__main__":
    # Agregar una tarea
    tarea = agregar_tarea("Mi primera tarea")
    print(tarea)

    # Listar todas las tareas
    tareas = listar_tareas()
    print("Todas las tareas:", tareas)

    # Marcar una tarea como completada
    tarea_completada = completar_tarea(tarea.id)
    print("Tarea completada:", tarea_completada)
```

### Paso 2: Probar las Funcionalidades

Ejecuta el archivo `main.py` para probar las nuevas funcionalidades:

```bash
python main.py
```

Deberías ver una salida similar a:

```
<Tarea(id=1, descripcion='Mi primera tarea', completada=False)>
Todas las tareas: [<Tarea(id=1, descripcion='Mi primera tarea', completada=False)>]
Tarea completada: <Tarea(id=1, descripcion='Mi primera tarea', completada=True)>
```

# Taller: Gestor de Tareas con ORM - Parte 3

## Eliminar y Buscar Tareas

En esta parte, implementaremos las funcionalidades para eliminar tareas y buscar tareas por descripción.

### Paso 1: Eliminar Tareas

**Archivo `main.py` (Continuación):**

```python
def eliminar_tarea(tarea_id):
    session = SessionLocal()
    tarea = session.query(Tarea).filter(Tarea.id == tarea_id).first()
    if tarea:
        session.delete(tarea)
        session.commit()
        resultado = True
    else:
        resultado = False
    session.close()
    return resultado

def buscar_tareas(termino):
    session = SessionLocal()
    tareas = session.query(Tarea).filter(Tarea.descripcion.contains(termino)).all()
    session.close()
    return tareas

if __name__ == "__main__":
    # Agregar una tarea
    tarea = agregar_tarea("Mi primera tarea")
    print(tarea)

    # Listar todas las tareas
    tareas = listar_tareas()
    print("Todas las tareas:", tareas)

    # Marcar una tarea como completada
    tarea_completada = completar_tarea(tarea.id)
    print("Tarea completada:", tarea_completada)

    # Buscar tareas
    tareas_encontradas = buscar_tareas("primera")
    print("Tareas encontradas:", tareas_encontradas)

    # Eliminar una tarea
    eliminada = eliminar_tarea(tarea.id)
    print("Tarea eliminada:", eliminada)

    # Listar todas las tareas después de eliminar
    tareas = listar_tareas()
    print("Todas las tareas después de eliminar:", tareas)
```

### Paso 2: Probar las Funcionalidades

Ejecuta el archivo `main.py` para probar las nuevas funcionalidades:

```bash
python main.py
```

Deberías ver una salida similar a:

```
<Tarea(id=1, descripcion='Mi primera tarea', completada=False)>
Todas las tareas: [<Tarea(id=1, descripcion='Mi primera tarea', completada=False)>]
Tarea completada: <Tarea(id=1, descripcion='Mi primera tarea', completada=True)>
Tareas encontradas: [<Tarea(id=1, descripcion='Mi primera tarea', completada=True)>]
Tarea eliminada: True
Todas las tareas después de eliminar: []
```


# Taller: Gestor de Tareas con ORM - Parte 4

## Crear una Interfaz de Línea de Comandos (CLI)

En esta parte, implementaremos una interfaz de línea de comandos (CLI) para interactuar con la aplicación.

### Paso 1: Implementar la CLI

**Archivo `main.py` (Continuación):**

```python
import argparse

def main():
    parser = argparse.ArgumentParser(description="Gestor de Tareas")
    parser.add_argument('--agregar', type=str, help="Agregar una nueva tarea")
    parser.add_argument('--completar', type=int, help="Marcar una tarea como completada")
    parser.add_argument('--eliminar', type=int, help="Eliminar una tarea")
    parser.add_argument('--buscar', type=str, help="Buscar tareas por descripción")
    parser.add_argument('--listar', action='store_true', help="Listar todas las tareas")

    args = parser.parse_args()

    if args.agregar:
        tarea = agregar_tarea(args.agregar)
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

if __name__ == "__main__":
    main()
```

### Paso 2: Probar la CLI

Prueba los siguientes comandos en la terminal:

- **Agregar una tarea:**
  ```bash
  python main.py --agregar "Nueva tarea desde la CLI"
  ```

- **Listar todas las tareas:**
  ```bash
  python main.py --listar
  ```

- **Completar una tarea:**
  ```bash
  python main.py --completar 1
  ```

- **Eliminar una tarea:**
  ```bash
  python main.py --eliminar 1
  ```

- **Buscar tareas:**
  ```bash
  python main.py --buscar "Nueva"
  ```

# Taller: Gestor de Tareas con ORM - Parte 5

## Decoradores y Manejo de Errores

En esta parte, implementaremos decoradores y manejo de errores para mejorar la robustez de nuestra aplicación.

### Paso 1: Implementar Decoradores para Manejar la Sesión

**Archivo `main.py` (Continuación):**

```python
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
            print(f"Error: {e}")
        finally:
            session.close()
    return wrapper

@manejar_sesion
def agregar_tarea(session, descripcion):
    nueva_tarea = Tarea(descripcion=descripcion)
    session.add(nueva_tarea)
    session.refresh(nueva_tarea)
    return nueva_tarea

@manejar_sesion
def completar_tarea(session, tarea_id):
    tarea = session.query(Tarea).filter(Tarea.id == tarea_id).first()
    if tarea:
        tarea.completada = True
        session.refresh(tarea)
    return tarea

@manejar_sesion
def eliminar_tarea(session, tarea_id):
    tarea = session.query(Tarea).filter(Tarea.id == tarea_id).first()
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

if __name__ == "__main__":
    main()
```

### Paso 2: Probar las Funcionalidades con los Decoradores

Ejecuta el archivo `main.py` para asegurarte de que todo funciona correctamente con los decoradores.

```bash
python main.py --agregar "Prueba de decoradores"
python main.py --listar
```


# Tarea: Extensión del Gestor de Tareas con Nuevas Características

## Descripción de la Tarea

La tarea consiste en añadir nuevas características a la aplicación de Gestor de Tareas que hemos desarrollado durante el taller. El objetivo es mejorar la funcionalidad del gestor de tareas y proporcionar una experiencia de usuario más completa. A continuación, se detallan las características que se deben implementar.

## Características a Implementar

### 1. Prioridades de Tareas
**Descripción:**
- Permitir a los usuarios asignar una prioridad a cada tarea (baja, media, alta).
- Implementar comandos en la CLI para filtrar tareas por prioridad.

### 2. Fechas de Vencimiento
**Descripción:**
- Permitir a los usuarios asignar una fecha de vencimiento a cada tarea.
- Implementar comandos en la CLI para mostrar tareas que están próximas a vencer.

### 3. Exportar Tareas
**Descripción:**
- Permitir a los usuarios exportar la lista de tareas a un archivo CSV.
- Implementar un comando en la CLI para exportar las tareas.
- Utilizar la biblioteca `csv` de Python para manejar la exportación.

### 4. Historial de Tareas Completadas
**Descripción:**
- Permitir a los usuarios ver un historial de todas las tareas que han sido completadas.
- Implementar comandos en la CLI para listar y filtrar tareas completadas por fecha de finalización.


## Entregables

1. **Código Fuente:**
   - Modificaciones en el modelo de `Tarea` y cualquier otro modelo necesario.
   - Funciones nuevas o modificadas para manejar las nuevas características.
   - Comandos de la CLI actualizados para soportar las nuevas características.

## Evaluación

La tarea será evaluada en base a:
- Correctitud y funcionalidad del código.
- Uso adecuado de conceptos de programación orientada a objetos.
- Implementación de decoradores y manejo de errores.
- Eficiencia y organización del código.

¡Buena suerte y feliz codificación!
