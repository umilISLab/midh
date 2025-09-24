from game_utils import user_input

morra = {'C', 'S', 'F'}
tris = {'X', 'O'}

u = user_input(valid_options=tris)

print(f"L'utente ha scelto: {u}")