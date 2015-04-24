import sys
from lyontour import app

if __name__=='__main__':
    port = 8000
    if len(sys.argv) > 1:
        if sys.argv[1] == 'debug':
            port = 8081
    app.run(host='0.0.0.0',port=port,debug=True)