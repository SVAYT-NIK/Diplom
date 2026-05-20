from sqlalchemy import Column, String, Boolean, DateTime, ARRAY, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from backend.db.session import Base


class User(Base):
    """Модель пользователя системы."""
    
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=func.gen_random_uuid())
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="viewer")  # admin, operator, analyst, viewer
    mcd_access = Column(ARRAY(String), default=list)  # Список доступных МКД
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))
    
    def __repr__(self):
        return f"<User {self.username} ({self.role})>"


class MCD(Base):
    """Модель многоквартирного дома."""
    
    __tablename__ = "mcds"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=func.gen_random_uuid())
    mcd_code = Column(String(50), unique=True, nullable=False, index=True)  # Уникальный код МКД
    address = Column(String(500), nullable=False)  # Полный адрес
    region = Column(String(100))  # Регион
    city = Column(String(100))  # Город
    street = Column(String(200))  # Улица
    building_number = Column(String(20))  # Номер дома
    
    # Технические параметры
    total_area = Column(Integer)  # Общая площадь, м²
    living_area = Column(Integer)  # Жилая площадь, м²
    floors = Column(Integer)  # Количество этажей
    apartments_count = Column(Integer)  # Количество квартир
    year_built = Column(Integer)  # Год постройки
    
    # Энергоэффективность
    energy_class = Column(String(1))  # Класс энергоэффективности (A, B, C, D, E)
    gsop_value = Column(Integer)  # ГСОП, градусо-сутки
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<MCD {self.mcd_code} - {self.address}>"


class Device(Base):
    """Модель прибора учёта."""
    
    __tablename__ = "devices"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=func.gen_random_uuid())
    device_id = Column(String(100), unique=True, nullable=False, index=True)  # Идентификатор прибора
    mcd_id = Column(UUID(as_uuid=True), nullable=False, index=True)  # Ссылка на МКД
    device_type = Column(String(50), nullable=False)  # Тип прибора (heat_meter, electricity, water, etc.)
    manufacturer = Column(String(200))  # Производитель
    model = Column(String(200))  # Модель
    serial_number = Column(String(100))  # Серийный номер
    
    # Параметры установки
    installation_date = Column(DateTime(timezone=True))
    verification_date = Column(DateTime(timezone=True))  # Дата поверки
    verification_interval = Column(Integer)  # Интервал поверки, месяцев
    
    # Статус
    status = Column(String(20), default="active")  # active, inactive, maintenance, error
    last_seen = Column(DateTime(timezone=True))  # Последнее соединение
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Device {self.device_id} - {self.device_type}>"
