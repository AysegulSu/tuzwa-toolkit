Working dir /home/claude/work. READ-ONLY audit — do not edit any file, do not call any API.

Rule under test (rules/description-format-rule.md): "ADD ONLY, DELETE NOTHING: every existing product-specific detail (size, dimensions, color, material, capacity, weight, specs, compatibility…) is preserved unchanged" and "Never invent, remove, or alter product specifications". Exceptions are ONLY the rulings in RULINGS.md (read it first) — a fact a ruling says to omit or change is not a finding.

For each idx in RANGE: read extract/pNN.json (fields: facts, specs, package, how_to_use, faq_source, variants) and final/dNN.json (descriptionHtml — strip tags mentally, read the whole thing). Compare EVERY source fact against the description:
- a number, unit, dimension, weight, capacity, count, material, color, size, compatibility, mode name, timing, range, standard (e.g. G1/2, IPX6, Bluetooth 5.1) that is in the source but not in the description → DROPPED
- a value that changed (350-450 → 450; 20-25 h → 20 h; "1X 2X 3X 10X" → "2X 3X 10X"; metric unit removed leaving only imperial or vice versa) → ALTERED
- a value in the description that is NOT in the source (and not a ruling) → INVENTED
Unit abbreviations (ft for feet, in for inches, lb for pounds) and reworded but equivalent sentences are NOT findings. Marketing fluff sentences with no fact are not findings. Package Includes items must all be present.

Output ONLY, one block per product:
NN | CLEAN
or
NN | DROPPED: <spec/fact name>: <exact source value> ; ALTERED: <name>: <source> → <description> ; INVENTED: <text>
Be precise and exhaustive — every dropped item, not a sample. Nothing else in the reply.
