from unittest import case
import sys
# PY librares
from random import randint, shuffle
import datetime
from  flask import Flask, render_template, request, redirect, url_for
# My librares
from lib.lib_database_20 import Database

cfg_project_main = {
 "project_name":"project 15-FLASK"
,"project_page_name":"/"
}

cfg_project_pages = [
 {"page_url":"/","page_name":"home","page_title":"home page for this project","location":"topmenu"}
,{"page_url":"/dbs/sysinfo/0","page_name":"database / sysinfo","page_title":"system informations from database","location":"buttonmenu"}
,{"page_url":"/dbs/syslog/0","page_name":"database / syslog","page_title":"system log in schema dbadm","location":"buttonmenu"}
,{"page_url":"/mountains","page_name":"Mountains","page_title":"","location":"topmenu"}
,{"page_url":"/currentdatetime","page_name":"Current Date & Time","page_title":"","location":"hidden"}
,{"page_url":"/calculator","page_name":"Calculator","page_title":"mathematical operation between two factors","location":"hidden"}
,{"page_url":"/get_post","page_name":"get&post","page_title":"testing GET or POT methods","location":"hidden"}
]

message_detail = {
 "message_type":""
,"message_message":""
,"message_formated":""
}


class Webpage():
    def __init__(self):
        pass

    def tablegenerator(self, data):
        html = ""
        html = f"{html}<table>\n"
        html = f"{html}  <tr>\n"
        for tabheader in data[0].keys():
            html = f"{html}    <th>{tabheader}</th>\n"
        html = f"{html}  </tr>\n"

        for row in data:
            html = f"{html}  <tr>\n"
            for val in row.values():
                html = f"{html}<td>{val}</td>\n"

            html = f"{html}  </tr>\n"

        html = f"{html}</table>\n"
        # print(html)
        
        return html

def html_status_set(status_text: str = "", status_code: str = "warning"):
    match status_code.lower():
        case "error":
            status_text = f'<span style="color:#800;font-weight: bold;">{status_text}</span>'
        case "warning":
            status_text = f'<span style="color:#b8860b;font-weight: bold;">{status_text}</span>'
        case _:
            return status_text
    return status_text


def page_name_get(page_url, page_list=cfg_project_pages):
    for page in page_list:
        if page["page_url"] == page_url:
            return page["page_name"]
    return ""


def html_message_set(message: str = "", message_type: str = "message"):
    if message:
        mtype = ""
        if message_type.lower() != "message":
            mtype = f"<strong>{message_type.upper()}</strong>:"
        message_detail = {"message_type": f"{message_type.lower()}", "message_message": f"{message}",
                          "message_formated": f'<div class="message_{message_type.lower()}">{mtype} {message}</div>'}
    else:
        message_detail = {"message_type": "", "message_message": "", "message_formated": ""}
    return message_detail


def html_menu_get(menu_type="topmenu", menu_list: list = cfg_project_pages):
    menu = ""
    for row in menu_list:
        if menu_type.lower() in row["location"].lower():
            row_menu = f'<a href="{row["page_url"]}" title="{row["page_title"]}">{row["page_name"]}</a>'
            match menu_type.lower():
                case "buttonmenu":
                    pass
                case "topmenu":
                    row_menu = f'<li>{row_menu}</li>'
                case _:
                    pass
            menu = f'{menu}{row_menu}\n'
    return menu

# main body
try:
    dbs=Database()
    dbs.connect()

    mainpage=Webpage()
    app = Flask(__name__)

    message_detail=html_message_set()
    @app.route("/dbs/<string:action>/<string:idrecord>", methods=["GET", 'POST'])
    def dbs_info(action: str, idrecord: str):
        cfg_project_main["project_page_name"]=page_name_get(page_url=request.path, page_list=cfg_project_pages)
        message_detail = html_message_set()
        html_body = ""
        match action.lower():
            case "sysinfo":
                sysinfo=dbs.sys_database_info_show()
                for key, value in sysinfo.items():
                    html_body=f'{html_body}<tr><td style="width:15%;text-align:right;font-size:0.8em;">{key}: </td><td style="width:85%;"><strong>{value}<strong></td></tr>\n'
                html_body=f'<table>\n{html_body}\n</table>'
            case "syslog":
                data=dbs.execute_sqlcommand("SELECT TO_CHAR(timepoint, 'YYYY-MM-DD') timepoint_date,TO_CHAR(timepoint, 'HH24:MI:SS') timepoint_time,sid,modul_code,message,parameters,status_code,sql_command,error_number,error_message,id FROM dbadm.sys_log ORDER BY timepoint DESC",False, "NO")
                for row in data:
                    err_msg=''
                    #if row["error_number"] != 0:
                    #   err_msg = f'<tr><td>&nbsp;</td><td style="text-align:right;font-size: 0.8em;"><i>error:</i></td><td colspan="3" style="color:#800">{html_status_set("["+str(row["error_number"])+"] - "+row["error_message"],"error")}</td></tr>\n'
                    html_body=f'''
                                {html_body}<tr><td style="text-align:center;" rowspan="2">{row["id"]}<br><a href="/dbs/syslogdelid/{row["id"]}" style="font-size: 0.8em;">[del]</a></td>
                                <td>{html_status_set(row["status_code"],row["status_code"])}</td><td>{row["timepoint_date"]}&nbsp;{row["timepoint_time"]}</td><td>{row["modul_code"]}</td>
                                <td style="text-align:center;" rowspan="2">{row["sid"]}<br><a href="/dbs/syslogdelsid/{row["sid"]}" style="font-size: 0.8em;">[del]</a></td></tr>\n
                                <tr><td style="text-align:right;font-size: 0.8em;"><i>message:</i></td><td colspan="2">{row["message"]}</td></tr>\n
                                <tr><td>&nbsp;</td><td style="text-align:right;font-size: 0.8em;"><i>parameter:</i></td><td colspan="2">{row["parameters"]}</td></tr>\n
                                <tr><td>&nbsp;</td><td style="text-align:right;font-size: 0.8em;"><i>command:</i></td><td colspan="3">{row["sql_command"]}</td></tr>\n
                                {err_msg}\n
                                <tr><td colspan="5"><div style="border-top:0;border-right:0;border-bottom:1px solid #999;border-left:0;height:2px;">&nbsp;</div></td></tr>
                                '''
                html_body = f'''<table><tr><th>id</th><th>status_code</th><th>timepoint</th><th>modul_code</th>\n
                                <th>sid</th></tr>\n{html_body}\n</table>'''
                html_body = f'''<div style="font-size: 0.8em;text-align:right"><form method="post" action="/dbs/syslogtrunc/0"><button type="submit" style="padding:6px;font-size:1.0em;float:right;">truncate table</button></form></div>\n{html_body}'''
            case "syslogdelsid":
                data=dbs.execute_sqlcommand(f"DELETE FROM dbadm.sys_log WHERE sid = {idrecord}",True)
                message_detail=html_message_set(f"deleted records with pid = {idrecord}","warning")
                html_body = f'''<form method="post" action="/dbs/syslog/0">
                                    <button type="submit">continue</button>    
                                </form>
                            '''
            case "syslogdelid":
                data=dbs.execute_sqlcommand(f"DELETE FROM dbadm.sys_log WHERE id = {idrecord}",True)
                message_detail=html_message_set(f"deleted records with id = {idrecord}","warning")
                html_body = f'''<form method="post" action="/dbs/syslog/0">
                                    <button type="submit">continue</button>    
                                </form>
                            '''
            case "syslogtrunc":
                data=dbs.execute_sqlcommand(f"TRUNCATE TABLE dbadm.sys_log")
                message_detail=html_message_set(f"table dbadm.sys_log was truncated","warning")
                html_body = f'''<form method="post" action="/dbs/syslog/0">
                                    <button type="submit">continue</button>    
                                </form>
                            '''
            case _:
                html_body=''
        return render_template("rjdesign.html"
                               ,html_project_detail=cfg_project_main
                               ,html_body=html_body
                               ,html_message_detail=message_detail
                               ,html_menu_top=html_menu_get(menu_type="topmenu",menu_list=cfg_project_pages)
                               ,html_menu_button=html_menu_get(menu_type="buttonmenu",menu_list=cfg_project_pages)
                              )


    @app.route("/")
    def main():
        cfg_project_main["project_page_name"] = page_name_get(page_url=request.path, page_list=cfg_project_pages)
        html_body = f"flask started on: <a href=\"http://localhost:5000\">localhost:5000<a/>"
        return render_template("rjdesign.html"
                               , html_project_detail=cfg_project_main
                               , html_body=html_body
                               , html_message_detail=message_detail
                               , html_menu_top=html_menu_get(menu_type="topmenu", menu_list=cfg_project_pages)
                               , html_menu_button=html_menu_get(menu_type="buttonmenu", menu_list=cfg_project_pages)
                               )

    @app.route("/mountains")
    def mountains():
        cfg_project_main["project_page_name"] = page_name_get(page_url=request.path, page_list=cfg_project_pages)
        data = dbs.execute_sqlcommand(
            "SELECT ranking, mountain_name, elevation_meters, mountain_range, countries, id FROM alpha.mountain_8000;")
        html_body = mainpage.tablegenerator(data);
        return render_template("rjdesign.html"
                               , html_project_detail=cfg_project_main
                               , html_body=html_body
                               , html_message_detail=message_detail
                               , html_menu_top=html_menu_get(menu_type="topmenu", menu_list=cfg_project_pages)
                               , html_menu_button=html_menu_get(menu_type="buttonmenu", menu_list=cfg_project_pages)
                               )
    @app.route("/currentdatetime")
    def current_date_time():
        cfg_project_main["project_page_name"] = page_name_get(page_url=request.path, page_list=cfg_project_pages)
        csdays = ["pondělí", "úterý", "středa", "čtvrtek", "pátek", "sobota", "neděle"]
        currdate = datetime.datetime.now()
        html_body = f"the date is <strong>{str(currdate.date())}</strong> and today is <strong>{str(currdate.strftime("%A")).lower()}</strong>/<strong>{csdays[currdate.weekday()]}</strong>"
        html_body = f"{html_body}\n<br>\ncurrent time: <strong>{str(datetime.datetime.now().time())}</strong>"
        return render_template("rjdesign.html"
                               , html_project_detail=cfg_project_main
                               , html_body=html_body
                               , html_message_detail=message_detail
                               , html_menu_top=html_menu_get(menu_type="topmenu", menu_list=cfg_project_pages)
                               , html_menu_button=html_menu_get(menu_type="buttonmenu", menu_list=cfg_project_pages)
                               )


    @app.route("/calculator", methods=['GET', 'POST'])
    def calculator():
        cfg_project_main["project_page_name"] = page_name_get(page_url=request.path, page_list=cfg_project_pages)
        message_detail = html_message_set()
        result = ""
        number1 = ""
        number2 = ""
        operator = "+"
        if request.method == "POST":
            number1 = request.form.get("calculator_number1")
            number2 = request.form.get("calculator_number2")
            operator = request.form.get("calculator_operator")
            if number1 == "" or number2 == "" or operator == "":
                message_detail = html_message_set("All fields in the form must be filled in.", "error")
            else:
                result = eval(f"{number1} {operator} {number2}")
            # result = str(int(defval_number1) + int(defval_number2))
        html_body = f"""
        <form method="post" class="niceform">
            <label>
                number1:
                <input type="text" maxlength="10"
                       name="calculator_number1"
                       value="{number1}">
            </label>
            <label>
                operator
                <input type="text" maxlength="1"
                       name="calculator_operator"
                       value="{operator}">
            </label>
            <label>
                number2:
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
                               , html_project_detail=cfg_project_main
                               , html_body=html_body
                               , html_message_detail=message_detail
                               , html_menu_top=html_menu_get(menu_type="topmenu", menu_list=cfg_project_pages)
                               , html_menu_button=html_menu_get(menu_type="buttonmenu", menu_list=cfg_project_pages)
                               )


    @app.route("/get_post", methods=["GET", 'POST'])
    def get_post():
        cfg_project_main["project_page_name"] = page_name_get(page_url=request.path, page_list=cfg_project_pages)
        output = "GET"
        if request.method == "POST":
            output = "POST"
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
                               , html_project_detail=cfg_project_main
                               , html_body=html_body
                               , html_message_detail=message_detail
                               , html_menu_top=html_menu_get(menu_type="topmenu", menu_list=cfg_project_pages)
                               , html_menu_button=html_menu_get(menu_type="buttonmenu", menu_list=cfg_project_pages)
                               )


    if __name__ == "__main__":
        app.run(debug=True, port=5000)

    dbs.close()

except Exception as err:
    print(f"ERROR: {err}")
    sys.exit(22)