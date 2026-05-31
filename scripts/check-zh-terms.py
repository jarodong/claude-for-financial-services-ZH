#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

FENCE = chr(96) * 3

REQUIRED_EXPLANATIONS = {
    'DCF': '折现现金流估值法',
    'LBO': '杠杆收购模型',
    'Comps': '可比公司分析',
    'Precedents': '可比交易分析',
    'WACC': '加权平均资本成本',
    'IRR': '内部收益率',
    'MOIC': '投资倍数',
    'NAV': '净资产值',
    'GL': '总分类账',
    'KYC': '客户身份识别',
    'AML': '反洗钱',
    'TLH': '税损收割',
    'CIM': '保密信息备忘录',
    'Teaser': '匿名推介材料',
    'Pitch Deck': '推介材料',
    'Agent': '智能体',
    'Skill': '技能',
    'Plugin': '插件',
    'MCP': '模型上下文协议',
}

BANNED_VARIANTS = {
    '路演材料': '如指 Pitch Deck，统一为“Pitch Deck（推介材料）”或“推介材料”。',
    'Deck 质检': '统一为“Pitch Deck（推介材料）质检”。',
    '投委会 Memo': '统一为“投决会备忘录（Investment Committee Memo）”。',
    '公司 KYC': '合规语境优先使用“本机构 KYC”。',
}


def strip_fenced_code(text: str) -> str:
    lines = []
    in_code = False
    for line in text.splitlines():
        if line.strip().startswith(FENCE):
            in_code = not in_code
            lines.append('')
            continue
        lines.append('' if in_code else line)
    return '\n'.join(lines)


def has_required_explanation(window: str, explanation: str) -> bool:
    compact = re.sub(r'\s+', '', window)
    if explanation in compact:
        return True
    return explanation == '客户身份识别' and '了解你的客户' in compact


def check_first_explanations(path: Path, text: str) -> list[str]:
    issues = []
    for term, explanation in REQUIRED_EXPLANATIONS.items():
        pattern = re.compile(rf'(?<![A-Za-z0-9_-]){re.escape(term)}(?![A-Za-z0-9_-])')
        match = pattern.search(text)
        if not match:
            continue
        window = text[match.start(): match.start() + 80]
        if not has_required_explanation(window, explanation):
            line_no = text.count('\n', 0, match.start()) + 1
            issues.append(f'{path}:{line_no}: “{term}”首次出现附近缺少中文释义“{explanation}”。')
    return issues


def check_banned_variants(path: Path, text: str) -> list[str]:
    if path.name == 'STYLE-GUIDE.md':
        return []
    issues = []
    for phrase, suggestion in BANNED_VARIANTS.items():
        index = text.find(phrase)
        if index == -1:
            continue
        line_no = text.count('\n', 0, index) + 1
        issues.append(f'{path}:{line_no}: 出现不统一译法“{phrase}”。{suggestion}')
    return issues


def check_untranslated_lines(path: Path, text: str) -> list[str]:
    issues = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith(('#', '|', '>', '- ', '* ')):
            continue
        if 'http://' in stripped or 'https://' in stripped:
            continue
        english_words = re.findall(r"[A-Za-z][A-Za-z0-9'&/-]*", stripped)
        chinese_chars = re.findall(r'[一-鿿]', stripped)
        if len(english_words) >= 8 and len(chinese_chars) <= 2:
            issues.append(f'{path}:{line_no}: 疑似存在未翻译英文句子：{stripped[:100]}')
    return issues


def check_file(path: Path) -> list[str]:
    raw = path.read_text(encoding='utf-8')
    text = strip_fenced_code(raw)
    issues = []
    issues.extend(check_first_explanations(path, text))
    issues.extend(check_banned_variants(path, text))
    issues.extend(check_untranslated_lines(path, text))
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description='检查中文金融文档中的术语释义、译法混用和明显未翻译英文句子。')
    parser.add_argument('files', nargs='+', help='要检查的 Markdown 文件')
    args = parser.parse_args()
    all_issues = []
    for file_name in args.files:
        path = Path(file_name)
        if not path.exists():
            all_issues.append(f'{path}: 文件不存在。')
            continue
        if path.suffix.lower() != '.md':
            continue
        all_issues.extend(check_file(path))
    if all_issues:
        print('术语校对发现问题：')
        for issue in all_issues:
            print(f'- {issue}')
        return 1
    print('术语校对通过。')
    return 0


if __name__ == '__main__':
    sys.exit(main())
