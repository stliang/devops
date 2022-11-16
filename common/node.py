import paramiko

class Node:
    def __init__(self, host_address, username, password, port=22, **kwargs):
        self.host_address = host_address
        self.port = port
        self.username = username
        self.password = password
        self.__dict__.update(kwargs) # in case childern want to access their kwargs
        self.extra_kwargs = kwargs # for __str__ as I don't want to show credential

    def __str__(self):
        return f"{self.host_address}:{self.port} {self.extra_kwargs}"

    def send(self, cmd, timeout=20) -> str:
        rtn_output = ''
        with paramiko.SSHClient() as ssh:
            try:
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(self.host_address, port=self.port, username=self.username, password=self.password, timeout=timeout)
                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
                rtn_output = ssh_stdout.read().decode('ascii').strip("\n")
                ssh.close() # context manager should close ssh connection but close anyway
            except (paramiko.SSHException) as se:
                rtn_output = se
        return rtn_output