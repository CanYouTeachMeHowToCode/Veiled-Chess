# Main function
import argparse
from cli import CLI
from ui import app
from gui import pygameApp


def runningInStreamlit():
    """Detect whether this script was launched via `streamlit run`."""
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
    except ImportError:
        try:
            from streamlit.script_run_context import get_script_run_ctx
        except ImportError:
            try:
                from streamlit.report_thread import get_report_ctx as get_script_run_ctx
            except ImportError:
                return False
    return get_script_run_ctx() is not None


def main():
    # `streamlit run main.py` always wins: hand off to the Streamlit app
    if runningInStreamlit():
        app()
        return

    # Otherwise, pick the interface via --mode when invoked with `python main.py`
    parser = argparse.ArgumentParser(description="Veiled Chess")
    parser.add_argument(
        "--mode",
        choices=["cli", "gui"],
        default="cli",
        help="Interface to run: cli (default) or gui (PyGame)",
    )
    args = parser.parse_args()

    if args.mode == "gui":
        pygameApp()
    else:
        CLI()


if __name__ == '__main__':
    main()