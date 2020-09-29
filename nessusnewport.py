import requests
import subprocess
import datetime
import sqlite3

_output = subprocess.check_output('dir',shell=True)
if not 'port.db' in str(_output):
    conn = sqlite3.connect('port.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE portlar (port text, ip text, zaman text)''')
    c.close()
header = {'X-ApiKeys': 'accessKey=b802ad1e47b16a8ab240afba8768ae8872e32ce0f57f0f00f030e8ed121bd0d6; secretKey=eee60ba4f7a9126ead042806befa933f4ed7dbac4e31afea719637a835a22169;'}
url = 'https://127.0.0.1:8834/scans'
sonuc = requests.get(url=url,headers=header,verify=False)
for i in sonuc.json()['scans']:
    scan_id = i['id']
    url='https://127.0.0.1:8834/scans/'+str(scan_id)
    tarama = requests.get(url=url, headers=header, verify=False)
    for j in tarama.json()['hosts']:
        try:
            host_id = j['host_id']
            #Nessus'daki pluginslere göre açık portu görebilirsiniz.
            url = (f'https://127.0.0.1:8834/scans/{scan_id}/hosts/{host_id}/plugins/10736')
            IP = requests.get(url=url,headers=header, verify=False)
            for k in IP.json()['outputs']:
                port = list(k['ports'].keys())[0]
                IP = j['hostname']
                conn = sqlite3.connect('port.db')
                c=conn.cursor()
                _output = c.execute('select * from portlar where port=? and ip=?',(port,IP))
                port_sayisi=len(_output.fetchall())
                conn.close()
                if port_sayisi<1:
                    print(f'New port found : {port} IP Add: {IP}')
                    conn = sqlite3.connect('port.db')
                    c = conn.cursor()
                    c.execute('INSERT INTO portlar VALUES (?, ?, ?)',(port,IP,str(datetime.datetime.now())))
                    conn.commit()
                    conn.close()
        except:
            pass