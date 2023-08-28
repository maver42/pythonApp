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

def clean_up_output(output):
    output = str(output)
    output = output.replace(output[0], '').replace(output[1], '').replace(output[-1], '').replace('\\n', '\n')
    return output

def main():
    read_ip_file()
    print(f'Remote server connection:\nhost ip: {host}\nusername: {username}\n\n')

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=username, key_filename=os.path.join(os.path.expanduser('~'), ".ssh", "id_rsa"))

    #Read config commands from file
    commands = read_config_file()
    for item in commands:
        try:
            stdin, stdout, stderr = ssh.exec_command(item)
            output = clean_up_output(stdout.read())
            # formatted_output = output.replace(output[0], '').replace(output[1], '').replace(output[-1], '').replace('\\n', '\n')
            print(f'Command: {item}\n{output}')
        except Exception as e:
            print(f'Error happened while executing command:\n{e}')

    #read paramethers from command line arguments
    if len(sys.argv) > 1:
        # print(len(sys.argv))
        for i in range (1, len(sys.argv)):
            # print(sys.argv[i])
            try:
                stdin, stdout, stderr = ssh.exec_command(sys.argv[i])
                output = clean_up_output(stdout.read())
                print(f'Command: {sys.argv[i]}\n{output}')
                if (len(output) == 0):
                    stderr =
                    print(str(stderr.read()).replace(output[0], '').replace(output[1], '').replace(output[-1], '').replace('\\n', '\n'))
            except Exception as e:
                print(f'Error happened while executing command:\n{e}')

    # Cleanup
    ssh.close()

main()


