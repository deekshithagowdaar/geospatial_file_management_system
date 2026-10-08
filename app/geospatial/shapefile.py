from pathlib import Path
from zipfile import ZipFile

from fastapi import HTTPException


REQUIRED_COMPONENTS = {
    ".shp",
    ".shx",
    ".dbf",
}


def extract_shapefile_zip(
    zip_path: str | Path,
    extract_dir: str | Path
) -> Path:

    zip_path = Path(zip_path)
    extract_dir = Path(extract_dir)

    if not zip_path.exists():
        raise FileNotFoundError(
            f"ZIP file not found: {zip_path}"
        )

    extract_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    try:
        with ZipFile(zip_path, "r") as archive:

            for member in archive.infolist():
                member_path = extract_dir / member.filename

                if not member_path.resolve().is_relative_to(
                    extract_dir.resolve()
                ):
                    raise HTTPException(
                        status_code=400,
                        detail="Invalid ZIP file: unsafe file path detected."
                    )

            archive.extractall(extract_dir)

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid or corrupted ZIP file."
        )

    shapefile = find_shapefile(extract_dir)

    validate_shapefile_components(shapefile)

    return shapefile


def find_shapefile(extract_dir: Path) -> Path:
    shapefiles = list(
        extract_dir.rglob("*.shp")
    )

    if not shapefiles:
        raise HTTPException(
            status_code=400,
            detail="ZIP file does not contain a Shapefile (.shp)."
        )

    if len(shapefiles) > 1:
        raise HTTPException(
            status_code=400,
            detail="ZIP file contains multiple Shapefiles."
        )

    return shapefiles[0]


def validate_shapefile_components(
    shapefile: Path
) -> None:

    existing_components = {
        file.suffix.lower()
        for file in shapefile.parent.iterdir()
        if file.is_file()
        and file.stem.lower() == shapefile.stem.lower()
    }

    missing_components = (
        REQUIRED_COMPONENTS - existing_components
    )

    if missing_components:
        missing = ", ".join(
            sorted(missing_components)
        )

        raise HTTPException(
            status_code=400,
            detail=(
                f"Invalid Shapefile. "
                f"Missing required component(s): {missing}"
            )
        )