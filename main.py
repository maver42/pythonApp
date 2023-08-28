import os.path
import paramiko
import yaml
import sys

command = "df"


def read_ip_file():
    global host
    global username

    try:
        with open('ip.yml') as ip_file:
            data = yaml.safe_load(ip_file)

            host = data['server']['ip']
            username = data['server']['username']

            # print(f'host ip: {host}\nusername: {username}')

    except FileNotFoundError as err:
        print(f"File ip.yml does not exist")
        print(err)


def read_config_file():
    commands = []
    try:
        with open('config.yml') as conf_file:
            data = yaml.safe_load(conf_file)
            # print(type(data))
            for lines in data.items():
                # print(f'lines:{lines}')
                commands = lines[1]
                # print(len(commands))
                # for i in range(len(commands)):
                #     print(f'commands[i]: {commands[i]}')

    except FileNotFoundError as err:
        print(f"File config.yml does not exist")
        print(err)

    return commands



def main():
    read_ip_file()
    print(f'Remote server connection:\nhost ip: {host}\nusername: {username}\n\n')

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=username, key_filename=os.path.join(os.path.expanduser('~'), ".ssh", "id_rsa"))

    #Read config commands from file
    commands = read_config_file()
    for item in commands:
        stdin, stdout, stderr = ssh.exec_command(item)
        output = str(stdout.read())
        formatted_output = output.replace(output[0], '').replace(output[1], '').replace(output[-1], '').replace('\\n', '\n')
        print(f'Command: {item}\n{formatted_output}')

    #read paramethers from command line arguments
    if len(sys.argv) > 1:
        print(len(sys.argv))
        for i in range (1, len(sys.argv)):
            print(sys.argv[i])
            stdin, stdout, stderr = ssh.exec_command(sys.argv[i])
            output = str(stdout.read())
            formatted_output2 = output.replace(output[0], '').replace(output[1], '').replace(output[-1], '').replace('\\n', '\n')
            print(f'Command: {i}\n{formatted_output2}')

    # Cleanup
    ssh.close()

main()


