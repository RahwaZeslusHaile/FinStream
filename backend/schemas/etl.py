from pydantic import BaseModel


class EtlSyncResponse(BaseModel):
    message: str
    positions_added: int
    failed_brokers: dict[str, str] | None = None
    failed_normalizers: dict[str, str] | None = None
