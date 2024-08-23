import re
import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,Session

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id:Mapped[int]=mapped_column(primary_key=True)
    firstname: Mapped[str]
    lastname: Mapped[str]
    email: Mapped[str]

engine=sa.create_engine("sqlite:///users.db")
Base.metadata.create_all(engine)

def add_row():
    while True:
        print("Put the information like this: firstname lastname email (THE SPACES ARE IMPORTANT!)")
        user_input = input("Write the info: ")

        try:
            firstname, lastname, email = user_input.split()
            if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,4}$", email):
                print("Invalid email format. Please try again.")
                continue
            with Session(engine) as session:
                session.add(User(firstname=firstname, lastname=lastname, email=email))
                session.commit()
                print("User added successfully.")
                break


        except ValueError:

            print(
                "Incorrect input format. Please ensure you provide firstname, lastname, and email separated by spaces.")

        except Exception as e:

            print(f"An error occurred: {e}")

            print("Please try again.")


def delete_row():
    show_data()
    try:
        user_input = int(input("Which row do you want to delete? Write number (starting from 1): "))

        with Session(engine) as session:
            users = session.query(User).all()

            if 1 <= user_input <= len(users):
                user_to_delete = users[user_input - 1]
                session.delete(user_to_delete)
                session.commit()
                print("User deleted successfully.")
            else:
                print("Invalid row number.")

    except ValueError:
        print("Invalid input. Please enter a valid number.")
    except Exception as e:
        print(f"An error occurred: {e}")

def show_data():
    with Session(engine) as session:
        users=session.query(User).all()
        for row in users:
            print(f'{row.firstname} {row.lastname} {row.email}')
    return


def update_row():
    show_data()  # Assuming this function displays users with row numbers starting from 1

    while True:
        try:
            user_input = int(input("Which row do you want to update? Write number (starting from 1): "))

            with Session(engine) as session:
                users = session.query(User).all()  # Get all users

                if 1 <= user_input <= len(users):  # Check if the input is within the valid range
                    user_to_update = users[user_input - 1]  # Get the user based on the 1-indexed input
                    print(f'Current data: {user_to_update.firstname} {user_to_update.lastname} {user_to_update.email}')

                    user_input_2 = input("Which field do you want to update? (firstname, lastname, email): ").lower()

                    if user_input_2 in ("firstname", "lastname", "email"):
                        user_input_3 = input(f"Write the new value for {user_input_2}: ")

                        # Update the corresponding field dynamically
                        setattr(user_to_update, user_input_2, user_input_3)

                        session.commit()  # Commit the changes to the database
                        print("The update has been successful.")
                        break  # Exit the loop after a successful update
                    else:
                        print("Invalid field name, please try again.")
                else:
                    print("Invalid row number.")

        except ValueError:
            print("Invalid input. Please enter a valid number.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    print("Welcome to the database")
    comms = {1: show_data, 2: add_row, 3: delete_row, 4: update_row, 5: quit}

    while True:
        inp = int(input("Write what you want\n"
                        "1 to show data\n"
                        "2 to add new user\n"
                        "3 to delete user\n"
                        "4 to update user\n"
                        "5 to exit\n"))
        comms[inp]()
