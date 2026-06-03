from apscheduler.schedulers.blocking import BlockingScheduler
from threading import Lock

from app.config import SLEEP_INTERVAL_SECONDS
from app.pipeline import run_pipeline
from app.monitor import log_info, log_error


pipeline_lock = Lock()


def safe_run_pipeline():
    """
    Ensures only one pipeline run happens at a time.
    Prevents overlap if execution takes longer than interval.
    """

    if not pipeline_lock.acquire(blocking=False):
        log_info("Pipeline already running — skipping this cycle")
        return

    try:
        run_pipeline()
    except Exception as e:
        log_error(f"Scheduler caught pipeline error: {e}")
    finally:
        pipeline_lock.release()


def start_scheduler():
    """
    Starts a safe, non-overlapping blocking scheduler.
    """
    scheduler = BlockingScheduler()

    scheduler.add_job(
        safe_run_pipeline,
        "interval",
        seconds=SLEEP_INTERVAL_SECONDS,
        max_instances=1,
        coalesce=True
        )

    log_info(f"Scheduler started - running every {SLEEP_INTERVAL_SECONDS} seconds")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        log_info("Scheduler stopped gracefully")