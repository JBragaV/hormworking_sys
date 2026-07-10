import logging

from pomodoro import pomodoro

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )
    logger = logging.getLogger(__name__)
    # logger.info("Loaded 250 rows")
    # logger.warning("Skipped row 17 because email is missing")
    # logger.info("Prepared 238 payloads")
    # logger.error("Failed to send payload for user_id=%s", 132)
    pomodoro()
