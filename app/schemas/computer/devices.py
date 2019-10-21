from pydantic import Schema

from app.schemas.computer.base import BaseComponent


class PrinterModel(BaseComponent):
    caption: str
    hidden: bool
    shared: bool
    published: bool
    printer_status: str = Schema(..., alias="PrinterStatus")
    driver_name: str = Schema(..., alias="DriverName")
