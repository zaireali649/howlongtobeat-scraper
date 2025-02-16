"""Script to scrape all game data from HowLongToBeat.com."""
import requests
import json
import time

BASE_URL = "https://howlongtobeat.com/game/"


def scrape_hltb_game(game_id, max_retries=3, cooldown_time=60):
    url = f"{BASE_URL}{game_id}"
    headers = {"User-Agent": "Mozilla/5.0"}

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 404:
                return None

            # Extract JSON data from the script tag
            json_data_start = response.text.find('{"props":')
            json_data_end = response.text.rfind('</script>')
            if json_data_start == -1 or json_data_end == -1:
                return None  # JSON not found

            json_str = response.text[json_data_start:json_data_end]
            data = json.loads(json_str)

            game_data = data["props"]["pageProps"]["game"]["data"]

            for col in ["individuality", "relationships"]:
                if col in game_data:
                    del game_data[col]

            return game_data
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            print(f"Connection error on game {game_id}, attempt {attempt + 1}/{max_retries}: {e}")
            time.sleep(cooldown_time)

    print(f"Too many failures for game {game_id}. Waiting {cooldown_time} seconds...")
    time.sleep(cooldown_time)
    return None


def scrape_bulk(start_id=1, max_consecutive_404s=500, server_break=0.01, output_file="hltb_data.json"):
    results = []
    consecutive_404s = 0
    game_id = start_id

    print(f"Starting game_id: {game_id} Current 404s: {consecutive_404s}")

    while consecutive_404s < max_consecutive_404s:

        game_data = scrape_hltb_game(game_id)

        if game_data:
            results.append(game_data)
            consecutive_404s = 0  # Reset 404 counter when a valid game is found
        else:
            consecutive_404s += 1  # Increment 404 counter

        game_id += 1
        time.sleep(server_break)

        # Save progress every 100 games
        if game_id % 100 == 0:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=4)
            print(f"Starting game_id: {game_id} Current 404s: {consecutive_404s}")

    print(f"Stopped after {max_consecutive_404s} consecutive 404s.")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
    print(f"Saved {len(results)} games to {output_file}")


if '__main__' == __name__:
    scrape_bulk(max_consecutive_404s=10000)
