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
            print(row.firstname)
    return

def update_row():
    show_data()
    while True:
        user_input=int(input("Which row do you want to update? Write number (starting from 1): "))
        try:
            with Session(engine) as session:
                users = session.query(User).all()
                if 1<=user_input<=len(users):
                    user_input_2=input("Which row you want to update? Firstname, Lastname or Email?")
                    if user_input_2.lower() in ("firstname", "lastname", "email"):
                        user_row=user_input-1
                        User.up
                    else:
                        print("Invalid column name, try again")
                        continue
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue
        except Exception as e:
            print(f"An error occurred: {e}")
            continue
#comms={1:show_data,2:add_row,3:delete_row,4:update_row,5:quit}
