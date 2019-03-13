from flask  import Flask, jsonify, request, json
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from models import Users, Quizzes, Questions, OptionList, Game, Leaderboard
from random import randint

app = Flask (__name__)

POSTGRES = {
        'user': 'postgres',
        'pw': 'fasyaemad03',
        'db': 'kahoot_database',
        'host': 'localhost',
        'port': '5432'
}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# postgresql://username:password@localhost:5432/database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

db.init_app(app)


# USER=============================================================

@app.route('/')
def home():
    return 'hellow brother and sister'
    
@app.route('/getAllUsers', methods=["GET"])
def get_all_users():
        try:
                users = Users.query.order_by(Users.user_id).all()
                return jsonify([usr.serialize() 
                for usr in users])
        except Exception as e:
                return (str(e))
@app.route('/getUserBy/<userId_>', methods=["GET"])
def get_user_by(userId_):
        try:
                users = Users.query.filter_by(user_id = userId_).first()
                return jsonify(users.serialize())
        except Exception as e:
                return (str(e))


@app.route('/addUser', methods=["POST"])
def add_customer():

    username=request.args.get('username')
    password=request.args.get('password')
    email=request.args.get('email')

    try:
        users=Users(
            username=username,
            password=password,
            email=email
        )

        db.session.add(users)
        db.session.commit()
        return "User added. users id={}".format(users.user_id)

    except Exception as e:
        return(str(e))

@app.route('/deleteUser/<userId_>', methods=["DELETE"])
def delete_model(userId_):
    try:
        users =  Users.query.filter_by(user_id=userId_).first()
        db.session.delete(users)
        db.session.commit()
        return 'user deleted'
    except Exception as e:
        return(str(e))

@app.route('/updateUser/<userId_>', methods=["PUT"])
def update_user(userId_):
        user_existing = get_user_by(userId_).json
        username = request.args.get('username')
        password = request.args.get('password')
        email = request.args.get('email')
        if request.args.get('username') == None:
                username = user_existing['username']
        if request.args.get('password') == None:
                password = user_existing['password']
        if request.args.get('email') == None:
                email = user_existing['email']
        try:
                userUpdate = {
                'username' : username,
                'password' : password,
                'email' : email
                }
                users = Users.query.filter_by(user_id=userId_).update(userUpdate)
                db.session.commit()
                return 'update user'
        except Exception as e:
                return(str(e))
# ================================================================

# Quizzes ========================================================
@app.route('/getAllQuizzes', methods=["GET"])
def get_all_quizzes():
        try:
                quizzes = Quizzes.query.order_by(Quizzes.quiz_id).all()
                return jsonify([qzs.serialize() for qzs in quizzes])
        except Exception as e:
                return str(e) 
@app.route('/getQuizBy/<quizId_>', methods=["GET"])
def get_quiz_by(quizId_):
        try:
                quizzes = Quizzes.query.filter_by(quiz_id=quizId_).first()
                return jsonify(quizzes.serialize())
        except Exception as e:
                return str(e)

@app.route('/addQuiz', methods=["POST"])
def add_quiz():
        # quiz_id = request.args.get('quiz_id')
        creator_id = request.args.get('creator_id')
        quiz_name = request.args.get('quiz_name')
        quiz_category = request.args.get('quiz_category')

        try:
                quizzes = Quizzes(
                        # quiz_id = quiz_id,
                        creator_id = creator_id,
                        quiz_name = quiz_name,
                        quiz_category = quiz_category
                )
        except Exception as e:
                return str(e)
        db.session.add(quizzes)
        db.session.commit()
        return "Quiz Added. quiz id={}".format(quizzes.quiz_id)

@app.route('/updateQuiz/<quizId_>', methods=["PUT"])
def update_quiz(quizId_):
        quiz_existing = get_quiz_by(quizId_).json

        if request.args.get('creator_id') == None:
                creator_id = quiz_existing['creator_id']
        else:
                creator_id = request.args.get('creator_id')
        if request.args.get('quiz_name') == None:
                quiz_name = quiz_existing['quiz_name']
        else:
                quiz_name = request.args.get('quiz_name')
        if request.args.get('quiz_category') == None:
                quiz_category = quiz_existing['quiz_category']
        else:
                quiz_category = request.args.get('quiz_category')
        
        try:
                updateQuiz = {
                        'creator_id' : creator_id,
                        'quiz_name' : quiz_name,
                        'quiz_category' : quiz_category
                }
                quizzes = Quizzes.query.filter_by(quiz_id=quizId_).update(updateQuiz)
                db.session.commit()
                return "update quiz"
        except Exception as e:
                return str(e)

@app.route('/deleteQuiz/<quizId_>', methods=["DELETE"])
def delete_quiz(quizId_):
        try:
                quizzes = Quizzes.query.filter_by(quiz_id=quizId_).first()
                db.session.delete(quizzes)
                db.session.commit()
                return "id_quiz "+str(quizId_)+" deleted "
        except Exception as e:
                return str(e)
# ===========================================================

# Questions =================================================
@app.route('/getAllQuestion', methods=["GET"])
def get_all_question():
        try:
                questions = Questions.query.order_by(Questions.question_id).all()
                return jsonify([qstn.serialize() for qstn in questions])
        except Exception as e:
                return (str(e))

@app.route('/getQuestionBy/<quesId_>', methods=["GET"])
def get_question_by(quesId_):
        try:
                questions = Questions.query.filter_by(question_id = quesId_).first()
                return jsonify(questions.serialize())
        except Exception as e:
                return (str(e))

@app.route('/addQuestion', methods=["POST"])
def add_question():
        question_id = request.args.get('question_id')
        quiz_id = request.args.get('quiz_id')
        question_number = request.args.get('question_number')
        question = request.args.get('question')
        answer = request.args.get('answer')

        try:
                questions = Questions(
                        question_id = question_id,
                        quiz_id = quiz_id,
                        question_number = question_number,
                        question = question,
                        answer = answer
                )
        except Exception as e:
                return str(e)
        
        db.session.add(questions)
        db.session.commit()
        return "questio added. question id={}".format(questions.question_id)

@app.route('/deleteQuestion/<quesId_>', methods=["DELETE"])
def delete_question(quesId_):
        try:
                questions = Questions.query.filter_by(question_id=quesId_).first()
                db.session.delete(questions)
                db.session.commit()
                return "delete question"
        except Exception as e:
                return str(e)

@app.route('/updateQuestion/<quesId_>', methods=["PUT"])
def update_Question(quesId_):
        question_existing = get_question_by(quesId_).json

        if request.args.get('quiz_id') == None:
                quiz_id = question_existing['quiz_id']
        else:
                quiz_id = request.args.get('quiz_id')
        if request.args.get('question_id') == None:
                question_id = question_existing['question_id']
        else:
                question_id = request.args.get('question_id')
        if request.args.get('question_number') == None:
                question_number = question_existing['question_number']
        else:
                question_number = request.args.get('question_number')
        if request.args.get('question') == None:
                question = question_existing['question']
        else:
                question = request.args.get('question')
        if request.args.get('answer') == None:
                answer = question_existing['answer']
        else:
                answer = request.args.get('answer')
        
        try:
                questionUpdate = {
                        'quiz_id' : quiz_id,
                        'question_id' : question_id,
                        'question_number' : question_number,
                        'question' : question,
                        'answer' : answer
                }
                questions = Questions.query.filter_by(question_id=quesId_).update(questionUpdate)
                db.session.commit()
                return "update question"
        except Exception as e:
                return str(e)
# ===========================================================

#  Option List ==============================================
@app.route('/getAllOption', methods=["GET"])
def get_all_option():
        try:
                option_list = OptionList.query.order_by(OptionList.option_id).all()
                return jsonify([opl.serialize() for opl in option_list])
        except Exception as e:
                return str(e)

@app.route('/getOptionBy/<opsId_>', methods=["GET"])
def get_option_by(opsId_):
        try:
                option_list = OptionList.query.filter_by(option_id=opsId_).first()
                return jsonify(option_list.serialize())
        except Exception as e:
                return str(e)

@app.route('/addOption', methods=["POST"])
def add_option():
        question_id = request.args.get('question_id')
        option_id = request.args.get('question_id')
        a = request.args.get('a')
        b = request.args.get('b')
        c = request.args.get('c')
        d = request.args.get('d')

        try:
                option_list = OptionList(
                        question_id = question_id,
                        option_id = option_id,
                        a = a,
                        b = b,
                        c = c,
                        d = d
                )
                db.session.add(option_list)
                db.session.commit()
                return "optionn list added. option id={}".format(OptionList.option_id)
        except Exception as e:
                return str(e)


@app.route('/deleteOption/<quesId_>',methods=["DELETE"])
def delete_option(quesId_):
        try:
                option_list = OptionList.query.filter_by(option_id=quesId_).first()
                db.session.delete(option_list)
                db.session.commit()
                return "option delete"
        except Exception as e:
                return str(e)

@app.route('/updateOption/<opsId_>', methods=["PUT"])
def update_option(opsId_):
        option_existing = get_option_by(opsId_).json

        if request.args.get('question_id') == None:
                question_id = option_existing['question_id']
        else:
                question_id = request.args.get('question_id')
        if request.args.get('option_id') == None:
                option_id = option_existing['option_id']
        else:
                option_id = request.args.get('option_id')
        if request.args.get('a') == None:
                a = option_existing['a']
        else:
                a = request.args.get('a')
        if request.args.get('b') == None:
                b = option_existing['b']
        else:
                b = request.args.get('b')
        if request.args.get('c') == None:
                c = option_existing['c']
        else:
                c = request.args.get('c')
        if request.args.get('d') == None:
                d = option_existing['d']
        else:
                d = request.args.get('d')
        
        try:
                updateOption = {
                        'question_id' : question_id,
                        'option_id' : option_id,
                        'a' : a,
                        'b' : b,
                        'c' : c,
                        'd' : d
                }
                option_list = OptionList.query.filter_by(option_id=opsId_).update(updateOption)
                db.session.commit()
                return "update option"
        except Exception as e:
                return str(e)
#  ==========================================================

# Game =====================================================
@app.route('/getAllGame', methods=["GET"])
def get_all_game():
        try:
                game = Game.query.order_by(Game.game_pin).all()
                return jsonify([gem.serialize() for gem in game])
        except Exception as e:
                return str(e)

@app.route('/getGameBy/<gemPin_>', methods=["GET"])
def get_game_by(gemPin_):
        try:
                game = Game.query.filter_by(game_pin=gemPin_).first()
                return jsonify(game.serialize())
        except Exception as e:
                 return str(e)

@app.route('/createGame', methods=["POST"])
def create_game():

        game_pin = randint(90000,100000)
        quiz_id = request.args.get('quiz_id')

        try:
                game = Game(
                        game_pin = game_pin,
                        quiz_id = quiz_id
                )
                db.session.add(game)
                db.session.commit()
                return "Game created. game pin = {}".format(game.game_pin)
        except Exception as e:
                return str(e)
@app.route('/deleteGame/<gemPin_>', methods=["DELETE"])
def deleteGame(gemPin_):
        try:
                game = Game.query.filter_by(game_pin=gemPin_).all()
                for dele in game:
                        db.session.delete(dele)
                        db.session.commit()
                        return "game deleted"
        except Exception as e:
                return (str(e))

#  Leaderboard ================================================================
@app.route('/getAllLeaderboard', methods=["GET"])
def get_all_leaderboard():
        try:
                leaderboard = Leaderboard.query.order_by(Leaderboard.player_name).all()
                return jsonify([pnam.serialize() for pnam in leaderboard])
        except Exception as e:
                return (str(e))

@app.route('/getLeaderboardBy/<gemPin_>', methods=["GET"])
def get_leaderboard_by(gemPin_):
        try:
                leaderboard = Leaderboard.query.filter_by(game_pin = gemPin_).all()
                return jsonify([ldb.serialize() for ldb in leaderboard])
        except Exception as e:
                return str(e)

@app.route('/joinGame', methods=["POST"])
def join_game():

        game_pin = request.args.get('game_pin')
        score = 0
        player_name = request.args.get('player_name')

        try:
                leaderboard = Leaderboard(
                        game_pin = game_pin,
                        score = score,
                        player_name = player_name
                )
                db.session.add(leaderboard)
                db.session.commit()
                return "Join to Game. player name = {}".format(leaderboard.player_name)
        except Exception as e:
                return str(e)

@app.route('/deletePlayerBy/<penem_>', methods=["DELETE"])
def delete_player_By(penem_):
        try:
                leaderboard = Leaderboard.query.filter_by(player_name=penem_).first()
                db.session.delete(leaderboard)
                db.session.commit()
                return "delete player. player name = {}".format(leaderboard.player_name)
        except Exception as e:
                return str(e)

@app.route('/answerQuestion', methods=["POST"])
def answer_question():
        
        gemPin_ = request.args.get('gemPin_')
        game  = get_game_by(gemPin_).json

        pName_ = request.args.get('pName_')
        answer_ = request.args.get('answer_')
        quesId_ = request.args.get('quesId_')
        question = get_question_by(quesId_).json
        thisLeaderboard = get_leaderboard_by(gemPin_).json
        score = 0
        for i in thisLeaderboard:
                if i['player_name'] == pName_:
                        score = i['score']
                        break


        # print('can asup')
        # score = thisLeaderboard[0]['score']
        # print('asup')
        if question['answer'] == answer_ :
                score += 100
                print('asup')

        try:
                updateScore = {
                        'game_pin' : gemPin_,
                        'player_name' : pName_, 
                        'score' : score
                }
                db.session.query(Leaderboard).filter_by(player_name=pName_, game_pin=gemPin_).update(updateScore)
                db.session.commit()
                return "update score"
        except Exception as e:
                return str(e)                









if __name__=='__main__':
        app.run()

