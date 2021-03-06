#! python3.9
#python3 converting_pdf_to_csv.py




# Reading first pdf file

import PyPDF2
import pdfplumber
import re
import os
from datetime import datetime, timedelta



#get the number of pages
#map it to index (page_count-1)
#pass index as range to get each page text
#check the first line of each page for 'YOUR TRANSACTIONS'
#if the first line == 'YOUR TRANSACTIONS' then get date list from page
#do this for each page with the transactions title

#maybe get date, add to list and then delete all dates.  Then grab the first words and process that?


#classes
class Statement:
	def __init__(self,start_and_end_date):
			self.start_date = start_and_end_date[0]  #how to make this a timedelta?
			self.end_date = start_and_end_date[1]  #how to make this a timedelta?
			self.client_number = 0
			self.account = Account
		

class Transaction:
		def __init__(self,date):
			self.date = date_time
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
			self.book_value = 0
			self.market_value = 0
			#self.total_date = datetime #this is the final date of the time period of the statement
			self.sub_account = SubAccount


class SubAccount:
		def __init__(self,fund_code):
			self.name = ''
			self.fund_code = fund_code
			self.number = 0
			self.book_value = 0
			self.number_of_units = 0
			self.unit_price = 0
			self.market_value = 0
			self.transaction = Transaction

#------------------------------------------REUSABLE METHODS---------------------------

def print_list(this_list):
	for this_item in this_list:
		print(this_item)

def print_list_of_lists(this_list_of_lists):
	for this_list in this_list_of_lists:
		print()
		for this_item in this_list:
			print(this_item)

def print_list_of_objects(this_list_of_objects):
	for this_object in this_list_of_objects:
		print(this_object.__dict__)

def get_number_of_pages_from(my_pdf):
    with open(my_pdf, 'rb') as f:
        pdf = PyPDF2.PdfFileReader(f)
        info = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()
        return number_of_pages

def get_the_text_from(pdf_at_complete_path, page): #this gets the text from each page number sent to it from the PDF
	#this gets the text from the page of the index
	index = page + 1
	with pdfplumber.open(pdf_at_complete_path) as pdf:
		first_page = pdf.pages[page]
		the_extracted_text = first_page.extract_text()
		#print(f'\nScanned page {index} of {pdf_at_complete_path}.')
		return the_extracted_text

#------------------------------------------STATEMENT METHODS---------------------------

def get_start_and_end_date_from(pdf_at_complete_path):  #For the period of 2019-04-01 to 2019-06-30
	#go through each page until a time period is found, then stop
	number_of_pages = get_number_of_pages_from(pdf_at_complete_path)
	for page in range(number_of_pages):
		this_page = get_the_text_from(pdf_at_complete_path,page)
		#get the whole line containing the time period
		period_line_regex = r'(For the period of .*)'
		period_line = re.search(period_line_regex, this_page)
		
		if period_line is not None:
			dates_regex = r'(?:[12]\d{3}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01]))'
			dates_list = re.findall(dates_regex, period_line.group())
			#break it into 2 dates
			start_date = dates_list[0]
			end_date = dates_list[1]
			time_period = (start_date, end_date)
			#print(f'From the method: {time_period}')
			return(time_period)
		else:
			#print(f'No time period found on page {page+1}.')	
			pass

def get_the_client_number_from(pdf_at_complete_path):
	number_of_pages = get_number_of_pages_from(pdf_at_complete_path)
	for page in range(number_of_pages):
		this_page = get_the_text_from(pdf_at_complete_path,page)
		#get the whole line containing the client number
		client_number_regex = r'(?<=Client number: ).+?(?=\n)'
		client_number = re.search(client_number_regex, this_page)
		if client_number is not None:
			return client_number.group(0)
		else:
			#print(f'No client number found on page {page+1}.')
			pass

#------------------------------------------TRANSACTION METHODS---------------------------

def get_lines_containing_dates_list_from(the_extracted_text): #this extracts list of dates from each page of extracted data
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
	return lines_containing_account_numbers_list #called from get_new_style_transaction_info_from(pdf_at_complete_path)

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

#------------------------------------------ACCOUNT METHODS---------------------------

def get_your_account_page_list_from(pdf_at_complete_path): #gather all pages with "Your Account" on it, combine if needed
	#this gets the 'your account' pages and combines them if they are on multipe pages then returns the list of them
	your_account_pages_list = []
	full_account_string = '' #these two lines are for combining multiple page 'your accounts'
	number_of_your_account_pages = 0
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
			number_of_your_account_pages += 1  #these two lines combine multiple page your accounts
			#print(number_of_account_pages)
			if number_of_your_account_pages == 1:
				full_account_string = this_page
				#print(f'-------Start of single page-------\n Your Accounts found and pages combined:\n {full_account_string}\n-------End of single page-----------')
			else:
				full_account_string += this_page
				#print(f'-------Start of combined string-------\n Your Accounts found and pages combined:\n {full_account_string}\n-------End of combined String-----------')
	#print(f'--------------\n Your Accounts found and pages combined:\n {full_account_string}\n------------------')
	your_account_pages_list.append(full_account_string)
	return your_account_pages_list

def get_your_account_number_list_from(your_account_pages_list): #account numbers found and master list of unique account numbers created

	#change this to create a list of account numbers, DO NOT update the object
	total_list_of_account_numbers = []
	for your_account_page in your_account_pages_list:
		account_numbers_list = []
		account_numbers_regex = r'(?<=Account number:).+?(?=\n)'
		account_numbers_list = re.findall(account_numbers_regex, your_account_page)
	total_list_of_account_numbers += account_numbers_list
	unique_account_numbers_list = remove_duplicate_account_numbers_from(total_list_of_account_numbers)	
	#print(unique_account_numbers_list)
	return unique_account_numbers_list

def remove_duplicate_account_numbers_from(total_list_of_account_numbers): #called from get_your_account_numbers_list_from(your_account_pages_list)
	new_dict = dict()
	for account_number in total_list_of_account_numbers:
		if account_number not in new_dict:
			new_dict[account_number] = account_number
	unique_account_numbers_list = list(new_dict.values())
	return unique_account_numbers_list

def get_each_account_number_info_list(unique_account_numbers_list, your_account_page_list):
	list_of_all_account_data_lists = []
	for your_account_page in your_account_page_list:
		list_of_lists = []
		index_list = []
		line_list = your_account_page.splitlines()
		for account_number in unique_account_numbers_list:
			#print(f'account number for search: {account_object.number}')
			for line in line_list:
				#print(f'line: {line}')
				if account_number in line:
					#print(f'account number found in line: {account_object.number}')
					this_index = line_list.index(line)
					#print(f'index of line containing the accout number found: {this_index}')
					index_list.append(this_index-1)
		index_list.append(len(line_list))
		index_list.sort()
		for i in range(len(index_list)-1):  #this is the count of the items in index_list
			#print(i)
			this_account_data_broken_down_as_list = []
			for ii in range(index_list[i], index_list[i+1]): 
				#print(ii)
				this_account_data_broken_down_as_list.append(line_list[ii])
			list_of_all_account_data_lists.append(this_account_data_broken_down_as_list)
			# print_list(each_list) 
	return list_of_all_account_data_lists 

def get_attributes_for_each_unique_account_number_from(list_of_all_account_data_lists, unique_account_numbers_list):
	list_of_all_accounts_attributes_lists = []
	for each_account_number in unique_account_numbers_list:
		account_number = 0
		account_name = 'no name'
		book_value = 0
		market_value = 0
		for each_account_number_info in list_of_all_account_data_lists:
			for each_line in each_account_number_info:
				if each_account_number in each_line:
					account_number_index = each_account_number_info.index(each_line)
					verbose_account_number = each_account_number_info[account_number_index].split(':')
					account_number = verbose_account_number[1]
					#print(f'Account number found: {account_number}')
					verbose_account_name = each_account_number_info[account_number_index-1].split(' - ')
					account_name = verbose_account_name[0]
					for each_line in each_account_number_info:
						#print(each_line)
						total_of_investments_regex = r'(Total of investments )(.*)'
						match = re.search(total_of_investments_regex, each_line)
						if match:
							#print('Total investments match!')
							both_totals_of_investments = match.group(2).split(' ')
							book_value = float(both_totals_of_investments[0].replace('$','').replace(',',''))
							market_value = float(both_totals_of_investments[1].replace('$','').replace(',',''))
							#print(f'Book value found: {book_value}')
							#print(f'Market value found: {market_value}')
						else:
							#print('No Total of investments regex match')
							pass
				else:
					#print(f'No number, name when searching for this account number: {each_account_number}')
					pass
		this_account_attributes_list = [account_number, account_name, book_value, market_value]
		#print(this_account_attributes_list)
		list_of_all_accounts_attributes_lists.append(this_account_attributes_list)
	#print_list_of_lists(list_of_all_accounts_attributes_lists)
	return list_of_all_accounts_attributes_lists

#--------------------------------------------VARIABLES-------------------------------------

# TFSA = '#339698847'
# RRSP = '#339579618'
# OPEN = '#339555240'

total_list_of_transaction_objects = []
total_list_of_account_objects = []
#my_pdf = '/Users/Jamie/Desktop/Quarterly statement.pdf - 2019 339199914.pdf'
#path = '/Users/Jamie/Desktop/pdf_files/Old_Statements/'
old_style_path = '/Users/Jamie/Desktop/pdf_files/Old_Statements/'
new_style_path = '/Users/Jamie/Desktop/pdf_files/New_Statements/'

#-----------------------------------------------------BEGIN-------------------------------

#What do I need from each file?  All unique accounts with name, number, subaccounts (with name, number, balance)
for filename in os.listdir(old_style_path):
	total_list_of_account_objects = []
	print(f'-----------------------------------------Filename:{filename}')
	pdf_at_complete_path = os.path.join(old_style_path, filename)

	#----------gather the attributes to populate the STATEMENT objects and then create them

	start_and_end_date = get_start_and_end_date_from(pdf_at_complete_path)
	client_number = get_the_client_number_from(pdf_at_complete_path)

	this_statement = Statement(start_and_end_date) #can this be a touple of datetimes?
	this_statement.client_number = client_number

	#----------gather the attributes to populate the ACCOUNT objects and then create them

	your_account_pages_list = get_your_account_page_list_from(pdf_at_complete_path) #gets any page that has "Your Account" on the top, combines into 1 if needed
	unique_account_numbers_list = get_your_account_number_list_from(your_account_pages_list)
	list_of_all_account_data_lists = get_each_account_number_info_list(unique_account_numbers_list, your_account_pages_list)
	list_of_all_accounts_attributes_lists = get_attributes_for_each_unique_account_number_from(list_of_all_account_data_lists, unique_account_numbers_list)
	#print_list_of_lists(list_of_all_accounts_attributes_lists)


	#create and update the account objects here after I have all of the information

	for each_account_attributes_list in list_of_all_accounts_attributes_lists:
		this_account = Account(each_account_attributes_list[0])
		this_account.name = each_account_attributes_list[1]
		this_account.book_value = each_account_attributes_list[2]
		this_account.market_value = each_account_attributes_list[3]	
		total_list_of_account_objects.append(this_account)
	#print_list_of_objects(total_list_of_account_objects)

	for account_object in total_list_of_account_objects:
		this_statement.account = account_object

	print(this_statement.__dict__)





	
	#----------create the sub account objects and gather the info to populate it

	#for each account pages list, get the sub account info and add it to the proper account

	#----------create the transaction objects and gather the info to populate it

#----------create a list of Statements for comparison and graphing













	#this_pdf_date_list = get_transaction_info_from(pdf_at_complete_path)
	
	#print(your_account_pages_list)
	
	
	#, your_account_page)

	# for your_account_page in your_account_pages_list:
	# 	account_object_list = get_your_account_object_list_from(your_account_page)
	# 	#print_list_of_objects(account_object_list)
	# 	total_list_of_account_objects += account_object_list
	# 	#print_list_of_objects(total_list_of_account_objects)
	# 	#print()
	# 	unique_account_objects_list = remove_duplicate_accounts_from(total_list_of_account_objects)
	# 	#print_list_of_objects(unique_account_objects_list)
	# 	list_of_all_account_data_lists = get_each_account_info_list(unique_account_objects_list, your_account_page)
	# 	#here I need to update the object with the balance
	# 	print(each_account_info)
	# 	print()
	#at this point, all the data from each file is collected.

		#print()


	#each page grabs the info after the account number and before the next account number or the end of the page
	# for account_page in your_account_pages_list:
	# 	index_list = []
	# 	line_list = account_page.splitlines()
	# 	for account_object in unique_account_objects_list:
	# 		#print(f'account number for search: {account_object.number}')
	# 		for line in line_list:
	# 			#print(f'line: {line}')
	# 			if account_object.number in line:
	# 				#print(f'account number found in line: {account_object.number}')
	# 				this_index = line_list.index(line)
	# 				#print(f'index of line containing the accout number found: {this_index}')
	# 				index_list.append(this_index-1)
	# 	index_list.append(len(line_list))
	# 	index_list.sort()
	# 	for i in range(len(index_list)-1):  #this is the count of the items in index_list
	# 		#print(i)
	# 		each_list = []
	# 		for ii in range(index_list[i], index_list[i+1]): #this is the 
	# 			#print(ii)
	# 			each_list.append(line_list[ii])
	# 		print_list(each_list) 
			#print('***********************')




#-----------------------------------------------------------

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









