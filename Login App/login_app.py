import sys
import pickle


class Account:
	"""
	This class contains attributes of an account.
	"""
	
	def __init__(self, username, password):
		# type: (str, str) -> None
		self.username: str = username
		self.password: str = password
		
	def to_string(self):
		# type: () -> str
		return "Username: " + str(self.username) + "\nPassword: " + str(self.password) + "\n"
		
		
def main():
	"""
	This class is used to run the program.
	:return:
	"""
	accounts: list # initial value
	print("Enter 1 to sign-up.")
	print("Enter 2 to login.")
	filename: str = "Accounts Saved"
	try:
		accounts = pickle.load(open(filename, "rb"))
	except FileNotFoundError:
		accounts = []
	
	option: int = int(input("Please enter a number: "))
	while option < 1 or option > 2:
		option = int(input("Invalid input! Please enter a number: "))
		
	if option == 1:
		usernames_used: list = [accounts[i].username for i in range(len(accounts))]
		username: str = input("Please enter your username: ")
		while username in usernames_used:
			username = input("Username already used! Please enter another username: ")
			
		password: str = input("Please enter your password: ")
		new_account: Account = Account(username, password)
		print("Your new account's details are as below.\n", new_account.to_string())
		accounts.append(new_account)
	else:
		print("Please login to your account.")
		username: str = input("Please enter your username: ")
		password: str = input("Please enter your password: ")
		has_match: bool = False  # initial value
		for account in accounts:
			if account.username == username and account.password == password:
				has_match = True
				break
				
		if not has_match:
			print("Invalid username or password!")
		else:
			print("Login successful!")
			
	pickle.dump(accounts, open(filename, "wb"))
	sys.exit()
	
	
main()
