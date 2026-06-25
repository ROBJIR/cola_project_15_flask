# flaskfoream2.py
# - exam2
# robert.jiranek@gmail.com

import sys
from  flask import Flask, render_template, request, redirect, url_for
from lib.lib_database import *

DATABASE_CONNECT_EXAM2={
        "database": "exam2",
        "host":"192.168.56.1",
        "port":"5432",
        "username":"robert",
        "userpwd":"central"
        }

CFG_WEB_PROJECT = {
 "project_name":"EXAM2 / flask"
,"project_root_url":"/"
,"project_template":"rjdesign.html"
}

CFG_WEB_PAGES = [
 {"page_url":"/","page_name":"home","page_title":"home page for this project","location":"topmenu"}
,{"page_url":"/databaseinfo","page_name":"database info","page_title":"informations about database connection","location":"buttonmenu"}
,{"page_url":"/items","page_name":"items","page_title":"select products","location":"topmenu,litlemenu"}
,{"page_url":"/add_product","page_name":"add product","page_title":"add product in my project","location":"topmenu,litlemenu"}
]

FORM_ADD_ITEM=f"""
<form method="post" name="add_product" class="niceform" action="">
    <label for="name">name:</label>
        <input type="text" 
               name="name" id="name"
               value="<<name_value>>">
    <label for="description">description:</label> 
        <textarea name="description" id="description" rows="5" cols="10"><<description_value>></textarea>
    <label for="price">price:</label>
        <input type="number" 
               name="price" id="price" step="1"
               value="<<price_value>>">   
    <br>             
    <button type="submit" >submit</button>
</form>
"""

class HtmlMachine():
    def __init__(self, web_config):
        self.message = {"message_type": "", "message": "", "message_html": ""}
        self.html_page = {"page_name": "", "page_body": "", "page_message": ""}
        self.html_web = {"web_name": web_config["project_name"], "web_root_url": web_config["project_root_url"], "web_template": web_config["project_template"]}

    def html_message_set(self, msg: str = "", msgtype: str = "message"):

        msgtype=msgtype.lower()
        msgtype_html=""

        if msgtype.lower() != "message":
            msgtype_html=f"<strong>{msgtype.upper()}</strong>:"

        if msg:
            self.message = {"message_type": msgtype, "message": msg, "message_html": f'<div class="message_{msgtype}">{msgtype_html} {msg}</div>'}
        else:
            self.message = {"message_type": "", "message": "", "message_html": ""}

        self.html_page["page_message"] = self.message["message_html"]

        return self.message

    def page_name_get(self, url, page_list=CFG_WEB_PAGES):
        for page in page_list:
            if page["page_url"] == url:
                return page["page_name"]
        return ""

    def html_menu_get(self, menutype: str="topmenu", isulli: bool = False, menulist: list = CFG_WEB_PAGES):
        menutype = menutype.lower()
        htmlmenu = ""

        for row in menulist:
            if menutype in row["location"].lower():
                rowmenu = f'<a href="{row["page_url"]}">{row["page_name"]}</a>'
                if isulli:
                        rowmenu = f'<li>{rowmenu}</li>'

                htmlmenu = f'{htmlmenu}{rowmenu}\n'

        if not htmlmenu:
            htmlmenu=f"<div>no records for {menutype}</div>"

        return htmlmenu

    def table_list_genertor(self, data):
        if len(data) == 0:
            self.message_detail  = self.html_message_set("data was not loaded", "warning")
            return ""

        htmlcode = f"<table>\n"
        htmlcode = f"{htmlcode}  <tr>\n"
        for tabheader in data[0].keys():
            htmlcode = f"{htmlcode}    <th>{tabheader}</th>\n"
        htmlcode = f"{htmlcode}  </tr>\n"

        for row in data:
            htmlcode = f"{htmlcode}  <tr>\n"
            for ikey, ivalue in row.items():
                htmlcode = f"{htmlcode}    <td>{ivalue}</td>\n"

            htmlcode = f"{htmlcode}  </tr>\n"

        htmlcode = f"{htmlcode}</table>\n"

        return htmlcode

    def table_detail_genertor(self, data):
        if len(data) == 0:
            self.message_detail = self.html_message_set("data was not loaded", "warning")
            return ""

        htmlcode = f"<table>\n"

        for ikey, ivalue in data.items():
            htmlcode = f"{htmlcode}  <tr>\n"
            htmlcode = f'{htmlcode}  <th class="detail">{ikey}</th><td class="detail">{ivalue}</td>\n'
            htmlcode = f"{htmlcode}  </tr>\n"

        htmlcode = f"{htmlcode}</table>\n"

        return htmlcode

    def html_renderer (self, body: str = ""):
        self.html_page={"page_name": self.page_name_get(request.path), "page_body": body, "page_message": self.html_page["page_message"]}
        return render_template(self.html_web["web_template"]
                               ,html_web=self.html_web
                               ,html_page=self.html_page
                               ,html_menu_top=self.html_menu_get("topmenu")
                               ,html_menu_button=self.html_menu_get("buttonmenu")
                            )

if True:
# try:
    # connect to database
    myDbs=DatabasePostgresql()
    # myDbs.sys_database_info(onscreen = True)
    myHtml = HtmlMachine(CFG_WEB_PROJECT)

    app = Flask(__name__)

    # reset for message


    @app.route("/")
    def root():
        myHtml.message_detail = myHtml.html_message_set()
        html_body = f"""
                    <div>
                    flask started on: <a href="{request.url_root}">{request.url_root}<a/>
                    </div>
                    """""
        html_body = f"""
                    {html_body}<div><ul>{myHtml.html_menu_get("litlemenu", True)}</ul></div>
                    """
        return myHtml.html_renderer(html_body)

    @app.route("/items", methods=["GET", 'POST'])
    def items():
        myHtml.message_detail = myHtml.html_message_set()
        myDbs.connect(connect_string=DATABASE_CONNECT_EXAM2)
        html_body = myHtml.table_list_genertor(myDbs.sqlcommand_execute('select id as "#", name as "Item Name", description as "Description", price as "Price" from items order by name,id'))
        myDbs.close()

        return myHtml.html_renderer(html_body)

    @app.route("/add_product", methods=["GET", 'POST'])
    def add_product():
        myHtml.message_detail = myHtml.html_message_set()
        if request.method == "GET":
            item_name = ""
            item_desc = ""
            item_price = 0
        else:
            item_name = request.form.get("name").strip()
            item_desc = f'{request.form.get("description")} '.strip()
            item_price = float(request.form.get("price"))
            msg=""
            if not (item_name and len(item_name) <= 40 and item_price and item_price>=0 and item_price<=1000000):
                if not item_name:
                    msg=f"{msg}, name is required"
                if not item_price:
                    msg=f"{msg}, price is required"
                if item_price<0 or item_price>1000000:
                    msg=f"{msg}, price is outside the allowed range (0 .. 1,000,000)"
                if len(item_name)>40:
                    msg=f"{msg}, length of the name is greater than 40 characters"
                myHtml.message_detail = myHtml.html_message_set(f"{msg[2:]}", "error")
            else:
                sqlcommand = f"insert into items (name,description,price) values ('{item_name}','{item_desc}',{item_price})"
                sqlcommand = sqlcommand.replace(",''",",null")

                myDbs.connect(connect_string=DATABASE_CONNECT_EXAM2)

                if myDbs.sqlcommand_execute(sqlcommand):
                    myHtml.message_detail = myHtml.html_message_set(f"Product {item_name} added!")
                    item_name = ""
                    item_desc = ""
                    item_price = 0
                else:
                    myHtml.message_detail = myHtml.html_message_set(f"Error during data inserting!","error")

                myDbs.close()

        html_body = FORM_ADD_ITEM.replace("<<name_value>>", item_name).replace("<<description_value>>",item_desc).replace("<<price_value>>", str(item_price))

        return myHtml.html_renderer(html_body)

    @app.route("/databaseinfo", methods=["GET"])
    def database_info():
        myHtml.message = myHtml.html_message_set(f'<div>flask started on: <a href="{request.url_root}">{request.url_root}<a/></div>')
        myDbs.connect(connect_string=DATABASE_CONNECT_EXAM2)
        sysinfo = myDbs.sys_database_info()
        myDbs.close()

        html_body = myHtml.table_detail_genertor(sysinfo)

        return myHtml.html_renderer(html_body)

    if __name__ == "__main__":
        app.run(debug=True, port=5000)

#except Exception as err:
#    print(f"{68*"_"}\nERROR\n {err}\n{68*"_"}")