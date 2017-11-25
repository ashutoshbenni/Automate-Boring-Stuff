#Prgram to fetch subtiltes for movies from http://www.yifysubtitles.com/

#system requires - Python3.x (A MUST) otherwise for Python2.x change all input() to raw_input() in code			
#			bs4
#			requests
#			Chrome browser
#			selenium
#			to install above use "pip2/pip3 install package_name"

from selenium import webdriver
from bs4 import BeautifulSoup as Soup
import requests
from sys import exit
from time import sleep
import re


main_url = "http://www.yifysubtitles.com"


def get_page_source(url):

	page_source = requests.get(url)
	soup = Soup(page_source.content, "html.parser")
	return soup

def abort_program():

	print("Aborting program.")
	sleep(3)
	exit(0)
	
def get_user_input(options):
	
	
	print("please enter the index of which movie's subtile you want ot download or enter 0 to exit")
	try:
		user_input = int(input().strip())
		count = 0
	except ValueError:
		print("input should be numric only.")
		abort_program()
				 	
	#At max 2 chances to enter right input
	while count < 2:
	
		count += 1
		if 0 <= user_input <= options:
			return user_input if user_input else exit(0)
		elif count < 2:
			print("invalid option. Please enter again")
			try:
				user_input = int(input().strip())
			except ValueError:
				print("input should numeric only.")
				abort_program()	
	abort_program()
		
		
def scrape_search_list(url):

	if not url:#if url is empty
		print("URL is empty")
		exit(0)
	print("WebScraping {0}".format(url))
	
	#getting HTML code of given url
	page_source = requests.get(url)
	soup = Soup(page_source.content, 'html.parser')
	
	#check if no results are there
	if str(soup.text).count("no results"):
		print("No results found.")
		sleep(3)
		print("Aborted")
		exit(0)
	
	#dictionary for index - movie_name
	d = {}
	d[0] = "Exit"
	
	#fetching movie names in <h3> tag
	for index, movie  in enumerate(soup.find_all("h3", {"class":"media-heading"}), 1):
		d[index] = movie.text,movie.find_previous().find_previous().get('href')
		print("{0} - {1}".format((index), d[index][0]))

	#getting user_input for given movie list 
	user_select = get_user_input(index)
	print("fetching subtitles for {0}". format(d[user_select][0]))
	return d[user_select][1]


def download_subtitles(url):

	
	soup = get_page_source(url)
	
	list_of_english_subtitles = {}
	count = 1 
	for subtitle in soup.find_all("tr", {"data-id":re.compile("[^\-][0-9]+")}):
		if subtitle.contents[1].text == "English":
			list_of_english_subtitles[int(subtitle.contents[0].text)] = subtitle.contents[2].text, subtitle.find("a").get("href")
			count += 1
	fav = max(list_of_english_subtitles)
	download_zip_url = main_url + list_of_english_subtitles[fav][1].replace("/subtitles/", "/subtitle/") + ".zip"
	print(download_zip_url)
	
	driver = webdriver.Chrome()
	driver.get(download_zip_url)
	sleep(5)
	
	
	
def main():
	
	#removing unnecessary left and righ spaces of text
	movie = input("please enter movie name\n").strip()
	
	#removing single/mulitpal spaces with '+'
	movie = re.sub(" +", "+", movie)
	
	#setting URL
	url = "http://www.yifysubtitles.com/search?q={0}".format(movie) 	
	search = scrape_search_list("http://www.yifysubtitles.com/search?q={0}".format(movie))
	
	download_subtitles(main_url + search)
	

if __name__ == "__main__":
	main()
	
