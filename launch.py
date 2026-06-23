from app.config import CANDLE_INTERVAL_HOURS
from app.database import create_table
from app.pipeline import run_pipeline
from app.scheduler import start_scheduler
from app.monitor import log_info, log_error


def main():
    """
    Entry point for the crypto pipeline system.
    """
    try:
        create_table()

        log_info("Executing immediate startup data fetch...")
        run_pipeline()

        log_info(f"Starting scheduler (interval={CANDLE_INTERVAL_HOURS * 3600}s)...")
        start_scheduler()

    except Exception as e:
        log_error(f"Application failed to start: {e}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log_info("Application stopped manually (KeyboardInterrupt)")