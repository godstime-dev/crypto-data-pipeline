from app.pipeline import run_pipeline
from app.monitor import log_info, log_error


def safe_run_pipeline():
    try:
        run_pipeline()
        log_info("[Scheduler] Pipeline executed successfully")

    except Exception as e:
        log_error(f"[Scheduler Guard] Pipeline crash prevented: {e}")