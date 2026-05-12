from typing import List, Dict


SEVERITY_POINTS = {
    "Crítico": 10,
    "Alto": 5,
    "Medio": 2,
    "Bajo": 1,
}

MAX_PENALTY = 200


def calculate_security_score(findings: List[Dict]) -> Dict:
    total_penalty = 0

    for f in findings:
        risk = f.get("risk", "Medio")
        total_penalty += SEVERITY_POINTS.get(risk, 2)

    final_score = max(0, round(100 * (1 - min(total_penalty, MAX_PENALTY) / MAX_PENALTY)))

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