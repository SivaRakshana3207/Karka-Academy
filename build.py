from pathlib import Path
import shutil


BASE_DIR = Path(__file__).resolve().parent
SOURCE_STATIC = BASE_DIR / "static"
PUBLIC_STATIC = BASE_DIR / "public" / "static"


if not SOURCE_STATIC.is_dir():
    raise SystemExit("Missing static/ source assets.")

if PUBLIC_STATIC.exists():
    shutil.rmtree(PUBLIC_STATIC)

shutil.copytree(SOURCE_STATIC, PUBLIC_STATIC, dirs_exist_ok=True)
print(f"Prepared Vercel static assets in {PUBLIC_STATIC.relative_to(BASE_DIR)}")
