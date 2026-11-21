#!/usr/bin/env python3
"""Kiểm tra cấu trúc kit: JSON hợp lệ, frontmatter của skills/agents/commands đúng chuẩn."""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors = []

def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        errors.append(f"{path}: thiếu frontmatter")
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"')
    return fm

for j in [ROOT / ".claude-plugin/marketplace.json", *ROOT.glob("plugins/*/.claude-plugin/plugin.json")]:
    try:
        json.loads(j.read_text(encoding="utf-8"))
    except Exception as e:
        errors.append(f"{j}: JSON lỗi: {e}")

market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
for p in market.get("plugins", []):
    if not (ROOT / p["source"] / ".claude-plugin/plugin.json").exists():
        errors.append(f"marketplace: plugin {p['name']} không có plugin.json tại {p['source']}")

for skill in ROOT.glob("plugins/*/skills/*/SKILL.md"):
    fm = frontmatter(skill)
    name, desc = fm.get("name", ""), fm.get("description", "")
    if name != skill.parent.name:
        errors.append(f"{skill}: name '{name}' phải trùng tên thư mục '{skill.parent.name}'")
    if not re.fullmatch(r"[a-z0-9-]{1,64}", name or "x" * 65):
        errors.append(f"{skill}: name chỉ gồm a-z, 0-9, '-' và tối đa 64 ký tự")
    if not desc or len(desc) > 1024:
        errors.append(f"{skill}: description bắt buộc và tối đa 1024 ký tự")
    if len(skill.read_text(encoding="utf-8").splitlines()) > 500:
        errors.append(f"{skill}: SKILL.md nên dưới 500 dòng, tách phần dài sang references/")

for agent in ROOT.glob("plugins/*/agents/*.md"):
    fm = frontmatter(agent)
    for key in ("name", "description"):
        if not fm.get(key):
            errors.append(f"{agent}: thiếu '{key}'")

for cmd in ROOT.glob("plugins/*/commands/*.md"):
    if not frontmatter(cmd).get("description"):
        errors.append(f"{cmd}: thiếu 'description'")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print("OK: cấu trúc hợp lệ")
