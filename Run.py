import sys
from .Decoder import decode_player_view
from .API import GameAPI
from .User import play

def main():
    raw = sys.stdin.read()

    view = decode_player_view(raw)
    api = GameAPI(view)

    actions = play(api) or []

    for action in actions:
        action.emit()


if __name__ == "__main__":
    main()
