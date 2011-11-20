#!/usr/bin/python

import sympy
n, e = sympy.var('n e')
z = sympy.var('z0 z1 z2 z3 z4 z5 z6 z7')

eta=((2*e)**2*(n+2)/2/(n+8)**2*
     (1+(2*e)/4/(n+8)**2*(-n*n+56*n+272) 
     +(2*e)**2/16/(n+8)**4*(-5*n**4-230*n**3+1124*n**2+17920*n+46144-384*(n+8)*(5*n+22)*z[3])
     -(2*e)**3/64/(n+8)**6*(13*n**6+946*n**5+27620*n**4+121472*n**3-262528*n**2-2912768*n-5655552
                           -z[3]*((n+8)*16*(n**5+10*n**4+1220*n**3-1136*n**2-68672*n-171264))
                           +z[4]*((n+8)**3*1152*(5*n+22))
                           -z[5]*((n+8)**2*5120*(2*n**2+55*n+186))
                           )
                                                                                                                               
      )
     )
zeta=sympy.special.zeta_functions.zeta
eta_n1=eta.subs(n, 1)

for i in range(len(z)):
    eta_n1=eta_n1.subs(z[i], zeta(i))

eta_n1=eta_n1.subs(e, e/2)
print eta_n1.evalf()

w=((2*e)- (2*e)**2/(n+8)**2*(9*n+42)
   +(2*e)**3/4/(n+8)**4*(33*n**3+538*n**2+4288*n+9568+96*(n+8)*(5*n+22)*z[3])
   -(2*e)**4/16/(n+8)**6*(-5*n**5+1488*n**4+46616*n**3+419528*n**2+1750080*n+2599552
                          +z[3]*96*(n+8)*(63*n**3+548*n**2+1916*n+3872)
                          -z[4]*288*(n+8)**3*(5*n+22)
                          +z[5]*1920*(n+8)**2*(2*n**2+55*n+186))  #n**2?  
   +(2*e)**5/64/(n+8)**8*(13*n**7+7196*n**6+240328*n**5+3760776*n**4+38877056*n**3+223778048*n**2+660389888*n+752420864
                          -z[3]*(n+8)*16*(9*n**6-1104*n**5-11648*n**4-243864*n**3-2413248*n**2-9603328*n-14734080)
                          -(z[3])**2*(n+8)**2*768*(6*n**4+107*n**3+1826*n**2+9008*n+8736)
                          -z[4]*(n+8)**3*288*(63*n**3+548*n**2+1916*n+3872)
                          +z[5]*(n+8)**2*256*(305*n**4+7386*n**3+45654*n**2+143212*n+226992)
                          -z[6]*(n+8)**4*9600*(2*n**2+55*n+186)
                          +z[7]*(n+8)**3*112896*(14*n**2+189*n+526)
                          )
   )
w_n1=w.subs(n, 1)

for i in range(len(z)):
    w_n1=w_n1.subs(z[i], zeta(i))

w_n1=w_n1.subs(e, e/2)
print w_n1.evalf()
