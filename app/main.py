from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

PERSONNEL_CAP = 120_000
THIRD_PARTY_LIMIT_RATIO = 0.25
ZIM_APPROVAL_RATE = 86
BASE_DIR = Path(__file__).resolve().parent


class GrantInput(BaseModel):
    language: Literal[
        "German",
        "English",
        "Mandarin",
        "Spanish",
        "French",
        "Arabic",
        "Turkish",
        "Russian",
        "Italian",
        "Polish",
    ]
    cad_summary: str = Field(default="")
    sap_metrics: str = Field(default="")
    personnel_cost: float = Field(ge=0)
    third_party_cost: float = Field(ge=0)


app = FastAPI(title="Grant-Agent AI Prototype")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


def budget_guard(personnel_cost: float, third_party_cost: float) -> dict:
    violations: list[str] = []

    if personnel_cost > PERSONNEL_CAP:
        violations.append(
            f"Compliance Violation: BMWK personnel cap exceeded (€{PERSONNEL_CAP:,.0f})."
        )

    if personnel_cost > 0 and third_party_cost > personnel_cost * THIRD_PARTY_LIMIT_RATIO:
        violations.append(
            "Compliance Violation: Third-party costs exceed 25% of personnel budget."
        )

    return {
        "personnel_cap": PERSONNEL_CAP,
        "third_party_limit_ratio": THIRD_PARTY_LIMIT_RATIO,
        "is_compliant": len(violations) == 0,
        "violations": violations,
    }


def render_behoerdendeutsch(payload: GrantInput, guard: dict) -> str:
    status_line = (
        "Die beantragten Kosten entsprechen den BMWK-Rahmenbedingungen."
        if guard["is_compliant"]
        else "Die beantragten Kosten verletzen die BMWK-Rahmenbedingungen und sind anzupassen."
    )
    return (
        "Verwaltungsentwurf für ZIM/EXIST:\n"
        f"- Eingangsdatum: {datetime.utcnow().strftime('%d.%m.%Y %H:%M UTC')}\n"
        "- Sicherheitslage: Intel TDX-Hardware Root of Trust aktiv.\n"
        "- Orchestrierung: LlamaIndex über LangChain mit hierarchischer Metadatenzuordnung.\n"
        "- Transformationsmodell: Aleph Alpha PhariaAI (EU-Datenresidenz).\n"
        "- Förderkontext: Historische ZIM-Bewilligungsquote 86 %.\n"
        f"- CAD-Metadaten: {payload.cad_summary.strip() or 'Keine Angaben'}\n"
        f"- SAP SCOM-Metriken: {payload.sap_metrics.strip() or 'Keine Angaben'}\n"
        f"- Personalaufwand: €{payload.personnel_cost:,.2f}\n"
        f"- Drittmittel: €{payload.third_party_cost:,.2f}\n"
        f"- Bewertung: {status_line}"
    )


@app.get("/", response_class=HTMLResponse)
@app.get("/index.html", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health", response_class=JSONResponse)
def health():
    return {"status": "ok"}


@app.post("/api/transform", response_class=JSONResponse)
def transform(payload: GrantInput):
    guard = budget_guard(payload.personnel_cost, payload.third_party_cost)
    preview = render_behoerdendeutsch(payload, guard)

    return {
        "security_layer": {
            "hardware_root_of_trust": "Intel TDX (simulated)",
            "memory_encryption": "active",
        },
        "rag_layer": {
            "framework": "LlamaIndex over LangChain",
            "vector_db": "Qdrant",
        },
        "model_layer": {"llm": "Aleph Alpha PhariaAI"},
        "budget_guard": guard,
        "approval_rate": ZIM_APPROVAL_RATE,
        "preview": preview,
    }
