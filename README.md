# trinkeypass
Adafruit Neo Trinkey password safe

## Intro

   Password managers and keys do a good job of authenticating us, but
each has at least one passphrase for authentication.  I find I need a
physical store for these especially sensitive passwords, passphrases, and
pins.  For that, we have the TrinKeyPass - the world's smallest password
vault.



## Quickstart

### Initial setup

1. Buy an Adafruit Neo Trinkey (<https://adafru.it/4870> , redirects to
<https://www.adafruit.com/product/4870> $6.95 ea., bulk discounts
available).  Better yet, buy 2 so you have a backup.

2. If you only have USB-C ports, buy a USB-A -> USB-C adaptor
(<https://www.amazon.com/gp/product/B086WFD4V6/>, $4.99 for a 4-pack).

3. If you want to connect it to a keychain, order some 1mm wide chains
(<https://www.amazon.com/gp/product/B01A438QHG/> , $9.60 for a 50-pack)

4. Download the firmware from <https://adafru.it/RD7> , redirects to
<https://circuitpython.org/board/neopixel_trinkey_m0/> .  You need the
UF2 file, which will download with a filename like
adafruit-circuitpython-neopixel_trinkey_m0-en_US-6.2.0.uf2 .

5. Insert the Trinkey into a USB port.  On a Mac - and possibly other
platforms too - the OS may note that a new keyboad and/or drive have been
inserted.  Feel free to dismiss any windows asking you to identify the
keyboard.  If you're asked if you want to automatically mount the drive,
I'd suggest Yes while you're going through this initial setup, then
change that to No when you're finished adding passwords.

6. Tap the black reset button in the middle of the board **twice**.

7. The storage on the Trinkey will be automatically mounted (under
/Volumes/TRINKEYBOOT/ on a Mac.)

8. Copy the .UF2 file into this directory.  All the LEDs will turn red,
that drive will automatically disconnect (and put up a harmless warning
that it disconnected without unmounting first).

9. After a few seconds it will mount the real storage you need (on
/Volumes/CIRCUITPY/ on a Mac).

10. Download trinkeypass.py from
https://raw.githubusercontent.com/william-stearns/trinkeypass/main/trinkeypass.py
, place it in this directory, and name it code.py.  Here's the command to
do it:

```
cd /Volumes/CIRCUITPY/
curl -fsSL https://raw.githubusercontent.com/william-stearns/trinkeypass/main/trinkeypass.py -o code.py
touch .metadata_never_index
sync
```

11. If you don't already have any password files (like 0000.txt and
0001.txt), create 2 test "password" files for Trinkey to use:

```
cd /Volumes/CIRCUITPY/
echo "This is a test password in 0000.txt." >>0000.txt
echo "And here's another one in 0001.txt" >>0001.txt
sync
```




### Trinkeypass components

1. You've already used the reset button, the black button between the
LEDs and the largest chip.  If anything goes weird, tap it once to
restart the software.

2. There are 4 LEDs numbered 0-3.  LED 0 is next to the reset button. 
LEDs 1-3 are clockwise from LED 0.  When the trinkeypass software starts,
it flashes the 4 LEDs in order in blue.

3. There are two touch-sensitive pads, T1 and T2 at the far end from the
USB connector.  You'll tap one or both of these to get the Trinkey to do
something.  T2 is on the same edge as the reset button, T1 on the
opposite edge.  (The board has a "1" and a "2" silkscreened as reminders
next to the pads and the outermost LEDs.)



### Using the password feature

1. Click your mouse in a window where you can enter some text.  This can
be a graphical application (notepad/gedit) or a text window/terminal.  To
see what's returned without any chance of actually doing something, run
the command `cat >/dev/null` to show and discard all keys.

2. Press button T2 (again, the one on the same edge as the reset key). 
This will send the contents of 0000.txt to your computer as if you'd
typed those characters by hand on a USB keyboard.  The blue light next to
the keypad will flash to show you the button worked.  Try it a few more
times.

3. Now switch to the next password.  To do this, press button T1 - the
LED next to it will flash briefly.  Now LED 0 will light green to
indicate we're on a different key.  Press T2 and password *2* will come
out into your selected window as if you typed it on a USB keyboard.

4. If you press T1 again, this would move to the third key (in 0002.txt,
if you had one).  Since you don't, it will go back to the beginning of
the list, 0000.txt .  Press T2 to confirm you're back on the first
password.

5. Unless you're tapping the pads to do something the LEDs show you which
key is selected.  Look at all the LEDs that are green and add up their
values:

* LED0 (next to the reset button) has a value of 1
* LED1 (between LED0 and T2) has a value of 2
* LED2 (next to T1) has a value of 4
* LED3 has a value of 8

   Add up the values for each LED that's lit; the sum is the number of
the key you're using.  That's why all LEDs are off when you're on Key
0000.txt at start.  When you switch to the second key (0001.txt), LED0
lights and all the rest are off.

   When you get to the 17th password (0016.txt), the LEDs start back at
all black since there are only 4 of them.  Similarly, when you get to the
33rd password, they'll go back to black again.



## Adding or editing passwords

1. You can add more passwords or edit them at any time.  Each one goes in
its own file starting with 0000.txt, 0001.txt, 0002.txt, etc.  

2. Everything you place in the file is sent verbatim, so if you want a
linefeed at the end of a password to automatically submit it, make sure
you have a linefeed in the file.  If you want to just have the password
keys entered but want to manually edit them before pressing enter, leave
off the linefeed.

3. As soon as you save the file (and run the command `sync` on MacOS or
Linux to make sure the changes are saved), the new password is ready to
use.  You don't have to restart or reinsert the key.

4. The password files are named 0000.txt through 9999.txt, so you can
have up to 10,000 of them.  


### Actually using this to enter passwords

1. Save a real password/passphrase/pin to 0001.txt .  Press T1 until just
LED0 is lit, indicating that you're on the 2nd password, 0001.txt .

2. Start logging in to whatever that password is for, and stop when you
get to the password/passphrase/pin field.

3. Make sure your cursor is in the password/passphrase/pin box or window.

4. Press T2 to type the characters from 0001.txt .  If that file ends in
a linefeed, the "Enter" key will be pressed and the password will be
automatically submitted.



## Tips and tricks

* If the key is loose in your USB port, place a folded post-it note under
it (the side *away* from the USB contact pins) before inserting it into
the USB port.

* This system can store and type any printable characters from your
keyboard.  This includes passwords, passphrases, pins, keys, and long
blocks of text you commonly use ("Thank you for writing in with your
computer issue.  Have you tried rebooting it?  --Tech support").

* Use 0000.txt to store contact information, including "How to return
this to me" information should someone find it.

* Since this device can only give the barest of feedback of which key
you're on (the LEDs that indicate 0-15, and wrap around when they reach
any multiple of 16), you might want to use a standard password vault like
lastpass and reserve this for master passwords and key passphrases -
things you wouldn't normally want to place in a vault.

* Can also use this drive to store key files, but we discourage placing
all factors needed to login on any single storage device including this
one.

* At the time of this writing (Apr 2021), it appears that circuitpython
may only support the US keyboard layout.  The authors are open to other
layouts.  For more info, see 
<https://github.com/adafruit/Adafruit_CircuitPython_HID/blob/master/adafruit_hid/keyboard_layout_us.py>

* You don't have to put the entire password in here.  If you have a way
to mentally generate, say, the first 5 characters of a password based on
the hostname, type those into the password box by hand and enter the
*remaining* letters that are stored in Trinkeypass.  Just remember that
the characters you type plus the characters provided by trinkeypass need
to end up the same as what the remote system/application expect.

* It's a good idea to buy 2 or more of these and load your passwords on
all of them.  You can keep one with you, perhaps in a wallet or on a
keyring, and place the others in a safe location.


### Using the transform feature

   There's an issue with placing your passwords verbatim in a file on
this key.  If the key were ever stolen or lost and found by someone else,
they could insert it into their own computer and read your passwords
verbatim by copying off those files.

   To handle this, we'll transform them.  What we'll store on disk will
no longer be the actual password; it'll be modified.  When it comes time
to actually type the keys,  we'll modify it back to the original
password.  Here's an example.

   Let's say my login password for a particular system is
"ANiceButBlandPassword" .  I want to store that with the the case swapped
for the second character out of every 4 swapped:

```
aNICEbutblandpassWORD
 ^   ^   ^   ^   ^   
123412341234123412341
```

   So I'll change the case of each character above a caret: "N", "b",
"l", "p", and "W", so here's what I save on 0001.txt:

```
anICEButbLandPasswORD
```

   This means that if anyone can get the files off my Trinkey, they won't
have the actual passwords, just these slightly modified ones.

   Now we tell Trinkeypass to do this transformation for the second
character of every block of 4:

1. Enter xform mode by pressing *both* pads and releasing (both lights
should light blue and go out when you release them).

2. Now tap the following buttons: T1, T2, T1, T1.  T1 means "leave this
character as it is".  T2 means "swap the case of this character".  By
pressing 4 of these you've said "break the password into groups of 4
characters", only the second of which gets its case swapped.  Press
*both* pads once more to exit transform mode.  (This transform stays in
memory and is used until the key is removed from the USB port or you
enter a different transform.

3. Now that we're back in normal mode I press T1 until I'm on the second
password (0001.txt, just LED0 lit green).  When I press T2 now, the
transform I just entered will *reverse* the character changes and type
"aNICEbutblandpassWORD" as a keyboard.

4. As of version 7 this just swaps the case of letters.  A future release
will also replace every digit with 9-thatdigit .



## Risks

* Note that if the system into which you've inserted the Trinkeypass is
running a keyboard sniffer, that program will see the injected password
just as easily as a password typed at an actual keyboard.

* We discourage indexing or backing up this drive.

* If you're using multiple factors to log in somewhere (such as a 
password, an ssh key, and the passphrase to unlock that ssh key, please
do not store all factors in any single place (including this Trinkey).


---
## Other resources

* Adafruit document describing the Neo Trinkey: <https://learn.adafruit.com/adafruit-neo-trinkey>





