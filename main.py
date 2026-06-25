# -*- coding: utf-8 -*-
"""
main.py  —  TrimbleOtomatikCizim giris noktasi.

GUI modu:
    python main.py

Robot (komut satiri) modu:
    python main.py --robot [--config robot_config.json]
"""
from __future__ import annotations
import argparse
import logging
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)


def get_base_dir() -> Path:
    """
    EXE veya script olarak calisirken dogru klasoru doner.
    PyInstaller ile derlendiyse sys.executable'in bulundugu klasor,
    script olarak calisiyorsa main.py'nin bulundugu klasor.
    """
    if getattr(sys, "frozen", False):
        # PyInstaller EXE modu
        return Path(sys.executable).parent
    else:
        # Normal Python script modu
        return Path(__file__).parent


def ensure_runtime_dirs(base: Path):
    """giris/, cikti/, islenmis/ klasorlerini EXE yaninda olusturur."""
    for d in ("giris", "cikti", "islenmis"):
        (base / d).mkdir(parents=True, exist_ok=True)
    # robot_config.json yoksa olustur
    cfg_path = base / "robot_config.json"
    if not cfg_path.exists():
        import json
        default = {
            "input_dir": "giris", "output_dir": "cikti", "processed_dir": "islenmis",
            "max_points": 200000, "target_crs": "LOCAL",
            "auto_ground": False, "detect_planes": False,
            "auto_section": False, "full_analysis": False,
            "cad_use_full_las": True, "export_trimble": False,
            "export_dxf": True, "move_when_done": True,
            "move_after_dxf": True, "watch_interval_sec": 3,
            "ground_cell_size": 1, "plane_distance_threshold": 0.05,
            "section_thickness": 0.5, "dxf_max_points": 50000,
            "auto_start_watch": False, "cad_flat_z": False,
            "cad_max_extract_points": 5000000,
            "building_full_data": True, "building_only": False,
            "building_cell_size": 0.25, "building_min_vertical_span": 1.5,
            "building_min_area": 0.0, "building_max_area": 10000,
            "building_max_count": 2000,
            "pole_max_elek": 8, "pole_max_tel": 1,
            "wall_min_length": 2.5,
            "sundurma_min_area": 4.0, "sundurma_max_area": 130.0,
            "sundurma_max_kose": 5, "sundurma_adet": 4,
        }
        cfg_path.write_text(json.dumps(default, indent=2, ensure_ascii=False), encoding="utf-8")


def run_gui():
    from PyQt6.QtWidgets import QApplication
    from ui.main_window import MainWindow

    base = get_base_dir()
    ensure_runtime_dirs(base)

    app = QApplication(sys.argv)
    app.setApplicationName("TrimbleOtomatikCizim")
    app.setStyle("Fusion")

    palette_css = """
        QWidget { background: #1e1e1e; color: #d4d4d4; }
        QTabWidget::pane { border: 1px solid #3a3a3a; }
        QTabBar::tab { background: #2d2d2d; color: #aaa; padding: 6px 12px; }
        QTabBar::tab:selected { background: #1e1e1e; color: #fff; border-bottom: 2px solid #4caf50; }
        QGroupBox { border: 1px solid #3a3a3a; border-radius: 4px; margin-top: 8px; padding: 6px; }
        QGroupBox::title { subcontrol-origin: margin; left: 8px; color: #888; }
        QPushButton { background: #2d2d2d; border: 1px solid #555; border-radius: 4px; padding: 5px 10px; }
        QPushButton:hover { background: #3a3a3a; }
        QPushButton:disabled { color: #555; }
        QSpinBox, QDoubleSpinBox, QComboBox { background: #2d2d2d; border: 1px solid #555; padding: 2px; }
        QTextEdit, QListWidget { background: #111; border: 1px solid #333; }
        QProgressBar { border: 1px solid #555; border-radius: 3px; background: #2d2d2d; }
        QProgressBar::chunk { background: #4caf50; }
        QStatusBar { background: #252525; color: #888; }
    """
    app.setStyleSheet(palette_css)

    win = MainWindow(base_dir=base)
    win.show()
    sys.exit(app.exec())


def run_robot_cli(config_path: Path):
    from core.robot.config import load_config
    from core.robot.pipeline import process_folder

    base_dir = config_path.parent
    ensure_runtime_dirs(base_dir)
    cfg   = load_config(config_path)
    paths = cfg.resolve_paths(base_dir)
    inp   = paths["input"]

    files = sorted([f for f in inp.iterdir() if f.suffix.lower() in (".las", ".laz")])
    if not files:
        print(f"Giris klasorunde ({inp}) LAZ/LAS dosyasi yok.")
        return

    ok = 0
    for f in files:
        def on_step(name, label, result=None, _f=f):
            print(f"  [{name}] {_f.name}: {label}")

        print(f"\n{'='*60}")
        print(f"Isleniyor: {f.name}")
        result = process_folder(f, cfg, base_dir, on_step)
        if result.success:
            print(f"BASARILI — {result.cad_object_count} nesne — DXF: {result.dxf_path}")
            ok += 1
        else:
            print(f"HATA: {result.error}")

    print(f"\nTamamlandi: {ok}/{len(files)} basarili")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TrimbleOtomatikCizim")
    parser.add_argument("--robot",  action="store_true", help="GUI olmadan robot modunda calistir")
    parser.add_argument("--config", default=None, help="Config dosyasi yolu")
    args = parser.parse_args()

    if args.robot:
        base = get_base_dir()
        cfg_path = Path(args.config) if args.config else base / "robot_config.json"
        run_robot_cli(cfg_path)
    else:
        run_gui()
