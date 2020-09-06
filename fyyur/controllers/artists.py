import sys

from flask import render_template, flash, request, redirect, url_for
from forms import *
from sqlalchemy.sql import func
import bleach

from .utils import entity_search, add_or_get_genre_objects


def make_routes(app, db, models):
    @app.route('/artists')
    def artists():
        artist_model = models['artist']
        data = db.session.query(
                artist_model.id.label('id'),
                artist_model.name.label('name')
            ).order_by(artist_model.id).all()
        return render_template('pages/artists.html', artists=data)

    @app.route('/artists/search', methods=['POST'])
    def search_artists():
        response = entity_search(
            db.session,
            models['artist'],
            models['show'],
            bleach.clean(request.form['search_term'])
        )

        return render_template('pages/search_artists.html', results=response,
                               search_term=request.form.get('search_term', ''))

    @app.route('/artists/<int:artist_id>')
    def show_artist(artist_id):
        data = db.session.query(models['artist']).get(artist_id).info()
        return render_template('pages/show_artist.html', artist=data)

    #  Update
    #  ----------------------------------------------------------------
    @app.route('/artists/<int:artist_id>/edit', methods=['GET'])
    def edit_artist(artist_id):
        form = ArtistForm()
        artist = db.session.query(models['artist']).get(artist_id)
        if artist:
            form.name.data = artist.name
            form.city.data = artist.city
            form.state.data = artist.state
            form.phone.data = artist.phone
            form.genres.data = [genre.name for genre in artist.genres]
            form.facebook_link.data = artist.facebook_link
            return render_template('forms/edit_artist.html', form=form, artist=artist)
        return render_template('errors/404.html')

    @app.route('/artists/<int:artist_id>/edit', methods=['POST'])
    def edit_artist_submission(artist_id):
        # TODO: take values from the form submitted, and update existing
        # artist record with ID <artist_id> using the new attributes

        return redirect(url_for('show_artist', artist_id=artist_id))

    #  Create Artist
    #  ----------------------------------------------------------------

    @app.route('/artists/create', methods=['GET'])
    def create_artist_form():
        form = ArtistForm()
        return render_template('forms/new_artist.html', form=form)

    @app.route('/artists/create', methods=['POST'])
    def create_artist_submission():
        data = request.form
        error = False
        try:
            artist = models['artist'](
                name=bleach.clean(data['name']),
                city=bleach.clean(data['city']),
                state=bleach.clean(data['state']),
                phone=bleach.clean(data['phone']),
                facebook_link=bleach.clean(data['facebook_link'])
            )

            genre_list = add_or_get_genre_objects(db.session, models['genre'], request.form.getlist('genres'))
            artist.genres = genre_list
            db.session.add(artist)
            db.session.commit()
        except:
            error = True
            db.session.rollback()
            print(sys.exc_info())
            flash('An error occurred. Artist ' + request.form['name'] + ' could not be created.')
        finally:
            db.session.close()

        if error:
            return render_template('pages/home.html')
        else:
            flash('Artist ' + request.form['name'] + ' was successfully listed!')
            return redirect(url_for('artists'))

