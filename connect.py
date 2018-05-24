def detect_promiscuous():
    while True:                                                           
        d = str(promiscping(sys.argv[2]+'/'+sys.argv[3], iface = sys.argv[4], fake_bcast='ff:ff:ff:ff:ff:fe'))
        e = d.split()[5:]
        f = d.split()[:5]        
        for i in list(zip(e,f))[1:3]:
            print(i[1].split(':')[1])
            if int(i[1].split(':')[1]) == 0:                                                                         
                print('Atacante no puede obtener ping requests de forma promiscua en {}'.format(i[0].split(':')[0]))
            else:                                                                                                             
                print('Respondidos {} ping requests en {} de forma promiscua. El servidor es vulnerable'.format(i[1].split(':')[1],i[1].split(':')[0]))          
            if int(i[0].split(':')[1]) == 0:                                                                     
                print('{} ping enviado pero el atacante no obtuvo ninguna respuesta'.format(i[0].split(':')[0]))
            else:                                                                                                   
                print('Atacante no obtuvo respuesta de {} paquetes de {}'.format(i[0].split(':')[1],i[0].split(':')[0]))
