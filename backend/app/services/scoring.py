from typing import List, Dict
import math


SEVERITY_POINTS = {
    "Crítico": 25,
    "Alto": 15,
    "Medio": 8,
    "Bajo": 3,
}


def calculate_security_score(findings: List[Dict]) -> Dict:
    total_penalty = 0

    for f in findings:
        risk = f.get("risk", "Medio")
        total_penalty += SEVERITY_POINTS.get(risk, 8)

    if total_penalty == 0:
        final_score = 100
    else:
        final_score = max(0, round(100 - (math.log1p(total_penalty) / math.log1p(400)) * 100))

    critical = sum(1 for f in findings if f.get("risk") == "Crítico")
    high = sum(1 for f in findings if f.get("risk") == "Alto")
    medium = sum(1 for f in findings if f.get("risk") == "Medio")
    low = sum(1 for f in findings if f.get("risk") == "Bajo")

    return {
        "score": final_score,
        "summary": {
            "total_findings": len(findings),
            "critical": critical,
            "high": high,
            "medium": medium,
            "low": low,
        },
    }