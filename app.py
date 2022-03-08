from bottle import default_app, get, post, view, redirect, request, response, run, static_file
import time
import json
import jwt



##############################
@get("/images/mitid.png")
def _():
  return static_file("mitid.png", root="./images")

##############################
@get("/")
@view("mitid")
def _():
  error = request.params.get("error")
  return dict(error=error)

##############################
@post("/login")
@view("call_parent")
def _():
  try:
    
    users = {
      "a@a.com":{"cpr":"221085-4079", "password":"passA"},
      "b@b.com":{"cpr":"010792-2078", "password":"passB"},
    }

    user_email = request.forms.get("user_email")
    user_password = request.forms.get("user_password")
    if users[user_email]["password"] != user_password:
      raise Exception("User not found")
    iat = int(time.time())
    exp = iat + 600
    user_jwt = jwt.encode({"cpr":users[user_email]["cpr"], "iat":str(iat), "exp":str(exp)}, "secret", algorithm="HS256")
    # if not isinstance(user_jwt, str):
    #   user_jwt = user_jwt.decode("UTF-8")
    print("#"*30)
    print(type(user_jwt))
    # response.set_cookie("mitid", user_jwt, expires=exp, httponly=True)    
    response.set_cookie("mitid", user_jwt)
    return dict(jwt=user_jwt)
  except Exception as ex: 
    print("#"*30)
    print(ex)
    return redirect("/?error=yes")




##############################
try:
  import production
  application = default_app()
except Exception as ex:
  run(host="127.0.0.1", port=3333, debug=True, reloader=True, server="paste")
