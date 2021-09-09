import re


def standard_deviation(srednja_vrijednost, duzina, podaci_i):
    suma = 0
    for n in range(duzina):
        suma = (podaci_i[n] - srednja_vrijednost)**2

    st_dev = (suma/(duzina-1))**(1/2)

    return st_dev


num_robots = input('Unesite broj robota (od 2 do 6):\n')
difficulty = input('Odaberite težinu prepreke (0 - easy, 1 - medium, 2 - hard):\n')
type_obs = input('Odaberite tip prepreke (1 - standardizovana, 2 - kombinirana):\n')

num_robots_words = ['dva', 'tri', 'četiri', 'pet', 'šest']
difficulty_words = ['easy', 'medium', 'hard']

if type_obs == '1':
    doku = open('standardne devijacije_standard' + num_robots + '_' + difficulty + '.txt', 'w')
    f = open('podaci' + str(num_robots) + '_' + str(difficulty) + '.txt', 'r')
    temp = []
    podaci = []
    devs = []
    it = 0

    for line in f:
        if 'Vrijeme izvršavanja: ' in line:
            num = re.findall('[0-9]+.', line)
            minute = float(num[1][1])*60
            num = float(num[2] + num[3]) + minute
            podaci.append(num)


    sr_vr = sum(podaci)/len(podaci)
    dev = standard_deviation(sr_vr, len(podaci), podaci)
    devs.append(dev)
    s_d_scientific_notation = "{:.2e}".format(dev)
    sr_vr_scientific_notation = "{:.2e}".format(sr_vr)

    doku.write('srednja vrijednost = ' + str(sr_vr_scientific_notation) + ', standardna devijacija = ' + str(s_d_scientific_notation) + '\n')


    it = it + 1


else:
    doku = open('standardne devijacije' + num_robots + '_' + difficulty + '.txt', 'w')

    doku.write('\\begin{table}[H]\n')
    doku.write('\\captionof{table}{Vremena izračunavanja puta za sistem od ' + num_robots_words[int(num_robots)-2] + ' robota na \\textit{' + difficulty_words[int(difficulty)] + '} terenu}\n')
    doku.write('\\label{tab:tabela' + num_robots + difficulty +'}\n')
    doku.write("\\begin{tabular}{@{}|l|l|l|l|@{}}\n")
    doku.write('\\toprule\n')
    doku.write('\\hline\n')
    doku.write(' & \\multicolumn{3}{c|}{[s]} \\\ \n')
    doku.write('\\hline\n')
    doku.write('  & \\thead{seed=2} & \\thead{seed=6} & \\thead{seed=8} \\\ \n')
    doku.write('\\hline\n')


    for num_randoms in range(40, 201, 40):

        if num_randoms == 120:
            continue

        doku.write(str(num_randoms) + ' prepreka' + ' & ')
        devs = []
        it = 0

        num_seeds = [2, 6, 8]

        for num_seed in num_seeds:

            try:

                f = open('podaci' + str(num_robots) + '_' + str(difficulty) + '_' + str(num_seed) + '_' +
                         str(num_randoms) + '.txt', 'r')

                podaci = []

                for line in f:
                    if 'Vrijeme izvršavanja: ' in line:
                        num = re.findall('[0-9]+.', line)
                        minute = float(num[1][1])*60
                        num = float(num[2] + num[3]) + minute
                        podaci.append(num)


                if len(podaci) != 0:

                    sr_vr = sum(podaci)/len(podaci)
                    dev = standard_deviation(sr_vr, len(podaci), podaci)
                    devs.append(dev)
                    s_d_scientific_notation = "{:.2e}".format(dev)
                    sr_vr_scientific_notation = "{:.2e}".format(sr_vr)

                    doku.write('\\makecell{sr. vr. = ' + str(sr_vr_scientific_notation) +
                               ', \\\  s. d. = ' + str(s_d_scientific_notation) + '}')

                    if num_seed != 8:
                        doku.write(' & ')

                else:

                    doku.write('/' + ' & ')

                it = it + 1

            except:

                continue

            f.close()

        doku.write(' \\\ \n')
        doku.write('\\hline\n')

    doku.write('\\end{tabular}\n')
    doku.write('\\end{table}\n')
doku.close()
