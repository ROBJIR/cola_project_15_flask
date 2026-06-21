from unittest import case

from  flask import Flask, render_template, request, redirect, url_for
from random import randint, shuffle
import datetime


cfg_project_main = {
 "project_name":"project 15-FLASK"
,"project_page_name":""
}

cfg_project_pages = [
 {"page_url":"/","page_name":"home","page_title":"home page for this project"}
,{"page_url":"/currentdatetime","page_name":"Current Date & Time","page_title":""}
,{"page_url":"/calculator","page_name":"Calculator","page_title":"mathematical operation between two factors"}
,{"page_url":"/get_post","page_name":"get&post","page_title":"testing GET or POT methods"}
]

message_detail = {
 "message_type":""
,"message_message":""
,"message_formated":""
}

def html_message_set(message:str="",message_type:str="message"):
    if  message:
        mtype=""
        if message_type.lower()!="message":
            mtype = f"<strong>{message_type.upper()}</strong>:"
        message_detail = {"message_type": f"{message_type.lower()}", "message_message": f"{message}",
                          "message_formated": f'<div class="message_{message_type.lower()}">{mtype} {message}</div>'}
    else:
        message_detail = {"message_type": "", "message_message": "", "message_formated": ""}
    return message_detail

def html_menu_get(menu_type="topmenu", menu_list: list=cfg_project_pages):
    menu=""
    for row in menu_list:
        row_menu=f'<a href="{row["page_url"]}" title="{row["page_title"]}">{row["page_name"]}</a>'
        match menu_type.lower():
            case "buttonmenu":
                pass
            case "topmenu":
                row_menu = f'<li>{row_menu}</li>'
            case _:
                pass

        menu = f'{menu}{row_menu}\n'
    return menu

app = Flask(__name__)
@app.route("/")
def main():
    cfg_project_main["project_page_name"]="home"
    message_detail=html_message_set()
    html_body = f"flask started on: <a href=\"http://localhost:5000\">localhost:5000<a/>"
    return render_template("rjdesign.html"
                           ,html_project_detail=cfg_project_main
                           ,html_body=html_body
                           ,html_message_detail=message_detail
                           ,html_menu_top=html_menu_get(menu_type="topmenu",menu_list=cfg_project_pages)
                           ,html_menu_button=html_menu_get(menu_type="buttonmenu",menu_list=cfg_project_pages)
                          )

@app.route("/currentdatetime")
def current_date_time():
    cfg_project_main["project_page_name"]="Current Date & Time"
    message_detail=html_message_set()
    csdays = ["pondělí", "úterý", "středa", "čtvrtek", "pátek", "sobota", "neděle"]
    currdate = datetime.datetime.now()
    html_body = f"the date is <strong>{str(currdate.date())}</strong> and today is <strong>{str(currdate.strftime("%A")).lower()}</strong>/<strong>{csdays[currdate.weekday()]}</strong>"
    html_body = f"{html_body}\n<br>\ncurrent time: <strong>{str(datetime.datetime.now().time())}</strong>"
    return render_template("rjdesign.html"
                           ,html_project_detail=cfg_project_main
                           ,html_body=html_body
                           ,html_message_detail=message_detail
                           ,html_menu_top=html_menu_get(menu_type="topmenu",menu_list=cfg_project_pages)
                           ,html_menu_button=html_menu_get(menu_type="buttonmenu",menu_list=cfg_project_pages)
                          )

@app.route("/calculator", methods=['GET', 'POST'])
def calculator():
    cfg_project_main["project_page_name"]="Calculator"
    message_detail=html_message_set()
    result=""
    number1=""
    number2=""
    operator="+"
    if request.method == "POST":
        number1=request.form.get("calculator_number1")
        number2=request.form.get("calculator_number2")
        operator = request.form.get("calculator_operator")
        if number1=="" or number2=="" or operator=="":
            message_detail=html_message_set("All fields in the form must be filled in.","error")
            print(message_detail)
        else:
            result = eval(f"{number1} {operator } {number2}")
        # result = str(int(defval_number1) + int(defval_number2))
    html_body = f"""
    <form method="post">
        <label>
            <input type="text" maxlength="10"
                   name="calculator_number1"
                   value="{number1}">
        </label>
        <label>
            <input type="text" maxlength="1"
                   name="calculator_operator"
                   value="{operator}">
        </label>
        <label>
            <input type="text" maxlength="10"
                   name="calculator_number2"
                   value="{number2}">
        </label>
        <button type="submit">calculate</button>
        <br>
        <label>
            result:
            <input type="text" maxlength="10"
                   name="calculator_result"
                   value="{result}">
        </label>

    </form>"""
    return render_template("rjdesign.html"
                           ,html_project_detail=cfg_project_main
                           ,html_body=html_body
                           ,html_message_detail=message_detail
                           ,html_menu_top=html_menu_get(menu_type="topmenu",menu_list=cfg_project_pages)
                           ,html_menu_button=html_menu_get(menu_type="buttonmenu",menu_list=cfg_project_pages)
                          )
@app.route("/get_post", methods=["GET", 'POST'])
def get_post():
    cfg_project_main["project_page_name"]="get&post"
    message_detail=html_message_set()
    output = "GET"
    if request.method == "POST":
        output  = "POST"
    message_detail = html_message_set(f"sended method was {output}!")
    html_body = f"""
    <form method="post">
        <button type="submit" >
            POST
        </button>
    </form>
    <form method="get">
       <button type="submit" >
            GET
        </button>
    </form>"""
    return render_template("rjdesign.html"
                           ,html_project_detail=cfg_project_main
                           ,html_body=html_body
                           ,html_message_detail=message_detail
                           ,html_menu_top=html_menu_get(menu_type="topmenu",menu_list=cfg_project_pages)
                           ,html_menu_button=html_menu_get(menu_type="buttonmenu",menu_list=cfg_project_pages)
                          )

if __name__ == "__main__":
    app.run(debug=True, port=5000)