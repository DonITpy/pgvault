from typing import TypedDict, Optional


class Finding(TypedDict, total=False):
    module: str
    rule_id: str
    risk: str
    confidence: int
    match_type: str
    table: Optional[str]
    column: Optional[str]
    details: str
