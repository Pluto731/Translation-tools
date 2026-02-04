from __future__ import annotations

import sys

from src.app import TranslationApp


def main() -> int:
    app = TranslationApp()
    try:
        return app.run()
    finally:
        app.cleanup()


if __name__ == "__main__":
    sys.exit(main())
