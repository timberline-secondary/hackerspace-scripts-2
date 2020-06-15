
def reimage_workstation():
    print("""
Unfortunately you can't reimage a computer from here, but here are the steps!

1. Restart the computer you want to image
2. Hit F12 while the computer is booting to enter the Startup Device menu
3. Choose the "Network 1 > Legacy" option
4. When the funny picture of Mr C and Nick shows up, hit enter to select the default choice
5. Wait for the computer to download the image and stat installing. Sometimes it can hang on "Host and Network Name Lookups", just be patient, go play a game of Tetris.
6. When the menu comes up, hit Enter to select English as the language
7. Select "Continue" to begin the installation
8. In the next screen, use Tab or up/down arrows to navigate.
9. Enter the proper hostname, it should be: "tbl-h10-#", where # is the computer's number from 0-31 or so
10. If it is not already entered, enter the admin password twice, then continue
11. Wait for the install process to finish (don't "Cancel update and reboot")
12. When it's finished it should only say "Reboot" at the bottom, hit Enter to reboot.
13. After it reboots, force a puppet run through this control panel.  It will take a while to install all our software.  
14. The computer should reboot on its own, and when the login screen appears, you should no longer see the Hackerspace Admin user there.  Then you know it's complete.
""")
