#!/usr/bin/python3.7
import sys, json, os, stripe
from datetime import timedelta, datetime
from flask import Flask, render_template, redirect, request, escape, jsonify, flash, current_app
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_wtf import CSRFProtect

# Import all the things
from setup_app import app
from frontend_action import FrontendAction
from service_calls.call_notifications_service import notification_api
from service_calls.call_user_service import user_api
from service_calls.call_stripe_service import stripe_api

csrf = CSRFProtect(app)
app.register_blueprint(notification_api)
app.register_blueprint(user_api)
app.register_blueprint(stripe_api)

action = FrontendAction(app)

@app.route("/")
def home():
    variables = dict(is_authenticated=current_user.is_authenticated)
    return render_template('index.html', **variables)

@app.route("/login_page")
def login_page():
    if current_user.is_authenticated:
        return redirect('/dashboard', code=302)
    return render_template('login_page.html')

@app.route("/dashboard")
@login_required
def dashboard():
    trial_period = timedelta(days=app.config['TRIAL_LENGTH_DAYS'])

    sub_active = action.is_user_subscription_active(False)

    notifications, notifications_for_display = action.get_unread_notifications(current_user.id)
    
    variables = dict(name=current_user.name,
                     expire_date=current_user.created_date + trial_period,
                     user_is_paying=sub_active,
                     notifications=notifications_for_display,
                     n_messages=len(notifications))
    
    return render_template('dashboard.html', **variables)

@app.route("/billing")
@login_required
def billing():
    sub_active, show_reactivate, sub_cancelled_at = action.is_user_subscription_active()
    stripe_objs = action.get_all_stripe_subscriptions_by_user_id(current_user.id)

    sub_dict = action.subscriptions_to_json(stripe_objs)

    notifications, notifications_for_display = action.get_unread_notifications(current_user.id)
    
    variables = dict(subscription_active=sub_active,
                     name=current_user.name,
                     show_reactivate=show_reactivate,
                     subscription_cancelled_at=sub_cancelled_at,
                     subscription_data=sub_dict,
                     notifications=notifications_for_display,
                     n_messages=len(notifications))
    
    return render_template('billing.html', **variables)

@app.route("/notifications")
@login_required
def notifications_center():
    all_notifications = action.get_all_notifications_by_user_id(current_user.id)
    notifications, notifications_for_display = action.get_unread_notifications(current_user.id)

    variables = dict(name=current_user.name,
                     notifications=notifications_for_display,
                     all_notifications=all_notifications,
                     n_messages=len(notifications))

    return render_template('notifications.html', **variables)

@app.route("/tos")
def terms_of_service():
    variables = dict(is_authenticated=current_user.is_authenticated)
    return render_template('terms_of_service.html', **variables)

@app.route("/logout")
def logout():
    if current_user.is_authenticated == True:
        current_user.is_authenticated = False
        logout_user()
    return redirect('/', code=302)

@app.errorhandler(401)
def not_logged_in(e):
    variables = dict(message='Please login first')
    
    return render_template('login_page.html', **variables)

@app.errorhandler(404)
def not_found(e):
    variables = dict(is_authenticated=current_user.is_authenticated,
                     message = '404 Page Not Found',
                     stacktrace = str(e))
    
    return render_template('error.html', **variables)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=app.config['FRONTEND_PORT'])