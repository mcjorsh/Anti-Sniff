# Anti-Sniff
Anti-Sniff CONNECT + Automatic Payload + Proxy

![2017-06-28](https://user-images.githubusercontent.com/37552072/40511175-2c606784-5f5c-11e8-8a9e-c3ea07c5448d.png)

To test the application with your own server you must first open an individual sale of the program and configure the IP address and port and give START
the server will remain running until the window closes.

After you start the server you can navigate to the website and see the sample files (in this case a fake login session)
Keep in mind that it depends what browser you use, it can give you an 'insecure connection warning' (because we use a certificate from us that is not the one that the browser has included in its list of trusted certs) but you can confirm the security exception and see the login

Finally for the antisniff test you must simply enter the port, the ip and the iner (which is the network interface, in this case it is used but according to the operating system it can be lo0 for localhost wlan0 for wireless etc)
After giving the test the anti-sniff test will be done
and the result will be displayed in the log window
If the attacker obtained a response, it means that the server is compromised (it might have been deconfigured or through some other attack it has been deconfigured and then violated)
in that case the log will warn that there is a problem
In the meantime you should report that the attacker did not get an answer after trying to track our data

in the autosniff module
you have to change only what is in quotes
on line 21, line 27 and 33
you have to change the IP for which you want
so it remains by default
I do not recommend that you change the port since that guarantees the authentication

then what you have to do is connect automatically when giving START

well now I tell you how it is done
pay attention because it has to be step by step
that is, connect in 443
for authentication
it's the same (you're not going to lose the data)
but you have to leave the 443 open for encryption

EXAMPLE
in the lines:
47 and 69 the IP appears between quotes and the port written as a whole number
you have to write in that format (that is, whenever you change the IP goes between '' and the port without '')
and on line 83
the IP and the port are written together and separated by /
'23 .252.105.89 / 443 '


above I told you in what lines you have to change the IP and the port of the proxy
the rest is activated when opening the interface after clicking on START if you open the Server or CONNECT if you are a client etc
same change it so that the proxy remains fixed and does not change so there should be no problems with the authentication


the payload is sent automatically after establishing the connection
it is understood?
that is: in the CONNECT part
When you connect as a client in the log window, the payload appears if the connection is satisfied and if no error is shown
