from pydantic import BaseModel


class EtlSyncResponse(BaseModel):
    message: str
    positions_added: int
