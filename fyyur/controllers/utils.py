def get_or_create_genre(db_session, genre_model, genre_name):
    instance = db_session.query(genre_model).filter_by(name=genre_name).first()
    if instance:
        return instance

    instance = genre_model(name=genre_name)
    db_session.add(instance)
    db_session.commit()
    return instance
