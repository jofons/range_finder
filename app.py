import flask
from ipaddress import ip_address, ip_network
app = flask.Flask(__name__)  
  
@app.route('/')  
def main():  
    return render_template("Index.html")  
  
@app.route('/dumproutinginfo', methods = ['POST'])  
def dumproutinginfo():  
    if request.method == 'POST':  
        f = request.files['file']
        ip = request.files['ip']
        result = range_search(ip, f.filename) 
        return render_template("Output.html", output = result)

@app.route('/effectiveroutes', methods = ['POST'])  
def effectiveroutes():  
    if request.method == 'POST':  
        f = request.files['file']
        try:
            extension = f.filename.split('.')[1]
            if extension != 'csv':
                return('Uploaded file is not csv, please upload the effective route excel file in the csv format')
        except:
            return('Uploaded file is not csv, please upload the effective routes excel file in the csv format')
        ip = request.files['ip']
        result = range_search(ip, f.filename) 
        return render_template("Output.html", output=result) 

def range_search(ip, filename, effectiveroutes):
    try:
        addr = ip_address(ip)
    except:
        # add file delete
        return('The submitted IP is not in the correct format.')
    file = open(filename, 'r')
    lines = file.readlines()
    output = ''
    if effectiveroutes:
        for line in lines:
            aux = line.split()
            for range in aux:
                if '/' in aux:
                    if '"' in range:
                        aux2 = range.split(',')
                        for aux3 in aux2:
                            if '"' in aux3:
                                for aux4 in aux3:
                                    if "/" in aux4:
                                        net = aux4
                                        break
                                net = ip_network(aux, strict=False)
                                if addr in net:
                                    output += aux4 + '\n'
                    else:
                        net = ip_network(aux, strict=False)
                        if addr in net:
                            output += aux + '\n'
    else:
        for line in lines:
            aux = line.split()
            if aux[0] == 'B' or aux[0] == 'L' or aux[0] == 'C':
                net = ip_network(aux[1], strict=False)
                if addr in net:
                    output += aux[1] + '\n'
            else:
                next
    file.close()
    # add file delete
    return output