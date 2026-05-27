# 台科大資管 Python 考試作答區

---

## 基本資料

**學號：** B11409051  
**系級：** 資管系大一  
**姓名：** 郭柏佑  

---

## 一、 原始碼分析報告 (Static Analysis) (共8小題，每小題3分，總共24分)

### 1.1 變數與邏輯對照表

| 原始變數名稱 | 代表意義 (Business Logic) | 建議修正名稱 |
|---|---|---|
| Q1 l1 (in load_proc) |是從 lib_data.txt 讀出的所有原始行資料 | file_lines |
| Q2 d2 (in main) |是整個圖書資料庫的列表，每筆元素為一個字典，包含書名、ISBN、狀態。 | library_data |
| Q3 c_res (in check) |這個函式檢查給定 ISBN 是否已存在於 d2 中 | check_isbn_exists |

### 1.2 壞味道 (Code Smells) 診斷

請列出原程式碼中至少 5 個嚴重的設計問題，並說明為什麼不好：

- **Q1：** `d2` 當作全域可變資料結構
  - `d2` 定義在全域作用域，所有函式直接修改它，造成狀態散落且難以測試、除錯。
  - 這樣的設計讓程式難以重用，若要新增記憶體處理、單元測試或多次呼叫 `main()` 都會很麻煩。
- **Q2：** 檔案操作沒有使用 `with` 也沒有例外處理
  - `open(F_NAME, "r", encoding="utf-8")`、`open(F_NAME, "w", encoding="utf-8")` 沒有 `with`，若讀寫途中發生錯誤會造成檔案遺失或檔案未關閉。
  - 這種寫法不安全，程式遇到 I/O 錯誤時會直接崩潰，使用者無法優雅恢復。
- **Q3：** 變數命名完全無意義
  - `l1`, `d2`, `c_res`, `v` 等名稱不說明用途，讓程式可讀性極差。
  - 這會增加維護成本，其他開發者甚至自己回來看也很快忘記每個變數是什麼。
- **Q4：** 資料格式解析非常脆弱
  - `load_proc()` 假設每一行一定有 `@@` 與 `##`，沒有做任何驗證。
  - 如果檔案格式錯誤或資料不完整，程式會發生 `IndexError` 或產生錯誤資料。
- **Q5：** 沒有資料模型或結構化物件
  - 使用 `dict` 存書籍資料，且 key 名稱也是單個字母 `t`, `i`, `s`，可讀性差。
  - 若改成 `Book` 物件或命名更清楚的欄位，整體性會好很多。

---

## 二、 Vibe-Coding 協作紀錄 (共6小題，每小題3分，總共18分)

請記錄你如何引導 GitHub Copilot 進行重構。
重構的要求，請根據題目卷以及你發現的 Code Smells 來進行。

### 2.1 關鍵 Prompt 紀錄

請貼出你對 AI 下達過最有效的 3 個 Prompt：

```log
Prompt A：請把 legacy_lib.py 重構成 modern_library.py，避免全域變數、改用 JSON 儲存、並加入明確命名與例外處理。
Prompt B：請新增 add/show/borrow/exit 指令，borrow 需更新 status，exit 需寫回 books.json。
Prompt C：請使用 with 讀寫檔案並改成 ISBN 檢查函式 isbn_exists，確保格式錯誤不會崩潰。
```

### 2.2 AI 錯誤處理

1. AI 在撰寫過程中是否有出錯？（例如：漏寫了某個功能、語法錯誤）你是如何發現並請它修正的？

   有。初版設計若遇到 `books.json` 不存在或資料格式錯誤時，程式會直接失敗。後來我要求補上檔案載入例外處理與格式驗證。

2. 發現的問題：

   - AI 沒有處理 JSON 讀取時的 `JSONDecodeError`。
   - `borrow` 指令在找不到 ISBN 時沒有明確回應。

3. 修正的對話：

   我告訴它「請加入 JSON 讀取錯誤處理，並在 borrow 找不到 ISBN 時印出 'ISBN Not Found'。」

---

## 三、 成果驗證與測試  (共2小題，每小題10分，總共20分)

確保你的 `modern_library.py` 功能正確。

### 3.1 測試結果驗證 (Terminal)

請貼上執行程式並輸入 show 後，顯示資料清單。(請從呼叫執行程式到結束程式完整的把操作對話複製到下框)

```log
C:\Users\pclab\Desktop\NTUST-0527-Final-master> python modern_library.py
=== 圖書管理系統 v0.1 (Modern) ===
Commands:
  add <title>/<isbn>/<status>
  show
  borrow <isbn>
  exit
> Success
> Success
> 書名: Python Programming, ISBN: 9781234567897, 狀態: available
書名: Data Structures, ISBN: 9789876543210, 狀態: available
> Updated
> 書名: Python Programming, ISBN: 9781234567897, 狀態: borrowed
書名: Data Structures, ISBN: 9789876543210, 狀態: available
> 系統關閉
```

### 3.2 產出的資料檔案格式

請貼上重構後生成的 `books.json` 前幾行內容：

```json
[
  {
    "title": "Python Programming",
    "isbn": "9781234567897",
    "status": "borrowed"
  },
  {
    "title": "Data Structures",
    "isbn": "9789876543210",
    "status": "available"
  }
]
```

---

## 四、 Git 提交紀錄 (Commit History)  (共2小題，總共13分)

### 4.1. 請執行 `git log --oneline` 並將 Commit 紀錄貼在此處，以證明你的開發流程(此小題6分)


```log
32c26c8 Add modern_library.py, test data, and complete Answer.MD responses
```

### 4.2. GitHub Repository 連結(此小題7分)

將專案推送到 GitHub (Public) 若提交到 Private 連結不給分。 請設定 Repository 名稱為 `學號-0527-Final` Ex: B11526748-0527-Final **請用 - 不是 _**

```log
尚未推送到 GitHub，本地已建立 Git 倉庫。
```

希望這兩份 Markdown 格式能幫你省下不少排版時間！祝你的考試順利舉行！

最後請保留整份專案資料夾歐！
