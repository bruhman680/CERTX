"""Host-only portable world transport; no guest command accepts file paths."""
import argparse
import json
from pathlib import Path
from world_bundle import export_world, import_world
from world_store import World


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--db', required=True)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--export', dest='export_path')
    action.add_argument('--import', dest='import_path')
    args = parser.parse_args()
    profile = json.loads((Path(__file__).resolve().parents[1] / 'constants.json').read_text())
    if args.import_path:
        result = import_world(args.import_path, args.db, profile)
    else:
        if not Path(args.db).exists():
            parser.error('export requires an existing database')
        world = World(args.db, profile)
        try:
            result = export_world(world, args.export_path)
        finally:
            world.close()
    print(json.dumps(result))


if __name__ == '__main__':
    main()
