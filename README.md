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
After scraping, you can convert the dataset to CSV format:
```python
import pandas as pd
import json

with open("hltb_data.json", "r") as f:
    data = json.load(f)

df = pd.DataFrame(data)
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
    "game_id": 104683,
    "title": "Pokémon Scarlet and Violet",
    "platform": "Nintendo Switch",
    "genre": "Role-Playing, Open World",
    "developer": "Game Freak",
    "publisher": "Nintendo, The Pokémon Company",
    "release_date": "2022-11-18",
    "review_score": 72,
    "playtimes": {
        "Main Story": "32 Hours",
        "Main + Extra": "49.5 Hours",
        "Completionist": "87 Hours"
    },
    "summary": "The Pokémon Scarlet and Pokémon Violet games, the newest chapters in the Pokémon series..."
}
```

---

## 🔗 Related Links
- **📊 Dataset on Kaggle**: [🔗 (Insert Kaggle link here)]  
- **🌐 HowLongToBeat Website**: [🔗 howlongtobeat.com](https://howlongtobeat.com)  

---

## 📢 Want to Contribute?
Pull requests and improvements are welcome! Feel free to **fork** and submit PRs.
