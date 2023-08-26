# c2f_interface
c interface to fortran interface
# support
-  `int`,`long`,`float`,`double`,`char *`,`void`,add others in dict `type_map`
- `type *` as `type,intent(inout),dimension(*)::`
- `const type *` as `type,intent(in),dimension(*)::`

# Two verisons
## re version
no dependency
## parser version
Requirements : https://github.com/skywind3000/LIBLR

**parser version only**
- `[]` as `dimension(*)`
- `type (* foo) ()` as `type(c_funcptr),value::`

# remarks
- each line of c interface file should have `;`

# example

 c interface in `"test.h"` 
 
``` c
void print_hello(int,char*);
void print_double(int n,double * value);
int gcd(int,int m);
double sum(int n,double* a);
```
``` sh
python c2f.py test.h
```
``` fortran
interface
subroutine print_hello (my_arg0,my_arg1)bind(c)
    use iso_c_binding
    integer(c_int)  ,value                          ::  my_arg0
    character(len=c_char),intent(inout),dimension(*)::  my_arg1
end subroutine print_hello

subroutine print_double (n,value)bind(c)
    use iso_c_binding
    integer(c_int)  ,value                          ::  n
    real(c_double),intent(inout),dimension(*)       ::  value
end subroutine print_double

integer(c_int)  function gcd (my_arg0,m)bind(c)
    use iso_c_binding
    integer(c_int)  ,value                          ::  my_arg0
    integer(c_int)  ,value                          ::  m
end function gcd

real(c_double)  function sum (n,a)bind(c)
    use iso_c_binding
    integer(c_int)  ,value                          ::  n
    real(c_double),intent(inout),dimension(*)       ::  a
end function sum

end interface
```

parser version

``` c
void test(int hello);
void qsort(const T * test,int,int,int (*cmp)(const void*,const void*));
void test2(WIN hello[],int);
void test3(const LINUX* hello,int);
```
``` fortran
interface
subroutine test (hello)bind(c)
    use iso_c_binding
    integer(c_int) ,value:: hello
end subroutine test

subroutine qsort (test,myarg1,myarg2,myfunc3)bind(c)
    use iso_c_binding
    type(T),intent(in),dimension(*):: test
    integer(c_int) ,value:: myarg1
    integer(c_int) ,value:: myarg2
    type(c_funcptr),value:: myfunc3
end subroutine qsort

subroutine test2 (hello,myarg1)bind(c)
    use iso_c_binding
    type(WIN),intent(inout),dimension(*):: hello
    integer(c_int) ,value:: myarg1
end subroutine test2

subroutine test2 (hello,myarg1)bind(c)
    use iso_c_binding
    type(LINUX),intent(in),dimension(*):: hello
    integer(c_int) ,value:: myarg1
end subroutine test2

end interface
```
