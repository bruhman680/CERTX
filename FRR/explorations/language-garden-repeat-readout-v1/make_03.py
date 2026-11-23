"""Test whether the same multiple-choice channel reads a supplied answer."""
from make_panel import make_panel

items = []
for group, labels in (
    ("positions", ("First and third", "Second and third")),
    ("symbols", ("mip", "zav")),
):
    for i, label in enumerate(labels, 1):
        items.append((
            f"{group}-{i}", f"Value: {label}",
            "Which choice exactly matches the Value field?",
            labels, label, "garden",
        ))
make_panel(
    "03", items,
    "Can the menu channel copy an explicitly supplied answer into A/B without solving a relation?",
    "Use the original positional answers and a concrete-symbol control. Each value is supplied in the Value field and appears as both choices across its two prompts.",
)
