"""
SumoNoteBook Lint 矛盾偵測升級
============================
強化 health_check 的矛盾偵測功能

功能：
- detect_contradictions() - 偵測主題相同但結論相反的聲明
- 支援多層次矛盾檢測
- 生成詳細的矛盾報告

使用方式：
```python
from contradiction_detector import ContradictionDetector, run_contradiction_check

# 執行矛盾檢查
detector = ContradictionDetector(wiki_dir)
contradictions = detector.detect_all()

# 或使用便捷函數
results = run_contradiction_check(wiki_dir)
```
"""

import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict
import hashlib


# ============================================================================
# 矛盾偵測器
# ============================================================================

class ContradictionDetector:
    """
    矛盾偵測器
    
    偵測 Wiki 頁面中的矛盾聲明：
    1. 同一主題在不同頁面的衝突描述
    2. 同一頁面內的前後不一致
    3. 相反的肯定與否定聲明
    """
    
    # 矛盾關鍵詞對（用於檢測相反聲明）
    CONTRADICTION_PAIRS = [
        # 絕對肯定 vs 絕對否定
        (r'是\s+正確', r'是\s+錯誤'),
        (r'有效', r'無效'),
        (r'可行', r'不可行'),
        (r'可以', r'不可以'),
        (r'應該', r'不應該'),
        (r'必須', r'不必'),
        (r'有益', r'有害'),
        (r'成功', r'失敗'),
        (r'好', r'壞'),
        (r'正面', r'負面'),
        (r'支持', r'反對'),
        (r'讚成', r'反對'),
        
        # 數值矛盾
        (r'\d+%\s+(可能|會)', r'0%\s+(可能|會)'),
        (r'\d+\s+倍', r'\d+\s+分之一'),
        
        # 時間矛盾
        (r'一直', r'從不'),
        (r'總是', r'從不'),
        (r'永遠', r'從不'),
        (r'曾經', r'從未'),
    ]
    
    # 衝突概念關鍵詞（相似但相反的概念）
    CONFLICTING_CONCEPTS = [
        ('agent', 'human'),
        ('automated', 'manual'),
        ('centralized', 'decentralized'),
        ('static', 'dynamic'),
        ('closed', 'open'),
        ('synchronous', 'asynchronous'),
        ('deterministic', 'probabilistic'),
        ('serial', 'parallel'),
        ('monolithic', 'modular'),
        ('tightly coupled', 'loosely coupled'),
    ]
    
    def __init__(self, wiki_dir: Path):
        self.wiki_dir = wiki_dir
        self.concepts_dir = wiki_dir / "concepts"
        self.summaries_dir = wiki_dir / "summaries"
        self.contradictions: List[Dict] = []
        
    def detect_all(self) -> List[Dict]:
        """執行所有矛盾偵測"""
        self.contradictions = []
        
        # 1. 檢測頁面內矛盾
        self._detect_within_page_contradictions()
        
        # 2. 檢測跨頁面矛盾
        self._detect_cross_page_contradictions()
        
        # 3. 檢測概念衝突
        self._detect_concept_conflicts()
        
        return self.contradictions
    
    def _detect_within_page_contradictions(self):
        """偵測單一頁面內的矛盾"""
        if not self.concepts_dir.exists():
            return
            
        for md_file in self.concepts_dir.glob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception:
                continue
                
            page_contradictions = self._find_contradictions_in_content(content)
            
            if page_contradictions:
                self.contradictions.append({
                    'type': 'within_page',
                    'file': md_file.name,
                    'contradictions': page_contradictions
                })
    
    def _detect_cross_page_contradictions(self):
        """偵測跨頁面的矛盾"""
        if not self.concepts_dir.exists():
            return
            
        # 讀取所有概念
        concepts = {}
        for md_file in self.concepts_dir.glob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    concepts[md_file.stem] = f.read()
            except Exception:
                continue
        
        # 找出相似主題的頁面
        similar_groups = self._find_similar_topics(concepts)
        
        # 檢查每組相似主題是否有矛盾
        for group in similar_groups:
            if len(group) < 2:
                continue
                
            cross_contradictions = []
            for i, page1 in enumerate(group):
                for page2 in group[i+1:]:
                    # 檢查這兩個頁面是否有相反的結論
                    contradiction = self._check_pages_have_opposing_views(
                        concepts[page1], concepts[page2]
                    )
                    if contradiction:
                        cross_contradictions.append({
                            'page1': page1,
                            'page2': page2,
                            'reason': contradiction
                        })
            
            if cross_contradictions:
                self.contradictions.append({
                    'type': 'cross_page',
                    'pages': group,
                    'contradictions': cross_contradictions
                })
    
    def _detect_concept_conflicts(self):
        """偵測概念衝突"""
        if not self.concepts_dir.exists():
            return
            
        for md_file in self.concepts_dir.glob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception:
                continue
            
            conflicts = self._find_conflicting_concepts(content)
            
            if conflicts:
                self.contradictions.append({
                    'type': 'concept_conflict',
                    'file': md_file.name,
                    'conflicts': conflicts
                })
    
    def _find_contradictions_in_content(self, content: str) -> List[Dict]:
        """在內容中找矛盾"""
        results = []
        
        # 檢查矛盾關鍵詞對
        lines = content.split('\n')
        for i, line in enumerate(lines):
            for pos_pattern, neg_pattern in self.CONTRADICTION_PAIRS:
                if re.search(pos_pattern, line) or re.search(neg_pattern, line):
                    # 檢查附近是否有相反的聲明
                    context_start = max(0, i - 3)
                    context_end = min(len(lines), i + 4)
                    context = '\n'.join(lines[context_start:context_end])
                    
                    # 尋找相反的陳述
                    for p2, n2 in self.CONTRADICTION_PAIRS:
                        if p2 != pos_pattern and re.search(n2, context):
                            results.append({
                                'line': i + 1,
                                'statement': line.strip(),
                                'context': context,
                                'pair': (pos_pattern, neg_pattern)
                            })
                            break
        
        return results
    
    def _find_similar_topics(self, concepts: Dict[str, str]) -> List[List[str]]:
        """找出相似主題的頁面群組"""
        # 簡單實現：基於標題相似性
        topics = {}
        
        for name, content in concepts.items():
            # 提取關鍵詞
            words = set(re.findall(r'\b[a-zA-Z]{4,}\b', content.lower()))
            topics[name] = words
        
        # 找出有共同關鍵詞的頁面
        groups = []
        processed = set()
        
        for name1 in topics:
            if name1 in processed:
                continue
                
            group = [name1]
            for name2 in topics:
                if name1 == name2 or name2 in processed:
                    continue
                    
                # 計算 Jaccard 相似度
                intersection = len(topics[name1] & topics[name2])
                union = len(topics[name1] | topics[name2])
                similarity = intersection / union if union > 0 else 0
                
                if similarity > 0.2:  # 相似度閾值
                    group.append(name2)
            
            if len(group) > 1:
                groups.append(group)
                processed.update(group)
        
        return groups
    
    def _check_pages_have_opposing_views(self, content1: str, content2: str) -> Optional[str]:
        """檢查兩頁面是否有相反觀點"""
        # 提取雙方的主要結論/觀點
        conclusions1 = self._extract_conclusions(content1)
        conclusions2 = self._extract_conclusions(content2)
        
        # 檢查是否有相反的結論
        for c1 in conclusions1:
            for c2 in conclusions2:
                if self._are_opposing(c1, c2):
                    return f"'{c1}' vs '{c2}'"
        
        return None
    
    def _extract_conclusions(self, content: str) -> List[str]:
        """提取主要結論"""
        conclusions = []
        
        # 找結論文法（如：總之、因此、最終、結論是）
        for line in content.split('\n'):
            if any(kw in line for kw in ['總之', '因此', '結論', '最終', '總結', '總結果']):
                # 提取簡短結論
                match = re.search(r'[，。；][^，。；]*', line)
                if match:
                    conclusions.append(match.group(0))
        
        return conclusions[:5]  # 最多5個
    
    def _are_opposing(self, statement1: str, statement2: str) -> bool:
        """判斷兩個聲明是否相反"""
        s1 = statement1.lower()
        s2 = statement2.lower()
        
        # 檢查是否有明顯相反的詞
        opposing_pairs = [
            ('好', '壞'), ('是', '否'), ('對', '錯'),
            ('有益', '有害'), ('正確', '錯誤'),
            ('有效', '無效'), ('成功', '失敗'),
        ]
        
        for pos, neg in opposing_pairs:
            if (pos in s1 and neg in s2) or (neg in s1 and pos in s2):
                return True
        
        return False
    
    def _find_conflicting_concepts(self, content: str) -> List[Dict]:
        """找出內容中的概念衝突"""
        conflicts = []
        content_lower = content.lower()
        
        for concept1, concept2 in self.CONFLICTING_CONCEPTS:
            if concept1 in content_lower and concept2 in content_lower:
                # 找到可能衝突的概念
                conflicts.append({
                    'concept1': concept1,
                    'concept2': concept2,
                    'severity': 'warning'
                })
        
        return conflicts
    
    def generate_report(self) -> str:
        """產生矛盾檢測報告"""
        if not self.contradictions:
            return "# 矛盾檢測報告\n\n[OK] 沒有偵測到矛盾！"
        
        report = "# 矛盾檢測報告\n\n"
        report += f"[WARNING] 偵測到 {len(self.contradictions)} 組潛在矛盾：\n\n"
        
        for i, item in enumerate(self.contradictions, 1):
            report += f"## {i}. {item['type'].replace('_', ' ').title()}\n\n"
            
            if item['type'] == 'within_page':
                report += f"**檔案**: {item['file']}\n\n"
                for contr in item['contradictions'][:3]:
                    report += f"- 第 {contr['line']} 行: {contr['statement'][:50]}...\n"
                    
            elif item['type'] == 'cross_page':
                report += f"**相關頁面**: {', '.join(item['pages'])}\n\n"
                for contr in item['contradictions']:
                    report += f"- {contr['page1']} ↔ {contr['page2']}: {contr['reason']}\n"
                    
            elif item['type'] == 'concept_conflict':
                report += f"**檔案**: {item['file']}\n\n"
                for conflict in item['conflicts']:
                    report += f"- {conflict['concept1']} vs {conflict['concept2']}\n"
            
            report += "\n"
        
        return report


def run_contradiction_check(wiki_dir: Path) -> Dict:
    """
    執行矛盾檢查的便捷函數
    
    Args:
        wiki_dir: Wiki 目錄路徑
    
    Returns:
        包含 contradictions 和 report 的字典
    """
    detector = ContradictionDetector(wiki_dir)
    contradictions = detector.detect_all()
    report = detector.generate_report()
    
    return {
        'contradictions': contradictions,
        'report': report,
        'count': len(contradictions),
        'timestamp': datetime.now().isoformat()
    }


# ============================================================================
# 整合進現有 health_check
# ============================================================================

def enhanced_check_contradictions(wiki_dir: Path) -> Dict:
    """
    強化的矛盾檢查（可整合進 health_check_v3.py）
    
    Returns:
        矛盾檢查結果字典
    """
    return run_contradiction_check(wiki_dir)


# ============================================================================
# 命令列介面
# ============================================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="SumoNoteBook 矛盾偵測")
    parser.add_argument('--wiki-dir', default='c:/butler_sumo/library/SumoNoteBook/Sumo_wiki', 
                       help='Wiki 目錄')
    parser.add_argument('--output', '-o', help='輸出報告檔案')
    
    args = parser.parse_args()
    
    wiki_dir = Path(args.wiki_dir)
    results = run_contradiction_check(wiki_dir)
    
    print(results['report'])
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(results['report'])
        print(f"\n報告已儲存至: {args.output}")


if __name__ == "__main__":
    main()