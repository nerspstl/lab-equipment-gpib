from struct import unpack
import pyvisa as visa
import numpy as np
import datetime
rm = visa.ResourceManager()

class TDS640a:
    def __init__(self, channel, port):
        try:
            scope = rm.open_resource(port)
            scope.write("DATA:SOURCE " + channel)
            scope.write('DATA:WIDTH 1')
            scope.write('DATA:ENC RPB')
            ymult = float(scope.query('WFMPRE:' + channel + ':YMULT?'))
            yzero = float(scope.query('WFMPRE:' + channel + ':YZERO?'))
            yoff = float(scope.query('WFMPRE:' + channel + ':YOFF?'))
            xincr = float(scope.query('WFMPRE:' + channel + ':XINCR?'))
            xdelay = float(scope.query('HORizontal:POSition?'))
            wfid = str(scope.query("WFMPRE:" + channel + ":WFID?"))
            wfid =  wfid.replace('\n','')
            wfmpre = str(scope.query("WFMPRE:" + channel + "?"))
            wfmpre =  wfmpre.replace('\n',';')
            yunit = (scope.query("WFMPRE:" + channel + ":YUNIT?"))
            yunit = yunit.replace('"','')
            yunit = yunit.replace('\n','')
            xunit = (scope.query("WFMPRE:" + channel + ":XUNIT?"))
            xunit = xunit.replace('"','')
            xunit = xunit.replace('\n','')
            date = datetime.datetime.now()
            scope.write('CURVE?')
            data = scope.read_raw()
            headerlen = 5
            header = data[:headerlen]
            ADC_wave = data[headerlen:-1]
            ADC_wave = np.array(unpack('%sB' % len(ADC_wave),ADC_wave))
            Volts = (ADC_wave - yoff) * ymult  + yzero
            Time = np.arange(0, (xincr * len(Volts)), xincr)-((xincr * len(Volts))/2-xdelay)

            self.ymult = ymult
            self.yzero = yzero
            self.yoff = yoff
            self.xincr = xincr
            self.xdelay = xdelay
            #self.data = data
            self.volts = Volts
            self.time = Time
            self.xunit = xunit
            self.yunit = yunit

            date = date.strftime("%Y-%m-%d--%H-%M-%S")

            self.name = "TDS640A--date-" + date + "--source-" + str(channel)
            self.title = wfid
            self.wfid = wfid
            self.wfmpre = wfmpre

        except IndexError:
            return 0,0
