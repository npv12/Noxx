from noxx.database import init

class PmPermit:
    def __init__(self):
        self.pm_permit_db = init()["pmpermit"]

    #Check if user is approved or not
    def is_approved(self, user_id):
        get_user = self.pm_permit_db.find_one({"user_id": user_id})

        #User is new to the database
        if get_user is None:
            self.pm_permit_db.insert_one({"user_id": user_id, "approved": False, "blocked": False, "messages_sent": 0})
            return False
        elif get_user["approved"]:
            return True
        else:
            return False

    #Approve a user to pm
    def approve(self, user_id):
        if self.is_approved(user_id):
            return False
        else:
            self.pm_permit_db.update_one({"user_id": user_id}, {"$set":{"approved": True, "blocked": False}})
            return True

    #Is user blocked
    def is_blocked(self, user_id):
        get_user = self.pm_permit_db.find_one({"user_id": user_id})

        #User is new to the database
        if get_user is None:
            self.pm_permit_db.insert_one({"user_id": user_id, "approved": False, "blocked": False, "messages_sent": 0})
            return False
        elif get_user["blocked"]:
            return True
        else:
            return False

    #Block a user
    def block(self, user_id):
        self.pm_permit_db.update_one({"user_id": user_id}, {"$set":{"approved": False, "blocked": True}})
        return True

    #The user is allowed to send only a limited number of mesages when they are unapproved
    def increment_message_sent(self, user_id):
        if not self.is_approved(user_id):
            get_user = self.pm_permit_db.find_one({"user_id": user_id})

            if get_user is None:
                self.pm_permit_db.insert_one({"user_id": user_id, "approved": False, "blocked": False, "messages_sent": 1})
                return False
            elif "messages_sent" not in get_user:
                self.pm_permit_db.update_one({"user_id": user_id}, {"$set": {"messages_sent": 1}})
            else:
                self.pm_permit_db.update_one({"user_id": user_id}, {"$inc": {"messages_sent": 1}})

    def number_of_messages_sent(self, user_id):
        if not self.is_approved(user_id):
            get_user = self.pm_permit_db.find_one({"user_id": user_id})

            if "messages_sent" not in get_user:
                return 0
            else:
                return get_user["messages_sent"]
