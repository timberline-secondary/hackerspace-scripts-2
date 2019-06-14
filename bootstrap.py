import os

required_packages = ['sshpass', ]

def package_is_installed(pkg_name):
    """ Returns true if the package is installed"""
    # https://askubuntu.com/questions/2943/how-can-i-check-if-a-package-is-installed-no-superuser-privileges
    # exit code is 0 if installed, 1 if not.  Suppressed output
    exit_code = os.system('dpkg-query -s {} 2>/dev/null | grep -q ^"Status: install ok installed"$'.format(pkg_name))
    return exit_code == 0

print ("Making sure all the required packages are installed")

packages_to_install = []
for pkg in required_packages:
    if not package_is_installed(pkg):
        packages_to_install.append(pkg)
    
    if packages_to_install:
        pkg_install_string = " ".join(packages_to_install)
        print ("These pkgs are required to use this control panel: ", pkg_install_string)
        print ("You'll need to enter the admin password a couple times, sorry!")

        install_cmd = 'su -c "sudo -S apt install {}" -m hackerspace_admin'.format(pkg_install_string)
        os.system(install_cmd)

        
