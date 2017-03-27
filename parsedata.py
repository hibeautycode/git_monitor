from sshdata import SSHData
from time import sleep
import os

class ParseData():

	def __init__(self):

		self.local_filepath = './data/'
		self.filename_cpu = 'cpu.data'
		self.filename_gpu = 'gpu.data'

	# get cpu gpu data
	def update_sshdata(self, sshinfo, flag_gpu):

		if not os.path.exists(self.local_filepath):
			os.mkdir(self.local_filepath)
		local_file_path = os.path.join(self.local_filepath, sshinfo[ 'hostname' ])
		if not os.path.exists(local_file_path):
			os.mkdir(local_file_path)

		execmd1 = ''.join(['top -b -n 1 > ', self.filename_cpu])
		sshdata = SSHData(sshinfo[ 'hostip' ], sshinfo[ 'port' ], sshinfo[ 'username' ], sshinfo[ 'password' ])
		sshdata.sshclient_execmd(execmd1)
		if flag_gpu:
			execmd2 = ''.join(['nvidia-smi > ', self.filename_gpu])
			sshdata.sshclient_execmd(execmd2)
		sleep(0.5)
		sshdata.get_server_file(self.filename_cpu, os.path.join(local_file_path, self.filename_cpu))
		if flag_gpu:
			sshdata.get_server_file(self.filename_gpu, os.path.join(local_file_path, self.filename_gpu))
		sshdata.ssh_close()

	# parse cpu data
	def parse_cpudata(self, sshinfo):

		local_file_path = os.path.join(self.local_filepath, sshinfo[ 'hostname' ])
		dt_cpu = { 'load average' : [], 'Tasks' : { 'total' : '', 'running' : '',
			'sleeping' : '', 'stopped' : '', 'zombie' : '' }, 'process' : {
			'title' : [ 'PID', 'USER', 'S', '%CPU', '%MEM', 'COMMAND' ],
			'info' : [] } }
		flag_process = False
		fr = open(os.path.join(local_file_path, self.filename_cpu))
		for line in fr.readlines():
			ls_line = line.strip().split()
			if 'load' in ls_line and 'average:' in ls_line:
				ls_cpuload = [''.join([str(float(val.replace(',', ''))), '%']) for val in ls_line[ls_line.index('average:') + 1 :]]
				dt_cpu['load average'] = ls_cpuload
			if 'Tasks:' in ls_line:
				dt_cpu['Tasks']['total'] = ls_line[ls_line.index('total,') - 1]
				dt_cpu['Tasks']['running'] = ls_line[ls_line.index('running,') - 1]
				dt_cpu['Tasks']['sleeping'] = ls_line[ls_line.index('sleeping,') - 1]
				dt_cpu['Tasks']['stopped'] = ls_line[ls_line.index('stopped,') - 1]
				dt_cpu['Tasks']['zombie'] = ls_line[ls_line.index('zombie') - 1]
			if flag_process:
				# max record process number
				num_record_process = 15
				if len(dt_cpu['process']['info']) < num_record_process:
					dt_cpu['process']['info'].append([ls_line[0], ls_line[1], ls_line[7],
						ls_line[8], ls_line[9], ls_line[11]])
			if 'PID' in ls_line:
				flag_process = True
		return dt_cpu

	# parse gpu data
	def parse_gpudata(self, sshinfo):

		local_file_path = os.path.join(self.local_filepath, sshinfo[ 'hostname' ])
		dt_gpu = { 'Memory-Usage' : { 'usage' : '', 'total' : '' }, 'GPU-Util' : '', 'Temp' : '',
			'process' : { 'title' : [ 'GPU', 'PID', 'Process', 'Usage' ], 'info': [] } }
		fr = open(os.path.join(local_file_path, self.filename_gpu))
		ls_lines = fr.readlines()
		for i in range(len(ls_lines)-1):
			ls_line = ls_lines[i].strip().split()
			if i == 8:
				dt_gpu['Memory-Usage']['usage'] = ls_line[8]
				dt_gpu['Memory-Usage']['total'] = ls_line[10]
				dt_gpu['GPU-Util'] = ls_line[12]
				dt_gpu['Temp'] = ls_line[2]
			if i >= 15:
				dt_gpu['process']['info'].append([ls_line[1], ls_line[2], ls_line[4], ls_line[5]])

		return dt_gpu
