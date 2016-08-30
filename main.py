#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re

form="""
    <head>
        <style>
            .error {
                color: red;
            }
        </style>
    </head>
    <body>
    <h1>Signup</h1>
        <form method="post">
            <table>
                <tr>
                    <td><label for="username">Username</label></td>
                    <td>
                        <input name="username" type="text" value="%(username)s" required>
                        <span class="error">%(usernameError)s</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="password">Password</label></td>
                    <td>
                        <input name="password" type="password" value="" required>
                        <span class="error">%(validpasswordError)s</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="verify">Verify Password</label></td>
                    <td>
                        <input name="verify" type="password" value="" required>
                        <span class="error">%(passwordverifyError)s</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="email">Email (optional)</label></td>
                    <td>
                        <input name="email" type="email" value="%(email)s">
                        <span class="error">%(emailError)s</span>
                    </td>
                </tr>
            </table>
            <input type="submit">
        </form>
    </body>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r'^[\S]+@[\S]+.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class MainHandler(webapp2.RequestHandler):
    def write_form(self, error="", username="", email="", usernameError="",
                    validpasswordError="", passwordverifyError="", emailError=""):
        self.response.write(form % {"error":error, "username":username, "email":email,
                            "usernameError":usernameError, "validpasswordError":validpasswordError,
                            "passwordverifyError":passwordverifyError, "emailError":emailError})

    def get(self):
        self.write_form()

    def post(self):
        error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        usernameError = ""
        validpasswordError = ""
        passwordverifyError = ""
        emailError = ""

        if not valid_username(username):
            usernameError = "Your Username is not valid"
            error = True

        if not valid_password(password):
            validpasswordError = "Your Password is not valid"
            error = True
        elif password != verify:
            passwordverifyError = "Your Passwords do not match"
            error = True

        if not valid_email(email):
            emailError = "Your Email address is not valid"
            error = True

        if error:
            self.write_form(self, username, email, usernameError, validpasswordError, passwordverifyError, emailError)

        else:
            self.redirect("/welcome?username="+username)

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        self.response.write("Welcome, " + username)

app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/welcome', WelcomeHandler)], debug=True)
