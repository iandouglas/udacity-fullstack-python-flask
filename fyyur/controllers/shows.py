from flask import render_template, flash
from forms import *
from sqlalchemy.sql import func


def make_routes(app, db, models):
    @app.route('/shows')
    def shows():
        data = db.session.query(
                func.to_char(models['show'].start_time, 'YYYY-MM-DD HH24:MI:SS').label('start_time'),
                models['venue'].id.label('venue_id'),
                models['venue'].name.label('venue_name'),
                models['artist'].id.label('artist_id'),
                models['artist'].name.label('artist_name'),
                models['artist'].image_link.label('artist_image_link'))\
            .filter(
                models['show'].artist_id == models['artist'].id,
                models['show'].venue_id == models['venue'].id)\
            .order_by(models['show'].start_time)\
            .all()
        print('-'*80)
        print(data)
        print('-'*80)
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

