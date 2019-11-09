
import webapp2
import os
import jinja2
import logging

class HomeHandler(webapp2.RequestHandler):
    # your profile
    def get(self):
        profile_template = the_jinja_env.get_template('templates/home.html')
        user = users.get_current_user()
        email_address = user.nickname()
        schedify_user = SchedifyUser.query().filter(SchedifyUser.email == email_address).get()

        logout_url = users.create_logout_url('/')

        profile_data = {
            "user_instance": schedify_user,
            "account": "self",
            "sign_out": logout_url
        }
        self.response.write(profile_template.render(profile_data))

    # user profile lookup
    def post(self):
        profile_template = the_jinja_env.get_template('templates/profile.html')
        user = users.get_current_user()
        email_address = user.nickname()
        schedify_user = SchedifyUser.query().filter(SchedifyUser.email == email_address).get()

        # there should only be one username per account
        username_id = self.request.get('username_searchid')
        username_key = ndb.Key("SchedifyUser", int(username_id))
        user_search = username_key.get()

        # checks to see if user is passing in their own Account
        if user_search == schedify_user:
            account_status = "self"
            friend_status = None
            request_status = None
            user_key = None
        else:
            account_status = "other"
            friend_status = self.request.get('friend_status')
            request_status = False

            # if button to add/remove friend was cliked launch this code
            if (friend_status == "add friend"):
                request_status = True
                user_search.add_request(schedify_user.key)
            elif (friend_status == "remove friend"):
                schedify_user.remove_friend(user_search.key)
                user_search.remove_friend(schedify_user.key)
                request_status = False
            elif (friend_status == "request"):
                user_search.remove_request(schedify_user.key)
                request_status = False

            # checks if profile is part of friends group
            friend_status = False

            for friend_key in schedify_user.friends:
                if friend_key == user_search.key:
                    friend_status = True

            # check if you requested a connections
            for request_key in user_search.requests:
                if request_key == schedify_user.key:
                    request_status = True



        profile_data = {
            "user_instance": user_search,
            "friend_status": friend_status,
            "request_status": request_status,
            "account": account_status,
            "search_id": username_id,
        }
        self.response.write(profile_template.render(profile_data))




app = webapp2.WSGIApplication([
    ('/', HomeHandler),
    # schedule page should be connected to home page
    ('/Home', HomeHandler),


], debug=True)
