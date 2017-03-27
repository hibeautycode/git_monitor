import paramiko

class SSHData():

	def __init__( self, hostname, port, username, password ):
		self.hostname = hostname
		self.port = port
		self.username = username
		self.password = password
		self.logname = 'paramiko.log'
		self.ssh_connect()

	def ssh_connect(self):
		paramiko.util.log_to_file(self.logname)
		self.ssh = paramiko.SSHClient()
		self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		self.ssh.connect(self.hostname, self.port, self.username, self.password)

	def sshclient_execmd(self, execmd):
		self.ssh.exec_command (execmd)

	def get_server_file(self, src, dst):
		ftp = self.ssh.open_sftp()
		ftp.get(src, dst)
		ftp.close()

	def put_server_file(self, src, dst):
		ftp = self.ssh.open_sftp()
		ftp.put(src, dst)
		ftp.close()

	def ssh_close(self):
		self.ssh.close()
