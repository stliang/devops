#!/usr/bin/env python3

import paramiko
import time
import json

def send_expect(ssh_channel, command, expect_prompt, timeout=1):
    """
    Send a command to the remote SSH channel and wait for the expected prompt.

    Args:
        ssh_channel (paramiko.Channel): The opened SSH channel.
        command (str): The command to send to the remote shell.
        expect_prompt (str): The prompt or expected output to wait for.
        timeout (int): Time to wait for the expected prompt in seconds.

    Returns:
        str: The output from the command execution.
    """
    ssh_channel.send(command + '\n')
    time.sleep(timeout)

    # Collect the output until the expected prompt is encountered
    output = ""
    while not ssh_channel.recv_ready():
        time.sleep(0.1)
    
    while ssh_channel.recv_ready():
        # Receive data from the channel
        output += ssh_channel.recv(1024).decode('utf-8')
    
    # Check if the expected prompt is not in the output
    if expect_prompt not in output:
        raise RuntimeError("Expected prompt not found in the response!")
    
    return output

def main():
    # Load configuration from JSON file
    config_file = "config.json"
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Configuration file '{config_file}' not found. Please create the file.")
        return
    except json.JSONDecodeError:
        print(f"Error parsing the JSON configuration file '{config_file}'. Please check for syntax errors.")
        return
    
    # Extract credentials and list of hostnames
    username = config.get("username")
    password = config.get("password")
    hostnames = config.get("hostnames", [])

    if not username or not password:
        print("Error: 'username' or 'password' not found in the configuration file!")
        return

    if not hostnames:
        print("Error: No hostnames found in the configuration file!")
        return

    # Commands to execute on each host
    commands = ["ls -l", "pwd", "whoami"]

    for hostname in hostnames:
        print(f"\nConnecting to host: {hostname}")
        try:
            # Create an SSH client instance
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname, username=username, password=password)

            # Open an interactive shell session
            channel = client.invoke_shell()
            time.sleep(1)  # Give the shell time to initialize

            # Receive the initial shell output
            if channel.recv_ready():
                shell_output = channel.recv(1024).decode('utf-8')
                print(shell_output)
            
            # Execute commands in sequence
            prompt = "$"  # Adjust the expected shell prompt if necessary
            for command in commands:
                print(f"Executing command: {command}")
                output = send_expect(channel, command, prompt)
                print(f"Output from {command} ({hostname}):\n{output}")

            # Close the channel and connection
            channel.close()
            client.close()

        except paramiko.SSHException as e:
            print(f"SSH error while connecting to {hostname}: {e}")
        except RuntimeError as e:
            print(f"Runtime error on {hostname}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred on {hostname}: {e}")

if __name__ == "__main__":
    main()
