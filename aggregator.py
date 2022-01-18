from sniff import Sniff
import threading 
import json
class Aggregator:
    def __init__(self, interval_time):
        self.file = open('full_program.txt','w')
        self.sniffer = Sniff(self.add_to_list)
        self.len = 1
        self.arr_length = 60
        self.call_list = []
        self.interval_time = interval_time
        self.functions = {}
        self.values = {
            'total': {
                    'total': [0 for i in range(self.len)],
                    'incoming': [0 for i in range(self.len)],
                    'outgoing': [0 for i in range(self.len)]
            },
            'package':{
                'total': [0 for i in range(self.len)],
                'incoming': [0 for i in range(self.len)],
                'outgoing': [0 for i in range(self.len)]
            },
            'programs': {}
        }
    
    def update_total(self, obj, sum_value):
        multiplier = obj['multiplier']
        number = obj['number']
        number += sum_value/(10**(3*multiplier))
        if(number > 1000):
            multiplier += 1
            number /=1000
        
        obj['multiplier'] = multiplier
        obj['number'] = number
        return obj

    def define_function(self, obj):
        self.functions.update(obj)

    def adder_function(self):
        interval = threading.Event()
        while not interval.wait(0.001):
            if len(self.call_list):
                value = self.call_list.pop(0)
                self.add_value(value)
    
    def add_to_list(self,pct):
        self.file.write(json.dumps(pct) + '\n')
        self.call_list.append(pct)
    
    def start(self):
        t = threading.Thread(target=self.sniffer.start)
        t.daemon = True
        t.start()
        t2 = threading.Thread(target=self.interval)
        t2.daemon = True
        t2.start()
        for i in range(3):
            thread = threading.Thread(target=self.adder_function)
            thread.daemon = True
            thread.start()

    
    def add_value(self, pct):
        program = pct['proc_name']
        connection = pct['Ip']
        protocol = pct['t_protocol']
        incoming = pct['incoming']
        outgoing = pct['outgoing']

        if program not in self.values['programs']:
            self.values['programs'][program] = {
                'total': {
                    'total': [0 for i in range(self.len)],
                    'incoming': [0 for i in range(self.len)],
                    'outgoing': [0 for i in range(self.len)]
                },
                'package':{
                'total': [0 for i in range(self.len)],
                'incoming': [0 for i in range(self.len)],
                'outgoing': [0 for i in range(self.len)]
                },
                'accumulated': {
                    'multiplier': 0,
                    'number': 0
                },
                'connections': {}
            }

            def caller():
                return self.values['programs'][program]
            self.functions['new_program']({
                'caller': caller,
                'name': program,

                }
            )
        
        if connection not in self.values['programs'][program]['connections']:
            self.values['programs'][program]['connections'][connection] = {
                'total': {
                    'total': [0 for i in range(self.len)],
                    'incoming': [0 for i in range(self.len)],
                    'outgoing': [0 for i in range(self.len)]
                },
                'package':{
                'total': [0 for i in range(self.len)],
                'incoming': [0 for i in range(self.len)],
                'outgoing': [0 for i in range(self.len)]
                },
                'accumulated': {
                    'multiplier': 0,
                    'number': 0
                },
                'protocol': {
                    'TCP': {
                        'total': {
                            'total': [0 for i in range(self.len)],
                            'incoming': [0 for i in range(self.len)],
                            'outgoing': [0 for i in range(self.len)]
                        },
                        'second': {
                            'incoming': 0,
                            'outgoing': 0
                        },
                        'pack_count':{
                            'incoming': 0,
                            'outgoing': 0
                        },
                        'package':{
                        'total': [0 for i in range(self.len)],
                        'incoming': [0 for i in range(self.len)],
                        'outgoing': [0 for i in range(self.len)]
                        },
                        'accumulated': {
                            'multiplier': 0,
                            'number': 0
                        },

                    },
                    'UDP': {
                        'total': {
                            'total': [0 for i in range(self.len)],
                            'incoming': [0 for i in range(self.len)],
                            'outgoing': [0 for i in range(self.len)]
                        },
                        'second': {
                            'incoming': 0,
                            'outgoing': 0
                        },
                        'pack_count':{
                            'total': 0,
                            'incoming': 0,
                            'outgoing': 0
                        },
                        'package':{
                        'total': [0 for i in range(self.len)],
                        'incoming': [0 for i in range(self.len)],
                        'outgoing': [0 for i in range(self.len)]
                        },
                        'accumulated': {
                            'multiplier': 0,
                            'number': 0
                        },
                    }
                }
            }
        
        self.values['programs'][program]['connections'][connection]['protocol'][protocol]['second']['incoming'] = incoming
        self.values['programs'][program]['connections'][connection]['protocol'][protocol]['second']['outgoing'] = outgoing

        self.values['programs'][program]['connections'][connection]['protocol'][protocol]['pack_count']['incoming'] = int(incoming > 0)
        self.values['programs'][program]['connections'][connection]['protocol'][protocol]['pack_count']['outgoing'] = int(outgoing > 0)
        


        
    def update_array(self):
        if(self.len < self.arr_length):
            self.len += 1
        
        total_in = 0
        total_out = 0

        total_pack_in = 0
        total_pack_out = 0

        for prog_name in self.values['programs']:
            program = self.values['programs'][prog_name]
            prog_in = 0
            prog_out = 0

            prog_pack_in = 0
            prog_pack_out = 0

            prog_accumulated = program['accumulated']

            for conn_name in program['connections']:
                connection = program['connections'][conn_name]
                conn_in = 0
                conn_out = 0

                conn_pack_in = 0
                conn_pack_out = 0

                conn_accumulated = connection['accumulated']

                for prot_name in connection['protocol']:
                    protocol = connection['protocol'][prot_name]
                    prot_in = 0
                    prot_out = 0

                    prot_in, prot_out = protocol['second']['incoming'], protocol['second']['outgoing']
                    pack_in,pack_out = protocol['pack_count']['incoming'], protocol['pack_count']['outgoing']
                    
                    prot_accumulated = protocol['accumulated']
                    
                    protocol['second']['incoming'] = 0
                    protocol['second']['outgoing'] = 0

                    protocol['pack_count']['incoming'] = 0
                    protocol['pack_count']['outgoing'] = 0

                    protocol['total']['incoming'].append(prot_in)
                    protocol['total']['outgoing'].append(prot_out)
                    protocol['total']['total'].append(prot_in + prot_out)

                    protocol['total']['incoming'].append(prot_in)
                    protocol['total']['outgoing'].append(prot_out)
                    protocol['total']['total'].append(prot_in + prot_out)

                    protocol['package']['incoming'].append(pack_in)
                    protocol['package']['outgoing'].append(pack_out)
                    protocol['package']['total'].append(pack_in + pack_out)

                    if len(protocol['total']['incoming']) > self.arr_length:
                        protocol['total']['incoming'] = protocol['total']['incoming'][1:]
                        protocol['total']['outgoing'] = protocol['total']['outgoing'][1:]
                        protocol['total']['total'] = protocol['total']['total'][1:]
                        protocol['package']['incoming'] = protocol['package']['incoming'][1:]
                        protocol['package']['outgoing'] = protocol['package']['outgoing'][1:]
                        protocol['package']['total'] = protocol['package']['total'][1:]
                    


                    conn_in += prot_in
                    conn_out += prot_out

                    conn_pack_in += pack_in
                    conn_pack_out += pack_out
                    
                    self.update_total(prot_accumulated,prot_in + prot_out)
                
                connection['total']['incoming'].append(conn_in)
                connection['total']['outgoing'].append(conn_out)
                connection['total']['total'].append(conn_in + conn_out)

                connection['package']['incoming'].append(conn_pack_in)
                connection['package']['outgoing'].append(conn_pack_out)
                connection['package']['total'].append(conn_pack_in + conn_pack_out)

                if len(connection['total']['incoming']) > self.arr_length:
                    connection['total']['incoming'] = connection['total']['incoming'][1:]
                    connection['total']['outgoing'] = connection['total']['outgoing'][1:]
                    connection['total']['total'] = connection['total']['total'][1:]
                    connection['package']['incoming'] = connection['package']['incoming'][1:]
                    connection['package']['outgoing'] = connection['package']['outgoing'][1:]
                    connection['package']['total'] = connection['package']['total'][1:]

                prog_in += conn_in
                prog_out += conn_out

                prog_pack_in += conn_pack_in
                prog_pack_out += conn_pack_out

                self.update_total(conn_accumulated,conn_in + conn_out)


            program['total']['incoming'].append(prog_in)
            program['total']['outgoing'].append(prog_out)
            program['total']['total'].append(prog_in + prog_out)

            program['package']['incoming'].append(prog_pack_in)
            program['package']['outgoing'].append(prog_pack_out)
            program['package']['total'].append(prog_pack_in + prog_pack_out)

            if len(program['total']['incoming']) > self.arr_length:
                program['total']['incoming'] = program['total']['incoming'][1:]
                program['total']['outgoing'] = program['total']['outgoing'][1:]
                program['total']['total'] = program['total']['total'][1:]

                program['package']['incoming'] = program['package']['incoming'][1:]
                program['package']['outgoing'] = program['package']['outgoing'][1:]
                program['package']['total'] = program['package']['total'][1:]

            total_in += prog_in
            total_out += prog_out

            total_pack_in += prog_pack_in
            total_pack_out += prog_pack_out

            self.update_total(prog_accumulated,prog_in + prog_out)
        
        self.values['total']['incoming'].append(total_in)
        self.values['total']['outgoing'].append(total_out)
        self.values['total']['total'].append(total_in + total_out)

        self.values['package']['incoming'].append(total_pack_in)
        self.values['package']['outgoing'].append(total_pack_out)
        self.values['package']['total'].append(total_pack_in + total_pack_out)



        if len(self.values['total']['incoming']) > self.arr_length:
            self.values['total']['incoming'] = self.values['total']['incoming'][1:]
            self.values['total']['outgoing'] = self.values['total']['outgoing'][1:]
            self.values['total']['total'] = self.values['total']['total'][1:]

            self.values['package']['incoming'] = self.values['package']['incoming'][1:]
            self.values['package']['outgoing'] = self.values['package']['outgoing'][1:]
            self.values['package']['total'] = self.values['package']['total'][1:]
                    

    def interval(self):
        interval = threading.Event()
        while not interval.wait(self.interval_time):
            self.update_array()

