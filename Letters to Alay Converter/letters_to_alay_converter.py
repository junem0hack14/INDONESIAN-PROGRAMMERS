# Letters to Alay Converter


import sys


def get_index(elem: object, a_str: str) -> int:
	for i in range(len(a_str)):
		if a_str[i] == elem:
			return i
			
	return -1

letters: str = "abcdefghijklmnopqrstuvwxyz "
alay: str = "4BCD3F9H1JKLMN0PQR5TUVWXYZ "


def convert(a_str: str):
	# type: (str) -> str
	lower: str = a_str.lower()
	converted: str = ""  # initial value
	for letter in lower:
		letter_index: int = get_index(letter, letters)
		if letter_index != -1:
			converted += alay[letter_index]
		else:
			converted += letter.upper()
			
	return converted
	
	
def main():
	"""
	This function is used to run the program.
	:return:
	"""
	print("Enter 1 to do conversion.")
	print("Enter 2 to quit.")
	option: int = int(input("Please enter a number: "))
	while option < 1 or option > 2:
		option = int(input("Invalid input! Please enter a number: "))
		
	while option != 2:
		original_text: str = input("Please enter text that you want to convert to alay: ")
		converted: str = convert(original_text)
		print("Converted text is as below.\n", converted)
		option = int(input("Please enter a number: "))
		while option < 1 or option > 2:
			option = int(input("Invalid input! Please enter a number: "))
			
	sys.exit()
	
	
main()
