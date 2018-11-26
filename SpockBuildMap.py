import argparse
from library.util.SpockMap import SpockMap
from library.util.SpockMap import parse_sfo_version


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Building SPOCK Map")
    parser.add_argument("-p", "--path", required=True, help="Opens or Creates a file that would read and written to.")
    parser.add_argument("--sfo", required=True, help="SFO version major_version.minor_version.build_version. i.e 1.1.0")
    parser.add_argument("--spock", required=True, help="Spock version")
    parser.add_argument("--url", required=True, help="Spock URL")
    args = parser.parse_args()

    major, minor, build = parse_sfo_version(args.sfo)
    spock_map = SpockMap()
    spock_map.open(args.path)
    spock_map.add_spock_entry(major_version=major, minor_version=minor, build_version=build, spock_version=args.spock,
                              spock_url=args.url)
    spock_map.write(args.path)
