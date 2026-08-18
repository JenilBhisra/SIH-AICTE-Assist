from fastapi import FastAPI

app = FastAPI(title="AICTE Model Curriculum Intelligence & Governance Portal")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
