import sys

import re
def parse_function_definition(definition):
    # get function name
    function_name = re.search(r'\w+(?=\()', definition).group()
    # get type
    return_type = re.search(r'\w+\s*\**(?=\s+\w+\()', definition)
    if return_type is None:
        return_type = 'NONETYPE'
    else:
        return_type = return_type.group()
    # parameter list
    parameters= re.search(r'\((.*?)\)', definition).group(1).split(",")
    para_type=[]
    para_list=[]
    for (i,p) in enumerate(parameters):
        r=re.findall(r'(\w+\s*\**)\s+(\w+)', p)
        if not r:
            # TYPE func(type)
            p=p.replace(" ", "")
            # TYPE func(void)
            if p=="void":
                pass
            else:
                para_type.append(p)
                para_list.append("my_arg"+str(i))
        else:
            # TYPE func(type a)
            para_type.append(r[0][0].replace(" ", ""))
            para_list.append(r[0][1].replace(" ", ""))
    return [return_type,function_name, para_type,para_list]


type_map={
        "int":"integer(c_int) ",
        "long":"integer(c_long) ",
        "float":"real(c_float) ",
        "double":"real(c_double) ",
        }
para_map={
        "int"     : "integer(c_int)  ,value                          :: ",
        "long"    : "integer(c_long) ,value                          :: ",
        "float"   : "real(c_float)   ,value                          :: ",
        "double"  : "real(c_double)  ,value                          :: ",
        "int*"    : "integer(c_int),intent(inout),dimension(*)       :: ",
        "long*"   : "integer(c_long),intent(inout),dimension(*)      :: ",
        "float*"  : "real(c_float),intent(inout),dimension(*)        :: ",
        "double*" : "real(c_double),intent(inout),dimension(*)       :: ",
        "char*"   : "character(len=c_char),intent(inout),dimension(*):: "
        }
print("interface")
with open(sys.argv[1], 'r') as file:
    lines = file.read().replace('\n', '').split(';')
for line in lines:
    if not line:
        continue
    ast=parse_function_definition(line)
    title=[]
    if ast[0]=="void":
        title.append("subroutine "+ast[1]+" (")
        endtitle="end subroutine "+ast[1]
    else:
        title.append(type_map[ast[0]]+" function "+ast[1]+" (")
        endtitle="end function "+ast[1]
    title.append(",".join(ast[3]))
    title.append(")bind(c)")
    print("".join(title))
    print("    "+"use iso_c_binding")
    for t,name in zip(ast[2],ast[3]):
        if t=="void":
            pass
        else:
            print("   ",para_map[t],name)
    print(endtitle)
    print()

print("end interface")
