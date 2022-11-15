
def reimage_workstation():
    print("""
Unfortunately you can't reimage a computer from here, but here are the steps!

1. Restart the computer you want to image
2. Hit F12 while the computer is booting to enter the Startup Device menu:
   2.1 Choose the "Network 1 > Legacy" option
   2.2 When the funny picture of Mr C and Nick shows up, hit enter to select the default choice
   2.3 Wait for the computer to download the image and stat installing. Sometimes it can hang on "Host and Network Name Lookups", just be patient, go play a game of Tetris.
   2.4 When the menu comes up, hit Enter to select English as the language
   2.5 Select "Continue" to begin the installation
   2.6 In the next screen, use Tab or up/down arrows to navigate.
   2.7 Enter the proper hostname, it should be: "tbl-h10-#", where # is the computer's number from 0-31 or so
   2.8 If it is not already entered, enter the admin password twice, then continue
   2.9 Wait for the install process to finish (don't "Cancel update and reboot")
   2.10 IMPORTANT: while it's installing Ubuntu, re-run this control panel and run Workstation Management > puppet_clear_certificates on the computer you are re-imaging
   2.11 When it's finished it should only say "Reboot" at the bottom, hit Enter to reboot.
3. When the computer boots, you will see "Hackerspace Admin" as the only log in option. Leave the computer for 5-10 minutes to install the rest of the lab's software in the background (automatic).
3. When finished installing, The computer should reboot on its own, and the normal login screen appears to enter a username and pw.  Then you know it's complete.
""")
