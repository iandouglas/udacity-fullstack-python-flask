from sqlalchemy import MetaData, ForeignKeyConstraint, Table
from sqlalchemy.engine import reflection
from sqlalchemy.sql.ddl import DropConstraint, DropTable
from flaskr.models import Question, Category


def db_drop_everything(db):
    # source: https://www.mbeckler.org/blog/?p=218
    # From http://www.sqlalchemy.org/trac/wiki/UsageRecipes/DropEverything

    conn = db.engine.connect()
    trans = conn.begin()
    inspector = reflection.Inspector.from_engine(db.engine)
    metadata = MetaData()
    tbs = []
    all_fks = []

    for table_name in inspector.get_table_names():
        fks = []
        for fk in inspector.get_foreign_keys(table_name):
            if not fk['name']:
                continue
            fks.append(
                ForeignKeyConstraint((), (), name=fk['name'])
            )
        t = Table(table_name, metadata, *fks)
        tbs.append(t)
        all_fks.extend(fks)
    for fkc in all_fks:
        conn.execute(DropConstraint(fkc))
    for table in tbs:
        conn.execute(DropTable(table))
    trans.commit()


def seed_data(db):
    cat_1 = Category(id=1, type='Science')
    db.session.add(cat_1)
    cat_2 = Category(id=2, type='Art')
    db.session.add(cat_2)
    cat_3 = Category(id=3, type='Geography')
    db.session.add(cat_3)
    cat_4 = Category(id=4, type='History')
    db.session.add(cat_4)
    cat_5 = Category(id=5, type='Entertainment')
    db.session.add(cat_5)
    cat_6 = Category(id=6, type='Sports')
    db.session.add(cat_6)
    db.session.execute("SELECT pg_catalog.setval('public.categories_id_seq', 6, true);")
    db.session.commit()

    q_2 = Question(id=2, question="What movie earned Tom Hanks his third straight Oscar nomination, in 1996?", answer="Apollo 13", difficulty=4, category=5)
    db.session.add(q_2)
    q_4 = Question(id=4, question="What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?", answer="Tom Cruise", difficulty=4, category=5)
    db.session.add(q_4)
    q_5 = Question(id=5, question="Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?", answer="Maya Angelou", difficulty=2, category=4)
    db.session.add(q_5)
    q_6 = Question(id=6, question="What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?", answer="Edward Scissorhands", difficulty=3, category=5)
    db.session.add(q_6)
    q_9 = Question(id=9, question="What boxer's original name is Cassius Clay?", answer="Muhammad Ali", difficulty=1, category=4)
    db.session.add(q_9)
    q_10 = Question(id=10, question="Which is the only team to play in every soccer World Cup tournament?", answer="Brazil", difficulty=3, category=6)
    db.session.add(q_10)
    q_11 = Question(id=11, question="Which country won the first ever soccer World Cup in 1930?", answer="Uruguay", difficulty=4, category=6)
    db.session.add(q_11)
    q_12 = Question(id=12, question="Who invented Peanut Butter?", answer="George Washington Carver", difficulty=2, category=4)
    db.session.add(q_12)
    q_13 = Question(id=13, question="What is the largest lake in Africa?", answer="Lake Victoria", difficulty=2, category=3)
    db.session.add(q_13)
    q_14 = Question(id=14, question="In which royal palace would you find the Hall of Mirrors?", answer="The Palace of Versailles", difficulty=3, category=3)
    db.session.add(q_14)
    q_15 = Question(id=15, question="The Taj Mahal is located in which Indian city?", answer="Agra", difficulty=2, category=3)
    db.session.add(q_15)
    q_16 = Question(id=16, question="Which Dutch graphic artist–initials M C was a creator of optical illusions?", answer="Escher", difficulty=1, category=2)
    db.session.add(q_16)
    q_17 = Question(id=17, question="La Giaconda is better known as what?", answer="Mona Lisa", difficulty=3, category=2)
    db.session.add(q_17)
    q_18 = Question(id=18, question="How many paintings did Van Gogh sell in his lifetime?", answer="One", difficulty=4, category=2)
    db.session.add(q_18)
    q_19 = Question(id=19, question="Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?", answer="Jackson Pollock", difficulty=2, category=2)
    db.session.add(q_19)
    q_20 = Question(id=20, question="What is the heaviest organ in the human body?", answer="The Liver", difficulty=4, category=1)
    db.session.add(q_20)
    q_21 = Question(id=21, question="Who discovered penicillin?", answer="Alexander Fleming", difficulty=3, category=1)
    db.session.add(q_21)
    q_22 = Question(id=22, question="Hematology is a branch of medicine involving the study of what?", answer="Blood", difficulty=4, category=1)
    db.session.add(q_22)
    q_23 = Question(id=23, question="Which dung beetle was worshipped by the ancient Egyptians?", answer="Scarab", difficulty=4, category=4)
    db.session.add(q_23)
    db.session.execute("SELECT pg_catalog.setval('public.questions_id_seq', 23, true);")

    db.session.commit()

