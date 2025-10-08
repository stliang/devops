import paramiko
import time

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
        # Receive data from the channel (up to 1024 bytes at a time)
        output += ssh_channel.recv(1024).decode('utf-8')
    
    # Check if the expected prompt is not in the output
    if expect_prompt not in output:
        raise RuntimeError("Expected prompt not found in the response!")
    
    return output


# SSH connection details
hostname = 'your-host'
username = 'your-username'
password = 'your-password'

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

    # Example send-expect interaction
    prompt = "$"  # This is the shell prompt expected after each command
    output = send_expect(channel, 'ls -l', prompt)  # Send 'ls -l' and wait for prompt
    print("Command 1 output:\n", output)

    output = send_expect(channel, 'pwd', prompt)  # Send 'pwd' and wait for prompt
    print("Command 2 output:\n", output)
    
    output = send_expect(channel, 'whoami', prompt)  # Send 'whoami' and wait for prompt
    print("Command 3 output:\n", output)

    # Close the channel and connection
    channel.close()
    client.close()

except paramiko.SSHException as e:
    print(f"An error occurred: {e}")
