def generate(criteria):
    try:
        import sqlite3
        # TO INSTALL : pip install binpacking
        # pip install latex
        import binpacking
        import random
        from latex import build_pdf

        db = sqlite3.connect(':memory:')
        db = sqlite3.connect('math_alevel_2019.db')
        #db = sqlite3.connect('E:/Dropbox/math_alevel.db')
        cursor = db.cursor()

        #criteria = input("Please input your desired topic or skills, separated by commas e.g Differentiation, 1.2.1 \n\n")
        criteria = criteria.split(",")

        sql_statement = '''SELECT question, mark, skill, type, year, paper, question_no
                        FROM questions_only_wip 
                        WHERE question IN (SELECT question FROM questions_only_wip ORDER BY RANDOM() LIMIT 100) 
                        '''
        sql_statement = sql_statement+'AND skill LIKE "%'+criteria[0]+'%"\n'

        if criteria[1:] != []:
            for x in criteria[1:]:
                sql_statement = sql_statement+'OR skill LIKE "%' + x + '%"\n'
        # skill=[]
        # for c in criteria:

        #'''SELECT question, mark FROM table WHERE id IN (SELECT id FROM questions_only_wip ORDER BY RANDOM() LIMIT 50)'''
        #'''SELECT question, mark FROM questions_only_wip'''
        # cursor.execute('''SELECT question, mark
        #                  FROM questions_only_wip
        #                  WHERE question
        #                  IN (SELECT question FROM questions_only_wip ORDER BY RANDOM() LIMIT 50)''')
        #                   WHERE topic LIKE "%DIFFERENTIATION%" ''')
        cursor.execute(sql_statement)

        # cursor.execute('''SELECT question
        #                   FROM ALVL_Math_Question_Bank
        #                   WHERE mark BETWEEN 10 AND 20
        #                   ''')
        questions = cursor.fetchall()

        questionpack = binpacking.to_constant_volume(
            questions, 20, weight_pos=1, lower_bound=None, upper_bound=None)
        with open("assets/latex_preamble.txt", "r") as inF:
            lines = inF.readlines()
        with open("assets/latex_recommender.txt", "w") as outF:
            outF.writelines(lines)

            #outF = open("E:/Dropbox/myOutFile.txt", "w")
            # for p in questions:# write line to output file
            #    currentQ = p[0].split("\n")
            #    finalQ = ""
            #    for i in range(len(currentQ)):
            #        if currentQ[i].strip() != "":
            #            finalQ += currentQ[i]
            #    outF.write(finalQ + "\n\n")

            # write line to output file
            for p in questionpack[random.randint(0, len(questionpack)-1)]:
                currentQ = p[0].split("\n")
                finalQ = ""
                for i in range(len(currentQ)):
                    if currentQ[i].strip() != "":
                        finalQ += currentQ[i]
                outF.write(finalQ + "\n\n" + " \hfill{} " +
                           "["+str(p[3])+"/"+str(p[4])+"/"+str(p[5])+"/"+str(p[5]) + "]\n\n")

            outF.write("\end{enumerate} \end{document}")
        db.close()
        with open("assets/latex_recommender.txt", "r") as f:
            pdf = build_pdf(f.read())
            path = "static/qn.pdf"
            pdf.save_to(path)
            return path
    except Exception as e:
        return "Error: " + str(e)
