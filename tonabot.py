import sys
import time
import argparse
import threading
from datetime import datetime
from modules.notify import show_notification
from modules.scrape import get_ads_for

# Set the last checked stamp to 1970....
LAST_CHECKED = datetime.strptime("1 Jan 12:00 am", "%d %b %I:%M %p")
WAIT_TIME_BETWEEN_CHECKS = 50
WAIT_TIME_BETWEEN_NOTIFICATIONS = 0


def run(product_name, interval, filter_name=None):
    """
    Entry Point of Tonabot: Runs the scraping function to get new ads for a product every set interval (seconds)

    Parameters:
    product_name (str): The product to search for
    interval (int): The number of seconds to wait before checking again
    filter_name (str): Get only ads with this in their titles
    """
    global LAST_CHECKED

    threading.Timer(interval, run, [product_name, interval]).start()

    ads = []
    try:
        ads = get_ads_for(product_name, LAST_CHECKED, filter_name)
    except AttributeError as error:
        print(f"Error: Could not extract ads from page \n {error}")

    # Update last checked to prevent duplicate notifications
    LAST_CHECKED = datetime.now()

    if len(ads) == 0:
        print("No new ads found")
    else:
        print(f"{len(ads)} ads found")
        for ad in ads:
            print(f"{ad['name']} - {ad['price']}")
            information = ad["price"] + "\n" + ad["name"]
            show_notification("Tonabot!", information, WAIT_TIME_BETWEEN_NOTIFICATIONS)
            time.sleep(WAIT_TIME_BETWEEN_NOTIFICATIONS)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search for ads on Tonaton")
    parser.add_argument(
        "product_name",
        metavar="product_name",
        type=str,
        help="the name of the product to look for",
    )
    parser.add_argument(
        "-f", "--filter", action="store", help="string to filter ads based on titles"
    )
    args = parser.parse_args()
    product_name = args.product_name

    if product_name:
        if len(sys.argv) > 1:
            filter = args.filter
            run(product_name, WAIT_TIME_BETWEEN_CHECKS, filter)
        else:
            print("Invalid Parameters")
            print("tonabot.py [search_term] [filter]")
