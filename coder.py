import sublime
import sublime_plugin
import requests
import json
import threading
from .prompts import system_prompt
from .database import Database


def getLang(o):
    s_p = o.view.settings().get('syntax')
    if s_p:
        l_s = s_p.rfind('/')
        if l_s != -1:
            n_w_e = s_p[l_s + 1:]
        else:
            n_w_e = s_p
        l_d = n_w_e.rfind('.')
        if l_d != -1:
            lang = n_w_e[:l_d]
        else:
            lang = n_w_e
    return lang


class GeminiCodeAssistantCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        settings = sublime.load_settings("gemini.sublime-settings")
        self.edit = edit
        self.api_key = settings.get("api_key")
        self.model = settings.get("model")
        self.config = settings.get("config")
        self.url = "https://generativelanguage.googleapis.com/v1beta/models/{}:generateContent".format(self.model)
        print(self.model)
        # the path of the current open project (if none then save in the in the temp folder)
        self.db_path = sublime.packages_path() + "/User/gemini_db.db"  # Store the database in the User package folder
        self.database = Database(self.db_path)
        if self.view.settings().get("conversation_id"):
            self.conversation_id = self.view.settings().get("conversation_id")
        else:
            self.conversation_id = self.start_new_conversation()

        sel = self.view.sel()

        selected_text = self.view.substr(sel[0]) if len(sel) > 0 and not sel[0].empty() else ""
        lang = getLang(self)
        # Modify this part to include the selected text in the input panel
        initial_text = "Selected code:```{0}\n{1}\n```\nYour question: ".format(lang, selected_text) if selected_text else ""
        self.view.window().show_input_panel("Ask Gemini:", initial_text, self.on_done, None, None)

    def start_new_conversation(self):
        cursor = self.database.conn.cursor()
        cursor.execute("INSERT INTO conversations DEFAULT VALUES")
        self.database.conn.commit()
        return cursor.lastrowid

    def send_messages(self, conversation):
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self.api_key
        }
        data = {
            "system_instruction": {"parts": {"text": system_prompt}},
            "contents": [{"parts": [{"text": msg[1]}]} for msg in conversation]
        }
        # print(json.dumps(data))
        response = requests.post(self.url.format(self.model), headers=headers, json=data)
        return response.json()

    def on_done(self, user_input):
        self.database.save_message(self.conversation_id, "user", user_input)
        conversation = self.database.get_conversation(self.conversation_id)
        self.show_result("\nUser:\n+++++++++++\n"+user_input + "\n\n+++++++++++++++++\nGemini:\n")
        # print(conversation)
        threading.Thread(target=self.handle_response, args=(conversation, self.db_path, self.conversation_id)).start()

    def handle_response(self, conversation, db_path, conversation_id):
        response_json = self.send_messages(conversation)
        local_db = Database(db_path)
        try:

            response_json = self.send_messages(conversation)

            if "candidates" in response_json and response_json["candidates"]:
                assistant_response = response_json["candidates"][0]["content"]["parts"][0]["text"]
                local_db.save_message(conversation_id, "gemini", assistant_response)  # Use local_db and the passed conversation_id

                sublime.set_timeout(lambda: self.show_result(assistant_response), 0)
            else:
                # Oh no, Gemini failed
                error_message = "Gemini failed to generate a response. {}".format(json.dumps(response_json, indent=2))
                sublime.set_timeout(lambda: sublime.status_message(error_message), 0)
                sublime.set_timeout(lambda: self.view.run_command("insert", {"characters": "\n--- ERROR ---\n\n{}\n\n".format(error_message)}), 0)
                sublime.set_timeout(lambda: self.view.show(self.view.size()), 0)

        except requests.exceptions.RequestException as e:
            error_message = "API Request Failed: {}".format(e)
            sublime.set_timeout(lambda: sublime.status_message(error_message), 0)
            sublime.set_timeout(lambda: self.view.run_command("insert", {"characters": "\n--- ERROR ---\n\n{}\n\n".format(error_message)}), 0)
            sublime.set_timeout(lambda: self.view.show(self.view.size()), 0)

        except Exception as e:
            error_message = "An unexpected error occurred: {}".format(e)
            sublime.set_timeout(lambda: sublime.status_message(error_message), 0)
            sublime.set_timeout(lambda: self.view.run_command("insert", {"characters": "\n--- ERROR ---\n\n{}\n\n".format(error_message)}), 0)
            sublime.set_timeout(lambda: self.view.show(self.view.size()), 0)
        finally:
            local_db.close()

    def show_result(self, text):
        # Look for an existing "Gemini Response" tab
        found_view = None
        for view in self.view.window().views():
            if view.name() == "Gemini Response":
                found_view = view
                break

        if found_view:
            # If the tab exists, clear its selection, move the cursor to the end,
            # and then insert the new text. This ensures text is always appended.
            found_view.sel().clear()
            found_view.sel().add(sublime.Region(found_view.size()))
            found_view.run_command("insert", {"characters": text})
            self.view.window().focus_view(found_view)
        else:
            # If no "Gemini Response" tab exists, create a new one.
            new_view = self.view.window().new_file()
            new_view.set_name("Gemini Response")
            new_view.set_scratch(True)
            # Disable automatic indentation in the new view for raw text display
            new_view.settings().set("auto_indent", False)
            new_view.run_command("insert", {"characters": text})
            # self.view.window().focus_view(new_view)
