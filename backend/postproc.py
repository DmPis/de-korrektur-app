def build_explanations(errors) -> list[dict]:
    expl = []
    for e in errors[:50]:  # limit to top-50
        expl.append({
            "rule": e.rule_id,
            "category": e.category,
            "hint": e.message,
            "example_fix": (e.replacements[0] if e.replacements else "—")
        })
    return expl
