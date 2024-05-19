"""
Entry point of the application.
It creates an instance of the Pypong class and runs it
"""


from pypong.pong import Pypong


if __name__ == "__main__":
    pypong = Pypong()
    pypong.run()