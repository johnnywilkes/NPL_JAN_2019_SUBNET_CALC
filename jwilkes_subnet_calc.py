#!/usr/bin/env python3

#ipaddress module for IP/subnet validation and also parsing IP information.
import ipaddress

#function to get ip/subnet mask input from user to be parsed.
def IP_validator():
    #entered a quit variable `q` to escape loop if necessary.
    print('Press `q` at any prompt to escape')
    #get ip address/subnet mask info from user.
    vf_str_IP_input = input('Enter IP: ')
    print('Enter subnet mask is decimal or CIDR length (ex. 255.255.255.0 or `24` for `/24`)')
    vf_str_mask_input = input('Enter Subnet Mask: ')
    #concatenate IP/mask to enter into ipaddress module for validation. 
    vf_str_IP_plus_mask = vf_str_IP_input + '/' + vf_str_mask_input
    #tracker variable for while loop.
    vf_bool_track = False
    #try entering IP/mask into ipaddress module, this will fail if it is a bad entry and will continue to prompt user for another entry until a good entry or `q` is entered.
    while vf_bool_track == False:
        try:
            ipaddress.IPv4Interface(vf_str_IP_plus_mask)
            vf_bool_track = True
        except:
            #exit program is `q` is entered
            if vf_str_IP_input == 'q':
                exit()
            print('IP or Mask entered in incorrect format, please try again!')
            vf_str_IP_input = input('Enter IP: ')
            vf_str_mask_input = input('Enter Subnet Mask (decimal or CIDR): ')
            vf_str_IP_plus_mask = vf_str_IP_input + '/' + vf_str_mask_input
    #if IP/mask are good, return to main.
    return(vf_str_IP_plus_mask)

#function to parse IP attributes in order: Wildcard mask, host bits, address class, network address, broadcast address, 1st host address, last host address, total host address.   
def format_IP(vf_str_IP_input):
    #input ipaddress info into ipaddress module to parse data.
    vf_ipad_ipinfo = ipaddress.IPv4Interface(vf_str_IP_input)
    #find IP address to be added to results dictionary.
    vf_str_ipaddr = vf_ipad_ipinfo.ip
    #find subnet mask (is dotted decimal format) to be added to results dictionary.
    vf_str_ip_plus_netmask = vf_ipad_ipinfo.with_netmask
    vf_list_split_netmask = vf_str_ip_plus_netmask.split('/')
    vf_str_netmask = vf_list_split_netmask[1]
    #find wildcard mask to be added to results dictionary.
    vf_ipad_host_mask = vf_ipad_ipinfo.with_hostmask
    vf_list_split_hmask = vf_ipad_host_mask.split('/')
    #find host bits to be added to results dictionary.
    vf_ipad_prefix_len = vf_ipad_ipinfo.with_prefixlen
    vf_list_split_prefix = vf_ipad_prefix_len.split('/')
    vf_int_prefix = int(vf_list_split_prefix[1])
    vf_int_host_bits = 32 - vf_int_prefix
    #find the address class to be added to results dictionary.
    vf_list_split_oct = vf_str_IP_input.split('.')
    vf_int_first_oct = int(vf_list_split_oct[0])
    if vf_int_first_oct < 128:
        vf_str_class = 'A'
    elif vf_int_first_oct < 192:
        vf_str_class = 'B'
    else:
        vf_str_class = 'C'
    #find the network address to be added to results dictionary.
    vf_str_netaddr_raw = str(vf_ipad_ipinfo.network)
    vf_list_split_netaddr = vf_str_netaddr_raw.split('/')
    vf_str_netaddr = vf_list_split_netaddr[0]
    #use IPv4Network submodule of ipaddress instead of IPv4Inferace to get different attributes.
    vf_ipad_network = ipaddress.IPv4Network(vf_ipad_ipinfo.network)
    #find the broadcast address to be added to results dictionary.
    vf_str_broadcast = vf_ipad_network.broadcast_address
    #find the first, last and number of host address to be added to results dictionary
    vf_list_ipaddr = list(vf_ipad_network.hosts())
    vf_str_firstaddr = vf_list_ipaddr[0]
    vf_str_lastaddr = vf_list_ipaddr[-1]
    vf_int_numaddr = int(vf_ipad_network.num_addresses) - 2
    #add values to results dictionary to be passed back to main.  Some keys are lists because the binary and hexadecimal equivalents will be added later.
    vf_dict_results = {'ipaddr':[vf_str_ipaddr,'',''],'subnet':[vf_str_netmask,'',''],'wildcard':[vf_list_split_hmask[1],'',''],'hostbits':vf_int_host_bits,'netclass':vf_str_class,'netaddr':[vf_str_netaddr,'',''],'broadcast':[vf_str_broadcast,'',''],'firstaddr':[vf_str_firstaddr,'',''],'lastaddr':[vf_str_lastaddr,'',''],'numaddr':vf_int_numaddr}
    ##print(vf_dict_results)
    ##print()
    #return dictionary of results back to main.
    return(vf_dict_results)

#function to convert select key values in dictionary from decimal to binary and hexadecimal.
def convert(vf_dict_results):
    #iterate over keys in dictionary and add additional binary/hexadecimal entries if the key type is a list.
    for vf_str_dict_values in vf_dict_results.keys():
        if type(vf_dict_results[vf_str_dict_values]) == list:    
            #a bit complicated: take first value in key of list in dictionary (decimal value) and pass through ipaddress module, then make it in integer and then make it a binary value.
            vf_str_binary_raw = format(int(ipaddress.IPv4Address(vf_dict_results[vf_str_dict_values][0])),'b')
            #this will no include leading zeros, therefore the length of the binary need to be compared to the desired value of 32 and the appropriate number of leading zeros added.
            vf_int_toadd = 32 - len(vf_str_binary_raw)
            #add value as the second list value within the dictionary entry.
            vf_dict_results[vf_str_dict_values][1] = ('0' * vf_int_toadd) + vf_str_binary_raw
            #pretty much same process as above but with hexadecimal.
            vf_str_hex_raw = format(int(ipaddress.IPv4Address(vf_dict_results[vf_str_dict_values][0])),'x')
            #desired length of hex is 8 characters, need to add trailing zeros if necessary.
            vf_int_toadd2 = 8 - len(vf_str_hex_raw)
            vf_dict_results[vf_str_dict_values][2] = ('0' * vf_int_toadd2) + vf_str_hex_raw
            #add value as the third list value within the dictionary entry.
    ##print(vf_dict_results)
    ##print()
    #return back same dictionary of results with added binary/hexadecimal values.
    return(vf_dict_results)

#function to print the results - all from dictionary of results.
def print_results(vf_dict_results):
    #define the output format.  Keys with a list value will require list number to be verified.
    print('RESULT IN FORMAT: DECIMAL (BINARY) (HEXADECIMAL)')
    #print IP address to include bin/hex formats.
    print('IP address: ',vf_dict_results['ipaddr'][0],' (',vf_dict_results['ipaddr'][1],')','(',vf_dict_results['ipaddr'][2],')',sep='')
    #print subnet mask to include bin/hex formats.
    print('Subnet mask: ',vf_dict_results['subnet'][0],' (',vf_dict_results['subnet'][1],')','(',vf_dict_results['subnet'][2],')',sep='')
    #print wildcard mask to include bin/hex formats.
    print('Wildcard Mask: ',vf_dict_results['wildcard'][0],' (',vf_dict_results['wildcard'][1],')','(',vf_dict_results['wildcard'][2],')',sep='')
    #print number of host bits.
    print('# Host Bits:',vf_dict_results['hostbits'])
    #print network class.
    print('This is a class',vf_dict_results['netclass'],'network')
    #print network address to include bin/hex formats.  the '/' and subnet mask are appended as well in all formats.
    print('Network address: ',vf_dict_results['netaddr'][0]+'/'+vf_dict_results['subnet'][0],' (',vf_dict_results['netaddr'][1]+'/'+vf_dict_results['subnet'][1],')','(',vf_dict_results['netaddr'][2]+'/'+vf_dict_results['subnet'][2],')',sep='')
    #print broadcast, first and last addresses to include bin/hex formats.
    print('Broadcast address: ',vf_dict_results['broadcast'][0],' (',vf_dict_results['broadcast'][1],')','(',vf_dict_results['broadcast'][2],')',sep='')
    print('First IP Address: ',vf_dict_results['firstaddr'][0],' (',vf_dict_results['firstaddr'][1],')','(',vf_dict_results['firstaddr'][2],')',sep='')
    print('Last IP Address: ',vf_dict_results['lastaddr'][0],' (',vf_dict_results['lastaddr'][1],')','(',vf_dict_results['lastaddr'][2],')',sep='')
    #print number of hosts.
    print('The number of hosts is:',vf_dict_results['numaddr'])
    
#main program: functions are called from here.       
if __name__ == '__main__':
    #call IP_validator() function to get the IP address and subnet mask from user input.
    vm_str_IP_input = IP_validator()
    #pass user input to format_IP() function to parse out IP attributes and pass back as dictionary.
    vm_dict_results = format_IP(vm_str_IP_input)
    #pass this same dictionary to the convert() to add additional binary/hexadecimal attributes.  Pass back as updated dictionary.
    vm_dict_results = convert(vm_dict_results)
    #pass results dictionary to print_results() function to print IP attributes onscreen.
    print_results(vm_dict_results)
