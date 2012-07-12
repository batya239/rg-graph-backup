#!/usr/bin/python

import sympy
from graphs import Graph
zeta = lambda x: sympy.special.zeta_functions.zeta(x).evalf()

def f(nomenkl):
    table={
        "e111-e-": [ -0.0208333331613, 0.0377625989829, -0.0560792174984, 0.0688067744096, ], # [ 2.54573904577e-10, 5.14279863139e-10, 1.64300408181e-10, 5.04508820933e-10, ], methods.feynmanSD_mpi ,
        "e112-22-e-": [ 0.0175813346501, -0.0796597088528, 0.222071327783, ], # [ 8.11228043515e-08, 9.99882936693e-08, 3.2465948796e-07, ], methods.feynmanSD_mpi ,
        "e112-23-33-e-": [ -0.0373537816334, 0.237744947449, ], # [ 2.19078496062e-07, 6.23873376524e-07, ], methods.feynmanSD_mpi ,
        "e112-23-34-44-e-": [ 0.0205101258045, ], # [ 6.14212736966e-07, ], methods.feynmanSD_mpi ,
        "e112-23-44-e44--": [ 0.0632308051123, ], # [ 4.44122881185e-07, ], methods.feynmanSD_mpi ,
        "e112-23-45-e45-e5-e-": [ 3.28544600978, ], # [ 6.04098181091e-05, ], methods.feynmanSD_mpi ,
        "e112-23-e4-444--": [ -0.000954745441731, ], # [ 9.0811624255e-08, ], methods.feynmanSD_mpi ,
        "e112-23-e4-455-e5-e-": [ 0.30986384882, ], # [ 2.2076282408e-05, ], methods.feynmanSD_mpi ,
        "e112-23-e4-e45-55-e-": [ 0.309835136171, ], # [ 2.23263442851e-05, ], methods.feynmanSD_mpi ,
        "e112-23-e4-e55-e55--": [ -0.267668315123, ], # [ 2.95093687267e-05, ], methods.feynmanSD_mpi ,
        "e112-33-444-e4--": [ -0.00365362695983, ], # [ 2.57188135229e-08, ], methods.feynmanSD_mpi ,
        "e112-33-e33--": [ -0.00915588782585, 0.0731263842626, ], # [ 1.07330256164e-07, 2.63504647073e-07, ], methods.feynmanSD_mpi ,
        "e112-33-e44-44--": [ 0.0076184303027, ], # [ 1.95339823221e-07, ], methods.feynmanSD_mpi ,
        "e112-33-e44-e5-55-e-": [ -0.418993298645, ], # [ 8.73642768255e-06, ], methods.feynmanSD_mpi ,
        "e112-33-e45-45-e5-e-": [ 1.48632421945, ], # [ 5.63654514545e-05, ], methods.feynmanSD_mpi ,
        "e112-34-334-4-e-": [ 0.0732747018082, ], # [ 6.20774855934e-07, ], methods.feynmanSD_mpi ,
        "e112-34-345-e5-e5-e-": [ -6.18319424763, ], # [ 9.43545870146e-05, ], methods.feynmanSD_mpi ,
        "e112-34-e34-44--": [ 0.00524946366472, ], # [ 4.69574437673e-07, ], methods.feynmanSD_mpi ,
        "e112-34-e34-e4-e-": [ -2.27620316573, 15.8912968331, ], # [ 1.49998364296e-05, 1.72706334735e-05, ], methods.feynmanSD_mpi ,
        "e112-34-e34-e5-55-e-": [ 0.0281733787356, ], # [ 6.90143408992e-05, ], methods.feynmanSD_mpi ,
        "e112-34-e35-45-e5-e-": [ -9.11558902782, ], # [ 0.000152261598994, ], methods.feynmanSD_mpi ,
        "e112-34-e35-e4-55-e-": [ 0.51425885231, ], # [ 6.58146050408e-05, ], methods.feynmanSD_mpi ,
        "e112-34-e35-e5-e55--": [ 1.02849838599, ], # [ 0.000108930266493, ], methods.feynmanSD_mpi ,
        "e112-34-e55-e45-e5--": [ 0.743157350182, ], # [ 3.63461223426e-05, ], methods.feynmanSD_mpi ,
        "e112-e3-333--": [ 0.0028211809317, -0.0176069370257, ], # [ 1.10632036175e-08, 3.92776772334e-08, ], methods.feynmanSD_mpi ,
        "e112-e3-334-5-e55-e-": [ 0.347756870959, ], # [ 6.45626088982e-06, ], methods.feynmanSD_mpi ,
        "e112-e3-344-44--": [ -0.00580593878392, ], # [ 4.31355740015e-08, ], methods.feynmanSD_mpi ,
        "e112-e3-344-55-e5-e-": [ 0.509745701636, ], # [ 1.26640176335e-05, ], methods.feynmanSD_mpi ,
        "e112-e3-345-45-e5-e-": [ -3.4995463975, ], # [ 4.82352298871e-05, ], methods.feynmanSD_mpi ,
        "e112-e3-445-455-e-e-": [ 0.820328960034, ], # [ 1.58594682228e-05, ], methods.feynmanSD_mpi ,
        "e112-e3-e33-e-": [ -0.439482976516, 1.77838904122, -4.68359448224, ], # [ 4.44106626971e-07, 9.21125121428e-07, 3.43602119066e-06, ], methods.feynmanSD_mpi ,
        "e112-e3-e34-44-e-": [ -0.374989231369, 1.88692860253, ], # [ 5.08148647351e-06, 1.7195791252e-05, ], methods.feynmanSD_mpi ,
        "e112-e3-e34-45-55-e-": [ -1.56055413472, ], # [ 3.3323220778e-05, ], methods.feynmanSD_mpi ,
        "e112-e3-e34-55-e55--": [ 1.01945983937, ], # [ 2.20327582494e-05, ], methods.feynmanSD_mpi ,
        "e112-e3-e34-e5-555--": [ 0.22853652574, ], # [ 4.78996871657e-06, ], methods.feynmanSD_mpi ,
        "e112-e3-e44-455-5-e-": [ -0.267687546117, ], # [ 4.29044670853e-05, ], methods.feynmanSD_mpi ,
        "e112-e3-e44-555-e5--": [ -0.139562559781, ], # [ 5.88070756476e-07, ], methods.feynmanSD_mpi ,
        "e112-e3-e44-e44--": [ 0.734994771643, -5.02090762347, ], # [ 1.74749467799e-06, 8.31815348549e-06, ], methods.feynmanSD_mpi ,
        "e112-e3-e44-e55-55--": [ -0.837993914553, ], # [ 1.55560829033e-05, ], methods.feynmanSD_mpi ,
        "e112-e3-e45-445-5-e-": [ 0.41294652564, ], # [ 5.21527002787e-05, ], methods.feynmanSD_mpi ,
        "e112-e3-e45-e45-55--": [ -0.690881104178, ], # [ 1.84160468228e-05, ], methods.feynmanSD_mpi ,
        "e123-234-34-4-e-": [ -0.0480448885523, ], # [ 7.59084464999e-07, ], methods.feynmanSD_mpi ,
        "e123-e23-33--": [ -0.0156249574793, 0.0950894387964, ], # [ 1.16908656248e-07, 3.41463230171e-07, ], methods.feynmanSD_mpi ,
        "e123-e23-44-44--": [ 0.0135447972776, ], # [ 1.78940558365e-07, ], methods.feynmanSD_mpi ,
        "e123-e23-45-45-e5-e-": [ 2.43836104538, ], # [ 3.04071056895e-05, ], methods.feynmanSD_mpi ,
        "e123-e23-e3-e-": [ 0.901542924583, -3.23392881647, 7.98063426439, ], # [ 6.6633352551e-07, 8.50483293986e-07, 3.93267048167e-06, ], methods.feynmanSD_mpi ,
        "e123-e23-e4-e5-555--": [ -0.11882871777, ], # [ 6.30591670866e-06, ], methods.feynmanSD_mpi ,
        "e123-e24-34-44--": [ -0.0248485751273, ], # [ 4.66849447927e-07, ], methods.feynmanSD_mpi ,
        "e123-e24-34-e4-e-": [ 3.88848011323, -22.3866224434, ], # [ 5.19925200582e-06, 1.25656164429e-05, ], methods.feynmanSD_mpi ,
        "e123-e24-35-45-e5-e-": [ 20.8453023305, ], # [ 0.000226416375149, ], methods.feynmanSD_mpi ,
        "e123-e24-55-e45-e5--": [ -3.9044944462, ], # [ 5.95138550903e-05, ], methods.feynmanSD_mpi ,
        "e123-e24-e5-e45-55--": [ 0.369136639255, ], # [ 8.19045633515e-05, ], methods.feynmanSD_mpi ,
        "e123-e45-e45-445--e-": [ -2.35861300064, ], # [ 3.47620226994e-05, ], methods.feynmanSD_mpi ,
        "e123-e45-e45-e45-5--": [ 3.25122310315, ], # [ 3.61737573773e-05, ], methods.feynmanSD_mpi ,
        "ee11-ee-": [ 0.75, -0.375, 0.308425137534, -0.154212568767, 0.0887843277654, ], # [ 5e-21, 2.5e-21, 4.55616758356e-21, 3.52808379178e-21, 4.11997931022e-21, ], methods.feynmanSD_mpi ,
        "ee12-223-3-ee-": [ 0.219741349279, -0.803427690242, 2.02122116032, ], # [ 2.59232047981e-07, 5.19204985707e-07, 1.58416749852e-06, ], methods.feynmanSD_mpi ,
        "ee12-223-4-445-5-ee-": [ -0.234754687428, ], # [ 4.06575296165e-06, ], methods.feynmanSD_mpi ,
#        "ee12-223-4-e44-e-": [ -0.612880071003, 3.97826819388, ], # [ 1.48399236443e-06, 6.01518941907e-06, ], methods.feynmanSD_mpi ,
        "ee12-223-4-e44-e-": [ -0.61436, 3.97826819388, ], # [ 1.48399236443e-06, 6.01518941907e-06, ], methods.feynmanSD_mpi ,
        "ee12-223-4-e45-55-e-": [ 0.0831194612738, ], # [ 2.89114288329e-05, ], methods.feynmanSD_mpi ,
        "ee12-223-4-e55-e55--": [ 0.619993875937, ], # [ 1.05988190214e-05, ], methods.feynmanSD_mpi ,
        "ee12-223-4-ee5-555--": [ 0.110431622312, ], # [ 1.94340304434e-06, ], methods.feynmanSD_mpi ,
        "ee12-233-34-4-ee-": [ 0.401919480979, -2.3516866, ], # [ 1.73866404976e-06, 4.95878224821e-06, ], methods.feynmanSD_mpi ,
        "ee12-233-34-5-e55-e-": [ 0.00789482088278, ], # [ 3.00877621726e-05, ], methods.feynmanSD_mpi ,
        "ee12-233-44-45-5-ee-": [ -0.35505489825, ], # [ 7.47263470556e-06, ], methods.feynmanSD_mpi ,
        "ee12-233-44-e4-e-": [ -0.734995959839, 4.79919998604, ], # [ 1.75311632224e-06, 7.37180282647e-06, ], methods.feynmanSD_mpi ,
        "ee12-233-44-e5-55-e-": [ 1.72263369247, ], # [ 3.0782277897e-05, ], methods.feynmanSD_mpi ,
        "ee12-233-45-44-5-ee-": [ -0.710125099952, ], # [ 1.41070831993e-05, ], methods.feynmanSD_mpi ,
        "ee12-233-45-45-e5-e-": [ -3.34315837111, ], # [ 5.30205685503e-05, ], methods.feynmanSD_mpi ,
        "ee12-233-45-e4-55-e-": [ -0.34452654903, ], # [ 3.54235044075e-05, ], methods.feynmanSD_mpi ,
        "ee12-234-34-45-5-ee-": [ 1.61159649485, ], # [ 1.91711114686e-05, ], methods.feynmanSD_mpi ,
        "ee12-234-34-e4-e-": [ 3.84273458863, -23.0125189252, ], # [ 4.9225864354e-06, 1.69644621584e-05, ], methods.feynmanSD_mpi ,
        "ee12-234-34-e5-55-e-": [ -1.88497662536, ], # [ 4.92857192046e-05, ], methods.feynmanSD_mpi ,
        "ee12-234-35-44-5-ee-": [ 0.349686441422, ], # [ 3.62744850679e-05, ], methods.feynmanSD_mpi ,
        "ee12-234-35-45-e5-e-": [ 12.3346896608, ], # [ 0.000130084847177, ], methods.feynmanSD_mpi ,
        "ee12-234-35-e4-55-e-": [ -4.74218040472, ], # [ 9.36385926831e-05, ], methods.feynmanSD_mpi ,
        "ee12-234-35-ee-555--": [ -0.152673539119, ], # [ 2.81747761575e-06, ], methods.feynmanSD_mpi ,
        "ee12-333-444-5-5-ee-": [ -0.00140797854821, ], # [ 6.53050003361e-08, ], methods.feynmanSD_mpi ,
        "ee12-333-445-5-e5-e-": [ -0.0831260464387, ], # [ 3.97372514889e-06, ], methods.feynmanSD_mpi ,
        "ee12-334-334--ee-": [ -0.24134520539, 1.58897150585, ], # [ 7.11694924577e-07, 2.99780374626e-06, ], methods.feynmanSD_mpi ,
        "ee12-334-335--e55-e-": [ 0.884273683903, ], # [ 1.49405912568e-05, ], methods.feynmanSD_mpi ,
        "ee12-334-344-5-5-ee-": [ -0.482188822633, ], # [ 8.91714794328e-06, ], methods.feynmanSD_mpi ,
        "ee12-334-344-e-e-": [ -0.960378386415, 6.22750277571, ], # [ 2.17647262647e-06, 9.30528827557e-06, ], methods.feynmanSD_mpi ,
        "ee12-334-345-5-e5-e-": [ -7.65843480441, ], # [ 0.000109412383706, ], methods.feynmanSD_mpi ,
        "ee12-334-345-e-55-e-": [ -0.174051206929, ], # [ 4.23357804502e-05, ], methods.feynmanSD_mpi ,
        "ee12-334-355-4-e5-e-": [ 0.191424054581, ], # [ 3.92907541165e-05, ], methods.feynmanSD_mpi ,
        "ee12-334-355-5-ee5--": [ -0.0403671129364, ], # [ 1.52394554167e-05, ], methods.feynmanSD_mpi ,
        "ee12-334-355-e-e55--": [ 2.11847881224, ], # [ 3.73506449353e-05, ], methods.feynmanSD_mpi ,
        "ee12-334-455-55-ee--": [ 0.311436019616, ], # [ 6.3372513304e-06, ], methods.feynmanSD_mpi ,
        "ee12-334-455-e4-5-e-": [ 0.154925219726, ], # [ 8.86550825867e-06, ], methods.feynmanSD_mpi ,
        "ee12-334-455-e5-e5--": [ 1.03797816257, ], # [ 3.91624246642e-05, ], methods.feynmanSD_mpi ,
        "ee12-345-345-e4-5-e-": [ 5.35456623051, ], # [ 5.81026173016e-05, ], methods.feynmanSD_mpi ,
        "ee12-345-345-ee-55--": [ 0.407141939506, ], # [ 8.04104651041e-06, ], methods.feynmanSD_mpi ,
        "ee12-e22-e-": [ 0.750000271588, -1.25396574675, 1.81337917669, -2.16385914942, ], # [ 2.68370079125e-07, -2.60912395846e-08, 3.57445985038e-07, -6.12201865261e-08, ], methods.feynmanSD_mpi ,
        "ee12-e23-33-e-": [ 1.50000187696, -5.34152744919, 13.1756246542, ], # [ 1.78181077168e-06, 2.71883047885e-06, 1.64598372476e-05, ], methods.feynmanSD_mpi ,
        "ee12-e23-34-44-e-": [ 1.87499728466, -10.8059213975, ], # [ 5.40033338069e-06, 1.43196254953e-05, ], methods.feynmanSD_mpi ,
        "ee12-e23-34-45-55-e-": [ 2.62506817749, ], # [ 5.78259295074e-05, ], methods.feynmanSD_mpi ,
        "ee12-e23-34-55-e55--": [ -2.34538114138, ], # [ 3.99062910999e-05, ], methods.feynmanSD_mpi ,
        "ee12-e23-34-e5-555--": [ -0.858684477201, ], # [ 1.63775979779e-05, ], methods.feynmanSD_mpi ,
        "ee12-e23-44-455-5-e-": [ -0.344555796523, ], # [ 4.00280591347e-05, ], methods.feynmanSD_mpi ,
        "ee12-e23-44-555-e5--": [ 0.396720778584, ], # [ 6.74227269536e-06, ], methods.feynmanSD_mpi ,
        "ee12-e23-44-e44--": [ -1.46999181486, 9.59841097738, ], # [ 3.28664707508e-06, 1.43203827197e-05, ], methods.feynmanSD_mpi ,
        "ee12-e23-44-e55-55--": [ 1.72262001503, ], # [ 3.0843144064e-05, ], methods.feynmanSD_mpi ,
        "ee12-e23-45-445-5-e-": [ -1.15154843878, ], # [ 7.33340941377e-05, ], methods.feynmanSD_mpi ,
        "ee12-e23-45-e45-55--": [ 2.41496901302, ], # [ 3.86743021397e-05, ], methods.feynmanSD_mpi ,
        "ee12-e23-e4-444--": [ -0.266849351878, 1.7240777267, ], # [ 6.28301824276e-07, 2.05616094288e-06, ], methods.feynmanSD_mpi ,
        "ee12-e23-e4-455-55--": [ 0.681150115114, ], # [ 1.54922120738e-05, ], methods.feynmanSD_mpi ,
        "ee12-e33-344-4-e-": [ -0.18749544493, 0.943474437, ], # [ 2.70484267678e-06, 8.73311510668e-06, ], methods.feynmanSD_mpi ,
        "ee12-e33-344-5-55-e-": [ 0.509729427939, ], # [ 1.10191184127e-05, ], methods.feynmanSD_mpi ,
        "ee12-e33-345-4-55-e-": [ -0.780267162686, ], # [ 1.5346563439e-05, ], methods.feynmanSD_mpi ,
        "ee12-e33-444-55-5-e-": [ -0.139568285925, ], # [ 2.54492400449e-06, ], methods.feynmanSD_mpi ,
        "ee12-e33-444-e4--": [ 0.164309268186, -1.10448563305, ], # [ 4.23928188459e-07, 1.43539024116e-06, ], methods.feynmanSD_mpi ,
        "ee12-e33-445-45-5-e-": [ 0.206412523721, ], # [ 2.64006941745e-05, ], methods.feynmanSD_mpi ,
        "ee12-e33-445-55-e5--": [ -0.133858019788, ], # [ 2.12771985949e-05, ], methods.feynmanSD_mpi ,
        "ee12-e33-445-e5-55--": [ -0.459771434744, ], # [ 9.78626692361e-06, ], methods.feynmanSD_mpi ,
        "ee12-e33-e33--": [ -0.439482518612, 1.7783865776, -4.6835899952, ], # [ 4.39627293653e-07, 9.05974452508e-07, 3.3401579595e-06, ], methods.feynmanSD_mpi ,
        "ee12-e33-e34-5-555--": [ 0.228537217785, ], # [ 4.73028250727e-06, ], methods.feynmanSD_mpi ,
        "ee12-e33-e44-44--": [ 0.367496192781, -2.51044348395, ], # [ 8.86670331404e-07, 4.34975699695e-06, ], methods.feynmanSD_mpi ,
        "ee12-e33-e44-55-55--": [ -0.418999471374, ], # [ 8.05599995413e-06, ], methods.feynmanSD_mpi ,
        "ee12-e33-e45-45-55--": [ -0.690884918162, ], # [ 1.77136176366e-05, ], methods.feynmanSD_mpi ,
        "ee12-e34-334-4-e-": [ 0.0719110773749, 0.37760406205, ], # [ 7.07233920197e-06, 1.61521165995e-05, ], methods.feynmanSD_mpi ,
        "ee12-e34-334-5-55-e-": [ -2.65615814181, ], # [ 4.56907517673e-05, ], methods.feynmanSD_mpi ,
        "ee12-e34-335-4-55-e-": [ -2.26029155129, ], # [ 3.75686382813e-05, ], methods.feynmanSD_mpi ,
        "ee12-e34-335-5-e55--": [ 0.191428995814, ], # [ 3.59847575092e-05, ], methods.feynmanSD_mpi ,
        "ee12-e34-335-e-555--": [ 0.430312401988, ], # [ 7.73182291119e-06, ], methods.feynmanSD_mpi ,
        "ee12-e34-345-45-5-e-": [ 8.5982165502, ], # [ 0.000105359663019, ], methods.feynmanSD_mpi ,
        "ee12-e34-345-e5-55--": [ 0.821927805197, ], # [ 5.69038178302e-05, ], methods.feynmanSD_mpi ,
        "ee12-e34-355-44-5-e-": [ -1.89524922514, ], # [ 4.14760272015e-05, ], methods.feynmanSD_mpi ,
        "ee12-e34-355-45-e5--": [ 1.8936352563, ], # [ 6.29954967799e-05, ], methods.feynmanSD_mpi ,
        "ee12-e34-355-e4-55--": [ -0.822843078606, ], # [ 3.21942219907e-05, ], methods.feynmanSD_mpi ,
        "ee12-e34-555-e44-5--": [ -0.0831237755248, ], # [ 3.59467684094e-06, ], methods.feynmanSD_mpi ,
        "ee12-e34-e34-44--": [ 0.783845815784, -4.96704642212, ], # [ 2.17570137379e-06, 8.36946804981e-06, ], methods.feynmanSD_mpi ,
        "ee12-e34-e34-55-55--": [ -0.906965490551, ], # [ 1.64556094668e-05, ], methods.feynmanSD_mpi ,
        "ee12-e34-e35-45-55--": [ -0.0535973147704, ], # [ 3.7133600284e-05, ], methods.feynmanSD_mpi ,
        "ee12-ee3-333--": [ -0.0800814437238, 0.326612529461, -0.863709633525, ], # [ 5.12811491382e-08, 7.58259136167e-08, 2.43855153796e-07, ], methods.feynmanSD_mpi ,
        "ee12-ee3-334-5-555--": [ 0.00570810948505, ], # [ 6.86406323453e-07, ], methods.feynmanSD_mpi ,
        "ee12-ee3-344-44--": [ 0.154181387237, -1.09944448995, ], # [ 5.9666211772e-07, 2.16066957817e-06, ], methods.feynmanSD_mpi ,
        "ee12-ee3-344-55-55--": [ -0.13646949462, ], # [ 3.83793308478e-06, ], methods.feynmanSD_mpi ,
        "ee12-ee3-345-45-55--": [ -0.133471511225, ], # [ 3.42027085183e-06, ], methods.feynmanSD_mpi ,
        "ee12-ee3-444-555-5--": [ -0.00281605880541, ], # [ 1.33881702715e-07, ], methods.feynmanSD_mpi ,
        "ee12-ee3-445-455-5--": [ -0.248380243483, ], # [ 7.57679386439e-06, ], methods.feynmanSD_mpi ,
    }

    if nomenkl not in table.keys():
        raise ValueError, "no such graph in table: %s"%nomenkl
    g=Graph(nomenkl)
    g.GenerateNickel()
    e=sympy.var('e')
    res=0
    i=0
    for value in table[nomenkl]:
        res+=value*e**i/g.sym_coef()
        i+=1
    return res

def K_ms(expr):
    e=sympy.var('e')
    return expr.series(e,0,0).removeO()

def K(expr,N=1000):
    e=sympy.var('e')
    return expr.series(e,0,N).removeO()

def printKR1(key):
    print key
    print "   ", KR1_ms[key]
#    print "       ", KR1[key]
#    print "       ", G[key]
    print

e=sympy.var('e')
KR1=dict()
KR1_ms=dict()
G=dict()

#4x 1loop 1
KR1['ee11-ee-'] = K(2/e*f('ee11-ee-'))
KR1_ms['ee11-ee-'] = K_ms(2/e*f('ee11-ee-'))
G['ee11-ee-'] = KR1['ee11-ee-']
printKR1('ee11-ee-')

#2x 2loop 1
KR1['e111-e-'] = K(1/e*f('e111-e-'))
KR1_ms['e111-e-'] = K_ms(KR1['e111-e-'])
G['e111-e-'] = KR1['e111-e-']
printKR1('e111-e-')


#4x 2loop 1
KR1['ee11-22-ee-'] = K(1/e*(sympy.Number(0)-2*KR1['ee11-ee-']*f('ee11-ee-')))
KR1_ms['ee11-22-ee-'] = K_ms(KR1['ee11-22-ee-']+2*2/e*f('ee11-ee-')*(KR1['ee11-ee-']-KR1_ms['ee11-ee-']))
G['ee11-22-ee-'] = K( KR1['ee11-22-ee-']+2*G['ee11-ee-']*KR1['ee11-ee-'])
printKR1('ee11-22-ee-')

#4x 2loop 2
KR1['ee12-e22-e-'] = K(1/e*(f('ee12-e22-e-')-KR1['ee11-ee-']*f('ee11-ee-')))
KR1_ms['ee12-e22-e-'] = K_ms(KR1['ee12-e22-e-'] + 2/e*f('ee11-ee-')*(2/e*f('ee11-ee-')-K_ms(2/e*f('ee11-ee-'))))
G['ee12-e22-e-'] = K(KR1['ee12-e22-e-'] + G['ee11-ee-']*KR1['ee11-ee-'])
printKR1('ee12-e22-e-')

#2x 3loop 1
gamma='e112-22-e-'
KR1[gamma] = K(sympy.Number(2)/3/e*(f(gamma)
    - 2*KR1['e111-e-']*f('ee11-ee-')
    ))
KR1_ms[gamma] = K_ms(KR1[gamma]
    + 2*G['e111-e-']*(KR1['ee11-ee-']-KR1_ms['ee11-ee-'])
    )

G[gamma] = K(KR1[gamma]
    + 2*G['e111-e-']*(KR1['ee11-ee-']-KR1_ms['ee11-ee-']))
printKR1(gamma)


#4x 3loop 1
KR1['ee11-22-33-ee-'] = K(sympy.Number(2)/3/e*(sympy.Number(0)-3*KR1['ee11-22-ee-']*f('ee11-ee-')))  #-2*G['ee11-ee-']*f('ee11-22-ee-')))
KR1_ms['ee11-22-33-ee-'] = K_ms(KR1['ee11-22-33-ee-']
                                + 3*G['ee11-22-ee-']*(KR1['ee11-ee-']-KR1_ms['ee11-ee-'])
                                + 2*G['ee11-ee-']*(KR1['ee11-22-ee-']-KR1_ms['ee11-22-ee-'])
                                - G['ee11-ee-']*(KR1['ee11-ee-']**2-KR1_ms['ee11-ee-']**2))
G['ee11-22-33-ee-'] = K(KR1['ee11-22-33-ee-']
                        + 3*G['ee11-22-ee-']*KR1['ee11-ee-']
                        +2*G['ee11-ee-']*KR1['ee11-22-ee-']
                        -G['ee11-ee-']*KR1['ee11-ee-']**2)
printKR1('ee11-22-33-ee-')

#4x 3loop 2
KR1['ee11-23-e33-e-'] = K(sympy.Number(2)/3/e*(sympy.Number(0)
    -KR1['ee11-22-ee-']*f('ee11-ee-')
    -KR1['ee11-ee-']*f('ee12-e22-e-')
    -KR1['ee12-e22-e-']*f('ee11-ee-')))
KR1_ms['ee11-23-e33-e-'] = K_ms(KR1['ee11-23-e33-e-']
    +G['ee12-e22-e-']*(KR1['ee11-ee-']-KR1_ms['ee11-ee-'])
    +G['ee11-ee-']*(KR1['ee12-e22-e-']-KR1_ms['ee12-e22-e-'])
    +G['ee11-22-ee-']*(KR1['ee11-ee-']-KR1_ms['ee11-ee-'])
    -G['ee11-ee-']*(KR1['ee11-ee-']**2-KR1_ms['ee11-ee-']**2)
    )
G['ee11-23-e33-e-'] = K(KR1['ee11-23-e33-e-']
    +G['ee12-e22-e-']*(KR1['ee11-ee-'])
    +G['ee11-ee-']*(KR1['ee12-e22-e-'])
    +G['ee11-22-ee-']*(KR1['ee11-ee-'])
    -G['ee11-ee-']*(KR1['ee11-ee-']**2)
    )
printKR1('ee11-23-e33-e-')



G['ee11-ee-_1']=sympy.Number(1)/2*f('ee11-ee-')
G['ee11-ee-_1k']=G['ee11-ee-']-G['ee11-ee-_1']
KR1['ee11-ee-_1k']=G['ee11-ee-_1k']

#4x 3loop 3
KR1['ee12-ee3-333--'] = K(sympy.Number(2)/3/e*(f('ee12-ee3-333--')
                                               -KR1['ee11-ee-_1k']*f('e111-e-')))
KR1_ms['ee12-ee3-333--'] = K_ms(KR1['ee12-ee3-333--']
                                +G['ee11-ee-_1k']*(KR1['e111-e-']-KR1_ms['e111-e-'])
                                )
G['ee12-ee3-333--'] = K(KR1['ee12-ee3-333--']
                        +G['ee11-ee-_1k']*(KR1['e111-e-'])
                        )
printKR1('ee12-ee3-333--')


#4x 3loop 4
KR1['e123-e23-e3-e-'] = K(sympy.Number(2)/3/e*f('e123-e23-e3-e-'))
KR1_ms['e123-e23-e3-e-'] = K_ms(KR1['e123-e23-e3-e-'])
G['e123-e23-e3-e-'] = KR1['e123-e23-e3-e-']
printKR1('e123-e23-e3-e-')


#4x 3loop 5
KR1['ee12-e33-e33--'] = K(sympy.Number(2)/3/e*(f('ee12-e33-e33--')-2*KR1['ee12-e22-e-']*f('ee11-ee-')))
KR1_ms['ee12-e33-e33--'] = K_ms(KR1['ee12-e33-e33--']
    + 2 * G['ee12-e22-e-']*(KR1['ee11-ee-']-KR1_ms['ee11-ee-'])
    + G['ee11-ee-']*(KR1['ee11-22-ee-']-KR1_ms['ee11-22-ee-'])
    )

G['ee12-e33-e33--'] = K(KR1['ee12-e33-e33--']
    + 2 * G['ee12-e22-e-']*(KR1['ee11-ee-'])
    + G['ee11-ee-']*(KR1['ee11-22-ee-'])
    )
printKR1('ee12-e33-e33--')


#4x 3loop 6
KR1['e112-e3-e33-e-'] = K(sympy.Number(2)/3/e*(f('e112-e3-e33-e-')-2*KR1['ee12-e22-e-']*f('ee11-ee-')))
KR1_ms['e112-e3-e33-e-'] = K_ms(KR1['e112-e3-e33-e-']
    + 2 * G['ee12-e22-e-']*(KR1['ee11-ee-']-KR1_ms['ee11-ee-'])
    - G['ee11-ee-']*(KR1['ee11-ee-']**2-KR1_ms['ee11-ee-']**2)
    )

G['e112-e3-e33-e-'] = K(KR1['e112-e3-e33-e-']
    + 2 * G['ee12-e22-e-']*(KR1['ee11-ee-'])
    - G['ee11-ee-']*(KR1['ee11-ee-']**2)
    )
printKR1('e112-e3-e33-e-')


#4x 3loop 7
gamma='ee12-e23-33-e-'
KR1[gamma] = K(sympy.Number(2)/3/e*(f(gamma)-KR1['ee12-e22-e-']*f('ee11-ee-')-KR1['ee11-ee-']*f('ee12-e22-e-')))
KR1_ms[gamma] = K_ms(KR1[gamma]
    + G['ee12-e22-e-']*(KR1['ee11-ee-']-KR1_ms['ee11-ee-'])
    + G['ee11-ee-']*(KR1['ee12-e22-e-']-KR1_ms['ee12-e22-e-'])
    )

G[gamma] = K(KR1[gamma]
    + G['ee12-e22-e-']*(KR1['ee11-ee-'])
    + G['ee11-ee-']*(KR1['ee12-e22-e-'])
    )
printKR1(gamma)

#4x 3loop 8
gamma='ee12-223-3-ee-'
KR1[gamma] = K(sympy.Number(2)/3/e*(f(gamma)-2*KR1['ee11-ee-']*f('ee12-e22-e-')-KR1['ee11-22-ee-']*f('ee11-ee-')))
KR1_ms[gamma] = K_ms(KR1[gamma]
    + 2*G['ee11-ee-']*(KR1['ee12-e22-e-']-KR1_ms['ee12-e22-e-'])
    + G['ee11-22-ee-']*(KR1['ee11-ee-']-KR1_ms['ee11-ee-'])
    )

G[gamma] = K(KR1[gamma]
    + 2*G['ee11-ee-']*(KR1['ee12-e22-e-'])
    + G['ee11-22-ee-']*(KR1['ee11-ee-'])
    )
printKR1(gamma)


#4x 4loop 1
gamma='ee11-22-33-44-ee-'
KR1[gamma] = K(sympy.Number(1)/2/e*(0-4*KR1['ee11-22-33-ee-']*f('ee11-ee-')))
KR1_ms[gamma] = K_ms(KR1[gamma]
    + 4*G['ee11-22-33-ee-']*(KR1['ee11-ee-']-KR1_ms['ee11-ee-'])
    + 3*G['ee11-22-ee-']*(KR1['ee11-22-ee-']-KR1_ms['ee11-22-ee-'])
    + 2*G['ee11-ee-']*(KR1['ee11-22-33-ee-']-KR1_ms['ee11-22-33-ee-'])
    - 3*G['ee11-22-ee-']*(KR1['ee11-ee-']**2-KR1_ms['ee11-ee-']**2)
    - 2*G['ee11-ee-']*(KR1['ee11-ee-']*KR1['ee11-22-ee-']-KR1_ms['ee11-ee-']*KR1_ms['ee11-22-ee-'])
    )

G[gamma] = K(KR1[gamma]
    + 4*G['ee11-22-33-ee-']*(KR1['ee11-ee-'])
    + 3*G['ee11-22-ee-']*(KR1['ee11-22-ee-'])
    + 2*G['ee11-ee-']*(KR1['ee11-22-33-ee-'])
    - 3*G['ee11-22-ee-']*(KR1['ee11-ee-']**2)
    - 2*G['ee11-ee-']*(KR1['ee11-ee-']*KR1['ee11-22-ee-'])
)
printKR1(gamma)


#4x 4loop 2
gamma='ee11-22-34-e44-e-'
KR1[gamma] = K(sympy.Number(1)/2/e*(0
     - 2*KR1['ee11-23-e33-e-']*f('ee11-ee-')
     - KR1['ee11-22-33-ee-']*f('ee11-ee-')
     - KR1['ee11-22-ee-']*f('ee12-e22-e-')
     ))
KR1_ms[gamma] = K_ms(KR1[gamma]
     + 2*G['ee11-23-e33-e-']*(KR1['ee11-ee-']-KR1_ms['ee11-ee-'])
     + G['ee11-22-33-ee-']*(KR1['ee11-ee-']-KR1_ms['ee11-ee-'])
     + G['ee11-22-ee-']*(KR1['ee12-e22-e-']-KR1_ms['ee12-e22-e-'])
     + G['ee11-ee-']*(KR1['ee11-23-e33-e-']-KR1_ms['ee11-23-e33-e-'])
     + G['ee12-e22-e-']*(KR1['ee11-22-ee-']-KR1_ms['ee11-22-ee-'])
     - 2*G['ee11-22-ee-']*(KR1['ee11-ee-']**2-KR1_ms['ee11-ee-']**2)
     - G['ee11-ee-']*(KR1['ee11-ee-']*KR1['ee12-e22-e-']-KR1_ms['ee11-ee-']*KR1_ms['ee12-e22-e-'])
     - G['ee11-ee-']*(KR1['ee11-22-ee-']*KR1['ee11-ee-']-KR1_ms['ee11-22-ee-']*KR1_ms['ee11-ee-'])
     )

G[gamma] = K(KR1[gamma]
     + 2*G['ee11-23-e33-e-']*(KR1['ee11-ee-'])
     + G['ee11-22-33-ee-']*(KR1['ee11-ee-'])
     + G['ee11-22-ee-']*(KR1['ee12-e22-e-'])
     + G['ee11-ee-']*(KR1['ee11-23-e33-e-'])
     + G['ee12-e22-e-']*(KR1['ee11-22-ee-'])
     - 2*G['ee11-22-ee-']*(KR1['ee11-ee-']**2)
     - G['ee11-ee-']*(KR1['ee11-ee-']*KR1['ee12-e22-e-'])
     - G['ee11-ee-']*(KR1['ee11-22-ee-']*KR1['ee11-ee-'])
     )

printKR1(gamma)


#4x 4loop 3
gamma='e112-e2-34-e44-e-'
KR1[gamma] = K(sympy.Number(1)/2/e*(0
    - 2*KR1['ee12-e22-e-']*f('ee12-e22-e-')
    - 2*KR1['ee11-23-e33-e-']*f('ee11-ee-')
    ))
KR1_ms[gamma] = K_ms(KR1[gamma]
    + 2*G['ee12-e22-e-']*(KR1['ee12-e22-e-']-KR1_ms['ee12-e22-e-'])
    + 2*G['ee11-23-e33-e-']*(KR1['ee11-ee-']-KR1_ms['ee11-ee-'])
    - 2*G['ee11-ee-']*(KR1['ee11-ee-']*KR1['ee12-e22-e-']-KR1_ms['ee11-ee-']*KR1_ms['ee12-e22-e-'])
    - G['ee11-22-ee-']*(KR1['ee11-ee-']**2-KR1_ms['ee11-ee-']**2)
    )

G[gamma] = K(KR1[gamma]
    + 2*G['ee12-e22-e-']*(KR1['ee12-e22-e-'])
    + 2*G['ee11-23-e33-e-']*(KR1['ee11-ee-'])
    - 2*G['ee11-ee-']*(KR1['ee11-ee-']*KR1['ee12-e22-e-'])
    - G['ee11-22-ee-']*(KR1['ee11-ee-']**2)
    )

printKR1(gamma)

#4x 4loop 4
gamma='ee11-23-e44-e44--'
KR1[gamma] = K(sympy.Number(1)/2/e*(0
    - KR1['ee12-e33-e33--']*f('ee11-ee-')
    - KR1['ee11-ee-']*f('ee12-e33-e33--')
    - 2*KR1['ee11-23-e33-e-']*f('ee11-ee-')
    ))
KR1_ms[gamma] = K_ms(KR1[gamma]
    + G['ee12-e33-e33--']*(KR1['ee11-ee-']-KR1_ms['ee11-ee-'])
    + G['ee11-ee-']*(KR1['ee12-e33-e33--']-KR1_ms['ee12-e33-e33--'])
    + 2*G['ee11-23-e33-e-']*(KR1['ee11-ee-']-KR1_ms['ee11-ee-'])
    + G['ee11-22-ee-']*(KR1['ee11-22-ee-']-KR1_ms['ee11-22-ee-'])
    - 2*G['ee12-e22-e-']*(KR1['ee11-ee-']**2-KR1_ms['ee11-ee-']**2)
    - G['ee11-ee-']*(KR1['ee11-ee-']*KR1['ee11-22-ee-']-KR1_ms['ee11-ee-']*KR1_ms['ee11-22-ee-'])
    )

G[gamma] = K(KR1[gamma]
    + G['ee12-e33-e33--']*(KR1['ee11-ee-'])
    + G['ee11-ee-']*(KR1['ee12-e33-e33--'])
    + 2*G['ee11-23-e33-e-']*(KR1['ee11-ee-'])
    + G['ee11-22-ee-']*(KR1['ee11-22-ee-'])
    - 2*G['ee12-e22-e-']*(KR1['ee11-ee-']**2)
    - G['ee11-ee-']*(KR1['ee11-ee-']*KR1['ee11-22-ee-'])
    )

printKR1(gamma)


G['ee11-22-ee-_1']=K(G['ee11-ee-']*G['ee11-ee-_1']) # K(G['ee11-22-ee-']-G['ee11-ee-']*G['ee11-ee-_1'])
G['ee11-22-ee-_1k']=K(G['ee11-ee-']*G['ee11-ee-_1k']) # K(G['ee11-22-ee-']-G['ee11-ee-']*G['ee11-ee-_1'])
KR1['ee11-22-ee-_1k']=K(G['ee11-22-ee-_1k']-G['ee11-ee-']*KR1['ee11-ee-_1k']-G['ee11-ee-_1k']*KR1['ee11-ee-'])

#4x 4loop 5
gamma='ee11-23-ee4-444--'
KR1[gamma] = K(sympy.Number(1)/2/e*(0
    - KR1['ee12-ee3-333--']*f('ee11-ee-')
    - KR1['ee11-ee-']*f('ee12-ee3-333--')
    - KR1['ee11-22-ee-_1k']*f('e111-e-')
    ))
KR1_ms[gamma] = K_ms(KR1[gamma]
    + G['ee12-ee3-333--']*(KR1['ee11-ee-']-KR1_ms['ee11-ee-'])
    + G['ee11-22-ee-_1k']*(KR1['e111-e-']-KR1_ms['e111-e-'])
    + G['ee11-ee-']*(KR1['ee12-ee3-333--']-KR1_ms['ee12-ee3-333--'])
    - G['ee11-ee-_1k']*(KR1['ee11-ee-']*KR1['e111-e-']-KR1_ms['ee11-ee-']*KR1_ms['e111-e-'])
    )

G[gamma] = K(KR1[gamma]
    + G['ee12-ee3-333--']*(KR1['ee11-ee-'])
    + G['ee11-22-ee-_1k']*(KR1['e111-e-'])
    + G['ee11-ee-']*(KR1['ee12-ee3-333--'])
    - G['ee11-ee-_1k']*(KR1['ee11-ee-']*KR1['e111-e-'])
    )

printKR1(gamma)

#4x 4loop 6
gamma='ee11-23-e34-44-e-'
KR1[gamma] = K(sympy.Number(1)/2/e*(0
    - KR1['ee12-e23-33-e-']*f('ee11-ee-')
    - KR1['ee11-23-e33-e-']*f('ee11-ee-')
    - KR1['ee11-22-ee-']*f('ee12-e22-e-')
    - KR1['ee11-ee-']*f('ee12-e23-33-e-')
    ))
KR1_ms[gamma] = K_ms(KR1[gamma]
    + G['ee12-e23-33-e-']*(KR1['ee11-ee-']-KR1_ms['ee11-ee-'])
    + G['ee11-23-e33-e-']*(KR1['ee11-ee-']-KR1_ms['ee11-ee-'])
    + G['ee11-22-ee-']*(KR1['ee12-e22-e-']-KR1_ms['ee12-e22-e-'])
    + G['ee11-ee-']*(KR1['ee12-e23-33-e-']-KR1_ms['ee12-e23-33-e-'])
    - G['ee12-e22-e-']*(KR1['ee11-ee-']**2-KR1_ms['ee11-ee-']**2)
    - G['ee11-ee-']*(KR1['ee11-ee-']*KR1['ee12-e22-e-']-KR1_ms['ee11-ee-']*KR1_ms['ee12-e22-e-'])
    )

G[gamma] = K(KR1[gamma]
    + G['ee12-e23-33-e-']*(KR1['ee11-ee-'])
    + G['ee11-23-e33-e-']*(KR1['ee11-ee-'])
    + G['ee11-22-ee-']*(KR1['ee12-e22-e-'])
    + G['ee11-ee-']*(KR1['ee12-e23-33-e-'])
    - G['ee12-e22-e-']*(KR1['ee11-ee-']**2)
    - G['ee11-ee-']*(KR1['ee11-ee-']*KR1['ee12-e22-e-'])
    )

printKR1(gamma)


#4x 4loop 7
gamma='ee11-23-334-4-ee-'
KR1[gamma] = K(sympy.Number(1)/2/e*(0
    - KR1['ee12-223-3-ee-']*f('ee11-ee-')
    - KR1['ee11-ee-']*f('ee12-223-3-ee-')
    - KR1['ee11-22-33-ee-']*f('ee11-ee-')
    - 2*KR1['ee11-22-ee-']*f('ee12-e22-e-')
    ))
KR1_ms[gamma] = K_ms(KR1[gamma]
    + G['ee12-223-3-ee-']*(KR1['ee11-ee-']-KR1_ms['ee11-ee-'])
    + G['ee11-ee-']*(KR1['ee12-223-3-ee-']-KR1_ms['ee12-223-3-ee-'])
    + G['ee11-22-33-ee-']*(KR1['ee11-ee-']-KR1_ms['ee11-ee-'])
    + 2*G['ee11-22-ee-']*(KR1['ee12-e22-e-']-KR1_ms['ee12-e22-e-'])
    + G['ee11-ee-']*(KR1['ee11-23-e33-e-']-KR1_ms['ee11-23-e33-e-'])
    - G['ee11-22-ee-']*(KR1['ee11-ee-']**2-KR1_ms['ee11-ee-']**2)
    - G['ee11-ee-']*(KR1['ee11-ee-']*KR1['ee12-e22-e-']-KR1_ms['ee11-ee-']*KR1_ms['ee12-e22-e-'])
    )

G[gamma] = K(KR1[gamma]
    + G['ee12-223-3-ee-']*(KR1['ee11-ee-'])
    + G['ee11-ee-']*(KR1['ee12-223-3-ee-'])
    + G['ee11-22-33-ee-']*(KR1['ee11-ee-'])
    + 2*G['ee11-22-ee-']*(KR1['ee12-e22-e-'])
    + G['ee11-ee-']*(KR1['ee11-23-e33-e-'])
    - G['ee11-22-ee-']*(KR1['ee11-ee-']**2)
    - G['ee11-ee-']*(KR1['ee11-ee-']*KR1['ee12-e22-e-'])
    )

printKR1(gamma)

#4x 4loop 8
gamma='ee12-233-34-4-ee-'
KR1[gamma] = K(sympy.Number(1)/2/e*(f(gamma)
    - KR1['ee12-223-3-ee-']*f('ee11-ee-')
    - KR1['ee11-22-ee-']*f('ee12-e22-e-')
    - 2*KR1['ee11-ee-']*f('ee12-e23-33-e-')
    ))
KR1_ms[gamma] = K_ms(KR1[gamma]
    + G['ee12-223-3-ee-']*(KR1['ee11-ee-']-KR1_ms['ee11-ee-'])
    + G['ee11-22-ee-']*(KR1['ee12-e22-e-']-KR1_ms['ee12-e22-e-'])
    + 2*G['ee11-ee-']*(KR1['ee12-e23-33-e-']-KR1_ms['ee12-e23-33-e-'])
    )

G[gamma] = K(KR1[gamma]
    + G['ee12-223-3-ee-']*(KR1['ee11-ee-'])
    + G['ee11-22-ee-']*(KR1['ee12-e22-e-'])
    + 2*G['ee11-ee-']*(KR1['ee12-e23-33-e-'])
    )

printKR1(gamma)
print "   ", (11./6-zeta(3))/16

#4x 4loop 9
gamma='ee12-223-4-e44-e-'
KR1[gamma] = K(sympy.Number(1)/2/e*(f(gamma)
    - KR1['ee12-223-3-ee-']*f('ee11-ee-')
    - KR1['ee11-23-e33-e-']*f('ee11-ee-')
    - KR1['ee12-e22-e-']*f('ee12-e22-e-')
    - KR1['ee11-ee-']*f('e112-e3-e33-e-')
    ))
KR1_ms[gamma] = K_ms(KR1[gamma]
    + G['ee12-223-3-ee-']*(KR1['ee11-ee-']-KR1_ms['ee11-ee-'])
    + G['ee11-23-e33-e-']*(KR1['ee11-ee-']-KR1_ms['ee11-ee-'])
    + G['ee12-e22-e-']*(KR1['ee12-e22-e-']-KR1_ms['ee12-e22-e-'])
    + G['ee11-ee-']*(KR1['e112-e3-e33-e-']-KR1_ms['e112-e3-e33-e-'])
    - G['ee11-22-ee-']*(KR1['ee11-ee-']**2-KR1_ms['ee11-ee-']**2)
    - G['ee11-ee-']*(KR1['ee11-ee-']*KR1['ee12-e22-e-']-KR1_ms['ee11-ee-']*KR1_ms['ee12-e22-e-'])
    )

G[gamma] = K(KR1[gamma]
    + G['ee12-223-3-ee-']*(KR1['ee11-ee-'])
    + G['ee11-23-e33-e-']*(KR1['ee11-ee-'])
    + G['ee12-e22-e-']*(KR1['ee12-e22-e-'])
    + G['ee11-ee-']*(KR1['e112-e3-e33-e-'])
    - G['ee11-22-ee-']*(KR1['ee11-ee-']**2)
    - G['ee11-ee-']*(KR1['ee11-ee-']*KR1['ee12-e22-e-'])
    )
printKR1(gamma)
print "   ", -1/32.

#4x 4loop 10
gamma='e123-e24-34-e4-e-'
KR1[gamma] = K(sympy.Number(1)/2/e*(f(gamma) ))
KR1_ms[gamma] = K_ms(KR1[gamma])

G[gamma] = K(KR1[gamma])
printKR1(gamma)
print "   ", 10*zeta(5)/16

#4x 4loop 11
gamma='e112-34-e34-e4-e-'
KR1[gamma] = K(sympy.Number(1)/2/e*(f(gamma)
    - KR1['e123-e23-e3-e-']*f('ee11-ee-')
    ))
KR1_ms[gamma] = K_ms(KR1[gamma]
    + G['e123-e23-e3-e-']*(KR1['ee11-ee-']-KR1_ms['ee11-ee-'])
    )

G[gamma] = K(KR1[gamma]
    + G['e123-e23-e3-e-']*(KR1['ee11-ee-'])
    )
printKR1(gamma)
print "   ", (3*zeta(3)-1.5*zeta(4))/16, -2*zeta(3)/16

#4x 4loop 12
gamma='e112-e3-e34-44-e-'
KR1[gamma] = K(sympy.Number(1)/2/e*(f(gamma)
    - KR1['ee12-e23-33-e-']*f('ee11-ee-')
    - KR1['e112-e3-e33-e-']*f('ee11-ee-')
    - KR1['ee12-e22-e-']*f('ee12-e22-e-')
    ))
KR1_ms[gamma] = K_ms(KR1[gamma]
    + G['ee12-e23-33-e-']*(KR1['ee11-ee-']-KR1_ms['ee11-ee-'])
    + G['e112-e3-e33-e-']*(KR1['ee11-ee-']-KR1_ms['ee11-ee-'])
    + G['ee12-e22-e-']*(KR1['ee12-e22-e-']-KR1_ms['ee12-e22-e-'])
    - G['ee12-e22-e-']*(KR1['ee11-ee-']**2-KR1_ms['ee11-ee-']**2)
    - G['ee11-ee-']*(KR1['ee11-ee-']*KR1['ee12-e22-e-']-KR1_ms['ee11-ee-']*KR1_ms['ee12-e22-e-'])
    )

G[gamma] = K(KR1[gamma]
    + G['ee12-e23-33-e-']*(KR1['ee11-ee-'])
    + G['e112-e3-e33-e-']*(KR1['ee11-ee-'])
    + G['ee12-e22-e-']*(KR1['ee12-e22-e-'])
    - G['ee12-e22-e-']*(KR1['ee11-ee-']**2)
    - G['ee11-ee-']*(KR1['ee11-ee-']*KR1['ee12-e22-e-'])
    )
printKR1(gamma)
print "   ", -(2/3.)/16


#4x 4loop 13
gamma='e112-e3-e44-e44--'
KR1[gamma] = K(sympy.Number(1)/2/e*(f(gamma)
    - KR1['ee12-e33-e33--']*f('ee11-ee-')
    - 2*KR1['e112-e3-e33-e-']*f('ee11-ee-')
    ))
KR1_ms[gamma] = K_ms(KR1[gamma]
    + G['ee12-e33-e33--']*(KR1['ee11-ee-']-KR1_ms['ee11-ee-'])
    + 2*G['e112-e3-e33-e-']*(KR1['ee11-ee-']-KR1_ms['ee11-ee-'])
    + G['ee12-e22-e-']*(KR1['ee11-22-ee-']-KR1_ms['ee11-22-ee-'])
    - 2*G['ee12-e22-e-']*(KR1['ee11-ee-']**2-KR1_ms['ee11-ee-']**2)
    - G['ee11-ee-']*(KR1['ee11-ee-']*KR1['ee11-22-ee-']-KR1_ms['ee11-ee-']*KR1_ms['ee11-22-ee-'])
    )

G[gamma] = K(KR1[gamma]
    + G['ee12-e33-e33--']*(KR1['ee11-ee-'])
    + 2*G['e112-e3-e33-e-']*(KR1['ee11-ee-'])
    + G['ee12-e22-e-']*(KR1['ee11-22-ee-'])
    - 2*G['ee12-e22-e-']*(KR1['ee11-ee-']**2)
    - G['ee11-ee-']*(KR1['ee11-ee-']*KR1['ee11-22-ee-'])
    )
printKR1(gamma)
print "   ", (0.5-zeta(3))/16

#4x 4loop 14
gamma='ee12-334-334--ee-'
KR1[gamma] = K(sympy.Number(1)/2/e*(f(gamma)
    - 2*KR1['ee12-223-3-ee-']*f('ee11-ee-')
    - 2*KR1['ee11-ee-']*f('ee12-e33-e33--')
    ))
KR1_ms[gamma] = K_ms(KR1[gamma]
    + 2*G['ee12-223-3-ee-']*(KR1['ee11-ee-']-KR1_ms['ee11-ee-'])
    + 2*G['ee11-ee-']*(KR1['ee12-e33-e33--']-KR1_ms['ee12-e33-e33--'])
    + G['ee11-22-ee-']*(KR1['ee11-22-ee-']-KR1_ms['ee11-22-ee-'])
    )

G[gamma] = K(KR1[gamma]
    + 2*G['ee12-223-3-ee-']*(KR1['ee11-ee-'])
    + 2*G['ee11-ee-']*(KR1['ee12-e33-e33--'])
    + G['ee11-22-ee-']*(KR1['ee11-22-ee-'])
    )
printKR1(gamma)
print "   ", -(2-2*zeta(3))/16