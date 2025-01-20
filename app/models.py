from pydantic import BaseModel, HttpUrl

# Req model
class ScrapeRequest(BaseModel):
    url: HttpUrl

# Res model (Pydantic)
class ScrapeResponse(BaseModel):
    industry: str | None
    company_size: str | None
    location: str | None

# Error res model
class ErrorResponse(BaseModel):
    detail: str
