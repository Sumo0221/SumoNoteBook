"""
SumoNoteBook Citation 追蹤系統
===========================
每個 Wiki 頁面強制附帶來源資訊

功能：
- Citation 抬頭模板
- Source: 必填（哪些 Raw 文件蒸餾而來）
- Confidence: 必填（high/medium/low）
- Verified: 必填（日期）
- 自動驗證 Citation 完整性

使用方式：
```python
from citation_tracker import CitationTemplate, add_citation_to_page, validate_citations

# 建立帶 Citation 的頁面
template = CitationTemplate()
page_content = template.generate(
    title="我的知識頁面",
    content="這是內容...",
    sources=["raw/agent-research/notes.md", "raw/development/api.md"],
    confidence="high",
    verified_date="2026-04-15"
)

# 驗證所有頁面的 Citation
issues = validate_citations(wiki_dir)
```
"""

import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Set
from dataclasses import dataclass


# ============================================================================
# Citation 模板
# ============================================================================

CITATION_TEMPLATE = """---

## Citation

- **Source**: {sources}
- **Confidence**: {confidence}
- **Verified**: {verified}
- **Raw Files**: {raw_files}

---

"""


@dataclass
class CitationInfo:
    """Citation 資訊"""
    sources: List[str]
    confidence: str  # high, medium, low
    verified: str    # 日期
    raw_files: List[str] = None
    
    def __post_init__(self):
        if self.raw_files is None:
            self.raw_files = []
        # 驗證 confidence
        if self.confidence not in ['high', 'medium', 'low']:
            self.confidence = 'medium'


class CitationTemplate:
    """Citation 模板生成器"""
    
    def __init__(self, raw_dir: Optional[Path] = None):
        self.raw_dir = raw_dir or Path("c:/butler_sumo/library/SumoNoteBook/Raw")
    
    def generate(
        self,
        title: str,
        content: str,
        sources: List[str],
        confidence: str = "medium",
        verified: str = None,
        raw_files: List[str] = None
    ) -> str:
        """
        生成帶 Citation 的頁面內容
        
        Args:
            title: 頁面標題
            content: 主要內容
            sources: 來源列表
            confidence: 信心程度 (high/medium/low)
            verified: 驗證日期
            raw_files: 原始檔案列表
        
        Returns:
            完整的 Markdown 內容（含 Citation）
        """
        if verified is None:
            verified = datetime.now().strftime("%Y-%m-%d")
        
        if raw_files is None:
            raw_files = sources  # 預設與 sources 相同
        
        # 格式化 sources
        sources_str = ", ".join(sources) if sources else "N/A"
        raw_files_str = ", ".join(raw_files) if raw_files else "N/A"
        
        # 生成 Citation 區塊
        citation_block = f"""---

## Citation

- **Source**: {sources_str}
- **Confidence**: {confidence}
- **Verified**: {verified}
- **Raw Files**: {raw_files_str}

---

"""
        # 組合完整內容
        full_content = f"# {title}\n\n{content}\n\n{citation_block}"
        
        return full_content
    
    def add_citation_header(self, content: str, **citation_kwargs) -> str:
        """
        在現有內容開頭新增 Citation 區塊
        
        Args:
            content: 現有 Markdown 內容
            **citation_kwargs: Citation 參數
        
        Returns:
            新增 Citation 後的內容
        """
        citation_block = self.generate(
            title="",  # 不需要標題，會被忽略
            content="",  # 不需要內容
            **citation_kwargs
        )
        
        # 移除標題部分（因為我們只想要 Citation 區塊）
        citation_block = re.sub(r'^#.*?\n\n', '', citation_block, flags=re.DOTALL)
        
        # 檢查內容是否已有 Citation 區塊
        if '## Citation' in content:
            # 已有 Citation，替換
            pattern = r'---[\s\S]*?## Citation[\s\S]*?---[\s\S]*?'
            content = re.sub(pattern, citation_block.strip() + '\n', content, count=1)
        else:
            # 新增 Citation
            content = content.strip() + '\n\n' + citation_block
        
        return content


# ============================================================================
# Citation 驗證
# ============================================================================

class CitationValidator:
    """Citation 驗證器"""
    
    def __init__(self, wiki_dir: Path):
        self.wiki_dir = wiki_dir
        self.concepts_dir = wiki_dir / "concepts"
        self.summaries_dir = wiki_dir / "summaries"
        self.issues: List[Dict] = []
    
    def validate_all(self) -> List[Dict]:
        """驗證所有 Wiki 頁面的 Citation"""
        self.issues = []
        
        # 檢查 concepts
        if self.concepts_dir.exists():
            for md_file in self.concepts_dir.glob("*.md"):
                self._validate_file(md_file)
        
        # 檢查 summaries
        if self.summaries_dir.exists():
            for md_file in self.summaries_dir.glob("*.md"):
                self._validate_file(md_file)
        
        return self.issues
    
    def _validate_file(self, file_path: Path):
        """驗證單個檔案"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            return
        
        # 檢查是否有 Citation 區塊
        if '## Citation' not in content:
            self.issues.append({
                'file': file_path.name,
                'type': 'missing_citation',
                'message': '缺少 Citation 區塊'
            })
            return
        
        # 解析 Citation 資訊
        citation_info = self._parse_citation(content)
        
        # 檢查必要欄位
        if not citation_info['source']:
            self.issues.append({
                'file': file_path.name,
                'type': 'missing_source',
                'message': 'Source 欄位為空'
            })
        
        if not citation_info['confidence']:
            self.issues.append({
                'file': file_path.name,
                'type': 'missing_confidence',
                'message': 'Confidence 欄位為空'
            })
        
        if not citation_info['verified']:
            self.issues.append({
                'file': file_path.name,
                'type': 'missing_verified',
                'message': 'Verified 欄位為空'
            })
        
        # 檢查 confidence 值是否有效
        if citation_info['confidence'] and citation_info['confidence'] not in ['high', 'medium', 'low']:
            self.issues.append({
                'file': file_path.name,
                'type': 'invalid_confidence',
                'message': f"Confidence 值 '{citation_info['confidence']}' 無效，應為 high/medium/low"
            })
    
    def _parse_citation(self, content: str) -> Dict:
        """解析 Citation 區塊"""
        result = {'source': '', 'confidence': '', 'verified': '', 'raw_files': ''}
        
        # 找 Citation 區塊
        match = re.search(r'## Citation\s*\n(.*?)(?=---|$)', content, re.DOTALL)
        if not match:
            return result
        
        citation_text = match.group(1)
        
        # 解析各欄位
        source_match = re.search(r'\*\*Source\*\*:\s*(.+)', citation_text)
        if source_match:
            result['source'] = source_match.group(1).strip()
        
        confidence_match = re.search(r'\*\*Confidence\*\*:\s*(.+)', citation_text)
        if confidence_match:
            result['confidence'] = confidence_match.group(1).strip().lower()
        
        verified_match = re.search(r'\*\*Verified\*\*:\s*(.+)', citation_text)
        if verified_match:
            result['verified'] = verified_match.group(1).strip()
        
        raw_files_match = re.search(r'\*\*Raw Files\*\*:\s*(.+)', citation_text)
        if raw_files_match:
            result['raw_files'] = raw_files_match.group(1).strip()
        
        return result
    
    def generate_report(self) -> str:
        """產生驗證報告"""
        if not self.issues:
            return "# Citation 驗證報告\n\n✅ 所有頁面的 Citation 都符合規範！"
        
        report = "# Citation 驗證報告\n\n"
        report += f"發現 {len(self.issues)} 個問題：\n\n"
        
        # 分類
        by_type = {}
        for issue in self.issues:
            t = issue['type']
            if t not in by_type:
                by_type[t] = []
            by_type[t].append(issue)
        
        for type_name, items in by_type.items():
            report += f"## {type_name.replace('_', ' ').title()}\n\n"
            for item in items:
                report += f"- `{item['file']}`: {item['message']}\n"
            report += "\n"
        
        return report


def validate_citations(wiki_dir: Path) -> List[Dict]:
    """驗證 Wiki 目錄中所有頁面的 Citation"""
    validator = CitationValidator(wiki_dir)
    return validator.validate_all()


def add_citation_to_page(file_path: Path, sources: List[str], confidence: str = "medium", raw_files: List[str] = None):
    """
    為現有頁面新增 Citation
    
    Args:
        file_path: 頁面檔案路徑
        sources: 來源列表
        confidence: 信心程度
        raw_files: 原始檔案列表
    """
    template = CitationTemplate()
    
    # 讀取現有內容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 新增 Citation
    new_content = template.add_citation_header(
        content,
        sources=sources,
        confidence=confidence,
        raw_files=raw_files
    )
    
    # 寫回
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)


# ============================================================================
# 命令列介面
# ============================================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="SumoNoteBook Citation 追蹤系統")
    subparsers = parser.add_subparsers(dest='command', help='子命令')
    
    # validate 命令
    validate_parser = subparsers.add_parser('validate', help='驗證所有頁面的 Citation')
    validate_parser.add_argument('--wiki-dir', default='c:/butler_sumo/library/SumoNoteBook/Sumo_wiki', help='Wiki 目錄')
    
    # add 命令
    add_parser = subparsers.add_parser('add', help='為頁面新增 Citation')
    add_parser.add_argument('file', help='檔案路徑')
    add_parser.add_argument('sources', nargs='+', help='來源列表')
    add_parser.add_argument('--confidence', default='medium', choices=['high', 'medium', 'low'], help='信心程度')
    add_parser.add_argument('--raw-files', nargs='*', help='原始檔案列表')
    
    args = parser.parse_args()
    
    if args.command == 'validate':
        wiki_dir = Path(args.wiki_dir)
        validator = CitationValidator(wiki_dir)
        validator.validate_all()
        
        print(validator.generate_report())
        
    elif args.command == 'add':
        file_path = Path(args.file)
        add_citation_to_page(
            file_path,
            args.sources,
            args.confidence,
            args.raw_files
        )
        print(f"已為 {file_path.name} 新增 Citation")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()