from pydantic import BaseModel


class PaginationCreate(BaseModel):
    skip: int
    limit: int
