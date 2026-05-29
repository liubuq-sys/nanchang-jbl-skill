#!/usr/bin/env python3
"""南昌嘉宝莉 Skill · 基础验证测试"""

import sys, os, json

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
errors = []

def check(label, condition):
    if condition:
        print(f"  [OK] {label}")
    else:
        print(f"  [FAIL] {label}")
        errors.append(label)

print("南昌嘉宝莉 Skill · 验证测试")
print("=" * 40)

# 1. Core files
print("\n[核心文件]")
check("SKILL.md 存在", os.path.isfile(os.path.join(SKILL_DIR, "SKILL.md")))
check("version.json 存在", os.path.isfile(os.path.join(SKILL_DIR, "version.json")))
check("README.md 存在", os.path.isfile(os.path.join(SKILL_DIR, "README.md")))
check("CHANGELOG.md 存在", os.path.isfile(os.path.join(SKILL_DIR, "CHANGELOG.md")))
check("install.sh 存在", os.path.isfile(os.path.join(SKILL_DIR, "install.sh")))
check("install.ps1 存在", os.path.isfile(os.path.join(SKILL_DIR, "install.ps1")))

# 2. References
print("\n[References 文件]")
ref_dir = os.path.join(SKILL_DIR, "references")
refs = ["business-info.md", "services.md", "recommendations.md", "promotions.md",
        "after-sales.md", "experience.md", "construction.md", "brand.md", "stores.md"]
for ref in refs:
    check(f"references/{ref} 存在", os.path.isfile(os.path.join(ref_dir, ref)))

# 3. SKILL.md content
print("\n[SKILL.md 内容检查]")
with open(os.path.join(SKILL_DIR, "SKILL.md"), "r", encoding="utf-8") as f:
    skill = f.read()

check("name: 南昌嘉宝莉", "南昌嘉宝莉" in skill)
check("包含场景一~九", all(f"场景{i}" in skill for i in ["一", "二", "三", "四", "五", "六", "七", "八", "九"]))
check("包含门店推荐场景", "门店位置推荐" in skill or "智能推荐" in skill)
check("包含价格声明", "参考价" in skill)
check("包含权限边界说明", "不具备处理售后" in skill or "引导联系" in skill)
check("包含 references 数据读取规则", "references/" in skill and "实时读取" in skill)
check("包含 stores.md 引用", "stores.md" in skill)

# 4. Data completeness
print("\n[数据完整性]")
with open(os.path.join(ref_dir, "stores.md"), "r", encoding="utf-8") as f:
    stores = f.read()
store_count = stores.count("| 嘉宝莉")
check(f"stores.md 包含 {store_count} 个门店信息", store_count >= 10)

with open(os.path.join(ref_dir, "business-info.md"), "r", encoding="utf-8") as f:
    biz = f.read()
check("包含公司全称", "江西陶乐嘉" in biz)
check("包含电话", "17779101790" in biz)
check("包含地址", "青山湖区" in biz)

with open(os.path.join(ref_dir, "services.md"), "r", encoding="utf-8") as f:
    svc = f.read()
check("包含主推商品信息", "海藻泥" in svc or "嘉宝莉" in svc)

# 5. version.json
print("\n[版本信息]")
with open(os.path.join(SKILL_DIR, "version.json"), "r", encoding="utf-8") as f:
    ver = json.load(f)
check("skill 名称正确", ver.get("skill") == "nanchang-jbl")
check("version 字段存在", "version" in ver)
check("data_version 字段存在", "data_version" in ver)

# Result
print(f"\n{'=' * 40}")
if errors:
    print(f"[FAIL] {len(errors)} 项未通过")
    for e in errors:
        print(f"   - {e}")
    sys.exit(1)
else:
    print("[PASS] 全部测试通过！")
    sys.exit(0)
