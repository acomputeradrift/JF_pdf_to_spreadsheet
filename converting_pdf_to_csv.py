#! python3.9
#python3 converting_pdf_to_csv.py




# Reading first pdf file

import PyPDF2
import pdfplumber
import re
import os



#get the number of pages
#map it to index (page_count-1)
#pass index as range to get each page text
#check the first line of each page for 'YOUR TRANSACTIONS'
#if the first line == 'YOUR TRANSACTIONS' then get date list from page
#do this for each page with the transactions title

#maybe get date, add to list and then delete all dates.  Then grab the first words and process that?


#classes

class Transaction:
		def __init__(self,date):
			self.date = date
			self.account_type = ''
			self.transaction_description = ''
			self.product_code = ''
			self.currency = ''
			self.number_of_units = ''
			self.unit_price = ''
			self.gross_amount = ''
			self.deduction = ''
			self.cash_account_transaction = ''
			self.net_amount = ''

class Account:
		def __init__(self,number):
			self.number = number
			self.name = ''
			self.balance = 0


def get_number_of_pages_from(my_pdf):
    with open(my_pdf, 'rb') as f:
        pdf = PyPDF2.PdfFileReader(f)
        info = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()
        return number_of_pages


def get_the_text_from(pdf_at_complete_path, page): 
	#this gets the text from the page of the index
	index = page + 1
	with pdfplumber.open(pdf_at_complete_path) as pdf:
		first_page = pdf.pages[page]
		the_extracted_text = first_page.extract_text()
		#print(f'\nScanned page {index} of {pdf_at_complete_path}.')
		return the_extracted_text


def get_lines_containing_dates_list_from(the_extracted_text): #this extracts the date list from each page of extracted data
	date_regex = r'((([0-9])|([0-2][0-9])|([3][0-1]))\-(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\-\d{4})|(T\+[0-9]+)'
	lines_containing_dates_list = []
	for line in the_extracted_text.split('\n'):
		match = re.search(date_regex,line)
		if match:
			lines_containing_dates_list.append(line)
	return lines_containing_dates_list

def get_transaction_info_from(pdf_at_complete_path):
	number_of_pages = get_number_of_pages_from(pdf_at_complete_path)
	all_transaction_lists_on_this_pdf_list = []
	for page in range(number_of_pages):
		all_transactions_on_this_page_list = []
		this_transaction_list = []
		this_page = get_the_text_from(pdf_at_complete_path,page)
		#print(this_page)
		 #this gets the text from one page
		first_line = this_page.partition('\n')[0] #this gets the first line of one page for comparison
		second_line = this_page.partition('\n')[1]
		if 'TRANSACTION' in first_line or 'TRANSACTION' in second_line:
			#print('Transactions found:')
			#print(f'This page data:\n{this_page}')
			lines_containing_dates_list = get_lines_containing_dates_list_from(this_page)

			#use the date list to get each transaction line, ignoring anything without a date at the start
			for line in lines_containing_dates_list:
				this_line_list = line.split()
				date = this_line_list[0]
				#get acount type by combining two words
				account_type = this_line_list[1] + ' ' + this_line_list[2]
				currency_index = this_line_list.index('CAD') #this is the anchor from which all else links
				product_code = this_line_list[currency_index-1]
				product_code_index = currency_index-1 #somewhere between 4 and 6

				all_words_in_transaction_description = []
				for i in range(3, product_code_index):
					all_words_in_transaction_description.append(this_line_list[i])
				transaction_description = ' '.join(all_words_in_transaction_description)

				currency = this_line_list[currency_index]
				number_of_units = this_line_list[currency_index+1]
				unit_price = this_line_list[currency_index+2]
				gross_amount = this_line_list[currency_index+3]
				deduction = this_line_list[currency_index+4]
				cash_account_transaction = this_line_list[currency_index+5]
				try:
					net_amount = this_line_list[currency_index+6]
				except IndexError:
					net_amount = '-'
				this_transaction_list = [date,account_type,product_code,transaction_description,currency,number_of_units,unit_price,gross_amount,deduction,cash_account_transaction,net_amount]
				#print(this_transaction_list)
				all_transactions_on_this_page_list.append(this_transaction_list) 
			#print(all_transactions_on_this_page_list)
		# else:
		# 	print('No transactions found on this page.')
		all_transaction_lists_on_this_pdf_list.append(all_transactions_on_this_page_list)
			
	return all_transaction_lists_on_this_pdf_list
	#return this_transaction_list

def get_lines_containing_account_numbers_list_from(this_page):
	account_regex = r'#'
	lines_containing_account_numbers_list = []
	for line in this_page.split('\n'):   #this_page.split('\n'):
		match = re.search(account_regex,line)
		if match:
			lines_containing_account_numbers_list.append(line)
	return lines_containing_account_numbers_list


def get_new_style_transaction_info_from(pdf_at_complete_path):
	number_of_pages = get_number_of_pages_from(pdf_at_complete_path)
	all_transaction_lists_on_this_pdf_list = []
	for page in range(number_of_pages):
		all_transactions_on_this_page_list = []
		this_transaction_list = []
		this_page = get_the_text_from(pdf_at_complete_path,page)
		#print(this_page)
		 #this gets the text from one page
		first_line = this_page.partition('\n')[0] #this gets the first line of one page for comparison
		second_line = this_page.partition('\n')[1]
		if 'TRANSACTION' in first_line or 'TRANSACTION' in second_line:
			print(f'Transactions found:\n {this_page}\n----------------------------')
			#print(f'This page data:\n{this_page}')
			lines_containing_account_numbers_list = get_lines_containing_account_numbers_list_from(this_page)

			#use the date list to get each transaction line, ignoring anything without a date at the start
			for line in lines_containing_account_numbers_list:
				print(line)
				print('---------------------------------------')
	# 			this_line_list = line.split()
	# 			date = this_line_list[0]
	# 			#get acount type by combining two words
	# 			account_type = this_line_list[1] + ' ' + this_line_list[2]
	# 			currency_index = this_line_list.index('CAD') #this is the anchor from which all else links
	# 			product_code = this_line_list[currency_index-1]
	# 			product_code_index = currency_index-1 #somewhere between 4 and 6

	# 			all_words_in_transaction_description = []
	# 			for i in range(3, product_code_index):
	# 				all_words_in_transaction_description.append(this_line_list[i])
	# 			transaction_description = ' '.join(all_words_in_transaction_description)

	# 			currency = this_line_list[currency_index]
	# 			number_of_units = this_line_list[currency_index+1]
	# 			unit_price = this_line_list[currency_index+2]
	# 			gross_amount = this_line_list[currency_index+3]
	# 			deduction = this_line_list[currency_index+4]
	# 			cash_account_transaction = this_line_list[currency_index+5]
	# 			try:
	# 				net_amount = this_line_list[currency_index+6]
	# 			except IndexError:
	# 				net_amount = '-'
	# 			this_transaction_list = [date,account_type,product_code,transaction_description,currency,number_of_units,unit_price,gross_amount,deduction,cash_account_transaction,net_amount]
	# 			#print(this_transaction_list)
	# 			all_transactions_on_this_page_list.append(this_transaction_list) 
	# 		#print(all_transactions_on_this_page_list)
	# 	# else:
	# 	# 	print('No transactions found on this page.')
	# 	all_transaction_lists_on_this_pdf_list.append(all_transactions_on_this_page_list)
			
	# return all_transaction_lists_on_this_pdf_list
	# #return this_transaction_list

def get_your_account_object_list_from(your_account_page):
	account_object_list = []
	account_number_list = []
	account_name_list = []
	account_numbers_regex = r'(?<=Account number:).+?(?=\n)'
	account_number_list = re.findall(account_numbers_regex, your_account_page)
	#breakdown the string into lines
	line_list = your_account_page.splitlines()
	for line in line_list:
		for account_number in account_number_list:
			if account_number in line:
				index = line_list.index(line)
				index_for_the_line_above = index - 1
				verbose_account_name = line_list[index_for_the_line_above]
				account_name = verbose_account_name.split(' - ')
				account_name_list.append(account_name[0])
	for i, account_number in enumerate(account_number_list):
		this_account_object = Account(account_number)
		this_account_object.name = account_name_list[i]
		account_object_list.append(this_account_object)
	return account_object_list



def get_your_account_page_list_from(pdf_at_complete_path): 
	#this gets the 'your account' pages and combines them if they are on multipe pages then returns the list of them
	your_account_pages_list = []
	full_account_string = '' #these two lines are for combining multiple page 'your accounts'
	number_of_account_pages = 0
	number_of_pages = get_number_of_pages_from(pdf_at_complete_path)
	all_transaction_lists_on_this_pdf_list = []
	for page in range(number_of_pages):
		all_transactions_on_this_page_list = []
		this_transaction_list = []
		this_page = get_the_text_from(pdf_at_complete_path,page)
		# print(this_page)
		# print('---------------------------------------')
		first_line = this_page.partition('\n')[0] #this gets the first line of one page for comparison
		second_line = this_page.partition('\n')[1]
		if 'YOUR ACCOUNTS' in first_line or 'YOUR ACCOUNTS' in second_line:
			number_of_account_pages += 1  #these two lines combine multiple page your accounts
			full_account_string += this_page
			print(f'Your Accounts found:\n {full_account_string}\n----------------------------')
			your_account_pages_list.append(full_account_string)
	return your_account_pages_list
#-----------------------------------------------------VARIABLES-------------------------------

TFSA = '#339698847'
RRSP = '#339579618'
OPEN = '#339555240'

total_list_of_transaction_objects = []
total_list_of_account_objects = []
#my_pdf = '/Users/Jamie/Desktop/Quarterly statement.pdf - 2019 339199914.pdf'
#path = '/Users/Jamie/Desktop/pdf_files/Old_Statements/'
old_style_path = '/Users/Jamie/Desktop/pdf_files/Old_Statements/'
new_style_path = '/Users/Jamie/Desktop/pdf_files/New_Statements/'

#-----------------------------------------------------BEGIN-------------------------------

#Old Style PDFs
# for filename in os.listdir(old_style_path):
# 	print(f'Filename:{filename}')
# 	pdf_at_complete_path = os.path.join(old_style_path, filename)
# 	#this_pdf_date_list = get_transaction_info_from(pdf_at_complete_path)
# 	all_transaction_lists_on_this_pdf_list = get_transaction_info_from(pdf_at_complete_path)
# 	for transaction_lists in all_transaction_lists_on_this_pdf_list:
# 		for transaction in transaction_lists:
# 			#create and update the object
# 			this_transaction = Transaction(transaction[0])
# 			this_transaction.account_type = transaction[1]
# 			this_transaction.transaction_description = transaction[2]
# 			this_transaction.product_code = transaction[3]
# 			this_transaction.currency = transaction[4]
# 			this_transaction.number_of_units = transaction[5]
# 			this_transaction.unit_price = transaction[6]
# 			this_transaction.gross_amount = transaction[7]
# 			this_transaction.deduction = transaction[8]
# 			this_transaction.cash_account_transaction = transaction[9]
# 			this_transaction.net_amount = transaction[10]
# 			total_list_of_transaction_objects.append(this_transaction


#New Style PDFs
# for filename in os.listdir(new_style_path):
# 	print(f'Filename:{filename}')
# 	pdf_at_complete_path = os.path.join(new_style_path, filename)
# 	#this_pdf_date_list = get_transaction_info_from(pdf_at_complete_path)
# 	all_transaction_lists_on_this_pdf_list = get_new_style_transaction_info_from(pdf_at_complete_path)
# 	for transaction_lists in all_transaction_lists_on_this_pdf_list:
# 		for transaction in transaction_lists:
# 			#create and update the object
# 			this_transaction = Transaction(transaction[0])
# 			this_transaction.account_type = transaction[1]
# 			this_transaction.transaction_description = transaction[2]
# 			this_transaction.product_code = transaction[3]
# 			this_transaction.currency = transaction[4]
# 			this_transaction.number_of_units = transaction[5]
# 			this_transaction.unit_price = transaction[6]
# 			this_transaction.gross_amount = transaction[7]
# 			this_transaction.deduction = transaction[8]
# 			this_transaction.cash_account_transaction = transaction[9]
# 			this_transaction.net_amount = transaction[10]
# 			total_list_of_transaction_objects.append(this_transaction)

#Get the summary from old style PDFs
for filename in os.listdir(old_style_path):
	print(f'Filename:{filename}')
	pdf_at_complete_path = os.path.join(old_style_path, filename)
	#this_pdf_date_list = get_transaction_info_from(pdf_at_complete_path)
	your_account_pages_list = get_your_account_page_list_from(pdf_at_complete_path)
	for your_account_page in your_account_pages_list:
		account_object_list = get_your_account_object_list_from(your_account_page)
		total_list_of_account_objects += account_object_list
		#this is where the duplicates start
		#how to compare the number for each rather than the object itself.  There is no dupicate objects but some duplicate numbers
		no_duplicates_list = list(set(total_list_of_account_objects))



#no_duplicates_list = list(set(total_list_of_account_objects))
print(no_duplicates_list)
# for account_object in no_duplicates_list:
# 		print(account_object.__dict__)

# for transaction_object in total_list_of_transaction_objects:
# 	print(f'{transaction_object.__dict__}\n')







