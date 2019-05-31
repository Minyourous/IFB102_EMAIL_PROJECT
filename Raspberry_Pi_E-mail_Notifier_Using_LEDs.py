import time
import adafruit_character_lcd.character_lcd as characterlcd
from imapclient import IMAPClient
import board
import digitalio

HOSTNAME = 'imap.gmail.com'
MAILBOX = 'Inbox'
MAIL_CHECK_FREQ = 10        # check mail every 10 seconds

# The following three variables must be customized for this
# script to work
USERNAME = 'IFB102boi@gmail.com'
PASSWORD = 'Secret.123'
NEWMAIL_OFFSET = 0          # my unread messages never goes to zero, use this to override

# setup Pi pins as output for LEDs
lcd_rs = digitalio.DigitalInOut(board.D22)
lcd_en = digitalio.DigitalInOut(board.D17)
lcd_d4 = digitalio.DigitalInOut(board.D25)
lcd_d5 = digitalio.DigitalInOut(board.D24)
lcd_d6 = digitalio.DigitalInOut(board.D23)
lcd_d7 = digitalio.DigitalInOut(board.D18)

lcd_columns = 16
lcd_rows = 2

lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

def mail_check():
	# login to mailserver
	server = IMAPClient(HOSTNAME, use_uid=True, ssl=True)
	server.login(USERNAME, PASSWORD)

	#fetch from address
	

	# select our MAILBOX and looked for unread messages
	unseen = server.folder_status(MAILBOX, ['UNSEEN'])

	# number of unread messages
	# print to console to determine NEWMAIL_OFFSET
	newmail_count = (unseen[b'UNSEEN'])
	print('%d unseen messages' % newmail_count)
	lcd.clear()
	lcd.message = '%d IN INBOX' % newmail_count
	time.sleep(5.0)
	lcd.clear()

	if newmail_count > NEWMAIL_OFFSET:
		lcd_line1 = 'NEW MAIL'
		time.sleep(5.0)
		lcd.clear()

	else:
		lcd.message = 'NO NEW MAIL'
		time.sleep(5.0)
		lcd.clear()

	time.sleep(MAIL_CHECK_FREQ)

while True:
	mail_check()
