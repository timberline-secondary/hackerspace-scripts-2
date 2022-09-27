from scripts._utils import ssh, pi

hostname = "pi-projector"


def flex_schedule_off():
    ssh_connection = ssh.SSH(hostname, pi.username, pi.password)
    ssh_connection.send_cmd("rm /tmp/flex")
    print("Done.")
    ssh_connection.close()
