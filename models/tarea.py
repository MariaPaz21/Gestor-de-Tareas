from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, Date, create_engine
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
    prioridad = Column(Enum('baja', 'media', 'alta', name='prioridades'), default='media')
    fecha_vencimiento = Column(Date, nullable=True)
    fecha_finalizacion = Column(DateTime, nullable=True)

    def __repr__(self):
        return (f"<Tarea(id={self.id}, "
            f"descripcion='{self.descripcion}', "
            f"completada={self.completada}, "
            f"fecha_creacion={self.fecha_creacion}, "
            f"prioridad={self.prioridad}, "
            f"fecha_vencimiento={self.fecha_vencimiento}, "
            f"fecha_finalizacion={self.fecha_finalizacion})>")

DATABASE_URL = "sqlite:///tareas.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)