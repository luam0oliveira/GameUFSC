import json


def save_score(max_score):
    try:
        with open('saved_game.txt', 'w') as save_file:
            data = {
                "best_score": max_score
            }
            json.dump(data, save_file)
            return True
    except FileExistsError:
        return False


def get_best_score():
    try:
        with open('saved_game.txt', 'r') as save_file:
            data = json.load(save_file)
            if data["best_score"]:
                return data["best_score"]
            return 0
    except FileNotFoundError:
        return 0
