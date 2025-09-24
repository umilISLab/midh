def user_input(valid_options):
    opt = " / ".join(list(valid_options))
    error = True
    while error:
        iu = input(f"Scegli fra {opt}\n")
        error = not iu in valid_options
        if error:
            print(f"Ho detto {opt}!!!!")
        else:
            pass
    return iu
