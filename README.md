# __Johnny's IPv4 Subnet Calculator__

> This document uses Markdown.  Please view on Github (https://github.com/johnnywilkes/NPL_JAN_2019_SUBNET_CALC) or use the following for viewing: https://stackedit.io/app#

## ___Overall Program Idea___

There are the requirements of the base challenge:
1. Input IP address and subnet mask (validate)
2. Calculate wildcard mask
3. Calculate number of host bits
4. Determine address class (A,B,C)
5. Calculate Network address
6. Calculate broadcast address 
7. Calculate first host address, last host address and total num of host addresses
8. Print all the relevant info

This could all be accomplished with the [ipaddress module](https://docs.python.org/3/library/ipaddress.html#ipaddress.IPv4Network.num_addresses). 

I know that there are other modules or DIY functions that could be done, but this seemed to be the easiest way and didn't require an additional library install.

Then the relevant values could be converted to binary and hexadecimal (first bonus) with a small snippet of code:

```
    vf_str_IP_input = input('Enter IP or Mask: ')
    print('Input is',vf_str_IP_input,'in decimal')
    vf_str_binary_raw = format(int(ipaddress.IPv4Address(vf_str_IP_input)),'b')
    vf_int_toadd = 32 - len(vf_str_binary_raw)
    vf_str_binary_format = ('0' * vf_int_toadd) + vf_str_binary_raw
    print('Input is',vf_str_binary_format,'in binary')
    vf_str_hex_raw = format(int(ipaddress.IPv4Address(vf_str_IP_input)),'x')
    vf_int_toadd2 = 8 - len(vf_str_hex_raw)
    vf_str_hex_format = ('0' * vf_int_toadd2) + vf_str_hex_raw
    print('Input is',vf_str_hex_format,'in hexadecimal')
```

I decided on the built-in module `format()` because the `bin()` and `hex()` modules append a `0b` or `0x` to the front.  The only issue with format() is that you need to first convert the IP address to an integer and at that point, format() doesn't necessary recognize it as a 32-bit IP.  What I mean by that is that it will leave off leading zeros.

`format(int(ipaddress.IPv4Address('10.0.0.1')),'b')` will output `1010000000000000000000000001` instead of `00001010000000000000000000000001`

Therefore, I had to find out the length of the output and add zeros when necessary.


## ___Variable Naming/Program Structure___

This program uses the same variable naming, comment and program structure as last month's submission for, more information, see the section with the same name (Variable Naming/Program Structure) in the following link:
https://github.com/johnnywilkes/NPL_NOV_2018_TIME/blob/master/README.md


## ___Possible Refactoring/Feature Releases___

 - I ran out of time and wanted to do the second bonus challenge.  However, my philosophy when challenged with either having to well document a solution or add additional features, is always to make the documentation right.
 - I believe I did it the "quick and dirty" way regarding the binary and hexadecimal conversion.  I believe there has to be a better was or at least a way that terry showed me that offered more control/flexibility (adding dots between octets).
 
