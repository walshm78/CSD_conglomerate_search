### CIF archive CIF Field Info extraction minimal 10/05/2022 ###
# script to search cifs for specific cif fields and output the information within them into a .csv file

## requires:
# attribute_text_file - text file containing list of cif fields to search for. One cif field per line.
# cif_file_location - file containing the locaiton of the cifs you wish to search
# output_file_name - a file where the information from the searched cifs will be stored.

import time
from ccdc import io

### files required

attribute_text_file = "congloms.txt" #list of cif fields to search CIF for
cif_file_locations = "cif_locations.gcd" #text file containing the location of one CIF file location per line
output_file_name = "output_attribute_info.csv" #location of file to write output into

### list of cif attributes to extract from CIF archive
attribute_txt = open(attribute_text_file,"r").readlines()
attribute_list = [i.strip() for i in attribute_txt]
print(attribute_list) #prints list 

def remove_formatting(inp):
    """ There maybe a neater way to remove formatting from source files, as this was being repeated multiple times."""
    inp_pre = latin1_to_ascii(inp) #write file can only deal with ascii characters
    inp1_ascii = inp_pre.replace(",", " ") #want to remove commas as upsets csv formatting
    inp_ascii = inp1_ascii.replace("\n", " ") #want to remove \n as it also upsets csv formatting
    return inp_ascii

def latin1_to_ascii (unicode_text):
    """ Function found online - unicode hammer from: http://www.noah.org/wiki/unicode_hammer
        It has been modified slightly by ccdc for python3.
        This takes a UNICODE string and replaces Latin-1 characters with
        something equivalent in 7-bit ASCII. It returns a plain ASCII string. 
        This function makes a best effort to convert Latin-1 characters into 
        ASCII equivalents. It does not just strip out the Latin-1 characters.
        All characters in the standard 7-bit ASCII range are preserved. 
        In the 8th bit range all the Latin-1 accented letters are converted 
        to unaccented equivalents. Most symbol characters are converted to 
        something meaningful. Anything not converted is deleted.
    """
    xlate={0xc0:'A', 0xc1:'A', 0xc2:'A', 0xc3:'A', 0xc4:'A', 0xc5:'A',
            0xc6:'Ae', 0xc7:'C',
            0xc8:'E', 0xc9:'E', 0xca:'E', 0xcb:'E',
            0xcc:'I', 0xcd:'I', 0xce:'I', 0xcf:'I',
            0xd0:'Th', 0xd1:'N',
            0xd2:'O', 0xd3:'O', 0xd4:'O', 0xd5:'O', 0xd6:'O', 0xd8:'O',
            0xd9:'U', 0xda:'U', 0xdb:'U', 0xdc:'U',
            0xdd:'Y', 0xde:'th', 0xdf:'ss',
            0xe0:'a', 0xe1:'a', 0xe2:'a', 0xe3:'a', 0xe4:'a', 0xe5:'a',
            0xe6:'ae', 0xe7:'c',
            0xe8:'e', 0xe9:'e', 0xea:'e', 0xeb:'e',
            0xec:'i', 0xed:'i', 0xee:'i', 0xef:'i',
            0xf0:'th', 0xf1:'n',
            0xf2:'o', 0xf3:'o', 0xf4:'o', 0xf5:'o', 0xf6:'o', 0xf8:'o',
            0xf9:'u', 0xfa:'u', 0xfb:'u', 0xfc:'u',
            0xfd:'y', 0xfe:'th', 0xff:'y', 0x17d:'Z',
            0xa1:'!', 0xa2:'{cent}', 0xa3:'{pound}', 0xa4:'{currency}',
            0xa5:'{yen}', 0xa6:'|', 0xa7:'{section}', 0xa8:'{umlaut}',
            0xa9:'{C}', 0xaa:'{^a}', 0xab:'<<', 0xac:'{not}',
            0xad:'-', 0xae:'{R}', 0xaf:'_', 0xb0:'{degrees}',
            0xb1:'{+/-}', 0xb2:'{^2}', 0xb3:'{^3}', 0xb4:"'",
            0xb5:'{micro}', 0xb6:'{paragraph}', 0xb7:'*', 0xb8:'{cedilla}',
            0xb9:'{^1}', 0xba:'{^o}', 0xbb:'>>', 
            0xbc:'{1/4}', 0xbd:'{1/2}', 0xbe:'{3/4}', 0xbf:'?',
            0xd7:'*', 0xf7:'/', 0x107:'c', 0x131: 'i', 0x142: 'l', 0x144: 'n',
            0x15b: 's', 0x160: 'S'
            }
    
    r = ''
    for i in unicode_text:
        if ord(i) in xlate:
            r += xlate[ord(i)]
        elif ord(i) >= 0x80:
            unicode_text.encode('ascii', 'ignore')
            pass
        else:
            r += str(i)
    return r


def function_to_run(x_tup): #input as a tuple so the number of cifs completed can be tracked
    """ function to extract data """
    global t0 #time of start
    global attribute_list
    x = x_tup[1] #location of the cif
    if x_tup[0] % 10000 == 0: #printout when x is a certain value
        print(x_tup[0],  (time.time() - t0)/60.0)

    ##assumes files are named ccdc_number.cif - if not the code might break
    ## ccdc_number is used as an identifier in the output file
    ccdc_number = x.split("\\")[-1]
    ccdc_number = ccdc_number.split('.')[0]
    ccdc_number = ccdc_number.lstrip("0")
    
    def extract_info(attribute): 
            """ function to extract attribute and remove formatting to return item in ascii format
                function needs to be here so it can use cif code, extraction of most source information the same and therefore function used,
                slightly slower than writing out same thing each time, but still faster than earlier version"""  
            try:
                source = cif.attributes[attribute]
            except AttributeError: #Usually file does not contain it
                source = None
            if source != None:
                try: #extract information and remove problematic characters for writing into csv (non-ascii, commmas, and \n)
                    source_strip = source.strip()
                except: #this normally hits if info is in a loop in CIF
                    source_list = []
                    for i in source:
                                if type(i) == type(None): pass
                                else: source_list.append(i)
                    if len(source_list) != 0:
                                source_strip = " ".join(source_list).strip()
                    else:
                                source_strip = "None"
                source_ascii =remove_formatting(source_strip)           
            else:
                source_ascii = "None"
            return source_ascii
    #####
            
    try:
        f = io.EntryReader(x.strip())#[0]
        cif = f[0]  #can it extract data from the cif file? - if not, print error message
        get_data = True
    except:
        get_data = False
        print("no data at [0] in this file %s " %x.strip())
    if get_data != True:
        return ["Unable to Open"]
    else:
        cif_info = [ccdc_number]
        for attribute in attribute_list:
            info = extract_info(attribute)
            cif_info.append(info)
        return cif_info
        pass

t0 = time.time()

if __name__ == "__main__": 
    cif_list = open(cif_file_locations, "r") #list of location of all cif files in cif archive
    header_list = ["ccdc_number"] + attribute_list
    header_string = ",".join(header_list) + "\n"
    c = cif_list.readlines()
    cif_list.close()
    total_list = c    #total list of cif file locations
    output_total = [] #output info to be written to file is stored here
    t0b = time.time() #time tracker for code progression
    for x  in enumerate(total_list): #x is a list of file names
            vals = function_to_run(x)
            if len(vals) == 1 and vals[0] == "Unable to Open":
                pass
            else:
                output_total.append(vals)
    output_total_file = open(output_file_name, "w")
    output_total_file.write(header_string)
    output_total_file.flush()
    print(len(output_total))
    for i in output_total:
            if len(i) < len(attribute_list): 
                print(i)
            else:
                csv_string = ",".join(i) + "\n"
                output_total_file.write(csv_string)
                output_total_file.flush()
    output_total_file.close()

    print("output file written")
