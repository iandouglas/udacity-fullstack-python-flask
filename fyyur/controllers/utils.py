from sqlalchemy import func

'''
Note to reviewers:
This collection of 'utility' methods is to allow for DRY'ing up of
code so I can reduce some repeated work.
'''


def add_or_get_genre_objects(db_session, genre_model, form_genre_list):
    """
    this method calls get_or_create_genre for a collection of genre strings
    and returns a list of objects from the database
    """
    genre_objects = []
    for genre in form_genre_list:
        db_genre = get_or_create_genre(db_session, genre_model, genre)
        if db_genre is not None:
            genre_objects.append(db_genre)
    return genre_objects


def get_or_create_genre(db_session, genre_model, genre_name):
    """
    this method will mimic Django's get_or_create() method by searching for a
    gender by name, and, if it does not exist, will inject it into the database
    """
    instance = db_session.query(genre_model).filter_by(name=genre_name).first()
    if instance:
        return instance

    instance = genre_model(name=genre_name)
    db_session.add(instance)
    db_session.commit()
    return instance


def entity_search(db_session, base_model, show_model, search_term):
    """
    I created this method to allow me to fetch the id, name, and show count
    for either the venue model or the artist model, and generate the
    resulting hash of data needed for the view since the hash was identical
    for both models
    """
    results = db_session.query(
        base_model.name.label('name'),
        base_model.id.label('id'),
        func.count(func.coalesce(show_model.id, 0)).label('upcoming_show_count')
    ).filter(
        base_model.name.ilike("%" + search_term + "%")
    ).outerjoin(
        show_model,
        base_model.id == show_model.artist_id
    ).group_by(
        base_model.id
    ).order_by(
        base_model.name,
    ).all()

    return {
        "count": len(results),
        "data": [{
            "id": obj.id,
            "name": obj.name,
            "num_upcoming_shows": obj.upcoming_show_count
        } for obj in results]
    }
