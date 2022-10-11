# hackerspace-scripts-2
Python based control panel and scripts for managing Timberline's Digital Hackerspace

This is an improved python-based version of [the original](https://github.com/timberline-secondary/hackerspace-scripts) created by Peder Skarabdkjfhkj(sp?)

Install Instructions:

1. Open a Terminal (Ctrl + Alt + T)
1. Create a bin directory in your home: `mkdir ~/bin`
1. Go into the bin dir:  `cd ~/bin`
1. Clone the git repository into the bin dir: `git clone https://github.com/timberline-secondary/hackerspace-scripts-2.git`
1. Move into the git repo: `cd hackerspace-scripts-2`
1. Run the setup script: `./control-panel` or `bash control-panel`

Once install is complete, log out and back in again. You should  now be able to run the control-panel from anywhere by typing `control-panel` in a terminal.  You can also autocomplete by typing `cont` + <kbd>Tab</kbd>

 ### Docker setup instrutions:
 #### ⚠️ `This has to be done every update.`

 1. Open a Terminal (Ctrl + Alt + T)
 2. ensure the working directory IS this repo (i.e. wherever it was cloned to)
 3. Run `docker build -t control-panel .`

 ### Docker run instructions:

 1. Open a Terminal (Ctrl + Alt + T)
 2. Run `docker run -it control-panel`