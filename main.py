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