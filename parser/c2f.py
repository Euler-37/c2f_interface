import LIBLR
grammar = r'''
start    : type  function              {getdouble}
         ;

type     : 'const' typename            {getconstype}
         | typename                    {gettype}
         ;

function : funcname paralist           {getdouble}
         ;

paralist : '(' paraitems ')'           {get2}
         ;

paraitems: paraitems ',' typedef       {list_many}
         | typedef                     {list_one}
         |                             {list_empty}
         ;

typedef  : type string                 {getdouble}
         | type string '[' ']'         {getarray}
         | type '[' ']'                {getnonamearray}
         | type                        {getnonameconst}
         | start                       {getfunc}
         ;

typename : string '*'                  {gettwo}
         | string                      {get1}
         ;

funcname : '(' '*' string ')'          {get3}
         | string                      {get1}
         ;
@ignore [ \r\n\t]*
@match string \w+
'''

class SemanticAction:
    def get1 (self, rule, args):
        return args[1]
    def get2  (self, rule, args):
        return args[2]
    def get3  (self, rule, args):
        return args[3]

    def getfunc (self, rule, args):
        return ("func",args[1])

    def getnone (self, rule, args):
        return None

    def gettwo  (self, rule, args):
        return args[1]+args[2]
    def getdouble  (self, rule, args):
        return (args[1],args[2])

    def getarray  (self, rule, args):
        if isinstance(args[1],tuple):
            return (args[1]+("array",),args[2])
        else:
            return ((args[1],"array"),args[2])
    def getnonamearray  (self, rule, args):
        if isinstance(args[1],tuple):
            return (args[1]+("array",),"")
        else:
            return ((args[1],"array"),"")

    def gettype  (self, rule, args):
        return args[1]
    def getconstype (self, rule, args):
        return ("const",args[2])

    def getnonameconst (self, rule, args):
        if isinstance(args[1],tuple):
            return (args[1],"")
        else:
            return args[1]

    def list_many (self, rule, args):
        return args[1] + [args[3]]
    def list_one (self, rule, args):
        return [args[1]]
    def list_empty (self, rule, args):
        return []
def generate_map(key,value):
    mymap={}
    mymap[key]=value+",value::"
    mymap[key+"*"]=value+",intent(inout),dimension(*)::"
    mymap[("const",key+"*")]=value+",intent(in),dimension(*)::"
    mymap[(key,"array")]=value+",intent(inout),dimension(*)::"
    mymap[("const",key,"array")]=value+",intent(in),dimension(*)::"
    return mymap

type_map={
        "int":"integer(c_int) ",
        "size_t":"integer(c_size_t)",
        "long":"integer(c_long) ",
        "float":"real(c_float) ",
        "double":"real(c_double) ",
        "char":"character(len=c_char)",
        "void":"type(*)"
        }
para_map={}
for key,value in type_map.items():
    para_map.update(generate_map(key,value))
para_map["func"]="type(c_funcptr),value::"

import sys
parser = LIBLR.create_parser(grammar, SemanticAction())
print("interface")
with open(sys.argv[1], 'r') as file:
    lines = file.read().replace('\n', '').split(';')
for line in lines:
    if not line:
        continue
    ast=parser(line)
    returntype,a=ast
    if returntype[-1]=="*":
        name=returntype[:-1]
    else:
        name=returntype
    if name in para_map:
         pass
    else:
        cname="type("+name+")"
        type_map[name]=cname
        para_map.update(generate_map(name,cname))

    funcname,items=a
    paralist=[]
    typelist=[]
    for i,s in enumerate(items):
       if isinstance(s, str):
          if s=="void":
              pass
          else:
              typelist.append(s)
              paralist.append("myarg"+str(i))
       else:
           if s[0]=="func":
               typelist.append("func")
               paralist.append("myfunc"+str(i))
           else:
               typelist.append(s[0])
               if s[1]=="":
                  paralist.append("myarg"+str(i))
               else:
                  paralist.append(s[1])
    for key in typelist:
       if key in para_map:
            pass
       else:
            # type,type*
           if isinstance(key, str):
               if key[-1]=="*":
                   name=key[:-1]
               else:
                   name=key
           else:
               # const type*
               # type array
               if len(key)==2:
                   if key[0]=="const":
                       name=key[1][:-1]
                   else:
                       name=key[0]
               elif len(key)==3:
               # const type array
                   name=key[1]
           cname="type("+name+")"
           type_map[name]=cname
           para_map.update(generate_map(name,cname))
    title=[]
    if returntype=="void":
        title.append("subroutine "+funcname+" (")
        endtitle="end subroutine "+funcname
    else:
        if returntype[-1]=="*":
            title.append("type(c_ptr) function "+funcname+" (")
        else:
            title.append(type_map[returntype]+" function "+funcname+" (")
        endtitle="end function "+funcname
    title.append(",".join(paralist))
    title.append(")bind(c)")
    print("".join(title))
    print("    "+"use iso_c_binding")
    for t,name in zip(typelist,paralist):
        if t=="void":
            pass
        else:
            print("   ",para_map[t],name)
    print(endtitle)
    print()
print("end interface")
