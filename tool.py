ls = [[0.4999385961460835, 0.501831182730999, 0.503636411337999, 0.5053530125010803, 0.5069801644906374, 0.5085170967624943, 0.5104714061301501, 0.5123396599589868, 0.514015187112349, 0.5155998313215618, 0.5176067200762023, 0.5195280052898257, 0.5212559335481683, 0.5228914884277122, 0.5249543608520537, 0.5269327173704166, 0.528820507180683, 0.5304060223035182, 0.5325286520645748, 0.5345679574297688, 0.536516207257781, 0.5381589311531879, 0.540345519137589, 0.542450093508988, 0.5444631958209812, 0.546167503646413, 0.5484227479660428], [1.49945005279221, 1.5011659699850073, 1.5028889609145506, 1.5046185549170887, 1.5063542459643202, 1.5080954910527702, 1.5098417085160987, 1.5115435869859815, 1.5133488613892558, 1.5151589533968708, 1.516973140106776, 1.5187906508887508, 1.5205322796739893, 1.5224141039660133, 1.5242986428320289, 1.5261849473687226, 1.5280720093711626, 1.5298963596493966, 1.5318518852662026, 1.5338069655394337, 1.5357603659444448, 1.5376357476508227, 1.5396606891398152, 1.5416821713705962, 1.5436986855241315, 1.5456551774292226, 1.5477451801288105]]
ls2 = [[0.4999385961460809, 0.5018311827309654, 0.5036364113379905, 0.5053530125010605, 0.5069801644906423, 0.5085170967624819], [1.4994500527922054, 1.5011659699849673, 1.5028889609145086, 1.5046185549170614, 1.5063542459643164, 1.508095491052747]]
ls3 = [[0.998741803869349, 0.9992302231519798, 1.0002365639824067, 0.44453909406171827, 0.40288050322746227, 0.36798538963577815, 0.33836831791795136, 0.31277394767133465, 0.29000341339317603, 0.27011233398514267, 0.2520468415333311, 0.23564360129033507, 0.2209640681531398, 0.20749149530176994, 0.19513261479232644, 0.18375071325065195, 0.1731866649572932, 0.16354888668368783, 0.15452335007698037, 0.14597346551619164, 0.13814565724272476, 0.13077757649068913, 0.12376092659520004, 0.11737239039289105, 0.11118044502312477, 0.10550039355887936, 0.09998126013899353, 0.09494451785717997, 0.09001983477646815, 0.08550260600821676, 0.08117595567450918, 0.07699495263779903, 0.07314901660392895, 0.06945782698650012, 0.06592513987535957, 0.0625516394144225, 0.059408986034165424, 0.05639484463708502, 0.053504012942138766, 0.050731646991721904, 0.048127321983795164, 0.04566680238221931, 0.043302550362409674, 0.04104042666110625, 0.03887433956249241, 0.03681657684279644, 0.03483166184219697, 0.03295920449153577, 0.031173858613039077, 0.02946791623138055, 0.027839567453043158, 0.02630077433990301, 0.024816304882520693], [6.380078586553672e-29, 1.0511302228016324e-50, 4.870157864661846e-58, 2.775315344245539, 2.6693145432282703, 2.5786188056223076, 2.4993425194724104, 2.428751780307531, 2.3651113561259987, 2.3071954529777026, 2.25382790634491, 2.204695061050728, 2.159328679100192, 2.1166761220589763, 2.076888183874833, 2.0395441404551256, 2.0041081420865923, 1.9706381936622397, 1.9389429456598104, 1.9085661203922517, 1.8795876049174733, 1.8520224790524353, 1.8258008969471367, 1.8007915389340265, 1.776819122590895, 1.7533963429825052, 1.7308436668814902, 1.709794965981298, 1.6890441017607347, 1.669046950425504, 1.6492850222354265, 1.6307846844682679, 1.612861247925818, 1.5950789209689729, 1.577763575841066, 1.5617287115674503, 1.5455887035717228, 1.5299329027661563, 1.514758006859606, 1.500049307433443, 1.4857826458632672, 1.4719260633253142, 1.4584411950232967, 1.444751097754535, 1.4320824069777764, 1.4190218085232198, 1.4070929372479326, 1.3947055852251637, 1.3833995082415698, 1.3716794305748472, 1.3602001336884133, 1.3497551974129391, 1.3388955504244686]]

print('1-(A_R/A_I)^2, (A_T/A_I)^2')
for i in range(len(ls3[0])):
    print(str(1-ls3[0][i]) + ', ' + str(ls3[1][i]))