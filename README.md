# c2f_interface
c interface to fortran interface
# support
-  `int`,`long`,`float`,`double`,`char *`
- `type *` as `dimension(*)`

# Two verisons
## re version
no dependency
## parser version
Requirements : https://github.com/skywind3000/LIBLR

**parser version only**
- "[]" as `dimension`
- "type (* foo) ()" as `type(c_funcptr),value::`

# remarks
- should have `;`

# example

 file "test.h" 
 
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
