import sys

from game.game import Game


def main():
    # Run `python main.py 2` for local co-op.
    num_players = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    Game(num_players).run()


if __name__ == "__main__":
    main()
