from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.scraping import scrape_homepage
from app.ai_agent import analyze_homepage_content
from app.models import ScrapeRequest, ScrapeResponse, ErrorResponse
from app.config import SECRET_KEY

app = FastAPI(
    title="AI Agent for Website Scraping",
    description="Scrapes only the homepage and uses Gemini AI for analysis.",
    version="1.0.0",
)

security = HTTPBearer()

def authenticate(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Dependency to verify the secret key from the Authorization header."""
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme."
        )
    if credentials.credentials != SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing secret key."
        )

@app.post("/scrape", response_model=ScrapeResponse, responses={401: {"model": ErrorResponse}})
def scrape_website(payload: ScrapeRequest, creds: HTTPAuthorizationCredentials = Depends(authenticate)):
    """
    POST endpoint to scrape the homepage of a website and get:
      - Industry
      - Company Size
      - Location
    """
    url = payload.url
    
    try:
        homepage_text = scrape_homepage(url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    analysis = analyze_homepage_content(homepage_text)
    
    return ScrapeResponse(
        industry=analysis.get("industry"),
        company_size=analysis.get("company_size"),
        location=analysis.get("location")
    )
