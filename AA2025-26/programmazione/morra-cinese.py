from game_utils import user_input, UniformPlayer

morra = list({'C', 'S', 'F'})

player1 = UniformPlayer(valid_options=morra)

outcomes = {
    "S": {"S": "X", "C": "2", "F": "1"},
    "C": {"S": "1", "C": "X", "F": "2"},
    "F": {"S": "2", "C": "1", "F": "X"}
}

user_choice = user_input(valid_options=morra)
machine_choice = player1.play()

result = outcomes[user_choice][machine_choice]

print(f"Il risultato è: {result}")