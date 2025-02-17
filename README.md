# ⏳ HowLongToBeat Scraper

## 📌 Overview
This repository contains a Python scraper for extracting game data from [HowLongToBeat](https://howlongtobeat.com).  
The scraper retrieves **playtime estimates**, **genres**, **platforms**, **developers**, **publishers**, and more.

🔹 **Dataset Available on Kaggle**: [🔗 (Insert Kaggle link here)]  
🔹 **Scraper Code**: This repo provides the code to scrape fresh data.

## 📂 Features
✅ Extracts **Main Story**, **Main + Extra**, and **Completionist** playtimes  
✅ Fetches **platforms, genres, developers, and publishers**  
✅ Saves data in **JSON & CSV formats**  
✅ Implements **rate limiting & retries** to avoid API bans  
✅ Stops automatically when **no more valid games exist**  
✅ Efficient error handling and automatic cooldown on request failures  
✅ Converts **nested JSON fields** into structured CSV format for analysis  

---

## 🚀 Installation

### Clone the repository
```bash
git clone https://github.com/zaireali649/howlongtobeat-scraper.git
cd howlongtobeat-scraper
```

### Install dependencies
```bash
pip install -r requirements.txt
```

---

## 🔍 Usage

### Scrape All Games
```bash
python hltb_scraper.py
```
This script will **scrape game data** until it reaches a set number of **consecutive 404 errors**,  
ensuring it stops when there are no more valid game IDs.

- It retries failed requests with **exponential backoff** to prevent rate limiting.
- If **too many consecutive errors** occur, it **pauses for 1 minute** before continuing.
- Saves progress **every 100 games** to prevent data loss.

### Convert JSON to CSV
After scraping, you can convert the dataset to CSV format while **flattening nested fields**:
```python
input_file = "hltb_data.json"

# Load the first JSON file
with open(input_file, "r") as f:
    data = json.load(f)

df = flatten_hltb_json(data)

df.to_csv("hltb_data.csv", index=False)
```

---

## ⚙️ Dependency Management
We use `pip-tools` to manage dependencies efficiently. Instead of manually updating `requirements.txt`, we generate it from `requirements.in`.

### Installing `pip-tools`
```bash
pip install pip-tools
```

### Generating `requirements.txt`
All required dependencies are defined in `requirements.in`. To compile and update `requirements.txt`, run:
```bash
pip-compile requirements.in
```
Then, install the dependencies:
```bash
pip install -r requirements.txt
```
This ensures all packages are pinned to specific versions, improving reproducibility.

---

## 📝 Code Consistency
We enforce clean and readable code using **`pycodestyle`** and **`pydocstyle`**.

### Installing the Linters
```bash
pip install pycodestyle pydocstyle
```

### Running Linting Checks
To check for style violations:
```bash
pycodestyle --max-line-length=120 .\hltb_scraper.py
pydocstyle .\hltb_scraper.py
```
**Customization:**  
- We allow a **maximum line length of 120 characters** instead of the default **79**.

To automate these checks, consider adding **pre-commit hooks**.

---

## 📊 Example Data Output
```json
{
    "game": [
        {
            "game_id": 1,
            "game_name": "688(I) Hunter/Killer",
            "profile_platform": "PC",
            "profile_genre": "Simulation",
            "profile_dev": "Sonalysts",
            "profile_pub": "Electronic Arts",
            "release_world": "1997-07-04",
            "review_score": 0,
            "playtimes": {
                "Main Story": "37.4 Hours",
                "Main + Extra": "87.06 Hours",
                "Completionist": "166.25 Hours"
            },
            "summary": "A realistic submarine simulation developed by Sonalysts."
        }
    ],
    "userReviews": {
        "review_count": 0
    },
    "platformData": [
        {
            "platform": "PC",
            "count_comp": 10,
            "comp_main": 42553,
            "comp_plus": 193015,
            "comp_100": 97200,
            "comp_low": 27262,
            "comp_high": 435044
        }
    ]
}
```

---

## 📊 CSV Output Example

| game_id | game_name                | profile_platform | profile_genre  | profile_dev  | profile_pub      | release_world | review_score | comp_main | comp_plus | comp_100 | review_count |
|---------|--------------------------|------------------|----------------|--------------|------------------|---------------|--------------|-----------|-----------|-----------|--------------|
| 1       | 688(I) Hunter/Killer     | PC              | Simulation     | Sonalysts    | Electronic Arts  | 1997-07-04    | 0            | 42553     | 193015    | 97200     | 0            |
| 2       | Beyond Good & Evil 2     | Xbox 360        | Action         | Ubisoft Montpellier | Ubisoft | 0000-00-00 | 100          | 28148     | 33243     | 67611     | 0            |

---

## 🔗 Related Links
- **📊 Dataset on Kaggle**: [🔗 (Insert Kaggle link here)]  
- **🌐 HowLongToBeat Website**: [🔗 howlongtobeat.com](https://howlongtobeat.com)  

---

## 📢 Want to Contribute?
Pull requests and improvements are welcome! Feel free to **fork** and submit PRs.
