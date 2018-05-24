import wx
from gui.stinky import *
from gui.connect import *
from socketserver import ThreadingMixIn
import threading
import gettext
import socket
import ssl
import time
from scapy.all import promiscping
import sys

class ThreadingSimpleServer(ThreadingMixIn, http.server.HTTPServer):
	pass

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, size = (wx.DisplaySize()[0]/2, wx.DisplaySize()[1]/2), style = wx.MAXIMIZE_BOX|wx.RESIZE_BORDER|wx.CLOSE_BOX|wx.CAPTION)
        self.Server = wx.StaticText(self, wx.ID_ANY, ("HTTPS SERVER   "))
        self.button_1 = wx.Button(self, wx.ID_ANY, ("START"),wx.DefaultPosition, wx.Size(80,25))
        self.label_3 = wx.StaticText(self, wx.ID_ANY, ("CLIENT                "))
        self.button_2 = wx.Button(self, wx.ID_ANY, ("Connect"),wx.DefaultPosition, wx.Size(80,25))
        self.label_6 = wx.StaticText(self, wx.ID_ANY, ("ANTI-SNIFF TEST"))
        self.label_9 = wx.StaticText(self, wx.ID_ANY, ("INET:"))
        self.text_ctrl_5 = wx.TextCtrl(self, wx.ID_ANY, "lo",wx.DefaultPosition, wx.Size(80,20))
        self.button_3 = wx.Button(self, wx.ID_ANY, ("Test"),wx.DefaultPosition, wx.Size(80,25))
        self.text_ctrl_8 = wx.TextCtrl(self, wx.ID_ANY, "",style = wx.TE_MULTILINE|wx.TE_READONLY)
        self.text_ctrl_8.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL))

        self.button_1.Bind(wx.EVT_BUTTON, self.WebServ)
        self.button_2.Bind(wx.EVT_BUTTON, self.connect)
        self.button_3.Bind(wx.EVT_BUTTON, self.detect_promiscuous)

        self.Bind(wx.EVT_MAXIMIZE, self.OnMaximize)

        self.SetSizeHints(350,600)
        self.Centre()
        self.__set_properties()
        self.__do_layout()

    def Print(self, text):
        wx.CallAfter(self.text_ctrl_8.AppendText, text+"\n")

    def WebServ(self, evt):
        ServerClass  = http.server.HTTPServer

        server_address = ('127.0.0.1', 8089)

        httpd = ThreadingSimpleServer(server_address, Handle)

        httpd.socket = ssl.wrap_socket(httpd.socket,
                               server_side=True,
                               certfile='server_data/server.crt',
                               keyfile='server_data/server.key',
                               cert_reqs = ssl.CERT_NONE,
                               ca_certs=None,
                               do_handshake_on_connect=True,
                               ssl_version = ssl.PROTOCOL_TLSv1,
                               suppress_ragged_eofs=True)
        sa = httpd.socket.getsockname()
        self.Print("Serving HTTPS on {} port {} ...".format(sa[0],sa [1]))
        httpd.handle_request()
        evt.Skip()

    def connect(self, evt):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
            ss = ssl.wrap_socket(s, ssl_version = ssl.PROTOCOL_TLSv1)
            addr = ('127.0.0.1',8089)
            ss.connect(addr)
            ss.send(b'GET / HTTP/1.0\r\n\r\n')
            resp = ss.recv(256)
            self.Print(str(resp))
            ss.close()
            time.sleep(5)
            evt.Skip()
        except Exception as e:
            self.Print(str(e))
            evt.Skip()

    def detect_promiscuous(self, evt): 
        self.inet = ('lo' if self.text_ctrl_5.GetValue() == ' ' else self.text_ctrl_5.GetValue())
        d = str(promiscping('127.0.0.1/8089', iface = self.inet, fake_bcast='ff:ff:ff:ff:ff:fe'))
        e = d.split()[5:]
        f = d.split()[:5]        
        for i in list(zip(e,f))[1:4]:
            if int(i[1].split(':')[1]) == 0: 
                self.Print('Atacante no puede obtener ping requests de forma promiscua en {}'.format(i[0].split(':')[0]))
            else:   
                self.Print('Respondidos {} ping requests en {} de forma promiscua. El servidor es vulnerable'.format(i[1].split(':')[1],i[1].split(':')[0]))
            if int(i[0].split(':')[1]) == 0:                                                                     
                self.Print('{} ping enviado pero el atacante no obtuvo ninguna respuesta'.format(i[0].split(':')[0]))
            else:                                                                                                   
                self.Print('Atacante no obtuvo respuesta de {} paquetes de {}'.format(i[0].split(':')[1],i[0].split(':')[0]))
        evt.Skip()

    def OnMaximize(self, event):
        self.SetSize(wx.Size(self.GetSize().GetWidth(),self.GetSize().GetHeight()))
        self.Layout()
        self.Refresh()

    def __set_properties(self):
        self.SetTitle(("Anti-Sniffing Tools"))
        self.Server.SetFont(wx.Font(11, wx.MODERN, wx.NORMAL, wx.BOLD, 0, ""))
        self.label_3.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.label_6.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))

    def __do_layout(self):

        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_3 = wx.FlexGridSizer(rows=1, cols=8, vgap = 70, hgap=10)
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_2 = wx.FlexGridSizer(rows=1, cols=6, vgap = 70, hgap=10)

        grid_sizer_1 = wx.FlexGridSizer(rows=1, cols=6, vgap = 70, hgap=10)

        grid_sizer_1.Add(self.Server, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.button_1, 0, wx.ALIGN_CENTER_VERTICAL | wx.SHAPED | wx.ALIGN_RIGHT, 0)

        sizer_2.Add(grid_sizer_1, 1, 0, 0)
        grid_sizer_2.Add(self.label_3, 0, wx.ALIGN_CENTER, 0)
        grid_sizer_2.Add(self.button_2, 0,  wx.ALIGN_CENTER | wx.SHAPED, 0)

        sizer_1.Add(grid_sizer_2, 1, 0, 0)
        sizer_2.Add(sizer_1, 1, 0, 0)
        grid_sizer_3.Add(self.label_6, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_3.Add(self.label_9, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        grid_sizer_3.Add(self.text_ctrl_5, 0, wx.ALIGN_CENTER_VERTICAL | wx.SHAPED, 0)
        grid_sizer_3.Add(self.button_3, 0, wx.ALIGN_CENTER_VERTICAL | wx.SHAPED, 0)
        sizer_2.Add(grid_sizer_3, 1, 0, 0)
        sizer_2.Add(self.text_ctrl_8, 5, wx.EXPAND, 0)
        self.SetSizer(sizer_2)
        self.Fit()
        self.Layout()

if __name__=="__main__":
    app = wx.App()
    frame = MyFrame()
    frame.Show(True)
    app.MainLoop()
