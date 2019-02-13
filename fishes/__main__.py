import argparse
import platform
import logging
import sys

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options


from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager


def get_fishes(driver, num_fishes):
    """
    Finds and clicks on the setting related to the number of fishes.

    Args:
        driver (object): The webdriver instance
        num_fishes (int): The number of fishes to spawn

    Returns:
        bool: The return value. True for success, False otherwise
    """
    fishes_dict = {
        1: 0,
        100: 1,
        500: 2,
        1000: 3,
        5000: 4,
        10000: 5,
        15000: 6,
        20000: 7,
        25000: 8,
        30000: 9,
    }
    try:
        fish_elem = driver.find_element_by_id(
            "setSetting{}".format(fishes_dict[num_fishes])
        )
        fish_elem.click()
    except Exception as e:
        print("There was an error setting the fish number. Check log.txt for details")
        log_error(e)
        return False
    return True


def set_speed(driver, speed):
    """
    Finds the xpath of the speed text and the slider object.
    Passes the xpaths and the speed setting to the slider handler.

    Args:
        driver (object): The webdriver instance
        speed (int): The speed of the aquarium

    Returns:
        bool: The return value. True for success, False otherwise
    """
    speed_xpath = "/html/body/div[3]/div/div[1]/div[1]/span[2]"
    try:
        speed_slider = driver.find_element_by_xpath(
            "/html/body/div[3]/div/div[1]/div[2]/a"
        )
    except Exception as e:
        print("There was an error getting the speed slider. Check log.txt for details")
        log_error(e)
        return False
    slider_success = slider_handler(driver, speed_slider, speed_xpath, speed)
    return slider_success


def set_fishspeed(driver, speed):
    """
    Finds the xpath of the fish speed text and the slider object.
    Passes the xpaths and the fish speed setting to the slider handler.

    Args:
        driver (object): The webdriver instance
        speed (int): The fish speed

    Returns:
        bool: The return value. True for success, False otherwise
    """
    fishspeed_xpath = "/html/body/div[3]/div/div[19]/div[1]/span[2]"
    try:
        fishspeed_slider = driver.find_element_by_xpath(
            "/html/body/div[3]/div/div[19]/div[2]/a"
        )
    except Exception as e:
        print(
            "There was an error getting the fish speed slider. Check log.txt for details"
        )
        log_error(e)
        return False

    slider_success = slider_handler(driver, fishspeed_slider, fishspeed_xpath, speed)
    return slider_success


def slider_handler(driver, slider, val_xpath, target_val):
    """
    Handles setting the slider value to the target value using the slider and
    slider value xpaths.

    Args:
        driver (object): The webdriver instance
        slider (object): The slider object
        val_xpath (str): The xpath of the current slider value
        target_val (int): The target value of the slider

    Returns:
        bool: The return value. True for success, False otherwise
    """
    try:
        current_val = float(driver.find_element_by_xpath(val_xpath).text)
        actions = ActionChains(driver)
        while abs(current_val - target_val) > 0.2:
            offset = target_val - current_val
            actions.drag_and_drop_by_offset(slider, 15 * offset, 0).perform()
            current_val = float(driver.find_element_by_xpath(val_xpath).text)
    except Exception as e:
        print(
            "There was an error setting a slider value. Check log.txt for more details"
        )
        log_error(e)
        return False
    return True


def init_browser(browser, system):
    """
    Creates the driver instance for a given browser given the browser type.

    Args:
        browser (str): The brower to use (Firefox, Chrome)

    Returns:
        The driver instance.
    """
    try:
        if browser == "Firefox":
            driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        elif browser == "Chrome":
            chrome_options = Options()
            chrome_options.add_experimental_option("detach", True)
            driver = webdriver.Chrome(
                executable_path=ChromeDriverManager().install(), options=chrome_options
            )
        return driver
    except Exception as e:
        print(
            "There was an error creating the browser instance. Check log.txt for details"
        )
        log_error(e)
        sys.exit("Program aborted due to errors")


def log_error(error):
    logging.basicConfig(
        filename="log.txt", format="\n%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.error(error, exc_info=True)


def main():
    system = platform.system()
    parser = argparse.ArgumentParser(
        description="Spawns an aquarium from https://webglsamples.org/aquarium/aquarium.html in the browser"
    )
    parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true")

    browser_choices = ["Firefox", "Chrome"]
    parser.add_argument(
        "browser",
        metavar="browser",
        help="browser used to load the website (options: {browsers})".format(
            browsers=", ".join(browser_choices)
        ),
        type=str,
        choices=browser_choices,
    )

    parser.add_argument(
        "-f",
        "--fishes",
        metavar="",
        help="number of fishes to spawn (options: 1, 100, 500, 1000, 5000, 10000, 15000, 20000, 25000, 30000) (default: 500)",
        type=int,
        choices=[1, 100, 500, 1000, 5000, 10000, 15000, 20000, 25000, 30000],
        default=500,
    )
    parser.add_argument(
        "-s",
        "--speed",
        metavar="",
        help="overall speed of the aquarium (options: 0, 1, 2, 3, 4) (default: 2)",
        type=int,
        choices=[0, 1, 2, 3, 4],
        default=2,
    )
    parser.add_argument(
        "-fs",
        "--fishspeed",
        metavar="",
        help="speed of the fish (options: 0, 1, 2) (default: 1)",
        type=int,
        choices=[0, 1, 2],
        default=1,
    )
    args = parser.parse_args()

    driver = init_browser(args.browser, system)
    driver.get("https://webglsamples.org/aquarium/aquarium.html")

    if args.verbose:
        print("Currently running on: {}".format(system))
        print("{} browser loaded.".format(args.browser))
        print("Webpage loaded.")

    fishes_success = get_fishes(driver, args.fishes)
    if fishes_success and args.verbose:
        print("Successfully spawned {} fish.".format(args.fishes))

    driver.find_element_by_id("setSettingAdvanced").click()

    speed_success = set_speed(driver, args.speed)
    if speed_success and args.verbose:
        print("Successfully set speed to {}.".format(args.speed))

    fishspeed_success = set_fishspeed(driver, args.fishspeed)
    if fishspeed_success and args.verbose:
        print("Successfully set fish speed to {}.".format(args.fishspeed))


if __name__ == "__main__":
    main()
