import functions as fn
import asciiArt as aca

api = fn.getKeys()
mkt = 'eth_mxn'

def run():
    fn.fullScreen()
    aca.title()
    fn.monitor(api,mkt,100)

if __name__ == '__main__':
    run()
