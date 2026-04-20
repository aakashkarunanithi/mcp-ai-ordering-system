from sqlalchemy import Column, Integer, Enum, text, DateTime, String, ForeignKey, Boolean, Float,UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()

# class Item(Base):
#     __tablename__ = "items"
#     item_id = Column(Integer, primary_key=True)
#     item_uuid = Column(UUID, server_default=text("gen_random_uuid()"), unique=True, index=True)
#     item_name = Column(String, nullable = False)
#     price = Column(Float, nullable= False)
#     is_active = Column(Boolean, server_default=text("True"))
#     created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
#     created_by = Column(String, server_default=text("'ADMIN'"))
#     updated_at = Column(DateTime)
#     updated_by = Column(String, nullable= True)

# class Status(enum.Enum):
#     ready = "ready"
#     inprogress="inprogress"
    
# class Order_Item_Mapping(Base):
#     __tablename__ = "order_item_mapping"
#     order_item_id = Column(Integer, primary_key=True,)
#     order_item_uuid = Column(UUID, server_default=text("gen_random_uuid()"), unique=True, index=True)
#     order_uuid = Column(UUID, ForeignKey("orders.order_uuid"))
#     item_uuid = Column(UUID, ForeignKey("items.item_uuid"))
#     quantity = Column(Integer, nullable= False)
#     is_active = Column(Boolean, server_default=text("True"))
#     created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
#     created_by = Column(String, server_default=text("'ADMIN'"))
#     updated_at = Column(DateTime)
#     updated_by = Column(String, nullable= True)
#     #  relationship
#     order = relationship("Order", backref = "order_item_mapping")
#     item = relationship("Item", backref="order_item_mapping")


# class Order(Base):
#     __tablename__ = "orders"
#     order_id = Column(Integer, primary_key=True,)
#     order_uuid = Column(UUID, server_default=text("gen_random_uuid()"), unique=True, index=True)
#     status = Column(Enum(Status), nullable= False, default= Status.inprogress)
#     ordered_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
#     is_active = Column(Boolean, server_default=text("True"))
#     created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
#     created_by = Column(String, server_default=text("'ADMIN'"))
#     updated_at = Column(DateTime)
#     updated_by = Column(String)



class Error(Base):
    __tablename__ = "errors"
    error_id = Column(Integer, primary_key=True)
    error_uuid = Column(UUID, server_default=text("gen_random_uuid()"), unique=True, index=True)
    error_code=Column(String,nullable=False)
    file_name = Column(String, nullable=False)
    function_name = Column(String, nullable=False)
    error_message = Column(String, nullable=False)
    is_active = Column(Boolean, server_default=text("True"))
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    created_by = Column(String, server_default=text("'ADMIN'"))
    updated_at = Column(DateTime)
    updated_by = Column(String)

