from flask import Flask, render_template
from parsedata import ParseData

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/<hostname>')
def index_host(hostname):

	parsedata = ParseData()
	if hostname == 'cist-PowerEdge-R730':
		sshinfo =  { 'hostname' : '', 'hostip' : '',
				  'port':22, 'username' : '', 'password' : '' }
		flag_gpu = True
	parsedata.update_sshdata(sshinfo, flag_gpu)
	cpu = parsedata.parse_cpudata(sshinfo)

	if flag_gpu:
		gpu = parsedata.parse_gpudata(sshinfo)
		return render_template('server_gpu.html', cpuload=cpu['load average'][0], cputasks=cpu['Tasks'], gpuload=gpu['GPU-Util'],
			gpumem=gpu['Memory-Usage'], gputemp=gpu['Temp'], cpuproctitle=cpu['process']['title'],
			cpuprocinfo=cpu['process']['info'], gpuproctitle=gpu['process']['title'],
			gpuprocinfo=gpu['process']['info'])
	else:
		return render_template('server_no_gpu.html', cpuload=cpu['load average'], cputasks=cpu['Tasks'],
			cpuproctitle=cpu['process']['title'], cpuprocinfo=cpu['process']['info'])

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)
