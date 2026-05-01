# Grad_counter

- 來自研究生的逆襲，抓住 agent 的救命繩

Grad_counter 是一個以 **AI Agent Scheduler** 為核心的專案：  
幫你管理課表、作業、meeting、學習資源、每日進度，並自動做排程與重排（re-schedule）。

這個 repo 的定位是 Agent 的「**記憶庫 + 規則庫 + 報表庫**」，讓 Agent 可以穩定地讀寫資料，而不是只靠對話臨時記憶。

---

## 1) 目前進度（已完成）

- 已建立完整資料夾骨架：`config/`、`memory/`、`reports/`、`logs/`、`resources/`、`src/`
- 已定義並建立核心 JSON 檔案（可直接給 Agent 用）
- 已建立週報/月報模板
- 已建立 Python 第一版模組骨架（含 `memory_manager`、`scheduler`、`agent_core`）
- `python src/main.py` 可執行，會寫入當月 schedule

---

## 2) 專案結構

```text
Grad_counter/
├── config/
│   ├── agent_instructions.md
│   ├── search_engines.json
│   └── system_settings.json
│
├── memory/
│   ├── profile.json
│   ├── backlog.json
│   ├── schedule/
│   │   └── 2026-05.json
│   └── tracker/
│       └── daily_logs.json
│
├── reports/
│   ├── weekly/
│   │   └── WEEKLY_REPORT_TEMPLATE.md
│   └── monthly/
│       └── MONTHLY_REPORT_TEMPLATE.md
│
├── resources/
│   ├── courses/
│   │   ├── Data_Structure/
│   │   └── Machine_Learning/
│   └── self_learning/
│
├── logs/
│   └── agent_action.log
│
└── src/
    ├── main.py
    ├── memory_manager.py
    ├── scheduler.py
    ├── search_engine.py
    ├── reporter.py
    └── agent_core.py
```

---

## 3) 核心資料檔案說明

### `memory/profile.json`

- 長期記憶：作息、固定課程、學習主題偏好
- 固定課程可綁定 `resource_dir`，供後續自動掃描新講義

### `memory/backlog.json`

- 任務池與學習資源池
- 每個項目都有 `id`，可被 schedule 的 `linked_id` 關聯
- 支援 `attachments` 指向實體檔案（`resources/...`）

### `memory/schedule/YYYY-MM.json`

- 每日排程輸出（固定行程 + 動態行程）
- key 使用 `YYYY-MM-DD`

### `memory/tracker/daily_logs.json`

- 每日追蹤與反思資料
- 週報/月報的主要輸入來源

---

## 4) 使用方式（目前版）

1. 先更新你的個人設定  
   - `memory/profile.json`
2. 把任務/學習內容放入 backlog  
   - `memory/backlog.json`
3. 執行排程  

   ```bash
   python src/main.py
   ```

4. 查看本月 schedule 是否更新  
   - `memory/schedule/YYYY-MM.json`
5. 追蹤 Agent 操作紀錄  
   - `logs/agent_action.log`

---

## 5) 資源檔案（講義/教材）管理

- 請把實際檔案放在 `resources/` 下，並在 backlog 的 `attachments` 填入相對路徑。
- 目前 `resources/` 內有 placeholder 檔案，之後可直接以真實 PDF/ZIP 覆蓋。

---

## 6) 開發中與下一步

- 將 `agent_core.py` 接上 LLM（決策輸出為安全 CRUD 指令）
- 強化 `scheduler.py`（衝突處理、deadline 驅動、疲勞感知重排）
- 實作 `reporter.py` 自動產生每週/每月報表
- 加入 RAG 流程：讀取 `resources/` 做講義摘要與預習建議

---

## 7) 設計原則

- JSON 結構固定，避免 Agent 亂寫格式
- 不做硬刪除：使用 `status`（`pending / in_progress / completed / dropped`）保留歷史
- 每次更新皆可追蹤（`agent_action.log`）
