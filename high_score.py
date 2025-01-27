def get_high_score():
    with open("high_score.txt", "r") as file:
        high_score = int(file.read())
    return high_score
    
def save_high_score(new_high_score):
    with open("high_score.txt", "wt") as file:
        file.write(str(new_high_score))
