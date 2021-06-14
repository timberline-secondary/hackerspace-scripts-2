
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
   2.10 When it's finished it should only say "Reboot" at the bottom, hit Enter to reboot.
3. After it reboots, force a puppet run: `rm /etc/puppetlabs/puppet/ssl/
    3.1 Run this command on the newly imaged workstation: `sudo puppet agent -t`. if you get certificate errors, you will need to clean them:
         3.1.1 Copy and paste the command it gives you for "On the agent: 1a." but add `sudo` before the `find ...`
         3.1.2 In this control panel, run the "puppet clear certificates" menu option to clear the certificate ont the puppet master.
4. The computer should reboot on its own, and when the login screen appears, you should no longer see the Hackerspace Admin user there.  Then you know it's complete.
""")
