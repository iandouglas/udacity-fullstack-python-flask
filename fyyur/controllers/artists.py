from flask import render_template, flash, request, redirect, url_for
from forms import *
from sqlalchemy.sql import func


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
        # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
        # search for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
        # search for "band" should return "The Wild Sax Band".
        # response = {
        #     "count": 1,
        #     "data": [{
        #         "id": 4,
        #         "name": "Guns N Petals",
        #         "num_upcoming_shows": 0,
        #     }]
        # }
        response = {}
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
        # artist = {
        #     "id": 4,
        #     "name": "Guns N Petals",
        #     "genres": ["Rock n Roll"],
        #     "city": "San Francisco",
        #     "state": "CA",
        #     "phone": "326-123-5000",
        #     "website": "https://www.gunsnpetalsband.com",
        #     "facebook_link": "https://www.facebook.com/GunsNPetals",
        #     "seeking_venue": True,
        #     "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
        #     "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
        # }
        artist = {}
        # TODO: populate form with fields from artist with ID <artist_id>
        return render_template('forms/edit_artist.html', form=form, artist=artist)

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
        # called upon submitting the new artist listing form
        # TODO: insert form data as a new Venue record in the db, instead
        # TODO: modify data to be the data object returned from db insertion

        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
        return render_template('pages/home.html')
