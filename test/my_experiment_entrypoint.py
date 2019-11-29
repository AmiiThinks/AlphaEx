import sys


def main():
    sweep_id = int(sys.argv[1])
    config_file = sys.argv[2]

    print(f"sweep_id: {sweep_id},\tconfig_file: {config_file}")


if __name__ == "__main__":
    main()
