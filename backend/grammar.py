import language_tool_python as lt
from dataclasses import dataclass
from typing import List

@dataclass
class ErrorItem:
    offset: int
    length: int
    message: str
    replacements: list[str]
    rule_id: str
    category: str

import os
class GrammarChecker:
    def __init__(self, host: str | None = None):
        if host is None:
            host = os.getenv("LANGUAGETOOL_URL", "http://localhost:8010")
        self.tool = lt.LanguageToolPublicAPI(url=host, language="de-DE")

    def check(self, text: str) -> list[ErrorItem]:
        matches = self.tool.check(text)
        out: list[ErrorItem] = []
        for m in matches:
            out.append(ErrorItem(
                offset=m.offset,
                length=m.errorLength,
                message=m.message,
                replacements=[r.value for r in m.replacements][:3],
                rule_id=m.ruleId or "",
                category=(m.ruleIssueType or m.ruleCategory or "")
            ))
        return out

    @staticmethod
    def apply_markers(text: str, errors: list[ErrorItem]) -> str:
        out = []
        i = 0
        errs = sorted(errors, key=lambda e: e.offset)
        for e in errs:
            out.append(text[i:e.offset])
            wrong = text[e.offset:e.offset+e.length]
            fix = e.replacements[0] if e.replacements else "—"
            # Basic HTML mark with tooltip and suggested fix
            out.append(f"<mark title=\"{e.message}\">{wrong}</mark><sup>[{fix}]</sup>")
            i = e.offset + e.length
        out.append(text[i:])
        return "".join(out)

    @staticmethod
    def stats(errors: list[ErrorItem]) -> dict[str, int]:
        from collections import Counter
        c = Counter(e.category or e.rule_id for e in errors)
        return dict(c)
