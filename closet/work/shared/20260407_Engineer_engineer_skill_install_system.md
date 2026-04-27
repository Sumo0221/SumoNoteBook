# Skills 安裝系統

## 📋 文件資訊
- **版本：** 1.0
- **建立日期：** 2026-04-03
- **目的：** 設計 .skill 封裝格式，建立安裝驗證機制

---

## 🎯 目的

標準化 Skill 安裝流程，確保一致性，簡化安裝過程並減少安裝錯誤，便於 Skill 分發和共享。

---

## 📦 .skill 封裝格式

### 格式類型

| 類型 | 副檔名 | 說明 | 適用場景 |
|------|--------|------|---------|
| 目錄格式 | `.skill/` | 資料夾結構 | 開發階段、本地使用 |
| 壓縮格式 | `.skill.zip` | ZIP 壓縮包 | 分發、下載 |

### 目錄結構

```
my-awesome-skill.skill/
├── manifest.json          # Skill 元資料
├── SKILL.md               # 技能說明文件
├── scripts/               # 輔助腳本目錄
│   ├── install.sh         # 安裝腳本（可選）
│   └── setup.py           # Python 安裝腳本（可選）
├── assets/                # 資源檔案目錄（可選）
│   ├── icon.png           # 圖示
│   └── templates/         # 範本檔案
├── references/            # 參考文檔（可選）
│   └── README.md          # 額外說明
└── .skillignore           # 安裝時忽略的檔案
```

---

## 📋 manifest.json 規範

```json
{
  "name": "my-awesome-skill",
  "version": "1.0.0",
  "display_name": "我的超棒技能",
  "description": "這個技能可以做很棒的事情",
  "author": {
    "name": "開發者名稱",
    "email": "developer@example.com",
    "url": "https://example.com"
  },
  "license": "MIT",
  "homepage": "https://github.com/user/my-awesome-skill",
  "repository": "https://github.com/user/my-awesome-skill.git",
  "tags": ["automation", "productivity", "coding"],
  "triggers": {
    "primary": ["關鍵字1", "關鍵字2"],
    "secondary": ["相關關鍵字"],
    "fuzzy": ["可能拼錯的"]
  },
  "compatibility": {
    "min_openclaw_version": "1.0.0",
    "platform": ["windows", "linux", "macos"]
  },
  "dependencies": {
    "required": [],
    "optional": []
  },
  "permissions": {
    "tools": ["read", "write", "exec"],
    "network": true,
    "filesystem": true
  },
  "install": {
    "method": "copy",       // copy | script | pip
    "target_dir": "memory/skills"
  },
  "uninstall": {
    "method": "delete"     // delete | script
  }
}
```

### 欄位說明

| 欄位 | 類型 | 必填 | 說明 |
|------|------|------|------|
| `name` | string | ✅ | 唯一識別名稱（小寫、英文、底線） |
| `version` | string | ✅ | SemVer 格式版本號 |
| `display_name` | string | ✅ | 顯示名稱（可含中文） |
| `description` | string | ✅ | 簡短描述 |
| `author` | object | ❌ | 作者資訊 |
| `tags` | array | ❌ | 標籤分類 |
| `triggers` | object | ❌ | 觸發關鍵字 |
| `compatibility` | object | ❌ | 相容性資訊 |
| `dependencies` | object | ❌ | 依賴套件 |
| `permissions` | object | ❌ | 權限需求 |
| `install` | object | ❌ | 安裝設定 |

---

## 🔧 安裝流程

### 流程圖

```
┌─────────────────────────────────────────────────────────┐
│                   Skill 安裝流程                         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  [開始安裝] ──► [解析 .skill 檔案] ──► [驗證 manifest]    │
│                                              │           │
│                                              ▼           │
│                               ┌────────────────────┐    │
│                               │ manifest 格式正確？ │    │
│                               └──────────┬─────────┘    │
│                              是            │ 否          │
│                    ┌───────────┴───┐       │            │
│                    ▼               ▼       ▼            │
│            [檢查依賴]        [返回錯誤:     │            │
│                    │         manifest 無效]              │
│                    ▼                                    │
│         ┌──────────────────┐                           │
│         │ 依賴都滿足？      │                           │
│         └────────┬─────────┘                           │
│        是         │ 否                                  │
│        │    ┌────▼─────┐                               │
│        │    │ 安裝依賴 │                               │
│        │    └────┬─────┘                               │
│        │         │                                     │
│        ▼         ▼                                     │
│   [複製檔案到    │                                     │
│    目標目錄]     │                                     │
│        │         │                                     │
│        ▼         │                                     │
│   [執行鉤子      │                                     │
│    (可選)]       │                                     │
│        │         │                                     │
│        ▼         │                                     │
│   [驗證安裝]     │                                     │
│        │         │                                     │
│        ▼         │                                     │
│  ┌────────────┐  │                                     │
│  │ 安裝成功？  │  │                                     │
│  └────┬───────┘  │                                     │
│       │          │                                     │
│       ▼          ▼                                     │
│  [返回成功]  [回滾變更]                                 │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 💻 安裝驗證腳本

### Python 安裝器

```python
import os
import json
import shutil
import zipfile
from pathlib import Path
from typing import Optional, List, Tuple

class SkillInstaller:
    """Skill 安裝器"""
    
    SKILLS_DIR = Path("memory/skills")
    
    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self.manifest = None
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def install(self) -> Tuple[bool, str]:
        """
        安裝 Skill
        
        返回: (成功與否, 訊息)
        """
        # 1. 解析 Skill 檔案
        if not self._parse():
            return False, f"解析失敗: {'; '.join(self.errors)}"
        
        # 2. 驗證 manifest
        if not self._validate_manifest():
            return False, f"驗證失敗: {'; '.join(self.errors)}"
        
        # 3. 檢查依賴
        if not self._check_dependencies():
            return False, f"依賴檢查失敗: {'; '.join(self.errors)}"
        
        # 4. 檢查是否已存在
        skill_name = self.manifest["name"]
        target_dir = self.SKILLS_DIR / skill_name
        
        if target_dir.exists():
            # 檢查版本
            existing_manifest = target_dir / "manifest.json"
            if existing_manifest.exists():
                with open(existing_manifest) as f:
                    existing = json.load(f)
                    if existing["version"] == self.manifest["version"]:
                        return False, f"Skill {skill_name} v{existing['version']} 已安裝"
                    else:
                        self.warnings.append(f"將更新 {existing['version']} -> {self.manifest['version']}")
        
        # 5. 複製檔案
        if not self._copy_files(target_dir):
            self._rollback(target_dir)
            return False, f"複製失敗: {'; '.join(self.errors)}"
        
        # 6. 執行安裝後鉤子
        if not self._run_install_hook(target_dir):
            self._rollback(target_dir)
            return False, f"安裝鉤子失敗: {'; '.join(self.errors)}"
        
        # 7. 驗證安裝
        if not self._verify_install(target_dir):
            self._rollback(target_dir)
            return False, f"驗證失敗: {'; '.join(self.errors)}"
        
        return True, f"Skill {skill_name} v{self.manifest['version']} 安裝成功"
    
    def _parse(self) -> bool:
        """解析 Skill 檔案"""
        self.errors.clear()
        
        if not self.skill_path.exists():
            self.errors.append(f"檔案不存在: {self.skill_path}")
            return False
        
        # 解壓縮 ZIP（如果是 ZIP 格式）
        if self.skill_path.suffix == ".zip":
            extract_dir = self.SKILLS_DIR / f".tmp_{self.skill_path.stem}"
            try:
                with zipfile.ZipFile(self.skill_path, "r") as zf:
                    zf.extractall(extract_dir)
                self.skill_path = extract_dir
            except zipfile.BadZipFile:
                self.errors.append("無效的 ZIP 檔案")
                return False
        
        # 讀取 manifest
        manifest_path = self.skill_path / "manifest.json"
        if not manifest_path.exists():
            self.errors.append("缺少 manifest.json")
            return False
        
        try:
            with open(manifest_path) as f:
                self.manifest = json.load(f)
        except json.JSONDecodeError as e:
            self.errors.append(f"manifest.json 格式錯誤: {e}")
            return False
        
        return True
    
    def _validate_manifest(self) -> bool:
        """驗證 manifest 必要欄位"""
        self.errors.clear()
        required_fields = ["name", "version", "display_name", "description"]
        
        for field in required_fields:
            if field not in self.manifest:
                self.errors.append(f"缺少必要欄位: {field}")
        
        # 驗證 name 格式
        name = self.manifest.get("name", "")
        if not name.replace("_", "").isalnum():
            self.errors.append("name 只能包含字母、數字和底線")
        
        # 驗證 version 格式 (SemVer)
        version = self.manifest.get("version", "")
        import re
        if not re.match(r"^\d+\.\d+\.\d+$", version):
            self.errors.append("version 必須為 SemVer 格式 (如: 1.0.0)")
        
        return len(self.errors) == 0
    
    def _check_dependencies(self) -> bool:
        """檢查依賴"""
        deps = self.manifest.get("dependencies", {})
        required = deps.get("required", [])
        
        for dep in required:
            if not self._check_dependency(dep):
                self.errors.append(f"缺少依賴: {dep}")
        
        return len(self.errors) == 0
    
    def _check_dependency(self, dep: str) -> bool:
        """檢查單個依賴"""
        # 簡化版本：僅檢查 Python 套件
        if dep.startswith("pip:"):
            package = dep[4:]
            try:
                __import__(package)
                return True
            except ImportError:
                return False
        return True
    
    def _copy_files(self, target_dir: Path) -> bool:
        """複製檔案到目標目錄"""
        try:
            # 創建目標目錄
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # 讀取 .skillignore
            ignore_file = self.skill_path / ".skillignore"
            ignore_patterns = []
            if ignore_file.exists():
                with open(ignore_file) as f:
                    ignore_patterns = [line.strip() for line in f if line.strip() and not line.startswith("#")]
            
            # 複製所有檔案
            for item in self.skill_path.iterdir():
                if item.name.startswith("."):
                    continue
                if item.name in [".skillignore", ".tmp_*"]:
                    continue
                
                dest = target_dir / item.name
                
                if item.is_dir():
                    shutil.copytree(item, dest, ignore=shutil.ignore_patterns(*ignore_patterns))
                else:
                    shutil.copy2(item, dest)
            
            return True
        except Exception as e:
            self.errors.append(f"複製失敗: {e}")
            return False
    
    def _rollback(self, target_dir: Path):
        """回滾變更"""
        if target_dir.exists():
            shutil.rmtree(target_dir, ignore_errors=True)
        
        # 清理暫存目錄
        if self.skill_path.name.startswith(".tmp_"):
            shutil.rmtree(self.skill_path, ignore_errors=True)
    
    def _run_install_hook(self, target_dir: Path) -> bool:
        """執行安裝後鉤子"""
        install_script = self.skill_path / "scripts" / "install.sh"
        setup_script = self.skill_path / "scripts" / "setup.py"
        
        if install_script.exists():
            # 執行 shell 腳本
            import subprocess
            result = subprocess.run([str(install_script)], cwd=str(target_dir))
            if result.returncode != 0:
                self.errors.append("install.sh 執行失敗")
                return False
        
        if setup_script.exists():
            # 執行 Python 安裝腳本
            import subprocess
            result = subprocess.run(["python", str(setup_script)], cwd=str(target_dir))
            if result.returncode != 0:
                self.errors.append("setup.py 執行失敗")
                return False
        
        return True
    
    def _verify_install(self, target_dir: Path) -> bool:
        """驗證安裝"""
        required_files = ["manifest.json", "SKILL.md"]
        
        for filename in required_files:
            if not (target_dir / filename).exists():
                self.errors.append(f"缺少必要檔案: {filename}")
        
        return len(self.errors) == 0


def install_skill(skill_path: str) -> Tuple[bool, str]:
    """安裝 Skill 的便捷函數"""
    installer = SkillInstaller(skill_path)
    return installer.install()
```

---

## 🔍 驗證清單

### 安裝前驗證

- [ ] 檔案/目錄存在
- [ ] manifest.json 格式正確
- [ ] 必要欄位齊全
- [ ] name 格式正確（小寫、英文、底線）
- [ ] version 為 SemVer 格式
- [ ] 依賴套件已滿足

### 安裝後驗證

- [ ] 檔案已複製到目標目錄
- [ ] manifest.json 存在
- [ ] SKILL.md 存在
- [ ] 權限設定正確
- [ ] 符號連結已建立（如有）

---

## 📦 安裝範例

### 命令列安裝

```bash
# 安裝本地 .skill 目錄
python -m skill_installer install ./my-awesome-skill.skill

# 安裝 ZIP 格式
python -m skill_installer install ./my-awesome-skill.skill.zip

# 從 URL 安裝
python -m skill_installer install https://example.com/my-awesome-skill.skill.zip

# 列出已安裝的 Skills
python -m skill_installer list

# 移除 Skill
python -m skill_installer uninstall my-awesome-skill
```

### 程式碼安裝

```python
from skill_installer import install_skill

success, message = install_skill("./my-awesome-skill.skill")
print(message)
```

---

## 📝 .skillignore 範例

```
# 安裝時忽略的檔案

# 版本控制
.git/
.svn/

# 開發檔案
*.psd
*.ai
*.sketch
drafts/

# 測試檔案
tests/
__pycache__/
*.pyc

# 隱藏檔案（除非必要）
.*
```

---

## 📊 版本管理

### 版本相容性檢查

```python
from packaging import version

def check_compatibility(skill_version: str, min_version: str) -> bool:
    """檢查版本是否相容"""
    try:
        return version.parse(skill_version) >= version.parse(min_version)
    except Exception:
        return False
```

### 更新策略

| 類型 | 說明 | 操作 |
|------|------|------|
| Patch 更新 | 1.0.**0** → 1.0.**1** | 自動更新 |
| Minor 更新 | 1.**0**.0 → 1.**1**.0 | 提示更新，用戶確認 |
| Major 更新 | **1**.0.0 → **2**.0.0 | 需卸載舊版後安裝 |

---

## ✅ 預期效益

1. **簡化安裝流程**
   - 一鍵安裝 .skill 檔案
   - 自動處理依賴

2. **減少安裝錯誤**
   - manifest 驗證
   - 安裝後驗證

3. **便於分發和共享**
   - 標準化封裝格式
   - 可發布至 Skill Store

4. **支援版本管理**
   - SemVer 版本控制
   - 相容性檢查

---

## 📝 實作檢查清單

- [x] 設計 .skill 目錄結構
- [x] 定義 manifest.json 規範
- [x] 實作安裝流程圖
- [x] 提供 Python 安裝器
- [x] 建立安裝驗證清單
- [x] 提供 .skillignore 範例
- [x] 設計版本管理策略
- [ ] 實作命令列工具
- [ ] 支援從 URL 安裝
- [ ] 建立 Skill Store 整合
