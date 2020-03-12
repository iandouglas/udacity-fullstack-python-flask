from flask import render_template, flash
from forms import *
from sqlalchemy.sql import func


def make_routes(app, db, models):
    @app.route('/shows')
    def shows():
        show_model = models['show']
        venue_model = models['venue']
        artist_model = models['artist']
        data = db.session.query(
                func.to_char(show_model.start_time, 'YYYY-MM-DD HH24:MI:SS').label('start_time'),
                venue_model.id.label('venue_id'),
                venue_model.name.label('venue_name'),
                artist_model.id.label('artist_id'),
                artist_model.name.label('artist_name'),
                artist_model.image_link.label('artist_image_link')
            ).filter(
                show_model.artist_id == artist_model.id,
                show_model.venue_id == venue_model.id
            ).order_by(show_model.start_time).all()
        return render_template('pages/shows.html', shows=data)

    @app.route('/shows/create')
    def create_shows():
        # renders form. do not touch.
        form = ShowForm()
        return render_template('forms/new_show.html', form=form)

    @app.route('/shows/create', methods=['POST'])
    def create_show_submission():
        # called to create new shows in the db, upon submitting new show listing form
        # TODO: insert form data as a new Show record in the db, instead

        # on successful db insert, flash success
        flash('Show was successfully listed!')
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Show could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        return render_template('pages/home.html')

