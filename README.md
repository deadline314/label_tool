# B2C / C2C Label 工具
## 簡介
這是一個商品匹配標註工具，主要用來處理兩種類型的標註：
1. **C2C（消費者對消費者）**：處理 C2C 搜尋結果。
2. **B2C（企業對消費者）**：處理 B2C 搜尋結果。

工具以 Streamlit 為基礎撰寫，操作方法請見[C2C/B2C 人工核實標註方法](https://youtu.be/p-yDBZYThUA)。

---

## 環境需求
需要的工具和套件如下：
- **Python**：版本 `>=3.9`
- 必裝套件：
  - `streamlit`
  - `pandas`
  - `streamlit-aggrid`
- 安裝方法：
  打開終端機跑這行：
  ```
  pip install -r requirements.txt
  ```

## 工具用法
### C2C 標註工具
啟動方式：
`streamlit run label_ui_c2c.py`
請將檔案路徑修改為組別代號，例如：`./c2c_result/G組_C2C搜尋結果.csv`
標註的結果會存成 `{搜尋詞}_annotations.csv`

### B2C 標註工具
啟動方式：
`streamlit run label_ui_b2c.py`
將檔案路徑為：`./b2c/B2C_Common_250.csv`
標註的結果會存成 `{搜尋詞}_annotations.csv`

## 人工核實
因為要計算模型商品匹配結果的 Recall、Accuracy、Precision、f1 score的分數，所以需要以下資料：
1. 利用 putback.ipynb 將檔案從o跟x的模式轉換成能夠計算分數的格式。**請注意，由於格式不同需要修改程式**
2. 人工核實結果（Ground Truth）：來自大家的人工標註結果。
    每對商品是否匹配的真實標籤（例如：匹配=1，不匹配=0）。
3. 模型預測結果：之前模型給出的商品匹配結果。
    同樣格式，標籤是 1 或 0。


## 標註工具
* 啟動工具：選好你的類型（C2C 或 B2C），執行對應指令。
* 選搜尋詞：從側邊欄挑出要標註的搜尋詞。
* 開始標註：
    * 看商品是否匹配：
    * x：不匹配。
    * o：匹配。
* 點一下表格的格子，就可以在 x 和 o 間切換。
* 保存進度：點「保存標註」按鈕，系統會幫你自動生成標註結果檔案。

## 檔案繳交方式
### B2C 部分：
依 grouped_queries.csv 的順序，找到搜尋詞後依序標註。
### C2C 部分：
必標 15 個共同搜尋詞，再加 35 個自選搜尋詞。
### 報告
拿大家人工核實的部分來算你們之前模型商品匹配結果的Recall、Accuracy、Precision、f1 score的分數，然後進行分析。
### 繳交方式：
**把結果資料整理成 c2c 和 b2c 兩個資料夾，壓縮後再提交。**
繳交期限：
2023/11/27 23:59 前


如果有問題請找助教
助教：旭清
Email：stanley890314@gmail.com
