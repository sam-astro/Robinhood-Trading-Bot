import robin_stocks.robinhood as robin
import pyotp
import sys
from time import sleep
import pandas as pd
from os import system
import colorama
from colorama import Fore, Back, Style
import time
import json
from datetime import datetime
colorama.init(autoreset=True)	
MFA = ''
login = robin.login('your-robinhood-email@email.com','yourrobinhoodPassword', MFA)
totp = pyotp.TOTP("your-one-time-password-code-that-robinhood-will-give-you").now()
#print("Current OTP:", totp)
returnData = [0]

t0=time.time()
#system('clear')

#robin.cancel_all_crypto_orders()
#def Gooo():
#	robin.cancel_all_crypto_orders()
#
#def po():
#	try:
#		Gooo()
#		sleep(10)
#	except:
#		pop()
#
#def pop():
#	try:
#		Gooo()
#		sleep(10)
#	except:
#		po()
#
#while True:
#	try:
#		Gooo()
#		sleep(10)
#	except:
#		po()
#

# Dollarsleft
# OwnedAmount
# Buys[]

def QUOTE(ticker):
	r = robin.get_latest_price(ticker)
	print(ticker.upper() + ": $" + str(r[0]))

def HISTC(ticker):
	histFile = open("./hist.txt","w")
	stock_data_week = robin.crypto.get_crypto_historicals(ticker, interval="week", span="year")
	stock_historical_week = pd.DataFrame(stock_data_week)
	for history in stock_historical_week.iloc:
		histFile.write(str(history['close_price']) + " ")

	histFile.close()
	
def HIST(ticker):
	print("Gathering History...")
	histFile = open("./hist.txt","w")
	stock_data_day = robin.stocks.get_stock_historicals(ticker, interval="week", span="5year")
	stock_historical_day = pd.DataFrame(stock_data_day)
	for history in stock_historical_day.iloc:
		histFile.write(str(history['close_price']) + " ")

	histFile.close()
	
def BUY(ticker, amount):
	r = robin.order_buy_market(ticker, amount)
	print(r['id'])
	
def SELL(ticker, amount):
	r = robin.order_sell_market(ticker, amount)
	print(r['id'])
	
def BUYC(ticker, amount):
	r = robin.order_buy_crypto_by_quantity(ticker, amount)
	print(r['id'])
	
def SELLC(ticker, amount):
	r = robin.order_sell_crypto_by_quantity(ticker, amount)
	print(r['id'])
	
def AUTO(ticker, maxDollars):
	
	ownedAmount = float(0);
	dollarsLeft = float(100000)
	buys = []
	houraverages = []
	lastprice = float(0)
	onehourlowlast = float(0)
	onehourhighlast = float(0)
	fiftytwoweekaverage = float(0)
	lasttotal = float(0)
	runtime = float(1) #Runtime is in hours
	
	currentPrice = float(robin.stocks.get_latest_price(ticker)[0])
	
	stock_data_day = robin.stocks.get_stock_historicals(ticker, interval="day", span="week")
	stock_historical_day = pd.DataFrame(stock_data_day)
	
	stock_data_week = robin.stocks.get_stock_historicals(ticker, interval="week", span="year")
	stock_historical_week = pd.DataFrame(stock_data_week)
	one_week_low = float(stock_historical_week.iloc[-1]['low_price']) * 1.0
	one_week_high = float(stock_historical_week.iloc[-1]['high_price'])
	
	fifty_two_week_average = (float(robin.stocks.get_fundamentals(ticker, info='low_52_weeks')[0])+float(robin.stocks.get_fundamentals(ticker, info='high_52_weeks')[0]))/2
	amounttotrade = float(maxDollars) / float(currentPrice)
	actionThisTime = ""
	print("Stock: " + ticker)
	
	# If the current price is more than the 1 week high
	if float(currentPrice) > float(one_week_high) and float(currentPrice) > (float(fifty_two_week_average) + float(currentPrice))/2:
		print(Fore.RED + "\033[1m" + "SELL!" + "\033[0m")
		r = robin.order_sell_fractional_by_quantity(ticker, amounttotrade)
		try:
			ownedAmount -= amounttotrade
			buys.remove(x)
			actionThisTime = "sold"
		except:
			print("failed")
			robin.cancel_all_stock_orders()
			actionThisTime = "failed"
	# If the current price is less than the 1 week low, greater than the large average
	if float(currentPrice) < float(one_week_high) and float(currentPrice) > (float(fifty_two_week_average) + float(currentPrice))/2:
		print(Fore.GREEN + "\033[1m" + "BUY!" + "\033[0m")
		r = robin.order_buy_fractional_by_quantity(ticker, amounttotrade)
		try:
			ownedAmount += amounttotrade
			buys.append(float(robin.orders.get_stock_order_info(r['id'])['price'])*amounttotrade)
			actionThisTime = "bought"
		except:
			print("failed")
			robin.cancel_all_stock_orders()
			actionThisTime = "failed"
	#Information indicators
	if float(currentPrice) > float(lastprice):
		print("Price:		   $" + Fore.GREEN + str(round(float(currentPrice)*1000)/1000))
	else:
		print("Price:		   $" + Fore.RED + str(round(float(currentPrice)*1000)/1000))
	print("Amnt Owned:		" + str(ownedAmount) + " at $" + str((round(float(ownedAmount) * float(currentPrice)*1000)/1000)))
	print("52	" + str(fifty_two_week_average))
	print("high " + str(one_week_high))
	print("low	" + str(one_week_low))
	print()
	print()
	sleep(3)
		
def SUGGEST():
	listofstocks= open("./listofstocks.txt", 'r+')
	tickers=listofstocks.read().split('\n')
	
	for ticker in tickers:
		if "//" not in ticker:
			ownedAmount = float(0);
			dollarsLeft = float(100000)
			buys = []
			houraverages = []
			lastprice = float(0)
			onehourlowlast = float(0)
			onehourhighlast = float(0)
			fiftytwoweekaverage = float(0)
			lasttotal = float(0)
			runtime = float(1) #Runtime is in hours
			
			currentPrice = float(robin.stocks.get_latest_price(ticker)[0])
			
			stock_data_day = robin.stocks.get_stock_historicals(ticker, interval="day", span="week")
			stock_historical_day = pd.DataFrame(stock_data_day)
			
			stock_data_week = robin.stocks.get_stock_historicals(ticker, interval="week", span="year")
			stock_historical_week = pd.DataFrame(stock_data_week)
			one_week_low = float(stock_historical_week.iloc[-1]['low_price']) * 1.0
			one_week_high = float(stock_historical_week.iloc[-1]['high_price'])
			
			fifty_two_week_average = (float(robin.stocks.get_fundamentals(ticker, info='low_52_weeks')[0])+float(robin.stocks.get_fundamentals(ticker, info='high_52_weeks')[0]))/2
			amounttotrade = 1
			actionThisTime = ""
			print("Stock: " + ticker)
			
			# If the current price is more than the 1 week high
			if float(currentPrice) > float(one_week_high) and float(currentPrice) > (float(fifty_two_week_average) + float(currentPrice))/2:
				print(Fore.RED + "\033[1m" + "SELL!" + "\033[0m")
				dollarsLeft += amounttotrade * currentPrice
				ownedAmount -= amounttotrade
				actionThisTime = "sold"
			# If the current price is less than the 1 week low, greater than the 52 week avg
			if float(currentPrice) < float(one_week_high) and float(currentPrice) > (float(fifty_two_week_average) + float(currentPrice))/2:
				print(Fore.GREEN + "\033[1m" + "BUY!" + "\033[0m")
				dollarsLeft -= currentPrice*amounttotrade
				ownedAmount += amounttotrade
				actionThisTime = "bought"
			#Information indicators
			if float(currentPrice) > float(lastprice):
				print("Price:		   $" + Fore.GREEN + str(round(float(currentPrice)*1000)/1000))
			else:
				print("Price:		   $" + Fore.RED + str(round(float(currentPrice)*1000)/1000))
			print("Amnt Owned:		" + str(ownedAmount) + " at $" + str((round(float(ownedAmount) * float(currentPrice)*1000)/1000)))
			print("52	" + str(fifty_two_week_average))
			print("high " + str(one_week_high))
			print("low	" + str(one_week_low))
			print()
			print()
		
def AUTOCC(ticker, maxDollars):
	print("\nStarted\n")
	
	persistence= open("./mytraderdata.txt", 'r+')
	lines=persistence.read().split('\n')
	if lines[0] != "0" or lines[1] != "0" or lines[2] != "":
		ans = input(Fore.YELLOW + "Persistance data found, do you wish to use it? Y/N  > " + Style.BRIGHT + Fore.WHITE)
		if ans.upper() == "Y":
			if len(lines) > 2:
				dollarsLeft = float(lines[0])
				print(dollarsLeft)
			else:
				dollarsLeft = float(maxDollars)

			if len(lines) > 2:
				ownedAmount = float(lines[1])
				print(ownedAmount)
			else:
				ownedAmount = float(0)

			if len(lines) > 2 and lines[2] != '':
				buyList = lines[2].split(',')
				buys = buyList
				print(buys)
			else:
				buys = []
		else:
			dollarsLeft = float(maxDollars)
			ownedAmount = float(0)
			buys = []
	else:
		dollarsLeft = float(maxDollars)
		ownedAmount = float(0)
		buys = []
	
	houraverages = []
	lastprice = float(0)
	onehourlowlast = float(0)
	onehourhighlast = float(0)
	onehouraverage = float(0)
	lasttotal = float(0)
	runtime = float(0) #Runtime is in hours
	
	if float(robin.crypto.get_crypto_quote(ticker, info="mark_price")) > float(maxDollars):
		amounttotrade = 0.50 / float(robin.crypto.get_crypto_quote(ticker, info="mark_price"))
	else:
		amounttotrade = 1
	largestBuy = float(0)
	amounttotrade = 30
	while True:
		returnData = [0]
		actionThisTime = ""
		print("")
		stock_data_minute = robin.crypto.get_crypto_historicals(ticker, interval="5minute", span="week")
		stock_historical_minute = pd.DataFrame(stock_data_minute)
		price_diff_fiveminutes = float(stock_historical_minute.iloc[-1]['close_price']) - float(stock_historical_minute.iloc[0]['close_price'])
		
		stock_data_day = robin.crypto.get_crypto_historicals(ticker, interval="day", span="week")
		stock_historical_day = pd.DataFrame(stock_data_day)
		price_diff_oneday = float(stock_historical_day.iloc[-1]['close_price']) - float(stock_historical_day.iloc[0]['close_price'])
		
		stock_data_hour = robin.crypto.get_crypto_historicals(ticker, interval="hour", span="week")
		stock_historical_hour = pd.DataFrame(stock_data_hour)
		
		one_hour_low = float(stock_historical_minute.iloc[-1]['low_price']) * 1.0
		one_hour_high = float(stock_historical_minute.iloc[-1]['high_price'])
		
		hour_average = float(pd.DataFrame(stock_data_hour).iloc[-1]['close_price'])

		dynamicChangePercent = (((float(one_hour_high) / float(one_hour_low))-1) / 2) + 1
		#dynamicChangePercent = 1.02
		#r = robin.order_sell_crypto_by_quantity(ticker, amount)
		for x in buys:
			if float(x) > float(largestBuy):
				largestBuy = float(x)
			# If the current price is more than the 1 hour high and it's price has increased
			if float(robin.crypto.get_crypto_quote(ticker, info="mark_price"))*amounttotrade > float(x) * float(dynamicChangePercent) and actionThisTime == "" and ownedAmount >= amounttotrade:
				print(Fore.RED + "\033[1m" + "SELL!" + "\033[0m")
				r = robin.order_sell_crypto_by_quantity(ticker, amounttotrade)
				try:
					count = float(0)
					while True:
						sleep(1)
						count += 1
						if robin.orders.get_crypto_order_info(r['id'])['state'] == 'filled':
							dollarsLeft += amounttotrade * float(robin.orders.get_crypto_order_info(r['id'])['price'])
							ownedAmount -= amounttotrade
							buys.remove(x)
							actionThisTime = "sold"
							break
						if count >= 6 and robin.orders.get_crypto_order_info(r['id'])['state'] != 'filled':
							try:
								robin.cancel_crypto_order(r['id'])
								actionThisTime = "failed"
							except:
								dollarsLeft += amounttotrade * float(robin.orders.get_crypto_order_info(r['id'])['price'])
								ownedAmount -= amounttotrade
								buys.remove(x)
								actionThisTime = "sold"
							break
				except:
					try:
						robin.cancel_crypto_order(r['id'])
						actionThisTime = "failed"
					except:
						dollarsLeft += amounttotrade * float(robin.orders.get_crypto_order_info(r['id'])['price'])
						ownedAmount -= amounttotrade
						buys.remove(x)
						actionThisTime = "sold"
			if float(robin.crypto.get_crypto_quote(ticker, info="mark_price"))*amounttotrade < float(x) * 0.9 and float(ownedAmount) >= amounttotrade and actionThisTime == "":
				r = robin.order_sell_crypto_by_quantity(ticker, amounttotrade)['id']
				try:
					count = float(0)
					while True:
						sleep(1)
						count += 1
						if robin.orders.get_crypto_order_info(r['id'])['state'] == 'filled':
							print(Fore.RED + "\033[1m" + "SELL! (scaredy)" + "\033[0m")
							dollarsLeft += float(robin.orders.get_crypto_order_info(r['id'])['price'])*amounttotrade
							ownedAmount -= amounttotrade
							buys.remove(x)
							actionThisTime = "sold"
							break
						if count >= 6 and robin.orders.get_crypto_order_info(r['id'])['state'] != 'filled':
							try:
								robin.cancel_crypto_order(r['id'])
								actionThisTime = "failed"
							except:
								dollarsLeft += amounttotrade*float(robin.orders.get_crypto_order_info(r['id'])['price'])
								ownedAmount -= amounttotrade
								buys.remove(x)
								actionThisTime = "sold"
							break
				except:
					try:
						robin.cancel_crypto_order(r['id'])
						actionThisTime = "failed"
					except:
						dollarsLeft += amounttotrade * float(robin.orders.get_crypto_order_info(r['id'])['price'])
						ownedAmount -= amounttotrade
						buys.remove(x)
						actionThisTime = "sold"
		if largestBuy == 0:
			largestBuy = float(robin.crypto.get_crypto_quote(ticker, info="mark_price"))
		# If the current price is less than the 1 hour low, greater than the large average, you can pay for it, and the current value is less than 101% of the largest bought value so far
		if float(robin.crypto.get_crypto_quote(ticker, info="mark_price")) < float(one_hour_low) * 1 and (float(robin.crypto.get_crypto_quote(ticker, info="mark_price"))*float(amounttotrade) < float(dollarsLeft)) and actionThisTime == "" and round(time.time()-t0) / 60 / 60 < float(runtime) and float(robin.crypto.get_crypto_quote(ticker, info="mark_price")) <= float(largestBuy) * 1.05:
			#also code above this stops buying after a certain time, so it can close all trades for that period of time
			print(Fore.GREEN + "\033[1m" + "BUY!" + "\033[0m")
			r = robin.order_buy_crypto_by_quantity(ticker, amounttotrade)
			
			try:
				count = float(0)
				while True:
					sleep(1)
					count += 1
					if robin.orders.get_crypto_order_info(r['id'])['state'] == 'filled':
						dollarsLeft -= float(robin.orders.get_crypto_order_info(r['id'])['price'])*amounttotrade
						ownedAmount += amounttotrade
						buys.append(float(robin.orders.get_crypto_order_info(r['id'])['price'])*amounttotrade)
						actionThisTime = "bought"
						break
					if count >= 6 and robin.orders.get_crypto_order_info(r['id'])['state'] != 'filled':
						try:
							robin.cancel_crypto_order(r['id'])
							actionThisTime = "failed"
						except:
							dollarsLeft += amounttotrade * float(robin.orders.get_crypto_order_info(r['id'])['price'])
							ownedAmount -= amounttotrade
							buys.remove(x)
							actionThisTime = "bought"
						break
			except:
				try:
					robin.cancel_crypto_order(r['id'])
					actionThisTime = "failed"
				except:
					dollarsLeft += amounttotrade * float(robin.orders.get_crypto_order_info(r['id'])['price'])
					ownedAmount -= amounttotrade
					buys.remove(x)
					actionThisTime = "bought"
		#Information indicators
		persistence.close()
		persistencewrite= open("./mytraderdata.txt", 'w')
		if float(robin.crypto.get_crypto_quote(ticker, info="mark_price")) > float(lastprice):
			print("Price:		   $" + Fore.GREEN + str(round(float(robin.crypto.get_crypto_quote(ticker, info="mark_price"))*1000)/1000))
		else:
			print("Price:		   $" + Fore.RED + str(round(float(robin.crypto.get_crypto_quote(ticker, info="mark_price"))*1000)/1000))
		if float(one_hour_high) > float(onehourhighlast):
			print("5 min high:	  $" + Fore.GREEN + str(round(one_hour_high*1000)/1000))
		else:
			print("5 min high:	  $" + Fore.RED + str(round(one_hour_high*1000)/1000))
			
		if float(one_hour_low) > float(onehourlowlast):
			print("5 min low:	  $" + Fore.GREEN + str(round(one_hour_low*1000)/1000))
		else:
			print("5 min low:	  $" + Fore.RED + str(round(one_hour_low*1000)/1000))
			
		if float(hour_average) > float(onehouraverage):
			print("1 Hr Avg:	  $" + Fore.GREEN + str(round(hour_average*1000)/1000))
		else:
			print("1 Hr Avg:	  $" + Fore.RED + str(round(hour_average*1000)/1000))
			
		print("Dollars:		   $" + str(dollarsLeft))
		persistencewrite.write(str(dollarsLeft) + "\n")
		print("Amnt Owned:		" + str(ownedAmount) + " at $" + str((round(float(ownedAmount) * float(robin.crypto.get_crypto_quote(ticker, info="mark_price"))*1000)/1000)))
		persistencewrite.write(str(ownedAmount) + "\n")
		if float(dollarsLeft) + (float(ownedAmount) * float(robin.crypto.get_crypto_quote(ticker, info="mark_price"))) > float(lasttotal):
			print("Total:		   $" + Fore.GREEN + str(round((float(dollarsLeft) + (float(ownedAmount) * float(robin.crypto.get_crypto_quote(ticker, info="mark_price"))))*1000)/1000))
		else:
			print("Total:		   $" + Fore.RED + str(round((float(dollarsLeft) + (float(ownedAmount) * float(robin.crypto.get_crypto_quote(ticker, info="mark_price"))))*1000)/1000))
		
		if len(buys) > 0:
			cnt = int(0)
			for buy in buys:
				if cnt < len(buys) - 1:
					persistencewrite.write(str(buy) + ",")
				else:
					persistencewrite.write(str(buy))
				cnt+=1
		
		seconds = round(time.time()-t0)
		minutes = 0
		hours = 0
		while seconds >= 60:
			seconds-=60
			minutes+=1
		while minutes >= 60:
			minutes-=60
			hours+=1
		print("Time Elapsed:	" + str(hours) + ":" + str(minutes) + ":" + str(seconds) + " at " + str(datetime.now()))
		added = float(0)
		for y in houraverages:
			added += float(y)
		if actionThisTime != "":
			houraverages.append((((float(dollarsLeft) + (float(ownedAmount) * float(robin.crypto.get_crypto_quote(ticker, info="mark_price"))))-float(maxDollars))/float(time.time()-t0))*60*60)
		#if len(houraverages) > 0:
		#	if float(added)/float(len(houraverages)) > 0:
		#		print (Fore.YELLOW + "$ Per Hour:	   $" + str(round(float(added)/float(len(houraverages))*100)/100) + " at " + Fore.GREEN + "+%" + str(((round(float(added)/float(len(houraverages))*100)/100)/float(maxDollars))*100))
		#	else:
		#		print (Fore.YELLOW + "$ Per Hour:	   $" + str(round(float(added)/float(len(houraverages))*100)/100) + " at " + Fore.RED + "-%" + str(((round(float(added)/float(len(houraverages))*100)/100)/float(maxDollars))*100))
		print("Dynamic percent:	   " + str( round( ((float(dynamicChangePercent) - 1) * 100) * 10 ) / 10 ) + "%	   OR	$" + str(round( ((float(dynamicChangePercent) - 1) * float(robin.crypto.get_crypto_quote(ticker, info="mark_price"))) * 100 ) / 100))
		lastprice = robin.crypto.get_crypto_quote(ticker, info="mark_price")
		onehourlowlast = one_hour_low
		onehourhighlast = one_hour_high
		onehouraverage = hour_average
		lasttotal = float(dollarsLeft) + (float(ownedAmount) * float(robin.crypto.get_crypto_quote(ticker, info="mark_price")))
		if float(seconds) / 60 /60 >= runtime and float(ownedAmount) <= 0:
			if (float(dollarsLeft)-float(maxDollars)) > 0:
				print("Successfully closed trading session with a profit of " + Fore.GREEN + str(float(dollarsLeft)-float(maxDollars)) + Fore.WHITE + " dollars")
			else:
				print("Successfully closed trading session with a profit of " + Fore.RED + str(float(dollarsLeft)-float(maxDollars)) + Fore.WHITE + " dollars")
			exit()
		persistencewrite.close()
		sleep(40)
		#system('clear')
		
		
		
		
def AUTOCA(ticker, maxDollars):
	print("\nStarted\n")
	ownedAmount = float(0);
	dollarsLeft = float(maxDollars);
	buys = []
	houraverages = []
	lastprice = float(0)
	onehourlowlast = float(0)
	onehourhighlast = float(0)
	fiftytwoweekaverage = float(0)
	lasttotal = float(0)
	
	stock_data_minuteA = robin.crypto.get_crypto_historicals(ticker, interval="5minute", span="week")
	stock_historical_minuteA = pd.DataFrame(stock_data_minuteA)
	
	stock_data_hourA = robin.crypto.get_crypto_historicals(ticker, interval="hour", span="week")
	stock_historical_hourA = pd.DataFrame(stock_data_hourA)
	if float(stock_historical_hourA.iloc[int(-1)]['close_price']) > float(maxDollars):
		amounttotrade = 2 / float(stock_historical_hourA.iloc[int(-24)]['close_price'])
	else:
		amounttotrade = 20
	secondcount = int(0)
	while True:
		secondcount += int(60)
		seconds = secondcount
		minutes = 0
		hours = 0
		while seconds >= 60:
			seconds-=60
			minutes+=1
		while minutes >= 60:
			minutes-=60
			hours+=1
		actionThisTime = ""
		print("")
		stock_data_minute = robin.crypto.get_crypto_historicals(ticker, interval="5minute", span="week")
		stock_historical_minute = pd.DataFrame(stock_data_minute)
		
		stock_data_day = robin.crypto.get_crypto_historicals(ticker, interval="day", span="week")
		stock_historical_day = pd.DataFrame(stock_data_day)
		
		stock_data_hour = robin.crypto.get_crypto_historicals(ticker, interval="hour", span="week")
		stock_historical_hour = pd.DataFrame(stock_data_hour)
		one_hour_low = float(stock_historical_hour.iloc[int(hours)-24]['low_price']) * 1.45
		one_hour_high = float(stock_historical_hour.iloc[int(hours)-24]['high_price'])
		
		fifty_two_week_average = (float(pd.DataFrame(stock_data_hour).iloc[int(hours)-36]['close_price'])+float(pd.DataFrame(stock_data_hour).iloc[int(hours)-35]['close_price'])+float(pd.DataFrame(stock_data_hour).iloc[int(hours)-34]['close_price'])+float(pd.DataFrame(stock_data_hour).iloc[int(hours)-33]['close_price'])+float(pd.DataFrame(stock_data_hour).iloc[int(hours)-32]['close_price'])+float(pd.DataFrame(stock_data_hour).iloc[int(hours)-31]['close_price'])+float(pd.DataFrame(stock_data_hour).iloc[int(hours)-30]['close_price'])+float(pd.DataFrame(stock_data_hour).iloc[int(hours)-29]['close_price'])+float(pd.DataFrame(stock_data_hour).iloc[int(hours)-28]['close_price'])+float(pd.DataFrame(stock_data_hour).iloc[int(hours)-27]['close_price'])+float(pd.DataFrame(stock_data_hour).iloc[int(hours)-26]['close_price'])+float(pd.DataFrame(stock_data_hour).iloc[int(hours)-25]['close_price']))/13
		#r = robin.order_sell_crypto_by_quantity(ticker, amount)
		largestBuy = float(0)
		for x in buys:
			if float(x) > float(largestBuy):
				largestBuy = float(x)
			# If the current price is more than the 1 hour high and it's price has increased
			if float(pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price'])*amounttotrade > float(x) * 1.01 and actionThisTime == "":
				print(Fore.RED + "\033[1m" + "SELL!" + "\033[0m")
				secondcount+=20
				dollarsLeft += amounttotrade * float(pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price'])
				ownedAmount -= amounttotrade
				buys.remove(x)
				actionThisTime = "sold"
			if float(pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price'])*amounttotrade < float(x) * 0.900 and float(ownedAmount) >= amounttotrade and actionThisTime == "":
				print(Fore.RED + "\033[1m" + "SELL! (scaredy)" + "\033[0m")
				secondcount+=20
				dollarsLeft += amounttotrade * float(pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price'])
				ownedAmount -= amounttotrade
				buys.remove(x)
				actionThisTime = "sold"
		if largestBuy == 0:
			largestBuy = float(pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price'])
		# If the current price is less than the 1 hour low, greater than the large average, you can pay for it, and the current value is less than 101% of the largest bought value so far
		if (float(pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price']) < float(one_hour_low) and float(pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price']) > float(fifty_two_week_average)) and (float(pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price'])*amounttotrade < float(dollarsLeft)) and actionThisTime == "" and float(secondcount) / 60 / 60 < 15 and float(pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price']) <= float(largestBuy) * 1.02:
			#also code above this stops buying after a certain time, so it can close all trades for that period of time
					print(Fore.GREEN + "\033[1m" + "BUY!" + "\033[0m")
					secondcount+=20
					dollarsLeft -= amounttotrade * float(pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price'])
					ownedAmount += amounttotrade
					buys.append(float(pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price'])*amounttotrade)
					actionThisTime = "sold"
		#Information indicators
		if float(pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price']) > float(lastprice):
			print("Price:		   $" + Fore.GREEN + str(round(float(pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price'])*1000)/1000))
		else:
			print("Price:		   $" + Fore.RED + str(round(float(pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price'])*1000)/1000))
			
		if float(one_hour_high) > float(onehourhighlast):
			print("Hour high:	   $" + Fore.GREEN + str(round(one_hour_high*1000)/1000))
		else:
			print("Hour high:	   $" + Fore.RED + str(round(one_hour_high*1000)/1000))
			
		if float(one_hour_low) > float(onehourlowlast):
			print("Hour low:	   $" + Fore.GREEN + str(round(one_hour_low*1000)/1000))
		else:
			print("Hour low:	   $" + Fore.RED + str(round(one_hour_low*1000)/1000))
			
		if float(fifty_two_week_average) > float(fiftytwoweekaverage):
			print("12 Hr Avg:	   $" + Fore.GREEN + str(round(fifty_two_week_average*1000)/1000))
		else:
			print("12 Hr Avg:	   $" + Fore.RED + str(round(fifty_two_week_average*1000)/1000))
			
		print("Dollars:		   $" + str(dollarsLeft))
		print("Amnt Owned:		" + str(ownedAmount) + " at $" + str((round(float(ownedAmount) * float(pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price'])*1000)/1000)))
		if float(dollarsLeft) + (float(ownedAmount) * float(pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price'])) > float(lasttotal):
			print("Total:		   $" + Fore.GREEN + str(round((float(dollarsLeft) + (float(ownedAmount) * float(pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price'])))*1000)/1000))
		else:
			print("Total:		   $" + Fore.RED + str(round((float(dollarsLeft) + (float(ownedAmount) * float(pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price'])))*1000)/1000))
		print("Time Elapsed:	" + str(hours) + ":" + str(minutes) + ":" + str(seconds))
		added = float(0)
		for y in houraverages:
			added += float(y)
		if actionThisTime != "":
			houraverages.append((((float(dollarsLeft) + (float(ownedAmount) * float(pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price'])))-float(maxDollars))/float(time.time()-t0))*60*60)
		if len(houraverages) > 0:
			if float(added)/float(len(houraverages)) > 0:
				print (Fore.YELLOW + "$ Per Hour:	   $" + str(round(float(added)/float(len(houraverages))*100)/100) + " at " + Fore.GREEN + "+%" + str(((round(float(added)/float(len(houraverages))*100)/100)/float(maxDollars))*100))
			else:
				print (Fore.YELLOW + "$ Per Hour:	   $" + str(round(float(added)/float(len(houraverages))*100)/100) + " at " + Fore.RED + "-%" + str(((round(float(added)/float(len(houraverages))*100)/100)/float(maxDollars))*100))
		lastprice = pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price']
		onehourlowlast = one_hour_low
		onehourhighlast = one_hour_high
		fiftytwoweekaverage = fifty_two_week_average
		lasttotal = float(dollarsLeft) + (float(ownedAmount) * float(pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price']))
		#system('clear')

# $1017 @5hrs
# $11 @5hrs
def AUTOCSIM(ticker, maxDollars):
	print("\nStarted\n")
	ownedAmount = float(0);
	dollarsLeft = float(maxDollars);
	buys = []
	houraverages = []
	lastprice = float(0)
	onehourlowlast = float(0)
	onehourhighlast = float(0)
	fiftytwoweekaverage = float(0)
	lasttotal = float(0)
	
	stock_data_minuteA = robin.crypto.get_crypto_historicals(ticker, interval="5minute", span="week")
	stock_historical_minuteA = pd.DataFrame(stock_data_minuteA)
	
	stock_data_hourA = robin.crypto.get_crypto_historicals(ticker, interval="hour", span="week")
	stock_historical_hourA = pd.DataFrame(stock_data_hourA)
	if float(stock_historical_hourA.iloc[int(-24)]['close_price']) > float(maxDollars):
		amounttotrade = 2 / float(stock_historical_hourA.iloc[int(-24)]['close_price'])
	else:
		amounttotrade = 20
	secondcount = int(0)
	while True:
		secondcount += int(60)
		seconds = secondcount
		minutes = 0
		hours = 0
		while seconds >= 60:
			seconds-=60
			minutes+=1
		while minutes >= 60:
			minutes-=60
			hours+=1
		actionThisTime = ""
		print("")
		stock_data_minute = robin.crypto.get_crypto_historicals(ticker, interval="5minute", span="week")
		stock_historical_minute = pd.DataFrame(stock_data_minute)
		
		stock_data_day = robin.crypto.get_crypto_historicals(ticker, interval="day", span="week")
		stock_historical_day = pd.DataFrame(stock_data_day)
		
		stock_data_hour = robin.crypto.get_crypto_historicals(ticker, interval="hour", span="week")
		stock_historical_hour = pd.DataFrame(stock_data_hour)
		one_hour_low = float(stock_historical_hour.iloc[int(hours)-24]['low_price']) * 1.45
		one_hour_high = float(stock_historical_hour.iloc[int(hours)-24]['high_price'])
		
		fifty_two_week_average = (float(pd.DataFrame(stock_data_hour).iloc[int(hours)-36]['close_price'])+float(pd.DataFrame(stock_data_hour).iloc[int(hours)-35]['close_price'])+float(pd.DataFrame(stock_data_hour).iloc[int(hours)-34]['close_price'])+float(pd.DataFrame(stock_data_hour).iloc[int(hours)-33]['close_price'])+float(pd.DataFrame(stock_data_hour).iloc[int(hours)-32]['close_price'])+float(pd.DataFrame(stock_data_hour).iloc[int(hours)-31]['close_price'])+float(pd.DataFrame(stock_data_hour).iloc[int(hours)-30]['close_price'])+float(pd.DataFrame(stock_data_hour).iloc[int(hours)-29]['close_price'])+float(pd.DataFrame(stock_data_hour).iloc[int(hours)-28]['close_price'])+float(pd.DataFrame(stock_data_hour).iloc[int(hours)-27]['close_price'])+float(pd.DataFrame(stock_data_hour).iloc[int(hours)-26]['close_price'])+float(pd.DataFrame(stock_data_hour).iloc[int(hours)-25]['close_price']))/13
		#r = robin.order_sell_crypto_by_quantity(ticker, amount)
		largestBuy = float(0)
		for x in buys:
			if float(x) > float(largestBuy):
				largestBuy = float(x)
			# If the current price is more than the 1 hour high and it's price has increased
			if float(pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price'])*amounttotrade > float(x) * 1.01 and actionThisTime == "":
				print(Fore.RED + "\033[1m" + "SELL!" + "\033[0m")
				secondcount+=20
				dollarsLeft += amounttotrade * float(pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price'])
				ownedAmount -= amounttotrade
				buys.remove(x)
				actionThisTime = "sold"
			if float(pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price'])*amounttotrade < float(x) * 0.900 and float(ownedAmount) >= amounttotrade and actionThisTime == "":
				print(Fore.RED + "\033[1m" + "SELL! (scaredy)" + "\033[0m")
				secondcount+=20
				dollarsLeft += amounttotrade * float(pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price'])
				ownedAmount -= amounttotrade
				buys.remove(x)
				actionThisTime = "sold"
		if largestBuy == 0:
			largestBuy = float(pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price'])
		# If the current price is less than the 1 hour low, greater than the large average, you can pay for it, and the current value is less than 101% of the largest bought value so far
		if (float(pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price']) < float(one_hour_low) and float(pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price']) > float(fifty_two_week_average)) and (float(pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price'])*amounttotrade < float(dollarsLeft)) and actionThisTime == "" and float(secondcount) / 60 / 60 < 15 and float(pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price']) <= float(largestBuy) * 1.02:
			#also code above this stops buying after a certain time, so it can close all trades for that period of time
					print(Fore.GREEN + "\033[1m" + "BUY!" + "\033[0m")
					secondcount+=20
					dollarsLeft -= amounttotrade * float(pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price'])
					ownedAmount += amounttotrade
					buys.append(float(pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price'])*amounttotrade)
					actionThisTime = "sold"
		#Information indicators
		if float(pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price']) > float(lastprice):
			print("Price:		   $" + Fore.GREEN + str(round(float(pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price'])*1000)/1000))
		else:
			print("Price:		   $" + Fore.RED + str(round(float(pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price'])*1000)/1000))
			
		if float(one_hour_high) > float(onehourhighlast):
			print("Hour high:	   $" + Fore.GREEN + str(round(one_hour_high*1000)/1000))
		else:
			print("Hour high:	   $" + Fore.RED + str(round(one_hour_high*1000)/1000))
			
		if float(one_hour_low) > float(onehourlowlast):
			print("Hour low:	   $" + Fore.GREEN + str(round(one_hour_low*1000)/1000))
		else:
			print("Hour low:	   $" + Fore.RED + str(round(one_hour_low*1000)/1000))
			
		if float(fifty_two_week_average) > float(fiftytwoweekaverage):
			print("12 Hr Avg:	   $" + Fore.GREEN + str(round(fifty_two_week_average*1000)/1000))
		else:
			print("12 Hr Avg:	   $" + Fore.RED + str(round(fifty_two_week_average*1000)/1000))
			
		print("Dollars:		   $" + str(dollarsLeft))
		print("Amnt Owned:		" + str(ownedAmount) + " at $" + str((round(float(ownedAmount) * float(pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price'])*1000)/1000)))
		if float(dollarsLeft) + (float(ownedAmount) * float(pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price'])) > float(lasttotal):
			print("Total:		   $" + Fore.GREEN + str(round((float(dollarsLeft) + (float(ownedAmount) * float(pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price'])))*1000)/1000))
		else:
			print("Total:		   $" + Fore.RED + str(round((float(dollarsLeft) + (float(ownedAmount) * float(pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price'])))*1000)/1000))
		print("Time Elapsed:	" + str(hours) + ":" + str(minutes) + ":" + str(seconds))
		added = float(0)
		for y in houraverages:
			added += float(y)
		if actionThisTime != "":
			houraverages.append((((float(dollarsLeft) + (float(ownedAmount) * float(pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price'])))-float(maxDollars))/float(time.time()-t0))*60*60)
		if len(houraverages) > 0:
			if float(added)/float(len(houraverages)) > 0:
				print (Fore.YELLOW + "$ Per Hour:	   $" + str(round(float(added)/float(len(houraverages))*100)/100) + " at " + Fore.GREEN + "+%" + str(((round(float(added)/float(len(houraverages))*100)/100)/float(maxDollars))*100))
			else:
				print (Fore.YELLOW + "$ Per Hour:	   $" + str(round(float(added)/float(len(houraverages))*100)/100) + " at " + Fore.RED + "-%" + str(((round(float(added)/float(len(houraverages))*100)/100)/float(maxDollars))*100))
		lastprice = pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price']
		onehourlowlast = one_hour_low
		onehourhighlast = one_hour_high
		fiftytwoweekaverage = fifty_two_week_average
		lasttotal = float(dollarsLeft) + (float(ownedAmount) * float(pd.DataFrame(stock_data_minute).iloc[minutes-720]['close_price']))
		#system('clear')
		


if len(sys.argv[1:]) > 2:
	TICKER = sys.argv[1:][1].upper()
	ACTION = sys.argv[1:][0]
	AMOUNT = sys.argv[1:][2]
	if ACTION.upper() == "-BUY":
		print("Buying " + AMOUNT + " of " + TICKER + "...")
		BUY(TICKER, AMOUNT)
	if ACTION.upper() == "-SELL":
		print("Selling " + AMOUNT + " of " + TICKER + "...")
		SELL(TICKER, AMOUNT)
	if ACTION.upper() == "-BUYC":
		print("Buying " + AMOUNT + " of crypto " + TICKER + "...")
		BUYC(TICKER, AMOUNT)
	if ACTION.upper() == "-SELLC":
		print("Selling " + AMOUNT + " of crypto " + TICKER + "...")
		SELLC(TICKER, AMOUNT)
	if ACTION.upper() == "-AUTOCA":
		print("Automatically trading crypto " + TICKER + " using $" + AMOUNT)
		AUTOCA(TICKER, AMOUNT)
	if ACTION.upper() == "-AUTOCB":
		print("Automatically trading crypto " + "\033[1m" + TICKER + "\033[0m" + " using $" + "\033[1m" + AMOUNT + "\033[0m")
		AUTOCB(TICKER, AMOUNT)
	if ACTION.upper() == "-AUTOCC":
		print("Automatically trading crypto " + "\033[1m" + TICKER + "\033[0m" + " using $" + "\033[1m" + AMOUNT + "\033[0m")
		AUTOCC(TICKER, AMOUNT)
	if ACTION.upper() == "-AUTOCSIM":
		print("Automatically trading crypto " + "\033[1m" + TICKER + "\033[0m" + " using $" + "\033[1m" + AMOUNT + "\033[0m")
		AUTOCSIM(TICKER, AMOUNT)
	if ACTION.upper() == "-AUTO":
		print("Automatically trading stock for $" + AMOUNT)
		AUTO(TICKER, AMOUNT)
		
elif len(sys.argv[1:]) > 1:
	ACTION = sys.argv[1:][0]
	AMOUNT = sys.argv[1:][1]
	TICKER = sys.argv[1:][1]
	if ACTION.upper() == "-HIST":
		TICKER = sys.argv[1:][1].upper()
		HIST(TICKER)
	if ACTION.upper() == "-HISTC":
		TICKER = sys.argv[1:][1].upper()
		HISTC(TICKER)
elif len(sys.argv[1:]) > 0:
	ACTION = sys.argv[1:][0]
	if ACTION.upper() == "-HELP":
		print("Format:	   mytrader -[action] [ticker] [amount]")
		print()
		print("-help	   Opens this help menu")
		print("-buy		   Buys a certain amount of a given stock")
		print("-sell	   Sells a certain amount of a given stock")
		print("-buyc	   Buys a certain amount of a given cryptocurrency")
		print("-sellc	   Sells a certain amount of a given cryptocurrency")
		print("-auto	   Automatically trades for all stocks in ./listofstocks.txt")
		print("-autoca	   Automatically trades a given cryptocurrency for you using strategy A")
		print("-autocb	   Automatically trades a given cryptocurrency for you using strategy B")
		print("-autocc	   Automatically trades a given cryptocurrency for you using strategy C")
		print("-autocsim   Tests an automatic trading algorithm based on previous prices")
		print("-hist	   Gathers history of stock and prints in neural network format to hist.txt")
		print("-histc	   Gathers history of crypto and prints in neural network format to hist.txt")
		print("-quote	   Gets quote for stock")
		print("-suggest	   Suggests what to do for all stocks in ./listofstocks.txt")
		exit()
	if ACTION.upper() == "-QUOTE":
		TICKER = sys.argv[1:][1].upper()
		QUOTE(TICKER)
	if ACTION.upper() == "-SUGGEST":
		print("Suggesting for list of tickers")
		SUGGEST()
else:
	print("Syntax error, try typing -help to learn more about the commands")
