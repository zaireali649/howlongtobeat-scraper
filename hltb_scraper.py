"""Script to scrape all game data from HowLongToBeat.com.

This script fetches game details such as playtime estimates, platforms, genres, and more
by iterating over game IDs on HowLongToBeat.com. It implements error handling, rate limiting,
and automatic stopping after a set number of consecutive 404 responses.
"""

import requests
import json
import time
from typing import Optional, Dict, List, Any

BASE_URL = "https://howlongtobeat.com/game/"


def scrape_hltb_game(game_id: int, max_retries: int = 3, cooldown_time: int = 60) -> Optional[Dict[str, Any]]:
    """Fetch game data from HowLongToBeat using a given game ID.

    Args:
        game_id (int): The ID of the game on HowLongToBeat.
        max_retries (int, optional): Maximum retry attempts in case of connection errors. Defaults to 3.
        cooldown_time (int, optional): Time in seconds to wait after repeated failures. Defaults to 60.

    Returns:
        Optional[Dict[str, Any]]: A dictionary containing game data, or None if the game does not exist.
    """
    url = f"{BASE_URL}{game_id}"
    headers = {"User-Agent": "Mozilla/5.0"}

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 404:
                return None  # Game ID does not exist

            # Extract JSON data from the script tag
            json_data_start = response.text.find('{"props":')
            json_data_end = response.text.rfind('</script>')
            if json_data_start == -1 or json_data_end == -1:
                return None  # JSON structure not found

            json_str = response.text[json_data_start:json_data_end]
            data = json.loads(json_str)

            game_data = data["props"]["pageProps"]["game"]["data"]

            # Remove unnecessary metadata columns
            for col in ["individuality", "relationships"]:
                if col in game_data:
                    del game_data[col]

            return game_data

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            print(f"Connection error on game {game_id}, attempt {attempt + 1}/{max_retries}: {e}")
            time.sleep(cooldown_time)  # Apply cooldown before retrying

    print(f"Too many failures for game {game_id}. Waiting {cooldown_time} seconds...")
    time.sleep(cooldown_time)
    return None


def scrape_bulk(start_id: int = 1,
                save_frequency: int = 100,
                max_consecutive_404s: int = 500,
                server_break: float = 0.01,
                output_file: str = "hltb_data.json") -> None:
    """Scrapes game data iterating over game IDs and saves the collected data in a JSON file.

    Args:
        start_id (int, optional): The starting game ID. Defaults to 1.
        save_frequency (int, optional): Number of links to attempt before saving. Defaults to 100.
        max_consecutive_404s (int, optional): Number of consecutive 404s before stopping. Defaults to 500.
        server_break (float, optional): Delay in seconds between requests to prevent rate limiting. Defaults to 0.01.
        output_file (str, optional): File path for saving the scraped data. Defaults to 'hltb_data.json'.

    Returns:
        None: Writes collected game data to the specified output file.
    """
    results: List[Dict[str, Any]] = []
    consecutive_404s = 0
    game_id = start_id

    print(f"Starting scraping from game ID {game_id} (Max consecutive 404s: {max_consecutive_404s})")

    while consecutive_404s < max_consecutive_404s:
        game_data = scrape_hltb_game(game_id)

        if game_data:
            results.append(game_data)
            consecutive_404s = 0  # Reset the 404 counter when a valid game is found
        else:
            consecutive_404s += 1  # Increment 404 counter

        game_id += 1
        time.sleep(server_break)  # Respect the server to avoid getting blocked

        # Save progress every save_frequency games to prevent data loss
        if game_id % save_frequency == 0 and consecutive_404s < save_frequency:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=4)
            print(f"Saved progress: {len(results)} games collected (Latest ID: {game_id})")

    print(f"Stopped after {max_consecutive_404s} consecutive 404s.")

    if consecutive_404s <= save_frequency:
        # Ensure the last chunk of data is saved if the total games scraped
        # since the last save is less than the save_frequency.
        # This prevents data loss if the script stops before hitting another save checkpoint.
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4)
        print(f"Final dataset saved: {len(results)} games in {output_file}")


if __name__ == "__main__":
    scrape_bulk(max_consecutive_404s=10000)
