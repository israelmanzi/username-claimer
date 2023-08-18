import functions
import login
import turbo
import swapper
import target
import time
from subprocess import call

if __name__ == '__main__':
	functions.firsttime()
	functions.clear()
	# mode = input(functions.YELLOW + "[>] Please choose one of the following\n[>] 1 = Autoclaimer / Turbo\n[>] 2 = Swapper\n[>] 3 = Target Handle\n[>] 4 = Login to Accounts (If you haven't done this before or it's been a while)\n[>] Selection: ")
	mode = input(functions.YELLOW + "[>] Please choose one of the following\n[>] 1 = Claim username\n[>] 2 = Login to account (If you haven't done this before or it's been a while)\n[>] Selection: ")

	if mode == "1":
		print("\n")
		turbo.turbo()
	# elif mode == "2":
	# 	print("\n")
	# 	swapper.swapper()
	# elif mode == "3":
		# target.target()
	elif mode == "2":
		print("\n")
		login.logintotheaccounts()
	else:
		print(functions.CRED+ "\n[?] Invalid option, try again.")
		pass
