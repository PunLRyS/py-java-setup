import os
import zipfile
import json
import subprocess
import tarfile

try:
    import requests
    print('You have requests installed')
except:
    os.system('pip install requests')
    print('You need to install requests')
    print('Installing requests...')
    import requests
version = ''
Name = 'Server'
path = '.'
if not os.path.exists(Name):
    os.mkdir(Name)
path = os.path.join(path, Name)

os_name = os.name
version_index = -1
chose = ''
memory = 1024
jar_path =''
jdk_path =''

def download_server():
    global version
    install = requests.get('https://gist.githubusercontent.com/PunLRyS/d20cdfd023b2cdb5664fb901f8921913/raw/666e2129771f72dfaef435efe6b7d7927b3dc12a/request.json')
    install_rs = install.json()

    ver_respone_api = install_rs.get('versions')
    ver_respone = requests.get(ver_respone_api)

    chose = input('Do you want to see the versions? (y/n): ')
    if chose == 'y' or chose == 'Y':
        print('List of versions:')
        for i in ver_respone.json()['versions']:
            print(i)

    while version not in ver_respone.json()['versions']:
        version = input('Enter the version you want to install: ')
        if version not in ver_respone.json()['versions']:
            print('Invalid version, please try again.')
            print('If you want to break, type "exit"')
        if version == 'exit':
            exit()

    memories = input('Enter the memory you want to use (default 1024M): ')
    if memories != '':
        try:
            memory = int(memories)
        except ValueError:
            print('Invalid memory, using default 1024M.')
            memory = 1024

    memory = str(memory) + 'M'

    version_index = ver_respone.json()['versions'].index(version)
    latest_version = ver_respone.json()['versions'][version_index]

    build_resp_api = install_rs.get('builds')
    build_resp_api = build_resp_api.replace('{latest_version}', latest_version)
    build_resp = requests.get(build_resp_api)


    latest_build = build_resp.json()['builds'][version_index]
    jar_name = f'paper-{latest_version}-{latest_build}.jar'

    download_url_api = install_rs.get('download')
    download_url_api = download_url_api.replace('{latest_version}', latest_version)
    download_url_api = download_url_api.replace('{latest_build}', str(latest_build))
    download_url_api = download_url_api.replace('{jar_name}', jar_name)
    download_url = requests.get(download_url_api)
    jar_path = os.path.join(path, jar_name)


    print (os.path.abspath(jar_path))
    print (f'Downloading {jar_name}...')
    with open(jar_path, 'wb') as f:
        f.write(requests.get(download_url_api).content)
    print(f'Downloaded {jar_name} to {jar_path}')

    # java17_url_api = install_rs.get('java17')
    # java17_url = requests.get(java17_url_api)
    # java17_name = os.path.basename('java17.zip')
    # java17_path = os.path.join(path, java17_name)
    # with open(java17_path, 'wb') as f:
    #     f.write(requests.get(java17_url).content)
    # print(f'Downloaded {java17_path} to {path}')

    # with zipfile.ZipFile(java17_path, 'r') as zip_extractor:
    #     zip_extractor.extractall(path)
    # print(f'Extracted {java17_path} to {path}')

    # os.remove(java17_path)
    # for file in os.listdir(path):
    #     if file.startswith('jdk-17'):
    #         jdk_path = os.path.join(path, file, 'bin', 'java.exe')
    #         break
    jdk_path =''
    if os.name == 'nt':
        java11_url_api = install_rs.get('java11')
        java11_url = requests.get(java11_url_api)
        java11_name = os.path.basename('java11.zip')
        java11_path = os.path.join(path, java11_name)
        with open(java11_path, 'wb') as f:
            f.write(java11_url.content)
        print(f'Downloaded {java11_path} to {path}')

        with zipfile.ZipFile(java11_path, 'r') as zip_extractor:
            zip_extractor.extractall(path)
        print(f'Extracted {java11_path} to {path}')

        for file in os.listdir(path):
            if file.startswith('jdk-11'):
                jdk_path = os.path.join(path, file, 'bin', 'java.exe')
                break
        print(os.path.abspath(jdk_path))
    else:
        java11_url_api = install_rs.get('java11_linux')
        java11_url = requests.get(java11_url_api)
        java11_name = os.path.basename('java11.tar.gz')
        java11_path = os.path.join(path, java11_name)
        java11_extract = os.path.join(path,'jdk-11')
        with open(java11_path, 'wb') as f:
            f.write(java11_url.content)
        print(f'Downloaded {java11_path} to {path}')

        with tarfile.open(java11_path, 'r:gz') as tar_extractor:
            tar_extractor.extractall(path)
        print(f'Extracted {java11_path} to {path}')

        print("File extracted successfully!")
        for file in os.listdir(path):
            if file.startswith('jdk-11'):
                jdk_path = os.path.join(path, file, 'bin', 'java')
                break
        print(os.path.abspath(jdk_path))

    data ={
        'version': version,
        'memory': memory,
        'jar_path': jar_path,
        'jdk_path': jdk_path,
    }

    with open('properties.json', 'w') as f:
        json.dump(data, f)

    # os.remove(java11_path)

def open_serveo_port(local_port=25565, remote_port=25962):
    print("Đang mở port với Serveo...")
    proc = subprocess.Popen(
        ['ssh', '-o', 'StrictHostKeyChecking=no', '-R', f'{remote_port}:localhost:{local_port}', 'serveo.net'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    for _ in range(10):
        line = proc.stdout.readline()
        if not line:
            break
        print(line.strip())
        if 'Forwarding' in line or 'serveo.net' in line:
            break


def run_server():
    if os.path.exists('properties.json'):
        with open('properties.json', 'r') as f:
            properties = json.load(f)
            memory = properties.get('memory')
            jar_path = properties.get('jar_path')
            jdk_path = properties.get('jdk_path')
    if not jdk_path or not os.path.exists(jdk_path):
        print("Không tìm thấy java.exe!")
        return
    print(f"Đang chạy server với {jdk_path}")
    
    os.system(f'"{jdk_path}" -Xmx{memory} -Xms{memory} -jar {jar_path} nogui')

def run_server_linux():
    if os.path.exists('properties.json'):
        with open('properties.json', 'r') as f:
            properties = json.load(f)
            memory = properties.get('memory')
            jar_path = properties.get('jar_path')
            jdk_path = properties.get('jdk_path')
    if not jdk_path or not os.path.exists(jdk_path):
        print("Không tìm thấy java.exe!")
        return
    print(f"Đang chạy server với {jdk_path}")
    os.system(f'sudo chmod +x {jdk_path}')
    
    os.system(f'java -Xmx{memory} -Xms{memory} -jar {jar_path} nogui')


def main():
    if os_name == 'nt':
        if os.path.exists('properties.json'):
            print(f'Found properties.json')
            open_serveo_port()
            run_server()
        else:
            print(f'Not found properties.json')
            download_server()
            open_serveo_port()
            run_server()
    else:
        if os.path.exists('properties.json'):
            print(f'Found properties.json')
            open_serveo_port()
            run_server_linux()
        else:
            print(f'Not found properties.json')
            download_server()
            open_serveo_port()
            run_server_linux()


if __name__ == '__main__':
    main()
