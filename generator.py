def generate(criteria, database_location, path_folder):
    import sqlite3
    import binpacking
    import random
    from latex import build_pdf
    import hashlib
    import time

    db = sqlite3.connect(database_location)

    cursor = db.cursor()

    criteria = criteria.split(",")
    sql_statement = '''
                    SELECT question, mark, skill, type, year, paper, question_no
                    FROM questions_only_wip 
                    WHERE question IN (SELECT question FROM questions_only_wip ORDER BY RANDOM() LIMIT 100)
                    AND skill LIKE "%" ||?|| "%" 
                    '''
    if criteria[1:] != []:
        for x in criteria[1:]:
            sql_statement = sql_statement + 'OR skill LIKE "%" ||?|| "%"'

    cursor.execute(sql_statement, criteria)

    questions = cursor.fetchall()

    questionpack = binpacking.to_constant_volume(
        questions, 20, weight_pos=1, lower_bound=None, upper_bound=None)
    with open("assets/latex_preamble.txt", "r") as inF:
        lines = inF.readlines()
    # Implement direct latex parsing
    latex_code = ""
    latex_code += ''.join(lines)
    for p in questionpack[random.randint(0, len(questionpack)-1)]:
        currentQ = p[0].split("\n")
        finalQ = ""
        for i in range(len(currentQ)):
            if currentQ[i].strip() != "":
                finalQ += currentQ[i]
        latex_code += finalQ + "\n\n" + " \hfill{} " + \
            "["+str(p[3])+"/"+str(p[4])+"/" + \
            str(p[5])+"/"+str(p[5]) + "]\n\n"
    latex_code += "\end{enumerate} \end{document}"
    db.close()
    pdf = build_pdf(latex_code)
    saved_path = f"{path_folder}/{hash(pdf)}.{time.time_ns()}.pdf"
    pdf.save_to(saved_path)
    return saved_path
