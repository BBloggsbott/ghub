from .ghubutils import Context, GHub, Interpreter

def run_ghub():
    print("Welcome to GHub - A Unix like CLI for GitHub.")
    print("Starting initial setup...")
    ghub = GHub()
    context = Context(ghub.user)
    interpreter = Interpreter()
    print("Setup done.")
    while(True):
        command = input("ghub:{} {}> ".format(context.context, context.location))
        interpreter.execute(command, ghub, context)
