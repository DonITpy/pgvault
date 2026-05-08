from typing import List, Dict


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

    base_score = 100
    final_score = max(0, base_score - total_penalty)

    critical = len([f for f in findings if f.get("risk") == "Crítico"])
    high = len([f for f in findings if f.get("risk") == "Alto"])
    medium = len([f for f in findings if f.get("risk") == "Medio"])
    low = len([f for f in findings if f.get("risk") == "Bajo"])

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
