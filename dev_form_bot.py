from datetime import date
from utils import get_initiator_approval_from_approvals, get_field_by_id, get_fields_to_lookup, \
                  all_person_fields_are_empty, person_has_approved, field_is_empty, \
                  participant_names, person_participates_in_project, status_to_person_relations


class DevFormBot:
    def __init__(self, task, settings=None):
        self.task = task
        self.settings = settings

    def set_status(self):
        # calculate_status()
        pass

    def set_release_date(self):
        # calculate_release_date()
        pass

    def calculate_status(self, fields, initiator, approvals, step):
        status = ""
        if step == 2 and initiator["approval_choice"] == "approved":
            status = "В релизе"
            return status

        detailed_status = get_field_by_id(fields, 40)
        if detailed_status:
            detailed_status_fields = detailed_status["value"]["fields"]
            fields_to_lookup = get_fields_to_lookup(detailed_status_fields)

            # если ни одно из интересующих нас полей не заполнено, возвращаем статус "Не начинали"
            if all_person_fields_are_empty(fields_to_lookup):
                status = "Не начинали"
                return status

            for field in fields_to_lookup:
                if "value" in field:
                    person_id = field["value"]["id"]
                    participant_name = participant_names[field["id"]]
                    if person_has_approved(person_id, approvals, 1):
                        status += f"{participant_name}: готово; "
                    else:
                        status += f"{participant_name}: не готово; "
            return status

    def calculate_release_date(self, fields, initiator, approvals, step):
        release_date = date.today().isoformat()

        #detailed_status = get_field_by_id(fields, 40)
        detailed_status = get_field_by_id(fields, 1)
        detailed_status_fields = detailed_status["value"]["fields"]
        #release_date_field = get_field_by_id(detailed_status_fields, 20)
        release_date_field = get_field_by_id(detailed_status_fields, 10)

        if field_is_empty(release_date_field) and step == 2:
            if initiator["approval_choice"] == "approved":
                return release_date

        # # 45, 50
        # in_release_field = get_field_by_id(detailed_status_fields, 50)
        # clients_got_releases_field = get_field_by_id(detailed_status_fields, 45)
        # if in_release_field["value"] == "checked" and field_is_empty(clients_got_releases_field):
        #     return release_date

    def check_task(self):
        fields = self.task["fields"]
        approvals = self.task["approvals"]
        author = self.task["author"]
        initiator = get_initiator_approval_from_approvals(approvals, author)
        current_step = self.task["current_step"]

        _date = self.calculate_release_date(fields, initiator, approvals, current_step)
        response = {"field_updates": [{"id": 10, "value": _date}]}
        return response
